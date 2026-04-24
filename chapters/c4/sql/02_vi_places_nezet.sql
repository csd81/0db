USE northwind;
GO

use DQS_STAGING_DATA
go
create view vi_places as
select distinct City, StateProvinceName StateProvince, EnglishCountryRegionName
CountryRegion
from AdventureworksDW2019.dbo.DimGeography
go
