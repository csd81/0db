USE northwind;
GO

--ki kinek a főnöke
select e.lastname, boss.lastname as boss, bboss.lastname as boss_of_boss
from employees e left outer join employees boss on e.reportsto=boss.employeeid
left outer join employees bboss on boss.reportsto=bboss.employeeid

--Hány rendelése van alkalmazottanként?
select e.lastname, count(orderid)
--a count(*) hamisan egy rendelést adna Lamernek, akinek valójában nincs rendelése
from employees e left outer join orders o on
--from employees e inner join orders o on
e.employeeid = o.employeeid
group by e.employeeid, e.lastname
order by count(*) desc

--kinek nincs rendelése?
select e.*
from employees e left outer join orders o on
e.employeeid = o.employeeid
where o.orderid is null
