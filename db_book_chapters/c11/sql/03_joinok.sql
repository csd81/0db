USE northwind;
GO

--milyen termékeket rendeltek a legfiatalabb alkalmazottól
--megjegyzés: mindig a lekérdezés FROM részével kezdjünk
select distinct p.productname, e.lastname
from orders o inner join employees e on o.employeeid=e.employeeid
inner join [order details] od on od.orderid=o.orderid
inner join products p on p.productid=od.productid
where e.employeeid=9 --ő a legfiatalabb
order by productname

--FELADAT: mely városokba szállítják az 1-es kategóriájú termékeket?
select distinct o.shipcity
from orders o inner join [order details] od on od.orderid=o.orderid
inner join products p on p.productid=od.productid
where p.categoryid = 1 --a keresési feltételünk
order by shipcity
