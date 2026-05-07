"""
Transparent MS SQL → SQLite fallback.

Usage:
    conn, backend = sql_or_sqlite(mssql_conn_str, 'europe.db')
    # backend is 'mssql' or 'sqlite'
    # both connections support positional-index row access: row[0], row[1], …

SQLite files live in:  instance/fallback/<name>
"""
import os
import sqlite3
import pyodbc

_FALLBACK_DIR = os.path.join(
    os.path.dirname(__file__), '..', 'instance', 'fallback'
)


def sql_or_sqlite(mssql_conn_str: str, fallback_db: str, timeout: int = 5):
    """Try MS SQL; on any connection error return a sqlite3 connection instead."""
    try:
        conn = pyodbc.connect(mssql_conn_str, timeout=timeout)
        conn.execute("SELECT 1")
        return conn, 'mssql'
    except Exception:
        path = os.path.join(_FALLBACK_DIR, fallback_db)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row   # row['Col'] and row[0] both work
        return conn, 'sqlite'
