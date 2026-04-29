-- Optional helper views for the Operations dashboard.
-- The Flask app queries sys tables directly; these views are provided for convenience.
USE Northwind;
GO

CREATE OR ALTER VIEW dbo.vw_low_stock_products AS
SELECT
    ProductID,
    ProductName,
    UnitsInStock,
    ReorderLevel,
    UnitsOnOrder,
    CASE WHEN Discontinued = 1 THEN 'Yes' ELSE 'No' END AS Discontinued
FROM dbo.Products
WHERE UnitsInStock <= ReorderLevel;
GO

CREATE OR ALTER VIEW dbo.vw_table_row_counts AS
SELECT
    t.name AS table_name,
    SUM(p.rows) AS row_count
FROM sys.tables t
JOIN sys.partitions p ON t.object_id = p.object_id
WHERE p.index_id IN (0, 1)
  AND t.is_ms_shipped = 0
GROUP BY t.name;
GO

PRINT 'Ops views created.';
