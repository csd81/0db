"""
db_adapter.py — Multi-database connection router.

Supports SQLite (sqlite3) and SQL Server (pyodbc).
Connections are cached in Flask g keyed by conn_id for request lifetime.
Does NOT affect the existing db.py / SQL Server connection used by the original modules.
"""

import sqlite3

import psycopg2
import psycopg2.extras
import pymysql
import pymysql.cursors
import pyodbc
from flask import g

import meta_db


def get_adapter_connection(conn_id: int):
    """Return a cached connection for this request, opening it if needed."""
    cache_key = f'_adapter_{conn_id}'
    conn = g.get(cache_key)
    if conn is not None:
        return conn

    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found in meta.db")

    db_type = rec['db_type']
    params = rec['conn_params']
    password = rec.get('password', '')

    if db_type == 'sqlite':
        path = params.get('database', ':memory:')
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
    elif db_type == 'sqlserver':
        driver = params.get('driver', 'ODBC Driver 18 for SQL Server')
        server = params.get('server', 'localhost')
        database = params.get('database', '')
        username = params.get('username', '')
        encrypt = params.get('encrypt', 'yes')
        trust_cert = params.get('trust_server_cert', 'yes')
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"UID={username};PWD={password};"
            f"Encrypt={encrypt};TrustServerCertificate={trust_cert};"
            "Connection Timeout=10;"
        )
        conn = pyodbc.connect(conn_str)
    elif db_type == 'postgresql':
        conn = psycopg2.connect(
            host=params.get('host', 'localhost'),
            port=int(params.get('port', 5432)),
            dbname=params.get('database', 'postgres'),
            user=params.get('username', 'postgres'),
            password=password,
        )
        conn.autocommit = True
    elif db_type == 'mysql':
        conn = pymysql.connect(
            host=params.get('host', 'localhost'),
            port=int(params.get('port', 3306)),
            database=params.get('database', ''),
            user=params.get('username', 'root'),
            password=password,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
    else:
        raise ValueError(f"Unsupported db_type: {db_type!r}")

    setattr(g, cache_key, conn)
    return conn


def adapter_select(conn_id: int, sql: str, params=None) -> tuple[list, list]:
    """Execute a SELECT and return (column_names, rows_as_lists)."""
    conn = get_adapter_connection(conn_id)
    rec = meta_db.get_connection_by_id(conn_id)
    db_type = rec['db_type']

    if db_type == 'mysql':
        cur = conn.cursor()
        cur.execute(sql, params or [])
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = [list(r.values()) for r in cur.fetchall()]
    else:
        cur = conn.execute(sql, params or [])
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = [list(r) for r in cur.fetchall()]

    return columns, rows


def adapter_execute(conn_id: int, sql: str, params=None) -> int:
    """Execute a non-SELECT statement, commit, and return rowcount."""
    conn = get_adapter_connection(conn_id)
    rec = meta_db.get_connection_by_id(conn_id)
    db_type = rec['db_type']

    if db_type == 'mysql':
        cur = conn.cursor()
        cur.execute(sql, params or [])
        return cur.rowcount
    else:
        cur = conn.execute(sql, params or [])
        conn.commit()
        return cur.rowcount


def adapter_test(conn_id: int) -> tuple[bool, str | None]:
    """Open a fresh connection (not cached) and run a trivial query."""
    try:
        rec = meta_db.get_connection_by_id(conn_id)
        if rec is None:
            return False, "Connection record not found."
        db_type = rec['db_type']
        params = rec['conn_params']
        password = rec.get('password', '')

        if db_type == 'sqlite':
            path = params.get('database', ':memory:')
            c = sqlite3.connect(path, timeout=5)
            c.execute("SELECT 1")
            c.close()
        elif db_type == 'sqlserver':
            driver = params.get('driver', 'ODBC Driver 18 for SQL Server')
            server = params.get('server', 'localhost')
            database = params.get('database', '')
            username = params.get('username', '')
            encrypt = params.get('encrypt', 'yes')
            trust_cert = params.get('trust_server_cert', 'yes')
            conn_str = (
                f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
                f"UID={username};PWD={password};"
                f"Encrypt={encrypt};TrustServerCertificate={trust_cert};"
                "Connection Timeout=5;"
            )
            c = pyodbc.connect(conn_str)
            c.execute("SELECT 1")
            c.close()
        elif db_type == 'postgresql':
            c = psycopg2.connect(
                host=params.get('host', 'localhost'),
                port=int(params.get('port', 5432)),
                dbname=params.get('database', 'postgres'),
                user=params.get('username', 'postgres'),
                password=password,
            )
            c.cursor().execute("SELECT 1")
            c.close()
        elif db_type == 'mysql':
            c = pymysql.connect(
                host=params.get('host', 'localhost'),
                port=int(params.get('port', 3306)),
                database=params.get('database', ''),
                user=params.get('username', 'root'),
                password=password,
                connect_timeout=5,
            )
            c.cursor().execute("SELECT 1")
            c.close()
        else:
            return False, f"Unsupported db_type: {db_type!r}"

        return True, None
    except Exception as e:
        return False, str(e)


def close_adapter_connections(e=None) -> None:
    """Teardown hook: close all adapter connections opened during this request."""
    for key in list(vars(g)):
        if key.startswith('_adapter_'):
            conn = getattr(g, key, None)
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
