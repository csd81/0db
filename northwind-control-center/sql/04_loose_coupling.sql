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
