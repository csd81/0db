use northwind
drop procedure if exists sp_new_order
go
create procedure sp_new_order @prod_name nvarchar(40), @quantity smallint, @cust_id nchar(5)
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
		--	waitfor delay '00:00:10'
		-- no more checks, we start the transaction (3 steps)
		-- 1. decrease the balance
    	--		print 'Processing order...'
				update customers set balance = balance-(@quantity*@unitprice) where customerid=@cust_id
		-- 2. new record in the  Orders, Order Details 
				insert into orders (customerID, orderdate) values (@cust_id, getdate()) --orderid: identity
				set @order_id = @@identity  --result of the last identity insert 
				insert [order details] (orderid, productid, quantity, UnitPrice, Discount) values(@order_id, @prod_id, @quantity, @unitprice, 0) --the correct line
		-- 3. update the stock
				update products set UnitsInStock=UnitsInStock-@quantity where ProductID=@prod_id
		--	waitfor delay '00:00:10'
		-- set the status				
				set @status = 0
				set @status_message = 'Order No. ' + cast(@order_id as varchar(20)) + ' processed successfully.'
			end
		end
	end
	--print 'Status: ' + cast(@status as varchar(50))
	--print @status_message	
	if @status = 0 commit tran else begin
		--print 'Rolling back transaction'
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
go
alter table products drop constraint DF_Products_UnitsInStock
alter table products drop constraint CK_UnitsInStock
alter table products alter column unitsinstock int
go
--we set parameters for testing
update Products set UnitsInStock =1000000, UnitPrice=1 where ProductName='chai'
update customers set balance=10000000 where CustomerID in ('AROUT', 'ALFKI', 'ANATR')
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID in ('AROUT', 'ALFKI', 'ANATR')
	and EmployeeID is null)
delete Orders where CustomerID in ('AROUT', 'ALFKI', 'ANATR') and EmployeeID is null
go
--exec sp_new_order 'chai', 1, 'AROUT' 

--set tran isolation level repeatable read  
--run the proc in 3 parallel sessions
declare @starttime DATETIME2 = sysdatetime();  
declare @runs int = 10000, @i int = 0, @r int, @custid nchar(5)
while @i < @runs begin
	set @r = cast(3*RAND() as int)
	set @custid = case when @r=0 then 'AROUT' when @r=1 then 'ALFKI' else 'ANATR' end
	exec sp_new_order 'chai', 1, @custid 
	set @i += 1
end
print concat('Runtime: ', datediff(ms, @starttime, sysdatetime()))
--in 3 parallel sessions: 11s
--in 1 session: 5 s

--with repeatable read: 15-20 minutes in each session with lots of deadlocks
---> only ca 15000 orders (of the 30000) were successful 

--using MOTs, 1 session: 6.1 s 
--parallel sessions: OTHER ERROR: The current transaction attempted to update a record that has been updated since this transaction started.
---> only ca 20000 orders were successful

--native sp. -> no transaction management, no one-part names, no options setting, no LIKE, no print, no identity

drop procedure if exists sp_new_order_nat
go
create procedure sp_new_order_nat @prod_name nvarchar(40), @quantity smallint, @cust_id nchar(5)
with native_compilation, schemabinding, execute as owner
as
begin atomic with (transaction isolation level = snapshot, language = 'us_english') 

declare @status_message nvarchar(100),  @status int --the result of the business process
declare @res_no int --No of hits
declare @prod_id int, @order_id int --IDs
declare @stock int --existing product stock
declare @cust_balance money --customers balance
declare @unitprice money --unit price of product
	select @res_no = count(*) from dbo.products where productname = @prod_name
	if @res_no <> 1 begin
		set @status = 1
	end else begin
		select @prod_id = productID, @stock = unitsInStock from dbo.products where productName = @prod_name		-- is the stock sufficient?
		if @stock < @quantity begin
			set @status = 2
		end else begin
			select @cust_balance = balance from dbo.customers where customerid = @cust_id
			select @unitprice = unitPrice from dbo.products where productID = @prod_id --no discount
			if @cust_balance < @quantity*@unitprice or @cust_balance is null begin 
				set @status = 3
			end else begin 
				update dbo.customers set balance = balance-(@quantity*@unitprice) where customerid=@cust_id
				insert into dbo.orders (customerID, orderdate) values (@cust_id, getdate()) --orderid: identity
				set @order_id = SCOPE_IDENTITY()  --result of the last identity insert 
				insert dbo.[order details] (orderid, productid, quantity, UnitPrice, Discount) values(@order_id, @prod_id, @quantity, @unitprice, 0) --the correct line
				update dbo.products set UnitsInStock=UnitsInStock-@quantity where ProductID=@prod_id
			end
		end
	end
end
go

exec sp_new_order_nat 'chai', 1, 'alfki'

--test
declare @starttime DATETIME2 = sysdatetime();  
declare @runs int = 10000, @i int = 0, @r int, @custid nchar(5)
while @i < @runs begin
	set @r = cast(3*RAND() as int)
	set @custid = case when @r=0 then 'AROUT' when @r=1 then 'ALFKI' else 'ANATR' end
	exec sp_new_order_nat 'chai', 1, @custid 
	set @i += 1
end
print concat('Runtime: ', datediff(ms, @starttime, sysdatetime()))
--1 session: 2.6 s
--3 sessions: 4/6.5/5.5 s, no conflicts due to snapshot isolation
