****************************************************************************************
triggers
We create a new insert trigger on the Orders table that runs long and throws an exception, thus disabling the order saving process 
*/


/****************************************************************************************
tight coupling demo
We create a new insert trigger on the Orders table that runs long and throws an exception, thus disabling the order saving process 
*/
drop trigger tr_demo_bad
go
create trigger tr_demo_bad on orders for insert as
declare @orderid int
select @orderid=OrderID from inserted
print 'New order ID: ' + cast(@orderid as varchar(50))
waitfor delay '00:00:10' --10 s
select 1/0 --we make an error
go
--test #1:  with both last lines commented out
insert  Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--restore table
delete Orders where CustomerID='AROUT' and EmployeeID is null
--test #2: recreate the trigger, with the last lines commented out
insert  Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--we have long to wait, but there is no error
--restore table
delete Orders where CustomerID='AROUT' and EmployeeID is null
--test #3: recreate the trigger, with all lines
insert  Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--we have long to wait, then we have the message:
'New order ID: 11094
Msg 8134, Level 16, State 1, Procedure tr_demo_bad, Line 6 [Batch Start Line 276]
Divide by zero error encountered.
The statement has been terminated.'
select * from Orders where CustomerID='AROUT' and EmployeeID is null
--no such record, because
--the insert statemant has been rolled back -> we crashed the trading system

--don't forget to drop the bad trigger
drop trigger tr_demo_bad

--PRACTICE
--write an update trigger for the Order Details: 
--when the quantity changes, update the UnitsInStock of the product
use northwind
drop trigger tr_demo
go
create trigger tr_demo on [order details] after update as
declare @productid int, @quantity_old int, @quantity_new int
if (select count(*) from inserted) > 1 
	raiserror('Only one item to be changed at a time', 16, 1)
else begin --we assume only one item was modified
	select @productid=productid, @quantity_new=Quantity from inserted 
	select @quantity_old=Quantity from deleted 
	print 'Product ID: ' + cast(@productid as varchar(50))
	update Products set UnitsInStock=UnitsInStock-(@quantity_new-@quantity_old) 
	where ProductID=@productid
		--may raise an error if the new UnitsInStock < 0
end
go

--test
select * from [Order Details] where OrderID=10248
--ordrid: 10248 pr.id 11, qu: 12
select UnitsInStock from Products where ProductID=11 --10
update [Order Details] set Quantity=6 where OrderID=10248 and ProductID=11
select UnitsInStock from Products where ProductID=11 --16
update [Order Details] set Quantity=40 where OrderID=10248 and ProductID=11 --error
--'The statement has been terminated.'
select UnitsInStock from Products where ProductID=11 --16
--OK
update [Order Details] set Quantity=40 where OrderID=10248 --more than 1 record
--the trigger does not run, but the Order Item records are updated

--restore original state
update Products set UnitsInStock=10 where ProductID=11
update [Order Details] set Quantity=12 where OrderID=10248 and ProductID=11

drop trigger tr_demo

--improved version that works for multiple updated records
drop trigger tr_demo
go
create trigger tr_demo on [order details] after update as
declare @ord_no int
begin --we allow more items to have been modified
	select @ord_no = count(*) from inserted 
	print 'updating records: ' + cast(@ord_no as varchar(50))
	update Products set UnitsInStock = UnitsInStock-(i.quantity-d.quantity) 
	from products p inner join inserted i on p.ProductID=i.ProductID
		inner join deleted d on i.ProductID=d.ProductID
		--may raise an error if the new UnitsInStock < 0
end
go

--TO BE TESTED....

/******************************************************				
loose coupling demo
The trigger only saves the events into a log table 
*******************************************************/

