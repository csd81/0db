import re
import pyodbc
from flask import current_app, g

# Strip "[Microsoft][ODBC Driver 18 for SQL Server][SQL Server]" prefix from messages
_MSG_PREFIX = re.compile(r'^\[.*?\]\[.*?\]\[.*?\]')


def _collect_messages(cursor):
    """Return list of clean server message strings from cursor.messages."""
    out = []
    for entry in (getattr(cursor, 'messages', None) or []):
        # entry is (state, message) or just a string depending on driver version
        msg = entry[1] if isinstance(entry, (tuple, list)) else str(entry)
        msg = _MSG_PREFIX.sub('', msg).strip()
        if msg:
            out.append(msg)
    return out


def _fix_str(v):
    """ODBC Driver 18 on Linux returns NVARCHAR as UTF-8 bytes decoded as Latin-1.
    Re-encoding to Latin-1 then decoding as UTF-8 recovers the correct string."""
    if not isinstance(v, str):
        return v
    try:
        return v.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return v


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
    rows = [[_fix_str(cell) for cell in row] for row in cursor.fetchall()]
    return columns, rows


def _split_go_batches(sql):
    """Split a SQL script on GO batch separators (case-insensitive, own line)."""
    parts = re.split(r'(?im)^\s*GO\s*$', sql)
    return [p.strip() for p in parts if p.strip()]


# Statements that SQL Server forbids inside a user transaction
_NEEDS_AUTOCOMMIT = re.compile(
    r'^\s*(drop|create|alter)\s+database\b|^\s*(backup|restore)\s+database\b',
    re.I,
)


def run_any(sql, params=None):
    """Execute any SQL statement (supports multi-batch GO scripts).
    Returns (columns, rows, rowcount, error, server_msgs).
    SELECT → rows populated; DML/DDL → committed, rowcount set, rows=[].
    For multi-batch scripts the last SELECT result is returned.
    server_msgs contains PRINT / informational messages from all batches.
    """
    batches = _split_go_batches(sql)
    if not batches:
        return [], [], 0, None, []

    conn = get_connection()
    needs_ac = any(_NEEDS_AUTOCOMMIT.search(b) for b in batches)
    if needs_ac:
        conn.autocommit = True
    cursor = conn.cursor()
    try:
        columns, rows, total_rowcount, all_msgs = [], [], 0, []
        for batch in batches:
            batch_params = (params or []) if len(batches) == 1 else []
            cursor.execute(batch, batch_params)
            all_msgs.extend(_collect_messages(cursor))
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = [[_fix_str(cell) for cell in row] for row in cursor.fetchall()]
            else:
                rc = cursor.rowcount if cursor.rowcount is not None else 0
                if rc > 0:
                    total_rowcount += rc
        if not needs_ac:
            conn.commit()
        if columns:
            return columns, rows, len(rows), None, all_msgs
        return [], [], total_rowcount, None, all_msgs
    except Exception as e:
        if not needs_ac:
            try:
                conn.rollback()
            except Exception:
                pass
        return [], [], 0, str(e), []
    finally:
        if needs_ac:
            conn.autocommit = False


def run_any_on_conn(conn, sql):
    """Like run_any but on a caller-provided connection (e.g. admin/SA connection).
    Returns (columns, rows, rowcount, error, server_msgs).
    Continues on error per batch, collecting the first error message."""
    batches = _split_go_batches(sql)
    if not batches:
        return [], [], 0, None, []
    is_autocommit = getattr(conn, 'autocommit', False)
    try:
        columns, rows, total_rowcount, first_error, all_msgs = [], [], 0, None, []
        for batch in batches:
            try:
                cursor = conn.cursor()
                cursor.execute(batch)
                all_msgs.extend(_collect_messages(cursor))
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = [[_fix_str(cell) for cell in row] for row in cursor.fetchall()]
                else:
                    rc = cursor.rowcount if cursor.rowcount is not None else 0
                    if rc > 0:
                        total_rowcount += rc
            except Exception as e:
                if first_error is None:
                    first_error = str(e)
        if not is_autocommit:
            conn.commit()
        if columns:
            return columns, rows, len(rows), first_error, all_msgs
        return [], [], total_rowcount, first_error, all_msgs
    except Exception as e:
        if not is_autocommit:
            try:
                conn.rollback()
            except Exception:
                pass
        return [], [], 0, str(e), []


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
