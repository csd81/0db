/*
PRACTICE: create a loosely coupled solution that monitors the Products table and orders new supply from
the associated Supplier when the UnitsinStock value falls below the value specified in the ReorderLevel
field.*/

--SOLUTION

go
create table product_log (
	event_id int IDENTITY (1, 1) primary key ,
	event_type varchar(50) NOT NULL ,
	product_id int NOT NULL , 
	status int NOT NULL default(0),
	time_created datetime NOT NULL default(getdate()) ,
	time_process_begin datetime NULL ,
	time_process_end datetime NULL ,
	process_duration as datediff(second, time_process_begin, time_process_end) 
) 
go
create trigger tr_log_product ON products for update as
declare @product_id int
select @product_id=productid from inserted 
print 'ProductID of the LAST record: ' + cast(@product_id as varchar(50))
if update(unitsinstock) begin 
	print 'Warning: stock changed'
	insert product_log (event_type, product_id)  
		select 'stock changed', productid from inserted
end else begin  --other change
	print 'Warning: other change'
	insert product_log (event_type, product_id)  
		select 'other change', productid from inserted
end 
go
--test 
update products set UnitsInStock=100 where productid=10
go
drop proc  sp_order_new_stock
go
create procedure sp_order_new_stock 
@productid int,
@result int output
as
declare @stock int, @level int
select @stock=UnitsInStock, @level=ReorderLevel from products where productid=@productid
if @stock < @level
	print 'Please order '+ cast(@level-@stock as varchar(50)) +' new units of product No. '+ cast(@productid as varchar(50))
else print 'No reorder necessary'
set @result=0
go
--test
select * from product_log --10
update products set ReorderLevel =80 where ProductID=10
update products set UnitsInStock =70 where ProductID=10

declare @res int
exec sp_order_new_stock 10, @res output
print @res

go
create proc sp_prod_process as
declare @event_id int, @event_type varchar(50), @product_id int, @result int
declare cursor_events cursor forward_only static
	for 
	select  event_id, event_type, product_id
	from product_log where status=0 
set xact_abort on 
set nocount on
open cursor_events
fetch next from cursor_events into @event_id, @event_type, @product_id
while @@fetch_status = 0
begin
	print 'Processing event ID=' + cast(@event_id as varchar(10)) + ', Product ID=' + cast(@product_id as varchar(10))
	update product_log set time_process_begin=getdate() where event_id=@event_id
	begin transaction 
	set @result = null
	if @event_type = 'stock changed' begin
		print '  changed stock...'
		exec sp_order_new_stock @product_id, @result output
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
	update product_log set time_process_end=getdate(), 
		status=case when @result=0 then 2 else 1 end 
		where event_id=@event_id		
	fetch next from cursor_events into @event_id, @event_type, @product_id
end
close cursor_events deallocate cursor_events
go

--test
select * from products where productid=10
select * from product_log
exec dbo.sp_prod_process
