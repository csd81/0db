from db import run_select, run_proc, run_command

STATUS_LABELS = {0: 'Pending', 1: 'Processing', 2: 'Success', 3: 'Failed'}


def _safe_select(sql, params=None):
    try:
        cols, rows = run_select(sql, params)
        return cols, rows, None
    except Exception as e:
        return [], [], str(e)


def get_event_summary():
    _, rows, err = _safe_select(
        """
        SELECT status, COUNT(*) AS cnt
        FROM dbo.order_log
        GROUP BY status
        """
    )
    summary = {0: 0, 1: 0, 2: 0, 3: 0}
    if not err:
        for row in rows:
            summary[row[0]] = row[1]
    return summary, err


def get_recent_events(limit=100):
    cols, rows, err = _safe_select(
        f"""
        SELECT TOP {limit}
            event_id, event_type, order_id,
            CASE status
                WHEN 0 THEN 'Pending'
                WHEN 1 THEN 'Processing'
                WHEN 2 THEN 'Success'
                WHEN 3 THEN 'Failed'
                ELSE CAST(status AS varchar)
            END AS status,
            time_created, time_process_begin, time_process_end,
            error_message
        FROM dbo.order_log
        ORDER BY time_created DESC
        """
    )
    return cols, rows, err


def process_pending():
    try:
        run_proc('dbo.sp_process_order_events')
        return None
    except Exception as e:
        return str(e)


def retry_event(event_id):
    try:
        run_proc('dbo.sp_retry_order_event', [event_id])
        return None
    except Exception as e:
        return str(e)


def get_events_by_day():
    _, rows, _ = _safe_select(
        """
        SELECT
            CAST(time_created AS DATE) AS day,
            COUNT(*) AS total,
            SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END) AS success,
            SUM(CASE WHEN status = 3 THEN 1 ELSE 0 END) AS failed
        FROM dbo.order_log
        WHERE time_created >= DATEADD(day, -30, GETDATE())
        GROUP BY CAST(time_created AS DATE)
        ORDER BY day
        """
    )
    return [
        {
            'day': str(r[0]),
            'total': r[1],
            'success': r[2],
            'failed': r[3],
        }
        for r in rows
    ]
