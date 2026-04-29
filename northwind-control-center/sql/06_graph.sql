-- Creates SQL Server graph tables for the Graph Explorer module.
-- Requires SQL Server 2017+ with graph tables enabled.
USE Northwind;
GO

-- Node tables
IF OBJECT_ID('dbo.g_orders',    'U') IS NULL CREATE TABLE dbo.g_orders    (orderid INT PRIMARY KEY, orderdate DATE NOT NULL) AS NODE;
IF OBJECT_ID('dbo.g_products',  'U') IS NULL CREATE TABLE dbo.g_products  (productid INT PRIMARY KEY, productname NVARCHAR(40) NOT NULL) AS NODE;
IF OBJECT_ID('dbo.g_customers', 'U') IS NULL CREATE TABLE dbo.g_customers (customerid NCHAR(5) PRIMARY KEY, companyname NVARCHAR(40) NOT NULL, country NVARCHAR(15) NULL) AS NODE;
GO

-- Edge tables
IF OBJECT_ID('dbo.g_order_contains', 'U') IS NULL
    CREATE TABLE dbo.g_order_contains (quantity SMALLINT NOT NULL, value MONEY NOT NULL) AS EDGE;

IF OBJECT_ID('dbo.g_customer_places', 'U') IS NULL
    CREATE TABLE dbo.g_customer_places AS EDGE;
GO

-- Populate nodes (safe to re-run; clears and reloads)
DELETE FROM dbo.g_order_contains;
DELETE FROM dbo.g_customer_places;
DELETE FROM dbo.g_orders;
DELETE FROM dbo.g_products;
DELETE FROM dbo.g_customers;
GO

INSERT INTO dbo.g_orders (orderid, orderdate)
SELECT OrderID, CAST(OrderDate AS DATE) FROM dbo.Orders;

INSERT INTO dbo.g_products (productid, productname)
SELECT ProductID, ProductName FROM dbo.Products;

INSERT INTO dbo.g_customers (customerid, companyname, country)
SELECT CustomerID, CompanyName, Country FROM dbo.Customers;
GO

-- Populate edges
INSERT INTO dbo.g_order_contains ($from_id, $to_id, quantity, value)
SELECT
    go_.$node_id,
    gp.$node_id,
    od.Quantity,
    CAST(od.UnitPrice * od.Quantity * (1 - od.Discount) AS MONEY)
FROM dbo.g_orders go_
JOIN dbo.[Order Details] od ON go_.orderid = od.OrderID
JOIN dbo.g_products gp      ON gp.productid = od.ProductID;

INSERT INTO dbo.g_customer_places ($from_id, $to_id)
SELECT
    gc.$node_id,
    go_.$node_id
FROM dbo.g_customers gc
JOIN dbo.Orders o    ON gc.customerid = o.CustomerID
JOIN dbo.g_orders go_ ON go_.orderid = o.OrderID;
GO

PRINT 'Graph tables loaded.';
DECLARE @n INT;
SELECT @n = COUNT(*) FROM dbo.g_orders;         PRINT 'Nodes - orders: '    + CAST(@n AS varchar);
SELECT @n = COUNT(*) FROM dbo.g_products;        PRINT 'Nodes - products: '  + CAST(@n AS varchar);
SELECT @n = COUNT(*) FROM dbo.g_customers;       PRINT 'Nodes - customers: ' + CAST(@n AS varchar);
SELECT @n = COUNT(*) FROM dbo.g_order_contains;  PRINT 'Edges - contains: '  + CAST(@n AS varchar);
SELECT @n = COUNT(*) FROM dbo.g_customer_places; PRINT 'Edges - places: '    + CAST(@n AS varchar);

-- Test query
SELECT TOP 5 p.productname, YEAR(o.orderdate) AS yr, SUM(e.value) AS rev
FROM dbo.g_products p, dbo.g_orders o, dbo.g_order_contains e
WHERE MATCH(o-(e)->p)
GROUP BY p.productname, YEAR(o.orderdate)
ORDER BY rev DESC;
GO
