import pyodbc
from flask import current_app, g


def _conn_str():
    c = current_app.config
    return (
        f"DRIVER={{{c['SQL_DRIVER']}}};"
        f"SERVER={c['SQL_SERVER']};"
        f"DATABASE={c['SQL_DATABASE']};"
        f"UID={c['SQL_USERNAME']};"
        f"PWD={c['SQL_PASSWORD']};"
        f"Encrypt={c['SQL_ENCRYPT']};"
        f"TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )


def get_connection():
    if 'db_conn' not in g:
        g.db_conn = pyodbc.connect(_conn_str(), timeout=10)
    return g.db_conn


def close_connection(e=None):
    conn = g.pop('db_conn', None)
    if conn is not None:
        conn.close()


def run_select(sql, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or [])
    if cursor.description is None:
        return [], []
    columns = [col[0] for col in cursor.description]
    rows = [list(row) for row in cursor.fetchall()]
    return columns, rows


def run_command(sql, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or [])
    conn.commit()
    return cursor.rowcount


def run_proc(proc_name, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    if params:
        placeholders = ', '.join(['?' for _ in params])
        cursor.execute(f"EXEC {proc_name} {placeholders}", params)
    else:
        cursor.execute(f"EXEC {proc_name}")
    conn.commit()


def test_connection():
    try:
        conn = pyodbc.connect(_conn_str(), timeout=5)
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)
