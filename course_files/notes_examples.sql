--EXAMPLE QUERIES FOR THE Northwind database

--	Value of each order
select o.orderid, o.orderdate,
    str(sum((1-discount)*unitprice*quantity), 15, 2) as order_value,
    sum(quantity) as no_of_pieces,
    count(d.orderid) as no_of_items
from orders o inner join [order details] d on o.orderid=d.orderid
group by o.orderid, o.orderdate
order by sum((1-discount)*unitprice*quantity) desc

--	Quantities sold for each product on a yearly basis
select p.ProductID, p.ProductName, year(o.orderdate), SUM(quantity) as quantity
from orders o inner join [order details] d on o.orderid=d.orderid
inner join Products p on p.ProductID=d.ProductID
group by p.ProductID, p.ProductName, year(o.orderdate)
order by p.ProductName

--	Which employee sold the most pieces of the most popular product in 1998?
select top 1 u.titleofcourtesy+' '+u.lastname+' '+ u.firstname +' ('+u.title +')'  as name,
    sum(quantity) as pieces_sold,
    pr.productname as productname
from orders o inner join [order details] d on o.orderid=d.orderid
    inner join employees u on u.employeeid=o.employeeid
    inner join products pr on pr.productid=d.productid
where year(o.orderdate)=1998 and d.productid =
    (select top 1 p.productid
    from products p left outer join [order details] d on p.productid=d.productid
    group by p.productid
    order by count(*) desc)
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname, pr.ProductID,pr.productname 
order by sum(quantity) desc

--a simple script that demonstrates the elements of T-SQL
--we search for an emplyee, and if we find a single matching record, 
--we increase the salary of the employee by 10%
set nocount on
declare @name nvarchar(20), @address nvarchar(max), @res_no int, @emp_id int
set @name='Fuller'
select @res_no=count(*) from Employees where LastName like @name + '%'
if @res_no=0 print 'No matching record.'
else if @res_no>1 print 'More than one matching record.'
else begin  --a single hit
	select @address=Country+', '+City+' '+Address, @emp_id=EmployeeID 
		from Employees where LastName like @name
	print 'Employee ID: ' + cast(@emp_id as varchar(10)) + ', address: ' + @address
	update Employees set salary=1.1*salary where EmployeeID=@emp_id
	print 'Salary increased.'
end
go

--wrap it in a stored procedure
create procedure sp_increase_salary @name nvarchar(40)
as
set nocount on
declare @address nvarchar(max), @res_no int, @emp_id int
select @res_no=count(*) from Employees where LastName like @name + '%'
if @res_no=0 print 'No matching record.'
else if @res_no>1 print 'More than one matching record.'
else begin  --a single hit
	select @address=Country+', '+City+' '+Address, @emp_id=EmployeeID 
		from Employees where LastName like @name
	print 'Employee ID: ' + cast(@emp_id as varchar(10)) + ', address: ' + @address
	update Employees set salary=1.1*salary where EmployeeID=@emp_id
	print 'Salary increased.'
end
go
--test
select Salary from Employees where LastName like 'Fuller%'
exec sp_increase_salary 'Fuller'
select Salary from Employees where LastName like 'Fuller%'

--a scalar valued function that returns the salary of a person or 0 if the person is not found
go
create function fn_salary (@name nvarchar(40)) returns money as
begin
	declare @salary money, @res_no int
	select @res_no=count(*) from Employees where LastName like @name + '%'
	if @res_no <> 1 set @salary=0
	else select @salary=Salary from Employees where LastName like @name  + '%'
	return @salary
end
go
--test
select dbo.fn_salary('Kingg') as salary


--an example script for making a new order that contains a single order item
--tables needed: products, customers, orders, order details
set nocount on 
--variables
declare @prod_name varchar(20), @quantity int, @cust_id nchar(5) --we receive the textual customer id over the phone
declare @status_message nvarchar(100),  @status int --the result of the business process
declare @res_no int --No of hits
declare @prod_id int, @order_id int --IDs
declare @stock int --existing product stock
declare @cust_balance money --customers balance
declare @unitprice money --unit price of product

-- parameters
set @prod_name = 'boston'
set @quantity = 10
set @cust_id = 'AROUT'

