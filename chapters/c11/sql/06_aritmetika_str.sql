USE northwind;
GO

--melyik a legnagyobb rendelés?
--aritmetika
4. select o.orderid,
   cast(o.orderdate as varchar(50)) as order_date,
   str(sum((1-discount)*unitprice*quantity), 15, 2) as order_total,
   sum(quantity) as no_of_units,
   count(d.orderid) as no_of_items
1. from orders o inner join [order details] d on o.orderid=d.orderid
2. where...
3. group by o.orderid, o.orderdate
   --order by o.orderdate
5. order by sum((1-discount)*unitprice*quantity) desc

--a dátum szerinti rendezéshez:
group by o.orderid, o.orderdate
