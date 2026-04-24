USE northwind;
GO

--TÖBBSZINTŰ CSOPORTOSÍTÁS
--dátum- és időfüggvények
select 2
select getdate() --datetime adattípus
select DATEDIFF(s,'2013-10-10 12:13:50.370', '2013-10-10 14:16:50.370')
select DATEADD(s, 1000, '2013-10-10 14:16:50.370')
select YEAR(getdate()), MONTH(getdate())

--RENDELÉSEK HÓNAP ÉS ALKALMAZOTT SZERINT
select e.employeeid, lastname, year(orderdate) as year, month(orderdate) as month,
count(orderid) as no_of_orders
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, year(orderdate), month(orderdate)
order by lastname, year, month

--ugyanez másképpen:
select e.employeeid, lastname,
cast(year(orderdate) as varchar(4)) +'_'+ cast(month(orderdate) as char(2)) as month,
count(orderid) as no_of_orders
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, cast(year(orderdate) as varchar(4)) +'_'+
cast(month(orderdate) as char(2))
order by lastname, month
