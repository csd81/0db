import re
import time
import io
import csv
from db import run_select, run_command

BLOCKED = re.compile(
    r'\b(DROP\s+TABLE|DROP\s+DATABASE|TRUNCATE|ALTER\s+LOGIN|SHUTDOWN|XP_CMDSHELL)\b',
    re.IGNORECASE,
)

ISOLATION_LEVELS = {
    'READ COMMITTED': 'SET TRANSACTION ISOLATION LEVEL READ COMMITTED;',
    'READ UNCOMMITTED': 'SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;',
    'REPEATABLE READ': 'SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;',
    'SERIALIZABLE': 'SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;',
    'SNAPSHOT': 'SET TRANSACTION ISOLATION LEVEL SNAPSHOT;',
}


def list_saved_queries():
    try:
        _, rows = run_select(
            "SELECT query_id, query_name, category, is_readonly, query_text "
            "FROM dbo.saved_queries ORDER BY category, query_name"
        )
        return [
            {
                'query_id': r[0],
                'query_name': r[1],
                'category': r[2],
                'is_readonly': r[3],
                'query_text': r[4],
            }
            for r in rows
        ]
    except Exception:
        return []


def get_saved_query(query_id):
    try:
        _, rows = run_select(
            "SELECT query_text, is_readonly FROM dbo.saved_queries WHERE query_id = ?",
            [query_id],
        )
        if rows:
            return rows[0][0], bool(rows[0][1])
    except Exception:
        pass
    return None, True


def run_user_query(sql_text, isolation_level='READ COMMITTED', readonly=True):
    sql = sql_text.strip()
    if not sql:
        return None, None, 0, 'No SQL provided.'

    if BLOCKED.search(sql):
        return None, None, 0, 'Query contains a blocked statement (DROP, TRUNCATE, ALTER LOGIN, SHUTDOWN).'

    if readonly:
        first_word = sql.split()[0].upper() if sql.split() else ''
        if first_word not in ('SELECT', 'WITH', 'EXEC'):
            return None, None, 0, 'Read-only mode: only SELECT / WITH / EXEC statements are allowed.'

    iso_stmt = ISOLATION_LEVELS.get(isolation_level, ISOLATION_LEVELS['READ COMMITTED'])
    full_sql = iso_stmt + '\n' + sql

    start = time.perf_counter()
    try:
        columns, rows = run_select(full_sql)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return columns, rows, elapsed_ms, None
    except Exception as e:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return None, None, elapsed_ms, str(e)


def rows_to_csv(columns, rows):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    writer.writerows(rows)
    return buf.getvalue()
