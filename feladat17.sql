go
drop table if exists #tmp2
go

select
    o.orderid,
    o.employeeid,
    o.orderdate,
    cast(sum((1 - d.discount) * d.unitprice * d.quantity) as money) as value
into #tmp2
from orders o
inner join [order details] d on o.orderid = d.orderid
group by o.orderid, o.employeeid, o.orderdate
go

select
    a.employeeid,
    a.orderid,
    a.orderdate,
    a.mini
from (
    select
        employeeid,
        orderid,
        orderdate,
        min(value) over (
            partition by employeeid
            order by orderdate, orderid
            rows between 4 preceding and current row
        ) as mini,
        row_number() over (
            partition by employeeid
            order by orderdate, orderid
        ) as sorsz
    from #tmp2
) as a
where a.mini > 1000
  and a.sorsz > 4
order by a.employeeid, a.orderdate, a.orderid
go
