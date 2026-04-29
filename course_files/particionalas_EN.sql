/* COLUMNSTORE INDEX DEMO */
--from BSc course
--restart server
USE AdventureworksDW2016CTP3
go
set statistics time on
set statistics io on
go
select count(*) from FactResellerSalesXL_CCI  --11669638
select count(*) from FactResellerSales_BTREE  --11669638
select count(*) from FactResellerSalesXL_PageCompressed  --11669638
go
dbcc freeproccache -- empty execution plan cache
dbcc dropcleanbuffers -- empty data buffer 

--B-TREE index
--============
select * into FactResellerSales_btree from FactResellerSalesXL_CCI
alter table FactResellerSales_btree add constraint p1 primary key (
	[SalesOrderNumber] ASC,
	[SalesOrderLineNumber] ASC
)--4 m 18 s
go
SELECT b.SalesTerritoryRegion
    ,FirstName + ' ' + LastName AS FullName
    ,count(SalesOrderNumber) AS NumSales
    ,sum(SalesAmount) AS TotalSalesAmt
    ,Avg(SalesAmount) AS AvgSalesAmt
    ,count(DISTINCT SalesOrderNumber) AS NumOrders
    ,count(DISTINCT ResellerKey) AS NumResellers
FROM FactResellerSales_BTREE a
INNER JOIN DimSalesTerritory b ON b.SalesTerritoryKey = a.SalesTerritoryKey
INNER JOIN DimEmployee d ON d.Employeekey = a.EmployeeKey
INNER JOIN DimDate c ON c.DateKey = a.OrderDateKey
WHERE b.SalesTerritoryKey = 3
    AND c.FullDateAlternateKey BETWEEN '1/1/2006' AND '1/1/2010'
GROUP BY b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
GO  --CPU time = 5218 ms,  elapsed time = 7719 ms

--Page compression
--(DATA_COMPRESSION = PAGE)
--================================
go
SELECT b.SalesTerritoryRegion
    ,FirstName + ' ' + LastName AS FullName
    ,count(SalesOrderNumber) AS NumSales
    ,sum(SalesAmount) AS TotalSalesAmt
    ,Avg(SalesAmount) AS AvgSalesAmt
    ,count(DISTINCT SalesOrderNumber) AS NumOrders
    ,count(DISTINCT ResellerKey) AS NumResellers
FROM FactResellerSalesXL_PageCompressed a
INNER JOIN DimSalesTerritory b ON b.SalesTerritoryKey = a.SalesTerritoryKey
INNER JOIN DimEmployee d ON d.Employeekey = a.EmployeeKey
INNER JOIN DimDate c ON c.DateKey = a.OrderDateKey
WHERE b.SalesTerritoryKey = 3
    AND c.FullDateAlternateKey BETWEEN '1/1/2006' AND '1/1/2010'
GROUP BY b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
GO  -- CPU time = 3264 ms,  elapsed time = 2356 ms.

--Column store with page compression
--CREATE CLUSTERED COLUMNSTORE INDEX [IndFactResellerSalesXL_CCI] ON [dbo].[FactResellerSalesXL_CCI] 
--WITH (DROP_EXISTING = OFF, COMPRESSION_DELAY = 0, DATA_COMPRESSION = COLUMNSTORE) ON [PRIMARY]
--===============================
SELECT b.SalesTerritoryRegion
    ,FirstName + ' ' + LastName AS FullName
    ,count(SalesOrderNumber) AS NumSales
    ,sum(SalesAmount) AS TotalSalesAmt
    ,Avg(SalesAmount) AS AvgSalesAmt
    ,count(DISTINCT SalesOrderNumber) AS NumOrders
    ,count(DISTINCT ResellerKey) AS NumResellers
FROM FactResellerSalesXL_CCI a
INNER JOIN DimSalesTerritory b ON b.SalesTerritoryKey = a.SalesTerritoryKey
INNER JOIN DimEmployee d ON d.Employeekey = a.EmployeeKey
INNER JOIN DimDate c ON c.DateKey = a.OrderDateKey
WHERE b.SalesTerritoryKey = 3
    AND c.FullDateAlternateKey BETWEEN '1/1/2006' AND '1/1/2010'
GROUP BY b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
GO  -- CPU time = 360 ms,  elapsed time = 492 ms.

-- Q. E. D.


