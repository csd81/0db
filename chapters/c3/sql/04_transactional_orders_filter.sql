USE northwind;
GO

SELECT <published_columns> FROM [dbo].[Orders]
WHERE orderid in (
    select orderid from [Order Details]
    where ProductID in (select productid from Products where CategoryID=1)
)
