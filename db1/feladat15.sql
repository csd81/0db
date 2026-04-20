use northwind
go

set nocount on

declare
    @cat_id int = 1,
    @min_days int = 14,
    @min_orders int = 5,
    @min_ratio int = 70

if object_id('tempdb..#periods') is not null
    drop table #periods;

;with order_flags as (
    select
        o.OrderID,
        convert(date, o.OrderDate) as OrderDate,
        max(case when p.CategoryID = @cat_id then 1 else 0 end) as HasCategory
    from Orders o
    inner join [Order Details] od on od.OrderID = o.OrderID
    inner join Products p on p.ProductID = od.ProductID
    group by o.OrderID, convert(date, o.OrderDate)
),
day_stats as (
    select
        OrderDate,
        count(*) as OrderCount,
        sum(HasCategory) as CatOrderCount
    from order_flags
    group by OrderDate
),
day_cum as (
    select
        OrderDate,
        OrderCount,
        CatOrderCount,
        sum(OrderCount) over (order by OrderDate rows between unbounded preceding and current row) as CumOrders,
        sum(CatOrderCount) over (order by OrderDate rows between unbounded preceding and current row) as CumCatOrders,
        row_number() over (order by OrderDate) as rn
    from day_stats
)
select
    s.OrderDate as StartDate,
    e.OrderDate as EndDate,
    datediff(day, s.OrderDate, e.OrderDate) as DaysCount,
    e.CumOrders - isnull(sp.CumOrders, 0) as OrderCount,
    cast(round(
        100.0 * (e.CumCatOrders - isnull(sp.CumCatOrders, 0))
        / nullif(e.CumOrders - isnull(sp.CumOrders, 0), 0),
        0
    ) as int) as RatioPercent
into #periods
from day_cum s
left join day_cum sp on sp.rn = s.rn - 1
join day_cum e on e.rn >= s.rn
where datediff(day, s.OrderDate, e.OrderDate) >= @min_days
  and (e.CumOrders - isnull(sp.CumOrders, 0)) >= @min_orders
  and 1.0 * (e.CumCatOrders - isnull(sp.CumCatOrders, 0))
      / nullif(e.CumOrders - isnull(sp.CumOrders, 0), 0) >= @min_ratio / 100.0;

if exists (select 1 from #periods)
begin
    select
        convert(varchar(10), StartDate, 120) as [Időszak eleje],
        convert(varchar(10), EndDate, 120) as [Vége],
        DaysCount as [Napok száma],
        OrderCount as [Rendelések száma],
        cast(RatioPercent as varchar(10)) + '%' as [Arány]
    from #periods
    order by StartDate, EndDate;
end
else
begin
    print 'Nincs a feltételeknek megfelelő időszak.';
end
go
