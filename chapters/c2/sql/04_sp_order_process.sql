USE northwind;
GO

--tárolt eljárás az order_log feldolgozásához
--drop proc sp_order_process
go
create proc sp_order_process as
declare @event_id int, @event_type varchar(50), @order_id int, @result int
declare cursor_events cursor forward_only static
        for
        select event_id, event_type, order_id
        from order_log where status=0  --csak a feldolgozatlan eseményeket kezeljük

set xact_abort on
set nocount on
open cursor_events
fetch next from cursor_events into @event_id, @event_type, @order_id
while @@fetch_status = 0
begin
        print 'Processing event ID=' + cast(@event_id as varchar(10)) + ', Order ID=' + cast(@order_id as varchar(10))
        update order_log set time_process_begin=getdate() where event_id=@event_id
        begin tran
        set @result = null
        if @event_type = 'new order' begin
                print '  Processing new order...'
                exec sp_commit_new_order_to_inventory @order_id, @result output
        end else if @event_type = 'address changed' begin
                print '  Processing address changed...'
                waitfor delay '00:00:01'  --csak szimuláljuk a többi eseménytípus feldolgozását
                set @result=0
        end else if @event_type = 'other change' begin
                print '  Processing other change...'
                waitfor delay '00:00:01'
                set @result=0
        end else begin
                print '  Unknown event type...'
                waitfor delay '00:00:01'
                set @result=1
        end

        if @result=0 begin
                print 'Event processing OK'
                commit tran
        end else begin
                print 'Event processing failed'
                rollback tran
        end
        print ''
        update order_log set time_process_end=getdate(),
                status=case when @result=0 then 2 else 1 end
                where event_id=@event_id
        fetch next from cursor_events into @event_id, @event_type, @order_id
end
close cursor_events deallocate cursor_events
go

--teszt
update order_log set status=0
select * from orders where EmployeeID is null
select * from order_log
exec dbo.sp_order_process
select * from order_log
