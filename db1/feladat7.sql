use northwind
go

set nocount on

declare @name nvarchar(100), @res_no int
declare @product_id int, @product_name nvarchar(100)
declare @units_in_stock int, @units_on_order int

set @name = 'Boston Crab Meat'

select @res_no = count(*)
from Products
where ProductName = @name

if @res_no = 0
    print 'Nincs ilyen nevű termék.'
else if @res_no > 1
    print 'Több mint 1 termék található.'
else
begin
    select
        @product_id = ProductID,
        @product_name = ProductName,
        @units_in_stock = UnitsInStock,
        @units_on_order = UnitsOnOrder
    from Products
    where ProductName = @name

    if @units_on_order = 0
        print 'A terméknek nincs függő rendelése, nem történt módosítás.'
    else
    begin
        update Products
        set
            UnitsInStock = UnitsInStock + UnitsOnOrder,
            UnitsOnOrder = 0
        where ProductID = @product_id

        select @units_in_stock = UnitsInStock
        from Products
        where ProductID = @product_id

        print 'Raktárkészlet frissítve.'
        print 'Új raktárkészlet: ' + cast(@units_in_stock as varchar(20))
    end
end
go
