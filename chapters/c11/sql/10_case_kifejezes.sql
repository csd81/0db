USE northwind;
GO

--select case szerkezet
select e.employeeid, lastname,
case
    when month(orderdate) < 10 then cast(year(orderdate) as varchar(4)) +'_0'+
        cast(month(orderdate) as char(2))
    when month(orderdate) >= 10 then cast(year(orderdate) as varchar(4)) +'_'+
        cast(month(orderdate) as char(2))
    else 'N.A'
end as month,
count(orderid) as no_of_orders
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname,
case
    when month(orderdate) < 10 then cast(year(orderdate) as varchar(4)) +'_0'+
        cast(month(orderdate) as char(2))
    when month(orderdate) >= 10 then cast(year(orderdate) as varchar(4)) +'_'+
        cast(month(orderdate) as char(2))
    else 'N.A'
end --egy függvény jobban szolgálná ezt a célt
order by lastname, month
