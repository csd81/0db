USE northwind;
GO

use northwind

create view vi_products as
select productid, productname from products;
go

create view vi_orders as
select orderid, cast(orderdate as date) odate from orders;
go

create view vi_orders_products as
select o.orderid, p.productid, od.Quantity quantity,
    od.Quantity * od.UnitPrice * (1 - od.Discount) price
from orders o join [Order Details] od on o.orderid = od.OrderID
    join products p on od.ProductID = p.productid;
go
