USE northwind;
GO

select o.orderdate::timestamp(0) without time zone as orderdate,
c.companyname, c.country, c.balance, p.productname, od.quantity,
od.quantity * od.unitprice as value, p.unitsinstock
from products p join orderdetails od on p.productid=od.productid
    join orders o on o.orderid=od.orderid
    join customers c on c.customerid=o.customerid
order by orderdate desc limit 5;
