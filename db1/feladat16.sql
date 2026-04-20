go
drop table if exists #tmp
go

select
    orderdate,
    cast(sum((1 - discount) * unitprice * quantity) as money) as value
into #tmp
from orders o
inner join [order details] d on o.orderid = d.orderid
group by o.orderid, o.orderdate
order by orderdate
go

select a.OrderDate, a.mini
from (
    select
        orderdate,
        min(value) over (
            order by orderdate
            rows between 4 preceding and current row
        ) as mini,
        row_number() over (order by orderdate) as sorsz
    from #tmp
) as a
where a.mini > 1000
  and a.sorsz > 4
order by a.OrderDate
go
