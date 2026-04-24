USE northwind;
GO

SELECT <published_columns> FROM [dbo].[Orders]
WHERE ShipCountry = 'USA'
