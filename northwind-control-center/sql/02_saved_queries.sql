-- Seed saved query templates. Run after 01_schema_support.sql.
USE Northwind;
GO

TRUNCATE TABLE dbo.saved_queries;
GO

INSERT INTO dbo.saved_queries (query_name, category, is_readonly, query_text) VALUES

('Top 10 Products by Revenue', 'Analytics', 1,
'SELECT TOP 10
    p.ProductName,
    SUM(od.Quantity) AS units_sold,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
FROM Products p
JOIN [Order Details] od ON p.ProductID = od.ProductID
GROUP BY p.ProductName
ORDER BY revenue DESC'),

('Revenue by Category', 'Analytics', 1,
'SELECT
    c.CategoryName,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
FROM Categories c
JOIN Products p ON c.CategoryID = p.CategoryID
JOIN [Order Details] od ON p.ProductID = od.ProductID
GROUP BY c.CategoryName
ORDER BY revenue DESC'),

('Orders by Country', 'Analytics', 1,
'SELECT
    c.Country,
    COUNT(DISTINCT o.OrderID) AS order_count
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.Country
ORDER BY order_count DESC'),

('Revenue by Month', 'Analytics', 1,
'SELECT
    YEAR(o.OrderDate) AS yr,
    MONTH(o.OrderDate) AS mo,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
FROM Orders o
JOIN [Order Details] od ON o.OrderID = od.OrderID
GROUP BY YEAR(o.OrderDate), MONTH(o.OrderDate)
ORDER BY yr, mo'),

('Low Stock Products', 'Operations', 1,
'SELECT ProductID, ProductName, UnitsInStock, ReorderLevel, UnitsOnOrder
FROM Products
WHERE UnitsInStock <= ReorderLevel
ORDER BY UnitsInStock'),

('Employee Hierarchy', 'Modeling', 1,
'SELECT
    e.FirstName + '' '' + e.LastName AS employee,
    e.Title,
    ISNULL(m.FirstName + '' '' + m.LastName, ''(top level)'') AS reports_to
FROM Employees e
LEFT JOIN Employees m ON e.ReportsTo = m.EmployeeID
ORDER BY e.ReportsTo, e.LastName'),

('Recent Event Log', 'Events', 1,
'SELECT TOP 50
    event_id, event_type, order_id,
    CASE status
        WHEN 0 THEN ''Pending''
        WHEN 1 THEN ''Processing''
        WHEN 2 THEN ''Success''
        WHEN 3 THEN ''Failed''
    END AS status,
    time_created, error_message
FROM dbo.order_log
ORDER BY time_created DESC'),

('Order Value Calculation', 'Querying', 1,
'SELECT TOP 20
    o.OrderID,
    o.OrderDate,
    c.CompanyName,
    CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS order_value,
    SUM(od.Quantity) AS total_items
FROM Orders o
JOIN [Order Details] od ON o.OrderID = od.OrderID
JOIN Customers c ON o.CustomerID = c.CustomerID
GROUP BY o.OrderID, o.OrderDate, c.CompanyName
ORDER BY order_value DESC'),

('Product Co-occurrence (Top 20)', 'Graph', 1,
'SELECT TOP 20
    p1.ProductName AS product_a,
    p2.ProductName AS product_b,
    COUNT(*) AS times_together
FROM [Order Details] od1
JOIN [Order Details] od2 ON od1.OrderID = od2.OrderID AND od1.ProductID < od2.ProductID
JOIN Products p1 ON od1.ProductID = p1.ProductID
JOIN Products p2 ON od2.ProductID = p2.ProductID
GROUP BY p1.ProductName, p2.ProductName
ORDER BY times_together DESC');

GO
PRINT 'Saved queries inserted: ' + CAST(@@ROWCOUNT AS varchar);
