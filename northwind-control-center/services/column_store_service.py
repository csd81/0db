"""
column_store_service.py — In-memory SQLite column store backed by Northwind data.

Reads from a registered SQL Server (or SQLite) connection via db_adapter,
joins/flattens data using pandas, then loads into a per-user in-memory SQLite.
Aggregation queries against the in-memory store are nearly instant.

NOTE: _stores is module-level and not shared across Gunicorn workers.
Run with python app.py or gunicorn --workers=1.
"""

import sqlite3
import threading

import pandas as pd

import db_adapter

_stores: dict[str, sqlite3.Connection] = {}
_lock = threading.Lock()


def get_or_create_store(session_key: str) -> sqlite3.Connection:
    with _lock:
        if session_key not in _stores:
            conn = sqlite3.connect(':memory:', check_same_thread=False)
            _stores[session_key] = conn
        return _stores[session_key]


def get_store_stats(session_key: str) -> dict:
    conn = get_or_create_store(session_key)
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    total_rows = 0
    for t in tables:
        row = conn.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()
        total_rows += row[0] if row else 0
    return {'tables': tables, 'total_rows': total_rows, 'loaded': bool(tables)}


def load_northwind_into_store(session_key: str, source_conn_id: int) -> tuple[bool, str | None]:
    """Fetch Northwind tables, join into a flat analytics table, load into memory store."""
    try:
        def sel(sql):
            cols, rows = db_adapter.adapter_select(source_conn_id, sql)
            return pd.DataFrame(rows, columns=cols)

        orders = sel("SELECT OrderID, CustomerID, OrderDate, Freight FROM Orders")
        details = sel("SELECT OrderID, ProductID, UnitPrice, Quantity, Discount FROM [Order Details]")
        products = sel("SELECT ProductID, ProductName, CategoryID FROM Products")
        categories = sel("SELECT CategoryID, CategoryName FROM Categories")
        customers = sel("SELECT CustomerID, CompanyName, Country FROM Customers")

        # Flat analytics fact table
        df = (details
              .merge(orders, on='OrderID')
              .merge(products, on='ProductID')
              .merge(categories, on='CategoryID')
              .merge(customers, on='CustomerID'))
        df['ItemValue'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

        conn = get_or_create_store(session_key)
        # Drop existing tables and reload
        conn.execute("DROP TABLE IF EXISTS fact_sales")
        conn.execute("DROP TABLE IF EXISTS dim_customers")
        conn.execute("DROP TABLE IF EXISTS dim_products")

        df.to_sql('fact_sales', conn, if_exists='replace', index=False)
        customers.to_sql('dim_customers', conn, if_exists='replace', index=False)
        products.to_sql('dim_products', conn, if_exists='replace', index=False)
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)


_AGGREGATIONS = {
    'revenue_by_category': """
        SELECT CategoryName, ROUND(SUM(ItemValue), 2) AS revenue
        FROM fact_sales GROUP BY CategoryName ORDER BY revenue DESC
    """,
    'orders_by_country': """
        SELECT Country, COUNT(DISTINCT OrderID) AS order_count
        FROM fact_sales GROUP BY Country ORDER BY order_count DESC
    """,
    'monthly_trend': """
        SELECT SUBSTR(OrderDate, 1, 7) AS month, ROUND(SUM(ItemValue), 2) AS revenue
        FROM fact_sales WHERE OrderDate IS NOT NULL
        GROUP BY month ORDER BY month
    """,
    'top_products': """
        SELECT ProductName, ROUND(SUM(ItemValue), 2) AS revenue
        FROM fact_sales GROUP BY ProductName ORDER BY revenue DESC LIMIT 10
    """,
}


def run_column_aggregation(session_key: str, agg_type: str) -> tuple[list, list, str | None]:
    sql = _AGGREGATIONS.get(agg_type)
    if not sql:
        return [], [], f"Unknown aggregation: {agg_type!r}"
    try:
        conn = get_or_create_store(session_key)
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [list(r) for r in cur.fetchall()]
        return cols, rows, None
    except Exception as e:
        return [], [], str(e)


def destroy_store(session_key: str) -> None:
    with _lock:
        conn = _stores.pop(session_key, None)
        if conn:
            conn.close()


AGGREGATION_LABELS = {
    'revenue_by_category': 'Revenue by Category',
    'orders_by_country': 'Orders by Country',
    'monthly_trend': 'Monthly Revenue Trend',
    'top_products': 'Top 10 Products',
}
