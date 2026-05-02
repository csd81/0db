USE northwind;
GO

--Ki a legfiatalabb alkalmazott? Mi a neve?
--1/2) a legnagyobb születési dátum
--aggregáló függvények: max, min, avg, std, sum, count
select max(birthdate) as max_year, min(birthdate) as min_year
--, lastname --hibát okozna
from employees

--2/2) ágyazd be ezt a lekérdezést
select lastname, birthdate from employees
where birthdate = ('1966-01-27 00:00:00.000')

select lastname, birthdate as "birth date" from employees
where birthdate = (
    select max(birthdate) as max_year
    from employees
)

--FELADAT: keresd meg az első rendelés ShipAddress mezőjét
select orderdate, shipaddress from orders
where orderdate = (
    select min(orderdate) as min_date
    from orders
)

--a legfiatalabb alkalmazott szállítási címei
--táblák összekapcsolása
select distinct lastname, shipaddress
from orders o inner join employees e on o.employeeid=e.employeeid
where e.employeeid = (
    select employeeid from employees
    where birthdate = (
        select max(birthdate) as max_year
        from employees
    )
)
order by shipaddress --desc
