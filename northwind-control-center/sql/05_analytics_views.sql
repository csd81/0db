-- Analytics views (optional — Flask queries these tables directly).
USE Northwind;
GO

CREATE OR ALTER VIEW dbo.vw_sales_by_month AS
SELECT
    YEAR(o.OrderDate)  AS sales_year,
    MONTH(o.OrderDate) AS sales_month,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
FROM dbo.Orders o
JOIN dbo.[Order Details] od ON o.OrderID = od.OrderID
WHERE o.OrderDate IS NOT NULL
GROUP BY YEAR(o.OrderDate), MONTH(o.OrderDate);
GO

CREATE OR ALTER VIEW dbo.vw_sales_by_category AS
SELECT
    c.CategoryName,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
FROM dbo.Categories c
JOIN dbo.Products p  ON c.CategoryID = p.CategoryID
JOIN dbo.[Order Details] od ON p.ProductID = od.ProductID
GROUP BY c.CategoryName;
GO

CREATE OR ALTER VIEW dbo.vw_top_products AS
SELECT
    p.ProductName,
    SUM(od.Quantity) AS units_sold,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
FROM dbo.Products p
JOIN dbo.[Order Details] od ON p.ProductID = od.ProductID
GROUP BY p.ProductName;
GO

CREATE OR ALTER VIEW dbo.vw_orders_by_country AS
SELECT
    c.Country,
    COUNT(DISTINCT o.OrderID) AS order_count,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
FROM dbo.Customers c
JOIN dbo.Orders o           ON c.CustomerID = o.CustomerID
JOIN dbo.[Order Details] od ON o.OrderID = od.OrderID
WHERE c.Country IS NOT NULL
GROUP BY c.Country;
GO

PRINT 'Analytics views created.';
