USE northwind;
GO

go
create procedure sp_new_order
    @prod_name nvarchar(40), @quantity smallint, @cust_id nchar(5)
as
set nocount on
set xact_abort on
-- változók
declare @status_message nvarchar(100), @status int  -- az üzleti folyamat eredménye
declare @res_no int                                 -- találatok száma
declare @prod_id int, @order_id int                 -- azonosítók
declare @stock int                                  -- meglévő termékkészlet
declare @cust_balance money                         -- a vevő egyenlege
declare @unitprice money                            -- a termék egységára

begin tran
begin try
    select @res_no = count(*) from products where productname like '%' + @prod_name + '%'
    if @res_no <> 1 begin
        set @status = 1
        set @status_message = 'ERROR: Ambiguous Product name.';
    end else begin
        -- ha egyetlen terméket találunk, kikeressük a kulcsát és a készletét
        select @prod_id = productID, @stock = unitsInStock from products
            where productName like '%' + @prod_name + '%'
        -- elegendő-e a készlet?
        if @stock < @quantity begin
            set @status = 2
            set @status_message = 'ERROR: Stock is insufficient.'
        end else begin
            -- Van-e fedezete a vevőnek?
            select @cust_balance = balance from customers where customerid = @cust_id
            -- ha nincs találat, a @cust_balance null; több találat nem lehet
            select @unitprice = unitPrice from products where productID = @prod_id -- kedvezmény nélkül
            if @cust_balance < @quantity*@unitprice or @cust_balance is null
            begin
                set @status = 3
                set @status_message = 'ERROR: Customer not found or balance insufficient.'
            end else begin
                -- nincs több ellenőrzés, kezdjük a tranzakciót (2 lépés)
                -- 1. egyenleg csökkentése
                print 'Processing order...'
                update customers set balance = balance-(@quantity*@unitprice) where customerid=@cust_id
                -- 2. új rekord az Orders és Order Details táblákban
                insert into orders (customerID, orderdate) values (@cust_id, getdate()) -- orderid: identity
                set @order_id = @@identity -- az utolsó identity beszúrás eredménye
                insert [order details] (orderid, productid, quantity, UnitPrice)
                    values(@order_id, @prod_id, @quantity, @unitprice) -- itt hibát vétünk
                -- a helyes sor a következő lenne:
                -- insert [order details] (orderid, productid, quantity, UnitPrice, Discount)
                --     values(@order_id, @prod_id, @quantity, @unitprice, 0)
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

-- teszt
set nocount off
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT' and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
-- a tárolt eljárás futtatása
exec sp_new_order 'boston', 10, 'Arout'
-- az eredmények ellenőrzése:
select * from Customers where CustomerID='AROUT' -- 816-nak kell lennie
select top 3 * from Orders o inner join [Order Details] od on o.OrderID=od.OrderID
    where CustomerID='arout' order by OrderDate desc -- látnunk kell az új tételt
select @@trancount -- 0-nak kell lennie
