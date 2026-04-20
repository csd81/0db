-- ÖNÁLLÓ FELADAT #3a: beszállítók x kategóriák kimutatás PIVOT-tal, majd visszaalakítás UNPIVOT-tal
use northwind;
go

-- Kiinduló összesítés: egy beszállító egy kategóriában hány különböző termékkel szerepel
if object_id('tempdb..#src') is not null
    drop table #src;
go

select
    s.SupplierID,
    s.CompanyName as SupplierName,
    c.CategoryName,
    count(distinct p.ProductID) as ProductCount
into #src
from Products p
inner join Suppliers s on s.SupplierID = p.SupplierID
inner join Categories c on c.CategoryID = p.CategoryID
group by
    s.SupplierID,
    s.CompanyName,
    c.CategoryName;
go

-- Kereszttábla: beszállítók sorokban, kategóriák oszlopokban
if object_id('tempdb..#pivoted') is not null
    drop table #pivoted;
go

select
    SupplierID,
    SupplierName,
    [Beverages],
    [Condiments],
    [Confections],
    [Dairy Products],
    [Grains/Cereals],
    [Meat/Poultry],
    [Produce],
    [Seafood]
into #pivoted
from #src
pivot (
    sum(ProductCount)
    for CategoryName in (
        [Beverages],
        [Condiments],
        [Confections],
        [Dairy Products],
        [Grains/Cereals],
        [Meat/Poultry],
        [Produce],
        [Seafood]
    )
) as pt;
go

-- Eredmény: beszállítók x kategóriák kimutatás
select *
from #pivoted
order by SupplierName;
go

-- Visszaalakítás UNPIVOT-tal
select
    SupplierID,
    SupplierName,
    CategoryName,
    ProductCount
from #pivoted
unpivot (
    ProductCount for CategoryName in (
        [Beverages],
        [Condiments],
        [Confections],
        [Dairy Products],
        [Grains/Cereals],
        [Meat/Poultry],
        [Produce],
        [Seafood]
    )
) as upt
order by SupplierName, CategoryName;
go

drop table #src;
drop table #pivoted;
go
