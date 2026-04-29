from db import run_select


def _safe_select(sql, params=None):
    try:
        cols, rows = run_select(sql, params)
        return cols, rows, None
    except Exception as e:
        return [], [], str(e)


def get_home_summary():
    summary = {
        'today_orders': 0,
        'pending_events': 0,
        'failed_events': 0,
        'low_stock_count': 0,
        'db_size_mb': 0,
        'events_available': False,
    }

    _, rows, _ = _safe_select(
        "SELECT COUNT(*) FROM Orders WHERE CAST(OrderDate AS DATE) = CAST(GETDATE() AS DATE)"
    )
    if rows:
        summary['today_orders'] = rows[0][0]

    _, rows, _ = _safe_select(
        "SELECT COUNT(*) FROM Products WHERE UnitsInStock <= ReorderLevel"
    )
    if rows:
        summary['low_stock_count'] = rows[0][0]

    try:
        _, rows, err = _safe_select(
            "SELECT COUNT(*) FROM dbo.order_log WHERE status = 0"
        )
        if not err and rows:
            summary['pending_events'] = rows[0][0]
            summary['events_available'] = True
        _, rows, _ = _safe_select(
            "SELECT COUNT(*) FROM dbo.order_log WHERE status = 3"
        )
        if rows:
            summary['failed_events'] = rows[0][0]
    except Exception:
        pass

    _, rows, _ = _safe_select(
        "SELECT CAST(SUM(size) * 8.0 / 1024 AS DECIMAL(10,1)) FROM sys.database_files"
    )
    if rows and rows[0][0] is not None:
        summary['db_size_mb'] = float(rows[0][0])

    return summary


def get_db_sizes():
    cols, rows, err = _safe_select(
        """
        SELECT
            name,
            type_desc,
            CAST(size * 8.0 / 1024 AS DECIMAL(10,1)) AS size_mb,
            CAST(FILEPROPERTY(name, 'SpaceUsed') * 8.0 / 1024 AS DECIMAL(10,1)) AS used_mb,
            physical_name
        FROM sys.database_files
        """
    )
    return cols, rows, err


def get_recent_backups():
    cols, rows, err = _safe_select(
        """
        SELECT TOP 10
            database_name,
            backup_start_date,
            backup_finish_date,
            CASE type
                WHEN 'D' THEN 'Full'
                WHEN 'L' THEN 'Log'
                WHEN 'I' THEN 'Differential'
                ELSE type
            END AS backup_type,
            CAST(backup_size / 1048576.0 AS DECIMAL(10,2)) AS size_mb
        FROM msdb.dbo.backupset
        WHERE database_name = DB_NAME()
        ORDER BY backup_finish_date DESC
        """
    )
    return cols, rows, err


def get_job_status():
    cols, rows, err = _safe_select(
        """
        SELECT TOP 20
            j.name AS job_name,
            CONVERT(datetime,
                CAST(h.run_date AS varchar(8)) + ' ' +
                STUFF(STUFF(RIGHT('000000' + CAST(h.run_time AS varchar(6)), 6), 5, 0, ':'), 3, 0, ':')
            ) AS run_datetime,
            CASE h.run_status
                WHEN 0 THEN 'Failed'
                WHEN 1 THEN 'Succeeded'
                WHEN 2 THEN 'Retry'
                WHEN 3 THEN 'Cancelled'
                WHEN 4 THEN 'In Progress'
                ELSE 'Unknown'
            END AS status,
            h.message
        FROM msdb.dbo.sysjobs j
        JOIN msdb.dbo.sysjobhistory h ON j.job_id = h.job_id
        WHERE h.step_id = 0
        ORDER BY h.run_date DESC, h.run_time DESC
        """
    )
    return cols, rows, err


def get_row_counts():
    cols, rows, err = _safe_select(
        """
        SELECT
            t.name AS table_name,
            SUM(p.rows) AS row_count
        FROM sys.tables t
        JOIN sys.partitions p ON t.object_id = p.object_id
        WHERE p.index_id IN (0, 1)
          AND t.is_ms_shipped = 0
        GROUP BY t.name
        ORDER BY SUM(p.rows) DESC
        """
    )
    return cols, rows, err


def get_low_stock():
    cols, rows, err = _safe_select(
        """
        SELECT
            ProductID, ProductName,
            UnitsInStock, ReorderLevel, UnitsOnOrder,
            CASE WHEN Discontinued = 1 THEN 'Yes' ELSE 'No' END AS Discontinued
        FROM Products
        WHERE UnitsInStock <= ReorderLevel
        ORDER BY UnitsInStock
        """
    )
    return cols, rows, err