begin try
	select @res_no = count(*) from products where productname like '%' + @prod_name + '%'
	if @res_no <> 1 begin
		set @status = 1
		set @status_message = 'ERROR: Ambiguous Product name.';
	end else begin
		-- if we find a single product, we look for the key and the stock
		select @prod_id = productID, @stock = unitsInStock from products where productName like '%' + @prod_name + '%'
		-- is the stock sufficient?
		if @stock < @quantity begin
			set @status = 2
			set @status_message = 'ERROR: Stock is insufficient.'
		end else begin
		-- Does the customer have credit?
			select @cust_balance = balance from customers where customerid = @cust_id
						--if there is no hit, the @cust_balance is null 
						--there cannot be more than one hit
			select @unitprice = unitPrice from products where productID = @prod_id --no discount
			if @cust_balance < @quantity*@unitprice or @cust_balance is null begin 
				set @status = 3
				set @status_message = 'ERROR: Customer not found or balance insufficient.'
			end else begin 
		-- no more checks, we start the transaction (2 steps)
		-- 1. decrease the balance
    			print 'Processing order...'
				update customers set balance = balance-(@quantity*@unitprice) where customerid=@cust_id
		-- 2. new record in the  Orders, Order Details 
				insert into orders (customerID, orderdate) values (@cust_id, getdate()) --orderid: identity
				set @order_id = @@identity  --result of the last identity insert 
		--		insert [order details] (orderid, productid, quantity, UnitPrice) --here we make an error
			--		values(@order_id, @prod_id, @quantity, @unitprice) --here we make an error
				insert [order details] (orderid, productid, quantity, UnitPrice, Discount) --the correct line
					values(@order_id, @prod_id, @quantity, @unitprice, 0) --the correct line
				set @status = 0
				set @status_message = 'Order No. ' + cast(@order_id as varchar(20)) + ' processed successfully.'
			end
		end
	end
	print 'Status: ' + cast(@status as varchar(50))
	print @status_message	
end try 
begin catch
	print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) + ')'
end catch
go

--we set parameters for testing
set nocount off
update products set unitsInStock = 900 where productid=40
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT' and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
--we run the script and then check:
select * from Customers where CustomerID='AROUT'
select * from Products where productid=40
select top 3 * from Orders where CustomerID='arout' order by OrderDate desc

--Seems fine. However we neglected a NOT NULL constraint of the discount field:
--"OTHER ERROR: Cannot insert the value NULL into column 'Discount'"
--But we decreased the balance of the customer!

--in a concurrent environment, other errors may manifest as well

--after correction, test the other two branches as well

--CURSORS

go
declare @emp_id int, @emp_name nvarchar(50), @i int, @address nvarchar(60)
declare cursor_emp cursor for
    select employeeid, lastname, address from employees order by lastname
set @i=1
open cursor_emp
fetch next from cursor_emp into @emp_id, @emp_name, @address
while @@fetch_status = 0
begin
    print cast(@i as varchar(5)) + ' EMPLOYEE:'
    print 'ID: ' + cast(@emp_id as varchar(5)) + ', LASTNAME: ' + @emp_name + ', ADDRESS: ' + @address
    set @i=@i+1
    fetch next from cursor_emp into @emp_id, @emp_name, @address
end
close cursor_emp
deallocate cursor_emp
go
--equivalent to this SELECT 
select 'ID: ' + cast(employeeid as varchar(5)) + isnull(', Név: ' + lastname, '') + isnull( ', cím: ' + address, '')
from employees order by lastname
--or, with a row number
select cast(row_number() over(order by lastname) as varchar(50))+ 
'. ügynök: ID: ' + cast(employeeid as varchar(5)) + isnull(', Név: ' + lastname, '') + isnull( ', cím: ' + address, '')
from employees 



--TRANSACTIONS
--implicit transaction demo
drop table t1
go
create table t1 (id int primary key)
create table t2 (id int primary key, t1_id int references t1(id))
go
insert t1 (id) values (1), (3), (4), (5)
insert t2 (id, t1_id) values (10, 3) --after this, the (3) record in t1 cannot be deleted
go
delete t1 --implicit transaction
--"The DELETE statement conflicted with the REFERENCE constraint ..." etc
select * from t1 --all records as before: the transaction has been rolled back

--nesting and trancount
begin tran
	print @@trancount  --1
	begin tran
		print @@trancount  --2
	commit tran
	print @@trancount  --1
commit tran
print @@trancount  --0

begin tran
	print @@trancount  --1
	begin tran
		print @@trancount  --2
rollback tran
print @@trancount  --0

--simple demo for atomicity, with xact_abort on
set xact_abort off
delete t2
go
begin tran
	insert t2 (id, t1_id) values (10, 1)
	insert t2 (id, t1_id) values (11, 2) --foreign key constraint violation
	insert t2 (id, t1_id) values (12, 3)
commit tran
go
--"The INSERT statement conflicted with the FOREIGN KEY constraint ..." etc
select * from t2
id	t1_id
10	1
12	3
--atomicity was not preserved
set xact_abort on
delete t2
go
begin tran
	insert t2 (id, t1_id) values (10, 1)
	insert t2 (id, t1_id) values (11, 2) --foreign key constraint violation
	insert t2 (id, t1_id) values (12, 3)
commit tran
go
--"The INSERT statement conflicted with the FOREIGN KEY constraint ..." etc
select * from t2
id	t1_id
--atomicity was preserved

--simple demo for atomicity, with programmed rollback
...

