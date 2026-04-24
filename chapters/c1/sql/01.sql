

select o.orderid, o.orderdate,
	str(sum((1-discount)*unitprice*quantity), 12, 2) as order_value,
	sum(quantity) as no_of_pieces,
	count(d.orderid) as no_of_items
from orders o inner join [order details] d on o.orderid=d.orderid
group by o.orderid, o.orderdate
order by sum((1-discount)*unitprice*quantity) desc
