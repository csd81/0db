-- Run this first. Creates support tables used by the Flask app.
USE Northwind;
GO

-- Saved queries table
IF OBJECT_ID('dbo.saved_queries', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.saved_queries (
        query_id    INT IDENTITY(1,1) PRIMARY KEY,
        query_name  NVARCHAR(100) NOT NULL,
        query_text  NVARCHAR(MAX) NOT NULL,
        category    NVARCHAR(50)  NOT NULL DEFAULT 'General',
        is_readonly BIT           NOT NULL DEFAULT 1,
        created_at  DATETIME2     NOT NULL DEFAULT SYSDATETIME()
    );
    PRINT 'Created dbo.saved_queries';
END
GO

-- Optional query execution log
IF OBJECT_ID('dbo.query_execution_log', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.query_execution_log (
        exec_id       INT IDENTITY(1,1) PRIMARY KEY,
        executed_at   DATETIME2     NOT NULL DEFAULT SYSDATETIME(),
        username      NVARCHAR(100) NULL,
        query_text    NVARCHAR(MAX) NOT NULL,
        duration_ms   INT           NULL,
        row_count     INT           NULL,
        success       BIT           NOT NULL,
        error_message NVARCHAR(4000) NULL
    );
    PRINT 'Created dbo.query_execution_log';
END
GO


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


-- Creates the full loose-coupling workflow:
--   order_log table → tr_log_order trigger → sp_process_order_events → sp_retry_order_event
--   Run this, then create the SQL Agent job manually (see comment at the bottom).
USE Northwind;
GO

-- 1. Event log table
IF OBJECT_ID('dbo.order_log', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.order_log (
        event_id          INT IDENTITY(1,1) PRIMARY KEY,
        event_type        NVARCHAR(50)   NOT NULL,
        order_id          INT            NOT NULL,
        status            TINYINT        NOT NULL DEFAULT 0, -- 0=pending 1=processing 2=success 3=failed
        time_created      DATETIME2      NOT NULL DEFAULT SYSDATETIME(),
        time_process_begin DATETIME2     NULL,
        time_process_end   DATETIME2     NULL,
        error_message      NVARCHAR(4000) NULL
    );
    PRINT 'Created dbo.order_log';
END
GO

-- 2. Trigger on Orders
CREATE OR ALTER TRIGGER dbo.tr_log_order
ON dbo.Orders
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.order_log (event_type, order_id)
    SELECT
        CASE
            WHEN d.OrderID IS NULL THEN 'new_order'
            WHEN UPDATE(ShipAddress) OR UPDATE(ShipCity) OR UPDATE(ShipCountry) THEN 'address_changed'
            ELSE 'order_updated'
        END,
        i.OrderID
    FROM inserted i
    LEFT JOIN deleted d ON i.OrderID = d.OrderID;
END;
GO
PRINT 'Created trigger dbo.tr_log_order';
GO

-- 3. Event processor
CREATE OR ALTER PROCEDURE dbo.sp_process_order_events
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @event_id INT, @order_id INT;

    DECLARE event_cursor CURSOR LOCAL FAST_FORWARD FOR
        SELECT event_id, order_id
        FROM dbo.order_log
        WHERE status = 0
        ORDER BY time_created;

    OPEN event_cursor;
    FETCH NEXT FROM event_cursor INTO @event_id, @order_id;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        BEGIN TRY
            UPDATE dbo.order_log
            SET status = 1, time_process_begin = SYSDATETIME(), error_message = NULL
            WHERE event_id = @event_id;

            -- Business logic: update UnitsInStock for products in this order
            -- (Skip if already processed to avoid double-decrement)
            UPDATE p
            SET p.UnitsInStock = p.UnitsInStock - od.Quantity
            FROM dbo.Products p
            JOIN dbo.[Order Details] od ON od.ProductID = p.ProductID
            WHERE od.OrderID = @order_id
              AND p.UnitsInStock >= od.Quantity; -- safety: never go negative

            UPDATE dbo.order_log
            SET status = 2, time_process_end = SYSDATETIME()
            WHERE event_id = @event_id;
        END TRY
        BEGIN CATCH
            UPDATE dbo.order_log
            SET status = 3,
                time_process_end = SYSDATETIME(),
                error_message = ERROR_MESSAGE()
            WHERE event_id = @event_id;
        END CATCH;

        FETCH NEXT FROM event_cursor INTO @event_id, @order_id;
    END;

    CLOSE event_cursor;
    DEALLOCATE event_cursor;
END;
GO
PRINT 'Created dbo.sp_process_order_events';
GO

-- 4. Retry helper
CREATE OR ALTER PROCEDURE dbo.sp_retry_order_event
    @event_id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.order_log
    SET status = 0,
        time_process_begin = NULL,
        time_process_end   = NULL,
        error_message      = NULL
    WHERE event_id = @event_id AND status = 3;

    IF @@ROWCOUNT = 0
        RAISERROR('Event %d not found or not in Failed state.', 16, 1, @event_id);
END;
GO
PRINT 'Created dbo.sp_retry_order_event';
GO

-- 5. Helper views
CREATE OR ALTER VIEW dbo.vw_event_status_summary AS
SELECT
    CASE status
        WHEN 0 THEN 'Pending'
        WHEN 1 THEN 'Processing'
        WHEN 2 THEN 'Success'
        WHEN 3 THEN 'Failed'
    END AS status_label,
    COUNT(*) AS cnt
FROM dbo.order_log
GROUP BY status;
GO

CREATE OR ALTER VIEW dbo.vw_event_log_recent AS
SELECT TOP 100
    event_id, event_type, order_id, status, time_created,
    time_process_begin, time_process_end, error_message
FROM dbo.order_log
ORDER BY time_created DESC;
GO

PRINT 'Loose coupling objects created.';

-- ── SQL Agent Job (create manually in SSMS) ───────────────────────────────
-- Name  : ProcessNorthwindOrderEvents
-- Step  : T-SQL step, command: EXEC dbo.sp_process_order_events;
-- Schedule: Every 1 minute (or use sp_add_jobschedule via T-SQL)
--
-- To create via T-SQL (requires sysadmin or SQLAgentOperatorRole):
--
-- EXEC msdb.dbo.sp_add_job @job_name = N'ProcessNorthwindOrderEvents';
-- EXEC msdb.dbo.sp_add_jobstep @job_name = N'ProcessNorthwindOrderEvents',
--      @step_name = N'Process events',
--      @subsystem = N'TSQL',
--      @command = N'EXEC Northwind.dbo.sp_process_order_events;',
--      @database_name = N'Northwind';
-- EXEC msdb.dbo.sp_add_schedule @schedule_name = N'Every1Min',
--      @freq_type = 4, @freq_interval = 1, @freq_subday_type = 4,
--      @freq_subday_interval = 1;
-- EXEC msdb.dbo.sp_attach_schedule @job_name = N'ProcessNorthwindOrderEvents',
--      @schedule_name = N'Every1Min';
-- EXEC msdb.dbo.sp_add_jobserver @job_name = N'ProcessNorthwindOrderEvents';


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
