"""
stock_agent_service.py — SQL Server Agent demo simulation.

Real:       sp_RefillStock stored procedure created on SQL Server
            UPDATE Products executed with real rowcount tracking
Simulated:  Python daemon thread = SQL Server Agent recurring schedule
            In-memory list = msdb.dbo.sysjobhistory

Architecture mirrors: Job → JobStep → Schedule → Alert → Operator
"""

import threading
import time
from datetime import datetime

import pyodbc

# ── Stored procedure DDL (shown in UI + created on server) ───────────────────

SP_DDL = """\
CREATE OR ALTER PROCEDURE sp_RefillStock
AS
BEGIN
    SET NOCOUNT ON;
    -- Bring every active low-stock product back to ReorderLevel + 100
    UPDATE Products
    SET    UnitsInStock = UnitsInStock + 100
    WHERE  UnitsInStock <= ReorderLevel
      AND  Discontinued = 0;
END;\
"""

# Direct UPDATE used at runtime so Python can capture exact rowcount
# (SET NOCOUNT ON in the SP suppresses @@ROWCOUNT from pyodbc)
_REFILL_SQL = """\
UPDATE Products
SET    UnitsInStock = UnitsInStock + 100
WHERE  UnitsInStock <= ReorderLevel
  AND  Discontinued = 0\
"""

# ── In-memory job log  (mirrors msdb.dbo.sysjobhistory) ──────────────────────

_log_lock:   threading.Lock = threading.Lock()
_JOB_HISTORY: list[dict]   = []

# ── Scheduler state  (mirrors SQLServerAgent service) ────────────────────────

_sched_lock:       threading.Lock         = threading.Lock()
_sched_running:    bool                   = False
_sched_interval:   int                    = 3600          # seconds
_sched_thread:     threading.Thread | None = None
_sched_conn_str:   str                    = ''


# ── Stored procedure setup ────────────────────────────────────────────────────

def ensure_sp_refill(conn_str: str) -> str | None:
    """
    CREATE OR ALTER sp_RefillStock on the connected SQL Server.
    Returns error string on failure (e.g. insufficient DDL permissions);
    the UI shows the DDL regardless.
    """
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        conn.autocommit = True
        conn.execute(SP_DDL)
        conn.close()
        return None
    except Exception as e:
        return str(e)


# ── Inventory queries ─────────────────────────────────────────────────────────

def get_low_stock(conn_str: str) -> list[dict]:
    """Products where UnitsInStock ≤ ReorderLevel and not discontinued."""
    try:
        with pyodbc.connect(conn_str, timeout=5) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT p.ProductID, p.ProductName,
                       p.UnitsInStock, p.ReorderLevel,
                       p.ReorderLevel - p.UnitsInStock AS Deficit,
                       cat.CategoryName
                FROM Products p
                JOIN Categories cat ON p.CategoryID = cat.CategoryID
                WHERE p.UnitsInStock <= p.ReorderLevel
                  AND p.Discontinued = 0
                ORDER BY Deficit DESC, p.ProductName
            """)
            cols = [d[0] for d in cur.description]
            rows = []
            for row in cur.fetchall():
                d = dict(zip(cols, row))
                d['UnitsInStock'] = int(d['UnitsInStock'] or 0)
                d['ReorderLevel'] = int(d['ReorderLevel'] or 0)
                d['Deficit']      = int(d['Deficit'] or 0)
                rows.append(d)
        return rows
    except Exception:
        return []


def get_stock_summary(conn_str: str) -> dict:
    """High-level inventory health numbers for the dashboard header."""
    try:
        with pyodbc.connect(conn_str, timeout=5) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE UnitsInStock <= ReorderLevel
                                       AND Discontinued = 0) AS low_count,
                    COUNT(*) FILTER (WHERE UnitsInStock = 0
                                       AND Discontinued = 0) AS out_count,
                    COUNT(*) FILTER (WHERE Discontinued = 0)  AS active_total
                FROM Products
            """)
            # SQL Server doesn't support FILTER — use CASE WHEN
            pass
    except Exception:
        pass
    try:
        with pyodbc.connect(conn_str, timeout=5) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT
                    SUM(CASE WHEN UnitsInStock <= ReorderLevel
                              AND Discontinued = 0 THEN 1 ELSE 0 END) AS low_count,
                    SUM(CASE WHEN UnitsInStock = 0
                              AND Discontinued = 0 THEN 1 ELSE 0 END) AS out_count,
                    SUM(CASE WHEN Discontinued = 0 THEN 1 ELSE 0 END)  AS active_total
                FROM Products
            """)
            r = cur.fetchone()
            return {
                'low_count':    int(r[0] or 0),
                'out_count':    int(r[1] or 0),
                'active_total': int(r[2] or 0),
            }
    except Exception:
        return {'low_count': 0, 'out_count': 0, 'active_total': 0}


# ── Job execution ─────────────────────────────────────────────────────────────

def _run(conn_str: str, trigger: str) -> dict:
    started = datetime.utcnow()
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        conn.autocommit = False
        cur  = conn.cursor()
        cur.execute(_REFILL_SQL)
        rows = cur.rowcount
        conn.commit()
        conn.close()
        ms = int((datetime.utcnow() - started).total_seconds() * 1000)
        result = {
            'run_at':       started.strftime('%Y-%m-%d %H:%M:%S'),
            'trigger':      trigger,
            'status':       'SUCCEEDED',
            'rows_updated': rows,
            'duration_ms':  ms,
            'error':        None,
        }
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        ms = int((datetime.utcnow() - started).total_seconds() * 1000)
        result = {
            'run_at':       started.strftime('%Y-%m-%d %H:%M:%S'),
            'trigger':      trigger,
            'status':       'FAILED',
            'rows_updated': 0,
            'duration_ms':  ms,
            'error':        str(e),
        }
    with _log_lock:
        _JOB_HISTORY.insert(0, result)
        if len(_JOB_HISTORY) > 100:
            _JOB_HISTORY.pop()
    return result


def run_refill_now(conn_str: str) -> dict:
    return _run(conn_str, 'MANUAL')


# ── Python scheduler  (mirrors SQL Server Agent schedule) ────────────────────

def _scheduler_loop():
    global _sched_running
    while True:
        with _sched_lock:
            if not _sched_running:
                return
            interval = _sched_interval
            cs       = _sched_conn_str
        time.sleep(interval)
        with _sched_lock:
            if not _sched_running:
                return
        _run(cs, 'SCHEDULED')


def start_scheduler(conn_str: str, interval_seconds: int = 3600):
    global _sched_running, _sched_interval, _sched_conn_str, _sched_thread
    with _sched_lock:
        if _sched_running:
            return
        _sched_running  = True
        _sched_interval = max(60, interval_seconds)
        _sched_conn_str = conn_str
    _sched_thread = threading.Thread(target=_scheduler_loop, daemon=True)
    _sched_thread.start()


def stop_scheduler():
    global _sched_running
    with _sched_lock:
        _sched_running = False


def set_interval(seconds: int):
    global _sched_interval
    with _sched_lock:
        _sched_interval = max(60, seconds)


def get_scheduler_state() -> dict:
    with _sched_lock:
        return {
            'running':          _sched_running,
            'interval_seconds': _sched_interval,
        }


def get_job_history() -> list:
    with _log_lock:
        return list(_JOB_HISTORY)
