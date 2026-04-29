drop procedure sp_new_order
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
			waitfor delay '00:00:10'
		-- no more checks, we start the transaction (3 steps)
		-- 1. decrease the balance
    			print 'Processing order...'
				update customers set balance = balance-(@quantity*@unitprice) where customerid=@cust_id
		-- 2. new record in the  Orders, Order Details 
				insert into orders (customerID, orderdate) values (@cust_id, getdate()) --orderid: identity
				set @order_id = @@identity  --result of the last identity insert 
				insert [order details] (orderid, productid, quantity, UnitPrice, Discount) values(@order_id, @prod_id, @quantity, @unitprice, 0) --the correct line
		-- 3. update the stock
				update products set UnitsInStock=UnitsInStock-@quantity where ProductID=@prod_id
			waitfor delay '00:00:10'
		-- set the status				
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
update Products set UnitsInStock =3 where ProductName='chai'
update customers set balance=1000 where CustomerID in ('AROUT', 'ALFKI', 'ANATR')
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT'
	and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
go
--we run the stored proc
--set tran isolation level repeatable read

--Read Committed Snapshot Isolation (RCSI), https://www.sqlshack.com/snapshot-isolation-in-sql-server/
-- https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/snapshot-isolation-in-sql-server
--when data is modified, the committed versions of affected rows are copied to tempdb and given version numbers
--when another session reads the same data in Read Committed isolation level, then:
--	o	no READ locks are acquired, but there are no dirty reads because: 
--	o	the committed version of the data as of the time the reading transaction began is returned
--		"data read within a transaction will never reflect changes made by other simultaneous transactions. 
--		The transaction uses the data row versions that exist when the transaction begins"
--	o -> the read is not blocked -> less waiting on other transactions
--  o	snapshot isolation uses an optimistic concurrency model. If a snapshot transaction attempts to commit modifications 
--		to data that has changed since the transaction began, the transaction will roll back and an error will be raised


--ALTER DATABASE northwind SET READ_COMMITTED_SNAPSHOT OFF 
ALTER DATABASE northwind SET ALLOW_SNAPSHOT_ISOLATION ON    
ALTER DATABASE northwind SET READ_COMMITTED_SNAPSHOT ON  --replace the default READ COMMITTED behavior with SNAPSHOT
SELECT DB_NAME(database_id), is_read_committed_snapshot_on, snapshot_isolation_state_desc 
	FROM sys.databases WHERE database_id = DB_ID();  --1, ON

set tran isolation level read committed  
--run in 3 parallel sessions for the 3 companies
--delete the check constraint on Unison Stock manually
exec sp_new_order 'chai', 2, 'Arout' --all 3 sucessful, logical error (stock: -3)
--check
select UnitsInStock from Products where ProductName='chai'
select CompanyName, Balance from Customers where CustomerID in ('AROUT', 'ALFKI', 'ANATR')
--restore data
set tran isolation level repeatable read  --run in 3 parallel sessions for the 3 companies
exec sp_new_order 'chai', 2, 'Arout' --deadlock, one successful, 2 rolled back, no logical error (stock: 1)
--> the snaphot mode has effect only in read committed isolation level 
--> higher throughput expected in read-heavy applications