--simple demo for isolation: the webshop case
create table test_product(id int primary key, prod_name varchar(50) not null, sold varchar(50), buyer varchar(50))
insert test_product(id, prod_name, sold) values (1, 'car', 'for sale')
insert test_product(id, prod_name, sold) values (2, 'horse', 'for sale')
go
select * from test_product
update test_product set sold='for sale', buyer=null where id=2
go
set tran isolation level read committed --the default
go
begin tran
declare @sold varchar(50)
select @sold=sold from test_product where id=2 
if @sold='for sale' begin
    waitfor delay '00:00:10' --now we are performing the bank transfer
    update test_product set sold='sold', buyer='My name' where id=2
    print 'sold successfully'
end else print 'product not available'
commit tran
go
--we run the above transaction concurrently in two query editors
--the second script:
set tran isolation level read committed 
go
begin tran
declare @sold varchar(50)
select @sold=sold from test_product where id=2
if @sold='for sale' begin
    waitfor delay '00:00:10' --now we are performing the bank transfer
    update test_product set sold='sold', buyer='Your name' where id=2 --note the diff
    print 'sold successfully'
end else print 'product not available'
commit tran
go
--check what happens:
select * from test_product
id	prod_name	sold		buyer
1	car			for sale	NULL
2	horse		sold		Your name
--The horse was sold successfully to two customers, but only Your name will receive it. Very awkward.
update test_product set sold='for sale', buyer=null where id=2
--Now try the same with set tran isolation level repeatable read  
--"Transaction (Process ID 53) was deadlocked on lock resources with another process and has been chosen as the deadlock victim. Rerun the transaction."
--No logical error. Only one horse is sold.

--Conclusion: be careful to select the right isolation level.

--We now add transactional support to our script and wrap it into a stored procedure
--drop procedure sp_new_order
go
create procedure sp_new_order 
@prod_name nvarchar(40), @quantity smallint, @cust_id nchar(5)
as
set nocount on 
set xact_abort on
--variables
declare @status_message nvarchar(100),  @status int --the result of the business process
declare @res_no int --No of hits
declare @prod_id int, @order_id int --IDs
declare @stock int --existing product stock
declare @cust_balance money --customers balance
declare @unitprice money --unit price of product
begin tran
begin try
	select @res_no = count(*) from products where productname like '%' + @prod_name + '%'
	if @res_no <> 1 begin
		set @status = 1
		set @status_message = 'ERROR: Ambiguous Product name.';
	end else begin
		-- if we find a single product, we look for the key and the stock
		select @prod_id = productID, @stock = unitsInStock from products where productName like '%' + @prod_name + '%'
		-- is the stock sufficient?
		if @stock < @quantity begin
			set @status = 2
			set @status_message = 'ERROR: Stock is insufficient.'
		end else begin
		-- Does the customer have credit?
			select @cust_balance = balance from customers where customerid = @cust_id
						--if there is no hit, the @cust_balance is null 
						--there cannot be more than one hit
			select @unitprice = unitPrice from products where productID = @prod_id --no discount
			if @cust_balance < @quantity*@unitprice or @cust_balance is null begin 
				set @status = 3
				set @status_message = 'ERROR: Customer not found or balance insufficient.'
			end else begin 
		-- no more checks, we start the transaction (2 steps)
		-- 1. decrease the balance
    			print 'Processing order...'
				update customers set balance = balance-(@quantity*@unitprice) where customerid=@cust_id
		-- 2. new record in the  Orders, Order Details 
				insert into orders (customerID, orderdate) values (@cust_id, getdate()) --orderid: identity
				set @order_id = @@identity  --result of the last identity insert 
				insert [order details] (orderid, productid, quantity, UnitPrice) values(@order_id, @prod_id, @quantity, @unitprice) --here we make an error
		--		insert [order details] (orderid, productid, quantity, UnitPrice, Discount) values(@order_id, @prod_id, @quantity, @unitprice, 0) --the correct line
				set @status = 0
				set @status_message = 'Order No. ' + cast(@order_id as varchar(20)) + ' processed successfully.'
			end
		end
	end
	print 'Status: ' + cast(@status as varchar(50))
	print @status_message	
	if @status = 0 commit tran else begin
		print 'Rolling back transaction'
		rollback tran
	end
end try 
begin catch
	print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) + ')'
	print 'Rolling back transaction'
	rollback tran
end catch
go

--test
--we set parameters for testing
set nocount off
update products set unitsInStock = 900 where productid=40
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT' and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
--we run the stored proc 
exec sp_new_order 'boston', 10, 'Arout' 
--check the results:
select * from Customers where CustomerID='AROUT' --should be 816
select * from Products where productid=40  --should be 890
select top 3 * from Orders o inner join [Order Details] od on o.OrderID=od.OrderID
	where CustomerID='arout' order by OrderDate desc --should see the new item
select @@trancount --must be 0

/****************************************************************************************
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

