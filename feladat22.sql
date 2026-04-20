go
create or alter function dbo.fn_order_fulfillable (@order_id int)
returns bit
as
begin
    declare @res bit = 0

    if exists (
        select 1
        from [Order Details]
        where OrderID = @order_id
    )
    and not exists (
        select 1
        from [Order Details] od
        inner join Products p on p.ProductID = od.ProductID
        where od.OrderID = @order_id
          and p.UnitsInStock < od.Quantity
    )
    begin
        set @res = 1
    end

    return @res
end
go

select
    o.OrderID,
    dbo.fn_order_fulfillable(o.OrderID) as Fulfillable
from Orders o
order by o.OrderID
go
