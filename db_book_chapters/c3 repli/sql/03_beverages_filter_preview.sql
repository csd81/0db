USE northwind;
GO

select * from [Order Details]
where ProductID in (select productid from Products where CategoryID=1)

select * from orders
where orderid in (
    select orderid from [Order Details]
    where ProductID in (select productid from Products where CategoryID=1)
)
