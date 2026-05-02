USE northwind;
GO

--Hány rendelése van alkalmazottanként?
--1/5) CSOPORTOSÍTÁS
select employeeid, count(*)
from orders
group by employeeid

--mellékes megjegyzés: hogyan teszteljük a NULL értéket?
select * from orders where employeeid is null
delete from orders where employeeid is null

--2/5) NE CSINÁLD EZT:
select e.lastname, count(*)
from orders o inner join employees e on o.employeeid=e.employeeid
group by e.lastname
--logikai hibát okoz, ha két személynek azonos a vezetékneve!!!

--3/5)
select e.lastname, e.firstname, count(*)
from orders o inner join employees e on o.employeeid=e.employeeid
group by e.employeeid, e.lastname, e.firstname
--ez a lekérdezés kihagyja azt az alkalmazottat, akinek nincs rendelése

--FELADAT: listázd ki az egyes kategóriákban lévő termékek számát (a CategoryName-re is szükségünk van)
3. select c.categoryid, c.categoryname, count(*) as no_prod
1. from products p inner join categories c on p.categoryid=c.categoryid
2. group by c.categoryid, c.categoryname
4. order by no_prod desc

--4/5)
select e.employeeid, e.lastname, e.firstname, count(*)
from employees e left outer join orders o on o.employeeid=e.employeeid
group by e.employeeid, e.lastname, e.firstname
--probléma: a tétlen alkalmazott hamisan 1-es darabszámot kap

--5/5)
select e.employeeid, e.lastname, e.firstname, count(o.orderid) as no_ord
from employees e left outer join orders o on o.employeeid=e.employeeid
group by e.employeeid, e.lastname, e.firstname
order by no_ord desc
--minden probléma megoldva
