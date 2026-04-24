USE northwind;
GO

--melyik a legnépszerűbb termék?
-- top 1
select top 1 p.productid, p.productname, count(*) as no_app,
sum(quantity) as total_pieces
from products p left outer join [order details] d on p.productid=d.productid
group by p.productid, p.productname
order by no_app desc

--melyik alkalmazott adta el a legtöbbet a legnépszerűbb termékből?
--első verzió
select top 1 u.titleofcourtesy+' '+u.lastname+' '+ u.firstname +' ('+u.title +')' as name,
sum(quantity) as no_pieces_sold
from orders o inner join [order details] d on o.orderid=d.orderid
inner join employees u on u.employeeid=o.employeeid
where d.productid = 59 --ezt már tudjuk
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
-- having....
order by sum(quantity) desc

/************************************************************************
FELADAT
--melyik alkalmazott adta el a legtöbbet a legnépszerűbb termékből, és mi annak a
terméknek a neve?
--a pubs_access adatbázisban: melyik a leggyakrabban használt kiadó annál a szerzőnél, akinek
a legtöbb publikációja van?
**************************************************************************/
