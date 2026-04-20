use northwind
go

set nocount on

declare @order_id int = 10248
declare @res_no int

select @res_no = count(*)
from [Order Details]
where OrderID = @order_id

if @res_no = 0
    print 'Nincs ilyen rendelés vagy nincs hozzá tétel.'
else
begin
    update p
    set p.UnitsInStock = p.UnitsInStock - od.Quantity
    from Products p
    inner join [Order Details] od on od.ProductID = p.ProductID
    where od.OrderID = @order_id

    print 'A rendelés teljesítve a raktárból.'
end
go
