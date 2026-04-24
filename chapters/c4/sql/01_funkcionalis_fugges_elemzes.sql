USE northwind;
GO

use AdventureworksDW2019

--vizsgáljuk, van-e funkcionális függés két oszlop között
select SalesReasonKey, SalesReasonName, SalesReasonReasonType from DimSalesReason

--az adatok azt sugallják, hogy a SalesReasonReasonType oszlop függ
--a SalesReasonName oszloptól, azaz az előbbi mindig megállapítható az utóbbiból
--ellenőrizzük, hogy az adatok alátámasztják-e ezt a feltevést

select SalesReasonReasonType, count(*) from DimSalesReason group by
SalesReasonReasonType  --3 csoport 4, 5 és 1 taggal
select SalesReasonName, count(*) from DimSalesReason group by SalesReasonName  --minden
--csoportnak 1 tagja van -> jelölt kulcs
--következtetés: a SalesReasonName valószínűleg a SalesReasonReasonType alkategóriája

--funkcionális függés ellenőrzése
--hogyan ellenőrizzük, hogy a CountryRegionCode funkcionálisan függ-e a StateProvinceCode-tól
select * from DimGeography

select StateProvinceCode, count(*) from DimGeography group by StateProvinceCode --71
select StateProvinceCode, count(*) from DimGeography group by
StateProvinceCode,CountryRegionCode  --71
--71=71, tehát egy StateProvinceCode mindig ugyanazt a CountryRegionCode-ot kapja
--nagy valószínűséggel funkcionális függés van a két mező között
select color, count(*) from dimproduct group by color --10
select ProductLine, count(*) from dimproduct group by productline --5
select ProductLine, count(*) from dimproduct group by productline, color --27 > 5, 27
> 10
--nincs funkcionális függés a két mező között
