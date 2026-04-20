use northwind;
go

-- Demo: new Northwind order with a single order item.
-- This version keeps the business-process structure from the notes,
-- but uses the corrected Order Details insert so the script is runnable.

set nocount on;

declare @prod_name varchar(20), @quantity int, @cust_id nchar(5);
declare @status_message nvarchar(100), @status int;
declare @res_no int;
declare @prod_id int, @order_id int;
declare @stock int;
declare @cust_balance money;
declare @unitprice money;

-- Parameters
set @prod_name = 'boston';
set @quantity = 10;
set @cust_id = 'AROUT';

begin try
    select @res_no = count(*)
    from products
    where productname like '%' + @prod_name + '%';

    if @res_no <> 1
    begin
        set @status = 1;
        set @status_message = 'ERROR: Ambiguous Product name.';
    end
    else
    begin
        -- If we find a single product, we look for the key and the stock.
        select @prod_id = productID, @stock = unitsInStock
        from products
        where productName like '%' + @prod_name + '%';

        if @stock < @quantity
        begin
            set @status = 2;
            set @status_message = 'ERROR: Stock is insufficient.';
        end
        else
        begin
            -- Does the customer have credit?
            select @cust_balance = balance
            from customers
            where customerid = @cust_id;

            -- There cannot be more than one hit because customerid is a key.
            select @unitprice = unitPrice
            from products
            where productID = @prod_id; -- no discount

            if @cust_balance < @quantity * @unitprice or @cust_balance is null
            begin
                set @status = 3;
                set @status_message = 'ERROR: Customer not found or balance insufficient.';
            end
            else
            begin
                -- No more checks, we start the transaction (3 steps).

                -- 1. Decrease the balance.
                update customers
                set balance = balance - (@quantity * @unitprice)
                where customerid = @cust_id;

                -- 2. New record in Orders, Order Details.
                insert into orders (customerID, orderdate)
                values (@cust_id, getdate()); -- orderid: identity

                set @order_id = @@identity; -- result of the last identity insert

                -- Original broken line from the notes:
                -- insert [order details] (orderid, productid, quantity, UnitPrice)
                -- values(@order_id, @prod_id, @quantity, @unitprice)

                -- Correct line:
                insert [order details] (orderid, productid, quantity, UnitPrice, Discount)
                values (@order_id, @prod_id, @quantity, @unitprice, 0);

                -- 3. Update product stock.
                update products
                set unitsInStock = unitsInStock - @quantity
                where productid = @prod_id;

                set @status = 0;
                set @status_message = cast(@order_id as varchar(20)) + ' order processed successfully.';
            end
        end
    end

    print cast(@status as varchar(20));
    print @status_message;
end try
begin catch
    print 'OTHER ERROR: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')';
end catch
go

-- Testing setup from the notes.
set nocount off;

update products set unitsInStock = 900 where productid = 40;
update customers set balance = 1000 where CustomerID = 'AROUT';
delete [Order Details]
where OrderID in (
    select orderid
    from Orders
    where CustomerID = 'AROUT'
      and EmployeeID is null
);
delete Orders
where CustomerID = 'AROUT'
  and EmployeeID is null;

-- Check results.
select * from Customers where CustomerID = 'AROUT';
select * from Products where productid = 40;
select top 3 * from Orders where CustomerID = 'arout' order by OrderDate desc;
go
