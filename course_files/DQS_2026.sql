use AdventureworksDW2019 

--Are there any relationships between NULLs in these columns? Does a NULL in one column lead to NULL in another column?
--Does a known, specific value in one column lead to NULL in another column?
select count(*) from DimCustomer --18484
select * from DimCustomer
select * from DimCustomer where AddressLine2 is not null
select * from DimCustomer where title is not null
select distinct Title from DimCustomer
select * from DimCustomer where Title='Sr.'
select * from DimCustomer where suffix is not null
--no
--another table:
select distinct Status from DimEmployee where EndDate is not null --always null
select distinct Status from DimEmployee where EndDate is null --always current -> functional dependency
--yes

--check if there is a functional dependency between two columns
select SalesReasonKey, SalesReasonName, SalesReasonReasonType from DimSalesReason

--the data suggests that the SalesReasonReasonType column depends on the SalesReasonName column i.e. we can always tell the former from the latter
--check if the data supports this assumption

select SalesReasonReasonType, count(*) from DimSalesReason group by SalesReasonReasonType  --3 groups with 4,5,1 members
select SalesReasonName, count(*) from DimSalesReason group by SalesReasonName  --each group has 1 member -> candidate key
--conclusion: the SalesReasonName is likely a subcategory of the SalesReasonReasonType

--checking functional dependency
--how to check if CountryRegionCode is functionally dependent on StateProvinceCode
select * from DimGeography
select StateProvinceCode, count(*) from DimGeography group by StateProvinceCode --71
select StateProvinceCode, count(*) from DimGeography group by StateProvinceCode,CountryRegionCode  --71
--71=71 so a StateProvinceCode will always have the same CountryRegionCode
--it is highly likely that we have a functional dependency between the two fields
select color, count(*) from dimproduct group by color --10
select ProductLine, count(*) from dimproduct group by productline --5
select ProductLine, count(*) from dimproduct group by productline, color --27 > 5, 27 > 10
--there is no functional dependency between the two fields

/*PRACTICE: analyze the columns of the DimCustomer and DimEmployee tables 
for completeness and functional dependency. 
DimCustomer: Education<->Occupation, DimEmployee: SalesTerritory<->Gender
*/

/*PRACTICE: cleanse the AdventureworksDW2019.DimGeography.EnglishCountryRegionName field using the Country/Region domain. 
Try again after adding a misspelled country to the table (Austrila).
*/

--CREATING A NEW KB
use DQS_STAGING_DATA
go
create view vi_places as
select distinct City, StateProvinceName StateProvince, EnglishCountryRegionName CountryRegion
from AdventureworksDW2019.dbo.DimGeography
go

/*PRACTICE: Build a KB using the DimProduct table, ProductName field and demonstrate its application as above.*/