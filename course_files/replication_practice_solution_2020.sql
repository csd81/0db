--PRIM server
use northwind
alter table orders add status int not null default 0
update orders set status=2
--update event for test
update Orders set EmployeeID=5 where orderid=10248
--new order evenrt for test
insert orders (EmployeeID) values (1)

go
create trigger tr_repl on orders for update as
update orders set status=1 where orderid in (select orderid from inserted)
go
update Orders set EmployeeID=2 where orderid=10248
update Orders set status=2 where orderid=10248



--THIRD server
use northwind_new_orders
--replicated table: orders
select * from Orders where orderid=10248
go
create proc sp_order_process as
declare @status int, @event_type varchar(50), @order_id int, @result int
declare cursor_events cursor forward_only static
	for 
	select orderid, status
	from orders where status in (0,1) --we only care for the unprocessed events
set xact_abort on 
set nocount on
open cursor_events
fetch next from cursor_events into  @order_id, @status
while @@fetch_status = 0
begin
	print 'Processing Order ID=' + cast(@order_id as varchar(10))
	begin tran 
	set @result = null
	if @status = 0 begin
		print '  Processing new order...'
		waitfor delay '00:00:01' 
		set @result=0
	end else begin
		print '  Processing changed order...'
		waitfor delay '00:00:01' --we only simulate the processing of other event types
		set @result=0
	end 
	if @result=0 begin
		print 'Event processing OK' 
		commit tran
	end else begin
		print 'Event processing failed'
		rollback tran
	end
	update orders set status=2 where orderid=@order_id		
	fetch next from cursor_events into @order_id, @status
end
close cursor_events deallocate cursor_events

--test locally

select * from orders where status=0
select * from orders where orderid=10248

exec dbo.sp_order_process
