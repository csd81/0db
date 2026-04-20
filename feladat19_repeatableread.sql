use northwind
go

set nocount on
set transaction isolation level repeatable read
go

declare @prod_name varchar(20), @quantity int, @cust_id nchar(5)
declare @status_message nvarchar(100), @status int
declare @res_no int
declare @prod_id int, @order_id int
declare @stock int
declare @cust_balance money
declare @unitprice money

set @prod_name = 'boston'
set @quantity = 10
set @cust_id = 'AROUT'

begin tran
begin try
    select @res_no = count(*)
    from Products
    where ProductName like '%' + @prod_name + '%'

    if @res_no <> 1
    begin
        set @status = 1
        set @status_message = 'HIBA: a terméknév nem egyértelmű.'
    end
    else
    begin
        select @prod_id = ProductID, @stock = UnitsInStock
        from Products
        where ProductName like '%' + @prod_name + '%'

        if @stock < @quantity
        begin
            set @status = 2
            set @status_message = 'HIBA: a raktárkészlet nem fedezi a megrendelést.'
        end
        else
        begin
            select @cust_balance = balance
            from Customers
            where CustomerID = @cust_id

            select @unitprice = UnitPrice
            from Products
            where ProductID = @prod_id

            if @cust_balance < @quantity * @unitprice or @cust_balance is null
            begin
                set @status = 3
                set @status_message = 'HIBA: a vásárló nem található, vagy az egyenlege túl alacsony.'
            end
            else
            begin
                waitfor delay '00:00:10'

                update Customers
                set Balance = Balance - (@quantity * @unitprice)
                where CustomerID = @cust_id

                insert into Orders (CustomerID, OrderDate)
                values (@cust_id, getdate())

                set @order_id = scope_identity()

                insert into [Order Details] (OrderID, ProductID, Quantity, UnitPrice, Discount)
                values (@order_id, @prod_id, @quantity, @unitprice, 0)

                set @status = 0
                set @status_message = cast(@order_id as varchar(20)) + ' sz. rendelés sikeresen felvéve.'
            end
        end
    end

    print 'Állapot: ' + cast(@status as varchar(50))
    print @status_message

    if @status = 0
        commit tran
    else
    begin
        rollback tran
        print 'Visszagörgetve'
    end
end try
begin catch
    if @@trancount > 0
        rollback tran

    print 'EGYÉB HIBA: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')'
end catch
go
