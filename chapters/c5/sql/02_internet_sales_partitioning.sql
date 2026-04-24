USE northwind;
GO

set statistics time off
set statistics io off
--év szerint:
select min(OrderDate), max(OrderDate)  from FactInternetSales s   --2010..2014
--5 évhez 5 partíciót hozunk létre
--drop table InternetSales
go
--particionáló függvény:
--drop partition function PfInternetSalesYear
create partition function PfInternetSalesYear (tinyint) as range left for values (10,
    11, 12, 13)
--pl. a '10' azt jelenti, hogy év <= 2010 (a LEFT miatt)
--TINYINT: 1 bájt, 0..255
--particionálási séma: minden ugyanabba a fájlcsoportba
--drop partition scheme PsInternetSalesYear
create partition scheme PsInternetSalesYear as partition PfInternetSalesYear all to
    ([PRIMARY])
go
--Megjegyzés: az identity kulcsot kombinálnunk kell a partíciószámmal, mert az identity
--csak a partíción belül lehet egyedi.
--drop table InternetSales
create table InternetSales(
      InternetSalesKey int not null identity(1,1),
      PcInternetSalesYear tinyint not null,  --partíciószám
      ProductKey int not null,
      DateKey int not null,
      OrderQuantity smallint not null default 0,
      SalesAmount money not null default 0,
      UnitPrice money not null default 0,
      DiscountAmount float not null default 0,
      constraint PK_InternetSales primary key (InternetSalesKey, PcInternetSalesYear)
)
ON PsInternetSalesYear(PcInternetSalesYear) --ez hozza létre a partíciókat
GO
--külső kulcsok hozzáadása és lap-alapú tömörítés
--ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_InternetSales_Customers FOREIGN
--KEY(CustomerDwKey)
--REFERENCES dbo.Customers (CustomerDwKey);
ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_InternetSales_Products FOREIGN
    KEY(ProductKey)
REFERENCES dbo.DimProduct (ProductKey);
ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_InternetSales_Dates FOREIGN
    KEY(DateKey)
REFERENCES dbo.DimDate (DateKey);
ALTER TABLE dbo.InternetSales REBUILD WITH (DATA_COMPRESSION = PAGE);
GO
--adatbetöltés 2013-ig
INSERT INTO dbo.InternetSales (PcInternetSalesYear, ProductKey, DateKey,
    OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)
SELECT CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) AS
    PcInternetSalesYear,
--figyelj a trükkre: a dátumok integerként tárolódnak, pl. 20110223, helytakarékosság miatt
      ProductKey, OrderDateKey, OrderQuantity, SalesAmount, UnitPrice, DiscountAmount
FROM FactInternetSales AS FIS
WHERE CAST(SUBSTRING(CAST(FIS.OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) < 13
GO
--hány rekord van a partíciókban?
SELECT $PARTITION.PfInternetSalesYear(PcInternetSalesYear) AS PartitionNumber,
    COUNT(*) AS NumberOfRows
FROM InternetSales GROUP BY $PARTITION.PfInternetSalesYear(PcInternetSalesYear)
PartitionNumber     NumberOfRows
1                   14          --2010
2                   2216        --2011
3                   3397        --2012
--az utolsó partíció még üres

--oszloptár:
CREATE COLUMNSTORE INDEX CSI_InternetSales ON dbo.InternetSales
      (InternetSalesKey, PcInternetSalesYear, ProductKey, DateKey,
      OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)
ON PsInternetSalesYear(PcInternetSalesYear) --Megjegyzés: az index igazított a partícióhoz
GO

--új segédtábla (staging) a 2013-as adatokhoz
--a hibák elkerülésére check-megszorítást használunk
create TABLE dbo.InternetSalesNew (
      InternetSalesKey INT NOT NULL IDENTITY(1,1),
      PcInternetSalesYear TINYINT NOT NULL CHECK (PcInternetSalesYear = 13), --check
      ProductKey INT NOT NULL,
      DateKey INT NOT NULL,
      OrderQuantity SMALLINT NOT NULL DEFAULT 0,
      SalesAmount MONEY NOT NULL DEFAULT 0,
      UnitPrice MONEY NOT NULL DEFAULT 0,
      DiscountAmount FLOAT NOT NULL DEFAULT 0,
      CONSTRAINT PK_InternetSalesNew PRIMARY KEY (InternetSalesKey,
    PcInternetSalesYear)
)
GO
ALTER TABLE dbo.InternetSalesNew ADD CONSTRAINT FK_InternetSalesNew_Products FOREIGN
    KEY(ProductKey) REFERENCES dbo.dimProduct (ProductKey);
ALTER TABLE dbo.InternetSalesNew ADD CONSTRAINT FK_InternetSalesNew_Dates FOREIGN
    KEY(DateKey) REFERENCES dbo.dimDate (DateKey);
go
ALTER TABLE dbo.InternetSalesNew REBUILD WITH (DATA_COMPRESSION = PAGE)
GO
--2013-as adatok betöltése
--mivel a tábla üres volt, a beszúrás nem kerül naplózásra
INSERT INTO dbo.InternetSalesNew (PcInternetSalesYear,ProductKey, DateKey,
      OrderQuantity, SalesAmount,UnitPrice, DiscountAmount)
SELECT CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) AS
    PcInternetSalesYear,
      ProductKey, OrderDateKey,OrderQuantity, SalesAmount, UnitPrice, DiscountAmount
FROM FactInternetSales
WHERE CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) = 13
GO
--oszloptár a segédtáblára
CREATE COLUMNSTORE INDEX CSI_InternetSalesNew
ON dbo.InternetSalesNew (InternetSalesKey, PcInternetSalesYear, ProductKey, DateKey,
    OrderQuantity, SalesAmount, UnitPrice, DiscountAmount);
GO
--a kulcslépés a 4. partíció betöltése
ALTER TABLE dbo.InternetSalesNew SWITCH TO dbo.InternetSales PARTITION 4
--ez nem igényelt adatátvitelt
--partíciók:
SELECT $PARTITION.PfInternetSalesYear(PcInternetSalesYear) AS PartitionNumber,
    COUNT(*) AS NumberOfRows
FROM dbo.InternetSales GROUP BY $PARTITION.PfInternetSalesYear(PcInternetSalesYear)
order by PartitionNumber
PartitionNumber     NumberOfRows
1                   14
2                   2216
3                   3397
4                   52801

select count(*) from InternetSalesNew --0!
