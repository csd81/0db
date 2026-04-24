USE northwind;
GO

-- Az egyes rendelések értéke
select o.orderid, o.orderdate,
    str(sum((1-discount)*unitprice*quantity), 15, 2) as order_value,
    sum(quantity) as no_of_pieces,
    count(d.orderid) as no_of_items
from orders o inner join [order details] d on o.orderid=d.orderid
group by o.orderid, o.orderdate
order by sum((1-discount)*unitprice*quantity) desc

-- Évenként eladott mennyiség termékenkénti bontásban
select p.ProductID, p.ProductName, year(o.orderdate), SUM(quantity) as quantity
from orders o inner join [order details] d on o.orderid=d.orderid
inner join Products p on p.ProductID=d.ProductID
group by p.ProductID, p.ProductName, year(o.orderdate)
order by p.ProductName

-- Melyik alkalmazott adta el a legtöbb darabot a legnépszerűbb termékből 1998-ban?
select top 1 u.titleofcourtesy+' '+u.lastname+' '+u.firstname+' ('+u.title+')' as name,
    sum(quantity) as pieces_sold,
    pr.productname as productname
from orders o inner join [order details] d on o.orderid=d.orderid
    inner join employees u on u.employeeid=o.employeeid
    inner join products pr on pr.productid=d.productid
where year(o.orderdate)=1998 and d.productid =
    (select top 1 p.productid
    from products p left outer join [order details] d on p.productid=d.productid
    group by p.productid
    order by count(*) desc)
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname,
pr.ProductID, pr.productname
order by sum(quantity) desc