--PARTITIONING
--We select YEAR as the basis of partitioning:
select min(OrderDate), max(OrderDate) FROM AdventureworksDW2016CTP3.dbo.FactInternetSales --2010..2014
--we'll have 5 partitions for the 5 years
go
--our partitioning function for the 5 years
CREATE PARTITION FUNCTION PfInternetSalesYear (TINYINT) AS RANGE LEFT FOR VALUES (10, 11, 12, 13)
go
--we have 4 limits that define 5 partitions
--e.g. '10': (year) <= 2010 due to the  LEFT 
--TINYINT: 1 byte, 0..255
--partitioning sheme: all partitions are stored in the same filegroup
CREATE PARTITION SCHEME PsInternetSalesYear AS PARTITION PfInternetSalesYear ALL TO ([PRIMARY])
go
--a new field is the partition number (tinyint), and we also need to change the key of the table because 
--the original key will be unique only within a single partition (due to partition swaps)
--drop table InternetSales
go
CREATE TABLE dbo.InternetSales(
	InternetSalesKey INT NOT NULL IDENTITY(1,1),
	PcInternetSalesYear TINYINT NOT NULL,  --new field
	CustomerDwKey INT,
	ProductKey INT NOT NULL,
	DateKey INT NOT NULL,
	OrderQuantity SMALLINT NOT NULL DEFAULT 0,
	SalesAmount MONEY NOT NULL DEFAULT 0,
	UnitPrice MONEY NOT NULL DEFAULT 0,
	DiscountAmount FLOAT NOT NULL DEFAULT 0,
	CONSTRAINT PK_InternetSales PRIMARY KEY (InternetSalesKey, PcInternetSalesYear)
)
ON PsInternetSalesYear(PcInternetSalesYear) --partition scheme
GO
--page compression
ALTER TABLE dbo.InternetSales REBUILD WITH (DATA_COMPRESSION = PAGE);
GO
--load data till 2013
INSERT INTO dbo.InternetSales (PcInternetSalesYear, CustomerDwKey, ProductKey, DateKey,
OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)
SELECT CAST(SUBSTRING(CAST(FIS.OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) AS PcInternetSalesYear,
--a trick: int type to make it small, but it contains a date, e.g. 20110223
	null,
	FIS.ProductKey, FIS.OrderDateKey, FIS.OrderQuantity, FIS.SalesAmount,
	FIS.UnitPrice, FIS.DiscountAmount
FROM AdventureworksDW2016CTP3.dbo.FactInternetSales AS FIS
WHERE CAST(SUBSTRING(CAST(FIS.OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) < 13
GO
--record count in each partition
SELECT
    partition_number,
    row_count
FROM sys.dm_db_partition_stats
WHERE object_id = OBJECT_ID('InternetSales');
--or:
SELECT $PARTITION.PfInternetSalesYear(PcInternetSalesYear), COUNT(*) AS NumberOfRows
FROM dbo.InternetSales GROUP BY $PARTITION.PfInternetSalesYear(PcInternetSalesYear)
--result:
PartitionNumber	NumberOfRows
1				14		--2010
2				2216	--2011
3				3397	--2012
--the fourth is yet empty

--columnstore index for all fields:
CREATE COLUMNSTORE INDEX CSI_InternetSales ON dbo.InternetSales
	(InternetSalesKey, PcInternetSalesYear, CustomerDwKey, ProductKey, DateKey,
	OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)
ON PsInternetSalesYear(PcInternetSalesYear) --here we match the index to the partition
GO

--we'll put new data in a table with a similar structure
--we use a check constraint to protect against errors
--drop table InternetSalesNew
go
create TABLE dbo.InternetSalesNew (
	InternetSalesKey INT NOT NULL IDENTITY(1,1),
	PcInternetSalesYear TINYINT NOT NULL CHECK (PcInternetSalesYear = 13), --protection
	CustomerDwKey INT,
	ProductKey INT NOT NULL,
	DateKey INT NOT NULL,
	OrderQuantity SMALLINT NOT NULL DEFAULT 0,
	SalesAmount MONEY NOT NULL DEFAULT 0,
	UnitPrice MONEY NOT NULL DEFAULT 0,
	DiscountAmount FLOAT NOT NULL DEFAULT 0,
	CONSTRAINT PK_InternetSalesNew PRIMARY KEY (InternetSalesKey, PcInternetSalesYear)
)
GO
--all settings are the same:
--go
ALTER TABLE dbo.InternetSalesNew REBUILD WITH (DATA_COMPRESSION = PAGE)
GO
--load year 2013
--since the table was empty, the insert will not be logged (FAST)
INSERT INTO dbo.InternetSalesNew (PcInternetSalesYear, CustomerDwKey,ProductKey, DateKey,
	OrderQuantity, SalesAmount,UnitPrice, DiscountAmount)
SELECT CAST(SUBSTRING(CAST(FIS.OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) AS PcInternetSalesYear,
	null, FIS.ProductKey, FIS.OrderDateKey,FIS.OrderQuantity, FIS.SalesAmount,
	FIS.UnitPrice, FIS.DiscountAmount
FROM AdventureworksDW2016CTP3.dbo.FactInternetSales AS FIS 
WHERE CAST(SUBSTRING(CAST(FIS.OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) = 13
GO
--create the colmunstore index also for the loading table
CREATE COLUMNSTORE INDEX CSI_InternetSalesNew
ON dbo.InternetSalesNew (InternetSalesKey, PcInternetSalesYear, CustomerDwKey, ProductKey, DateKey,
OrderQuantity, SalesAmount, UnitPrice, DiscountAmount);
GO
--swap the loading table in the fourth partition of the fact table
ALTER TABLE dbo.InternetSalesNew SWITCH TO dbo.InternetSales PARTITION 4
--THIS REQUIRED ONLY CHANGING METADATA, no data processing
--the new partitions:
SELECT $PARTITION.PfInternetSalesYear(PcInternetSalesYear) AS PartitionNumber, COUNT(*) AS NumberOfRows
FROM dbo.InternetSales GROUP BY $PARTITION.PfInternetSalesYear(PcInternetSalesYear) 
order by PartitionNumber

PartitionNumber	NumberOfRows
1				14
2				2216
3				3397
4				52801

select top 100 * from InternetSalesNew --empty
--before we can load the next partition, we must delete the columnstore index and change the check constraint
