"""
cqrs_service.py — CQRS pattern demo: route writes to primary, reads to replica.

Commands (INSERT/UPDATE/DELETE) → primary_conn_id
Queries  (SELECT)               → replica_conn_id
"""

import time
from collections import deque
from datetime import datetime

import db_adapter
import meta_db

# ── Module-level audit log (last 20 routing decisions) ────────────────────────
_audit_log: deque = deque(maxlen=20)

# ── Demo query presets ─────────────────────────────────────────────────────────
_DEMO_QUERIES = [
    {
        'key': 'select_analytics',
        'label': 'SELECT — Sales analytics (heavy read)',
        'sql': (
            "SELECT c.CategoryName, COUNT(od.OrderID) AS TotalOrders, "
            "SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS Revenue "
            "FROM [Order Details] od "
            "JOIN Products p ON od.ProductID = p.ProductID "
            "JOIN Categories c ON p.CategoryID = c.CategoryID "
            "GROUP BY c.CategoryName "
            "ORDER BY Revenue DESC"
        ),
    },
    {
        'key': 'insert_order',
        'label': 'INSERT — New order record',
        'sql': (
            "INSERT INTO Orders (CustomerID, EmployeeID, OrderDate, ShipCity, ShipCountry) "
            "VALUES ('ALFKI', 1, GETDATE(), 'Berlin', 'Germany')"
        ),
    },
    {
        'key': 'update_price',
        'label': 'UPDATE — Increase product price',
        'sql': (
            "UPDATE Products SET UnitPrice = UnitPrice * 1.05 "
            "WHERE CategoryID = 1 AND Discontinued = 0"
        ),
    },
    {
        'key': 'select_top_customers',
        'label': 'SELECT — Top customers by order count',
        'sql': (
            "SELECT TOP 10 c.CompanyName, c.Country, COUNT(o.OrderID) AS Orders "
            "FROM Customers c "
            "JOIN Orders o ON c.CustomerID = o.CustomerID "
            "GROUP BY c.CompanyName, c.Country "
            "ORDER BY Orders DESC"
        ),
    },
]

# Map key → entry
_DEMO_MAP = {d['key']: d for d in _DEMO_QUERIES}


# ── Classification ─────────────────────────────────────────────────────────────

def _classify(sql: str) -> str:
    """Return 'command' if sql starts with a write keyword, else 'query'."""
    first = sql.strip().split()[0].upper() if sql.strip() else ''
    command_keywords = {'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER', 'TRUNCATE'}
    return 'command' if first in command_keywords else 'query'


# ── Core executor ──────────────────────────────────────────────────────────────

def cqrs_execute(primary_conn_id: int, replica_conn_id: int, sql: str) -> dict:
    """
    Route sql to the appropriate connection based on classification.

    Returns a dict with keys:
        routed_to   : 'primary' | 'replica'
        sql         : the original SQL
        conn_type   : db_type of the chosen connection
        columns     : list of column names (queries only)
        rows        : list of rows as lists (queries only)
        rowcount    : int (commands only)
        elapsed_ms  : execution time in milliseconds
        error       : error string or None
    """
    sql_stripped = sql.strip()
    kind = _classify(sql_stripped)

    if kind == 'command':
        target_conn_id = primary_conn_id
        routed_to = 'primary'
    else:
        target_conn_id = replica_conn_id
        routed_to = 'replica'

    # Resolve db_type for display
    rec = meta_db.get_connection_by_id(target_conn_id)
    conn_type = rec['db_type'] if rec else 'unknown'

    columns: list = []
    rows: list = []
    rowcount: int = 0
    error: str | None = None

    t0 = time.perf_counter()
    try:
        if kind == 'query':
            columns, rows = db_adapter.adapter_select(target_conn_id, sql_stripped)
        else:
            rowcount = db_adapter.adapter_execute(target_conn_id, sql_stripped)
    except Exception as exc:
        error = str(exc)
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)

    # Record in audit log
    _audit_log.append({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'sql_snippet': (sql_stripped[:80] + '…') if len(sql_stripped) > 80 else sql_stripped,
        'routed_to': routed_to,
        'rows_returned': len(rows) if kind == 'query' else None,
        'rowcount': rowcount if kind == 'command' else None,
        'elapsed_ms': elapsed_ms,
        'error': error,
    })

    return {
        'routed_to': routed_to,
        'sql': sql_stripped,
        'conn_type': conn_type,
        'columns': columns,
        'rows': rows,
        'rowcount': rowcount,
        'elapsed_ms': elapsed_ms,
        'error': error,
    }


# ── Audit helpers ──────────────────────────────────────────────────────────────

def get_audit_log() -> list[dict]:
    """Return the last ≤20 routing decisions (most recent last)."""
    return list(_audit_log)


def clear_audit_log() -> None:
    """Clear all audit log entries."""
    _audit_log.clear()


# ── Demo queries ───────────────────────────────────────────────────────────────

def demo_queries() -> list[dict]:
    """Return the preset demo query list (label + sql pairs)."""
    return _DEMO_QUERIES


def get_demo_query(key: str) -> dict | None:
    """Look up a single demo query by key."""
    return _DEMO_MAP.get(key)
