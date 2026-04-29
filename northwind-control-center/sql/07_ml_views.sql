-- ML feature views for the Insights module.
-- These are optional — the Flask service queries the base tables directly,
-- but these views make ad-hoc exploration easier in SSMS.
USE Northwind;
GO

-- Order item features used for model training / inspection
CREATE OR ALTER VIEW dbo.vw_ml_order_features AS
SELECT
    od.OrderID,
    od.ProductID,
    p.ProductName,
    c.CategoryID,
    c.CategoryName,
    cu.Country,
    CAST(od.UnitPrice  AS FLOAT) AS unit_price,
    CAST(od.Discount   AS FLOAT) AS discount,
    od.Quantity,
    YEAR(o.OrderDate) AS order_year,
    CAST(od.UnitPrice * od.Quantity * (1.0 - od.Discount) AS FLOAT) AS item_value
FROM dbo.[Order Details] od
JOIN dbo.Orders     o  ON od.OrderID  = o.OrderID
JOIN dbo.Products   p  ON od.ProductID = p.ProductID
JOIN dbo.Categories c  ON p.CategoryID = c.CategoryID
JOIN dbo.Customers  cu ON o.CustomerID = cu.CustomerID
WHERE o.OrderDate IS NOT NULL;
GO

-- Inventory risk features (uses data-relative dates so it works on the 1996-1998 dataset)
CREATE OR ALTER VIEW dbo.vw_inventory_risk_features AS
WITH max_date AS (
    SELECT MAX(OrderDate) AS md FROM dbo.Orders
)
SELECT
    p.ProductID,
    p.ProductName,
    c.CategoryName,
    ISNULL(p.UnitsInStock, 0)  AS units_in_stock,
    ISNULL(p.ReorderLevel, 0)  AS reorder_level,
    ISNULL(p.UnitsOnOrder, 0)  AS units_on_order,
    ISNULL((
        SELECT SUM(od.Quantity)
        FROM dbo.[Order Details] od
        JOIN dbo.Orders o2 ON od.OrderID = o2.OrderID
        WHERE od.ProductID = p.ProductID
          AND o2.OrderDate >= DATEADD(day, -30, mx.md)
    ), 0) AS sales_last_30d,
    ISNULL((
        SELECT SUM(od.Quantity)
        FROM dbo.[Order Details] od
        JOIN dbo.Orders o2 ON od.OrderID = o2.OrderID
        WHERE od.ProductID = p.ProductID
          AND o2.OrderDate >= DATEADD(day, -90, mx.md)
    ), 0) AS sales_last_90d
FROM dbo.Products p
JOIN dbo.Categories c ON p.CategoryID = c.CategoryID
CROSS JOIN max_date mx
WHERE p.Discontinued = 0;
GO

-- Anomaly detection base data with statistical thresholds pre-computed as CTEs
-- (full anomaly logic runs in Python; this view is for exploration only)
CREATE OR ALTER VIEW dbo.vw_order_anomaly_candidates AS
WITH stats AS (
    SELECT
        AVG(CAST(od.Discount AS FLOAT)) AS avg_discount,
        STDEV(CAST(od.Discount AS FLOAT)) AS std_discount,
        AVG(CAST(od.UnitPrice * od.Quantity * (1.0 - od.Discount) AS FLOAT)) AS avg_value,
        STDEV(CAST(od.UnitPrice * od.Quantity * (1.0 - od.Discount) AS FLOAT)) AS std_value
    FROM dbo.[Order Details] od
),
items AS (
    SELECT
        od.OrderID,
        o.OrderDate,
        p.ProductName,
        c.CategoryName,
        cu.Country,
        CAST(od.UnitPrice AS FLOAT)  AS unit_price,
        od.Quantity,
        CAST(od.Discount AS FLOAT)   AS discount,
        CAST(od.UnitPrice * od.Quantity * (1.0 - od.Discount) AS FLOAT) AS item_value,
        CAST(ISNULL(o.Freight, 0) AS FLOAT) AS freight
    FROM dbo.[Order Details] od
    JOIN dbo.Orders     o  ON od.OrderID  = o.OrderID
    JOIN dbo.Products   p  ON od.ProductID = p.ProductID
    JOIN dbo.Categories c  ON p.CategoryID = c.CategoryID
    JOIN dbo.Customers  cu ON o.CustomerID = cu.CustomerID
)
SELECT
    i.*,
    CASE
        WHEN i.item_value > s.avg_value + 2 * s.std_value THEN 'high_value'
        WHEN i.discount   > s.avg_discount + 2 * s.std_discount AND i.discount > 0 THEN 'unusual_discount'
        ELSE 'normal'
    END AS anomaly_type
FROM items i
CROSS JOIN stats s
WHERE
    i.item_value > s.avg_value + 2 * s.std_value
    OR (i.discount > s.avg_discount + 2 * s.std_discount AND i.discount > 0);
GO

PRINT 'ML views created.';
