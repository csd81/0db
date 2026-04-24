USE northwind;
GO

use AdventureWorksDW2016_ext

/*
--BTREE tábla létrehozása
select * into FactResellerSalesXL_BTREE from FactResellerSalesXL_CCI --2 perc 30 mp
alter table FactResellerSalesXL_BTREE alter column SalesOrderLineNumber tinyint not null
alter table FactResellerSalesXL_BTREE alter column SalesOrderNumber nvarchar(20) not null
alter table FactResellerSalesXL_BTREE add constraint c1 primary key
    (SalesOrderLineNumber, SalesOrderNumber) --2 perc
*/

--SZERVER ÚJRAINDÍTÁSA
set statistics time on
set statistics io on
go
select count(*) from FactResellerSalesXL_BTREE  --11669638
exec sp_spaceused 'dbo.FactResellerSalesXL_BTREE', @updateusage = 'TRUE'
--adat: 2523168 KB, index: 9776 KB

select count(*) from FactResellerSalesXL_PageCompressed  --11669638
exec sp_spaceused 'dbo.FactResellerSalesXL_PageCompressed', @updateusage = 'TRUE'
--adat: 695624 KB, index: 2344 KB

select count(*) from FactResellerSalesXL_CCI  --11669638
exec sp_spaceused 'dbo.FactResellerSalesXL_CCI', @updateusage = 'TRUE'
--adat: 525344 KB, index: 157624 KB

go
dbcc freeproccache --

dbcc dropcleanbuffers -- adatpuffer ürítése

--B-TREE
--========
select b.SalesTerritoryRegion
    ,FirstName + ' ' + LastName as FullName
    ,count(SalesOrderNumber) as NumSales
    ,sum(SalesAmount) as TotalSalesAmt
    ,Avg(SalesAmount) as AvgSalesAmt
    ,count(distinct SalesOrderNumber) as NumOrders
    ,count(distinct ResellerKey) as NumResellers
from FactResellerSalesXL_BTREE a
inner join DimSalesTerritory b on b.SalesTerritoryKey = a.SalesTerritoryKey
inner join DimEmployee d on d.Employeekey = a.EmployeeKey
inner join DimDate c on c.DateKey = a.OrderDateKey
where b.SalesTerritoryKey = 3
    and c.FullDateAlternateKey between '1/1/2006' and '1/1/2010'
group by b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
--CPU idő = 3949 ms, eltelt idő = 9568 ms

--DATA_COMPRESSION = PAGE
--==================================
go
select b.SalesTerritoryRegion
    ,FirstName + ' ' + LastName as FullName
    ,count(SalesOrderNumber) as NumSales
    ,sum(SalesAmount) as TotalSalesAmt
    ,Avg(SalesAmount) as AvgSalesAmt
    ,count(distinct SalesOrderNumber) as NumOrders
    ,count(distinct ResellerKey) as NumResellers
from FactResellerSalesXL_PageCompressed a
inner join DimSalesTerritory b on b.SalesTerritoryKey = a.SalesTerritoryKey
inner join DimEmployee d on d.Employeekey = a.EmployeeKey
inner join DimDate c on c.DateKey = a.OrderDateKey
where b.SalesTerritoryKey = 3
    and c.FullDateAlternateKey between '1/1/2006' and '1/1/2010'
group by b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
GO  -- CPU idő = 3264 ms, eltelt idő = 3776 ms.

--oszloptár lap-alapú tömörítéssel
--create clustered columnstore index [IndFactResellerSalesXL_CCI] on
--[dbo].[FactResellerSalesXL_CCI]
--with (drop_existing = off, compression_delay = 0, data_compression = columnstore) on
--[primary]
--================================
select b.SalesTerritoryRegion
    ,FirstName + ' ' + LastName as FullName
    ,count(SalesOrderNumber) as NumSales
    ,sum(SalesAmount) as TotalSalesAmt
    ,Avg(SalesAmount) as AvgSalesAmt
    ,count(distinct SalesOrderNumber) as NumOrders
    ,count(distinct ResellerKey) as NumResellers
from FactResellerSalesXL_CCI a
inner join DimSalesTerritory b on b.SalesTerritoryKey = a.SalesTerritoryKey
inner join DimEmployee d on d.Employeekey = a.EmployeeKey
inner join DimDate c on c.DateKey = a.OrderDateKey
where b.SalesTerritoryKey = 3
    and c.FullDateAlternateKey between '1/1/2006' and '1/1/2010'
group by b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
GO  -- CPU idő = 360 ms, eltelt idő = 492 ms
