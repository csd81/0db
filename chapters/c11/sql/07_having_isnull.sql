USE northwind;
GO

--ki a legsikeresebb alkalmazott? hány rendeléssel?
-- figyeld meg: having
-- count distinct
-- számok formázása
select u.titleofcourtesy+' '+u.lastname+' '+ u.firstname +' ('+u.title +')' as name,
str(sum((1-discount)*unitprice*quantity), 15, 2) as cash_income,
count(distinct o.orderid) as no_of_orders, count(productid) as no_of_items
from orders o inner join [order details] d on o.orderid=d.orderid
inner join employees u on u.employeeid=o.employeeid
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
--having count(o.orderid)>200 --ha csak a több mint 200 rendeléssel rendelkező alkalmazottak érdekelnek
order by cash_income
--sum((1-discount)*unitprice*quantity) desc

--miért csak 9 van?
select count(*) from employees
--10-nek kellene lennie!
--szükségünk lenne azokra is, akiknek 0 rendelésük van
-- isnull függvény
select isnull(u.titleofcourtesy, '')+' '+isnull(u.lastname, '')+' '+ isnull(u.firstname,
'') +' ('+isnull(u.title, '') +')' as name,
isnull(str(sum((1-discount)*unitprice*quantity), 15, 2), 'N/A') as cash_income,
count(distinct o.orderid) as no_of_orders, COUNT(d.productid) as no_of_items
from employees u left outer join
(orders o inner join [order details] d on o.orderid=d.orderid)
on u.employeeid=o.employeeid
--where u.titleofcourtesy='Mr.' --ha csak a férfiak érdekelnek
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
order by sum((1-discount)*unitprice*quantity) desc
