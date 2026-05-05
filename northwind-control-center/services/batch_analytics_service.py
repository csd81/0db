"""
Batch Analytics Demo — Row-Store (SQL Server) vs Columnar (pandas) Comparison.

Demonstrates the BigQuery/columnar storage architecture lesson:
  SQL Server   → row-oriented OLTP store, fast for single-row lookups
  pandas/numpy → columnar in-memory store, fast for full-table aggregation scans

Runs 3 query types with timing:
  Q1 — Revenue by country (GROUP BY aggregation — columnar wins)
  Q2 — Single order lookup by PK (OLTP — row-store wins)
  Q3 — Top-N products by units sold (scan + sort — columnar competitive)
"""
import time
from datetime import datetime

import pyodbc

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False


def _connect(conn_str: str):
    return pyodbc.connect(conn_str, timeout=10)


def _ts() -> str:
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


def _run_sql_q1(cur):
    t0 = time.perf_counter()
    cur.execute("""
        SELECT o.ShipCountry,
               COUNT(DISTINCT o.OrderID) AS Orders,
               ROUND(SUM(od.UnitPrice * od.Quantity * (1.0 - od.Discount)), 2) AS Revenue
        FROM   Orders o
        JOIN   [Order Details] od ON o.OrderID = od.OrderID
        GROUP  BY o.ShipCountry
        ORDER  BY Revenue DESC
    """)
    rows = [{'country': r[0], 'orders': r[1], 'revenue': round(float(r[2]), 2)}
            for r in cur.fetchall()]
    return rows, (time.perf_counter() - t0) * 1000


def _run_sql_q2(cur):
    t0 = time.perf_counter()
    cur.execute("""
        SELECT o.OrderID, c.CompanyName, o.ShipCountry,
               ROUND(SUM(od.UnitPrice * od.Quantity * (1.0 - od.Discount)), 2) AS Total
        FROM   Orders o
        JOIN   Customers c        ON o.CustomerID = c.CustomerID
        JOIN   [Order Details] od ON o.OrderID   = od.OrderID
        WHERE  o.OrderID = 10248
        GROUP  BY o.OrderID, c.CompanyName, o.ShipCountry
    """)
    r = cur.fetchone()
    row = {'order_id': r[0], 'customer': r[1], 'country': r[2],
           'total': round(float(r[3]), 2)} if r else {}
    return row, (time.perf_counter() - t0) * 1000


def _run_sql_q3(cur):
    t0 = time.perf_counter()
    cur.execute("""
        SELECT TOP 10 p.ProductName, SUM(od.Quantity) AS UnitsSold
        FROM   [Order Details] od
        JOIN   Products p ON od.ProductID = p.ProductID
        GROUP  BY p.ProductName
        ORDER  BY UnitsSold DESC
    """)
    rows = [{'product': r[0], 'units': r[1]} for r in cur.fetchall()]
    return rows, (time.perf_counter() - t0) * 1000


def _run_pandas(df_orders, df_details, df_products):
    results = {}

    t0 = time.perf_counter()
    merged = df_details.merge(df_orders[['OrderID', 'ShipCountry']], on='OrderID')
    merged['Revenue'] = merged['UnitPrice'] * merged['Quantity'] * (1 - merged['Discount'])
    q1 = (merged.groupby('ShipCountry')['Revenue']
          .sum().reset_index()
          .sort_values('Revenue', ascending=False))
    q1['Revenue'] = q1['Revenue'].round(2)
    results['q1_ms']   = round((time.perf_counter() - t0) * 1000, 2)
    results['q1_rows'] = [{'country': r['ShipCountry'], 'revenue': r['Revenue']}
                          for _, r in q1.iterrows()]

    t0 = time.perf_counter()
    _ = df_orders[df_orders['OrderID'] == 10248].values.tolist()
    results['q2_ms'] = round((time.perf_counter() - t0) * 1000, 2)

    t0 = time.perf_counter()
    merged3 = df_details.merge(df_products[['ProductID', 'ProductName']], on='ProductID')
    q3 = (merged3.groupby('ProductName')['Quantity']
          .sum().reset_index()
          .sort_values('Quantity', ascending=False).head(10))
    results['q3_ms']   = round((time.perf_counter() - t0) * 1000, 2)
    results['q3_rows'] = [{'product': r['ProductName'], 'units': int(r['Quantity'])}
                          for _, r in q3.iterrows()]
    return results


def _scaling_projection(sql_base_ms, pd_base_ms):
    sizes  = [2155, 10_000, 100_000, 1_000_000, 10_000_000]
    factor = 2155
    out    = []
    for n in sizes:
        ratio   = n / factor
        sql_est = round(sql_base_ms * ratio * (1 + 0.08 * ratio ** 0.12), 1)
        pd_est  = round(pd_base_ms  * ratio * 0.55, 1) if pd_base_ms else None
        out.append({'n': n, 'sql_ms': sql_est, 'pd_ms': pd_est})
    return out


def ba_run(conn_str: str) -> dict:
    conn = _connect(conn_str)
    cur  = conn.cursor()

    sql_q1, sql_q1_ms = _run_sql_q1(cur)
    sql_q2, sql_q2_ms = _run_sql_q2(cur)
    sql_q3, sql_q3_ms = _run_sql_q3(cur)

    pandas_results = {}
    pandas_ok      = False

    if _PANDAS_OK:
        t_load = time.perf_counter()
        cur.execute("SELECT OrderID, CustomerID, ShipCountry FROM Orders")
        df_orders = __import__('pandas').DataFrame(
            [tuple(r) for r in cur.fetchall()], columns=['OrderID', 'CustomerID', 'ShipCountry'])
        cur.execute("SELECT OrderID, ProductID, UnitPrice, Quantity, Discount FROM [Order Details]")
        df_details = __import__('pandas').DataFrame(
            [tuple(r) for r in cur.fetchall()], columns=['OrderID', 'ProductID', 'UnitPrice', 'Quantity', 'Discount'])
        df_details = df_details.astype({'UnitPrice': float, 'Quantity': float, 'Discount': float})
        cur.execute("SELECT ProductID, ProductName FROM Products")
        df_products = __import__('pandas').DataFrame(
            [tuple(r) for r in cur.fetchall()], columns=['ProductID', 'ProductName'])
        pandas_results['load_ms'] = round((time.perf_counter() - t_load) * 1000, 2)
        pandas_results.update(_run_pandas(df_orders, df_details, df_products))
        pandas_ok = True

    conn.close()
    return {
        'ts':                _ts(),
        'pandas_available':  pandas_ok,
        'sql': {
            'q1_ms': round(sql_q1_ms, 2), 'q1_rows': sql_q1,
            'q2_ms': round(sql_q2_ms, 2), 'q2_row':  sql_q2,
            'q3_ms': round(sql_q3_ms, 2), 'q3_rows': sql_q3,
        },
        'pandas': pandas_results,
        'scaling': _scaling_projection(
            sql_q1_ms,
            pandas_results.get('q1_ms') if pandas_ok else None,
        ),
    }
