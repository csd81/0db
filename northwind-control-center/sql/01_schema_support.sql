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