--the log table
go
--drop table order_log
go
create table order_log (
	event_id int IDENTITY (1, 1) primary key ,
	event_type varchar(50) NOT NULL ,
	order_id int NOT NULL , 
		--we use no references constraint to avoid runtime error
	status int NOT NULL default(0),
	time_created datetime NOT NULL default(getdate()) ,
	time_process_begin datetime NULL ,
	time_process_end datetime NULL ,
	process_duration as datediff(second, time_process_begin, time_process_end) 
) 
go
drop trigger tr_log_order
go
create trigger tr_log_order ON Orders for insert, update as
declare @order_id int
select @order_id=orderid from inserted 
			--there can be more than a single record in table inserted
print 'OrderID of the LAST record: ' + cast(@order_id as varchar(50))
if update(orderid) begin --if the orderid has changed, then this is an INSERT
	print 'Warning: new order'
	insert order_log (event_type, order_id)  --status, time_created: use default
		select 'new order', orderid from inserted
end else if update(shipaddress) or update(shipcity) begin --shipaddress or shipcity has changed
	print 'Warning: address changed'
	insert order_log (event_type, order_id)  
		select 'address changed', orderid from inserted
end else begin  --other change
	print 'Warning: other change'
	insert order_log (event_type, order_id)  
		select 'other change', orderid from inserted
end 
go

select * from orders where EmployeeID is null
delete [Order Details] where OrderID in (
	select OrderID from orders where EmployeeID is null
)
delete orders where EmployeeID is null

--test #1
insert  Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
select * from order_log
--delete order_log
--we have one new record in the log table

--test #2
insert  Orders (CustomerID, OrderDate) values ('AROUT', GETDATE()), 
	('HANAR', GETDATE())
select * from order_log
--we have two new records in the log table

--test #3
update Orders set ShipVia = 3 where OrderID in (11110, 11109) 
				--these are the IDs of test #2
select * from order_log
--we have two new records of the type 'other change'

--restore tables
delete Orders where CustomerID in ('AROUT', 'HANAR') and EmployeeID is null
delete order_log

--we expect that the items of a new order are inserted subsequently

--a simple stored procedure that processes a new order 
--and returns 0 if all of its items could be 
--committed to the inventory without error
--demonstrating also the use of output parameters
drop proc  sp_commit_new_order_to_inventory
go
create procedure sp_commit_new_order_to_inventory 
@orderid int,
@result int output
as
begin try
	update products set unitsInStock = unitsInStock - od.quantity 
	from products p inner join [Order Details] od on od.ProductID=p.ProductID 
	where od.OrderID=@orderid
	set @result=0
end try
begin catch
	print '  Inventory error: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) + ')'
	set @result=1
end catch
go

--test
select * from order_log --11108
select * from Products where ProductID=10 --unitsinstock =31
select * from Products where ProductID=9 --unitsinstock =29
insert [Order Details]  (orderid, productid, quantity, UnitPrice, Discount)
values (11108, 9, 10, 30, 0),(11108, 10, 4, 30, 0)  --the second item will cause an error in sp_commit_new_order_to_inventory

delete from [Order Details] where OrderID=11108

go
declare @res int
exec sp_commit_new_order_to_inventory 11108, @res output
print @res
exec sp_commit_new_order_to_inventory 11096, @res output
print @res
go
--check: no change in unitsinstock (OK)
select * from Products where ProductID=10 --unitsinstock =31
select * from Products where ProductID=9 --unitsinstock =29

--stored procedure for processing the order_log
--drop proc sp_order_process 
go
create proc sp_order_process as
declare @event_id int, @event_type varchar(50), @order_id int, @result int
declare cursor_events cursor forward_only static
	for 
	select  event_id, event_type, order_id
	from order_log where status=0 --we only care for the unprocessed events

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
		waitfor delay '00:00:01' --we only simulate the processing of other event types
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

--test
update order_log set status=0
select * from orders where EmployeeID is null
select * from order_log
exec dbo.sp_order_process
select * from order_log

select * from Products where productid

select * from products where ProductID=11

--we get:
Processing event ID=5, Order ID=11097
  Processing new order...
  Inventory error: The UPDATE statement conflicted with the CHECK constraint etc.
Event processing failed
 
Processing event ID=6, Order ID=11096
  Processing new order...
Event processing OK

