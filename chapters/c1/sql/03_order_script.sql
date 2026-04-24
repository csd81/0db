USE northwind;
GO

-- változók
declare @prod_name varchar(20), @quantity int, @cust_id nchar(5) -- a telefonon kapott, szöveges vevőazonosító
declare @status_message nvarchar(100), @status int               -- az üzleti folyamat eredménye
declare @res_no int                                              -- találatok száma
declare @prod_id int, @order_id int                              -- azonosítók
declare @stock int                                               -- meglévő termékkészlet
declare @cust_balance money                                      -- a vevő egyenlege
declare @unitprice money                                         -- a termék egységára

-- paraméterek
set @prod_name = 'boston'
set @quantity = 10
set @cust_id = 'AROUT'

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
                -- nincs több ellenőrzés, kezdjük a tranzakciót (3 lépés)
                -- 1. egyenleg csökkentése
                update customers set balance = balance-(@quantity*@unitprice) where customerid=@cust_id
                -- 2. új rekord az Orders és Order Details táblákban
                insert into orders (customerID, orderdate) values (@cust_id, getdate()) -- orderid: identity
                set @order_id = @@identity -- az utolsó identity beszúrás eredménye
                insert [order details] (orderid, productid, quantity, UnitPrice) -- itt hibát vétünk
                    values(@order_id, @prod_id, @quantity, @unitprice)
                -- a helyes sor a következő lenne:
                -- insert [order details] (orderid, productid, quantity, UnitPrice, Discount)
                --     values(@order_id, @prod_id, @quantity, @unitprice, 0)
                -- 3. készlet frissítése
                update products set unitsInStock = unitsInStock - @quantity where productid = @prod_id
                set @status = 0
                set @status_message = cast(@order_id as varchar(20)) + ' order processed successfully.'
            end
        end
    end
    print @status
    print @status_message
end try
begin catch
    print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) + ')'
end catch
go

-- teszt-előkészítés
set nocount off
update products set unitsInStock = 900 where productid=40
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT' and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
-- a szkript futtatása után ellenőrizzük:
select * from Customers where CustomerID='AROUT'
select * from Products where productid=40
select top 3 * from Orders where CustomerID='arout' order by OrderDate desc
-- Látszólag rendben van. A Discount mezőn azonban figyelmen kívül hagytunk egy NOT NULL kényszert:
--   "OTHER ERROR: Cannot insert the value NULL into column 'Discount'"
-- Ráadásul a vevő egyenlegét is csökkentettük!
-- Egyidejű (konkurens) környezetben további hibák is felléphetnek.
-- Javítás után teszteljük a másik két ágat is.
