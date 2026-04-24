USE northwind;
GO

--ideiglenes táblák használata
select GETDATE() as ido into #uj_tabla
select * from #uj_tabla
drop table #uj_tabla

select * into #uj_tabla from employees

--drop table #tt
select e.employeeid, lastname, year(orderdate) as ev, month(orderdate) as month,
count(orderid) as no_of_orders
into #tt
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, year(orderdate), month(orderdate)
order by lastname, month

select * from #tt

--Figyelmeztetés: Null értéket kizár egy aggregáló vagy más SET művelet.
--ok: aggregáló függvény (max, sum, avg..) null értékeken működik
select * from #tt
select lastname, str(avg(cast(no_of_orders as float)), 15, 2) as avg_no_of_orders
--select lastname, avg(no_of_orders) as avg_no_of_orders
from #tt group by employeeid, lastname
order by avg_no_of_orders desc

--másik megoldás ugyanarra a problémára beágyazott lekérdezéssel
select forras.lastname, str(avg(cast(forras.no_of_orders as float)), 15, 2) as
avg_no_of_orders
from (
    select e.employeeid, lastname, year(orderdate) as ev, month(orderdate) as month,
    count(orderid) as no_of_orders
    from employees e left outer join orders o on e.employeeid=o.employeeid
    group by e.employeeid, lastname, year(orderdate), month(orderdate)
) as forras --alias használata kötelező
group by employeeid, lastname
order by avg_no_of_orders desc
