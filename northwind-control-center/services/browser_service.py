"""
browser_service.py — Schema introspection for the Northwind database browser.
All queries target the active pyodbc connection (db.run_select).
"""

import db


def get_schema_tree() -> dict:
    """Return all tables (with row counts), views, and stored procedures."""
    tables = _get_tables()
    views = _get_views()
    procs = _get_procedures()
    return {'tables': tables, 'views': views, 'procedures': procs}


def _get_tables() -> list[dict]:
    cols, rows = db.run_select("""
        SELECT
            t.name,
            p.rows,
            SUM(a.total_pages) * 8 / 1024.0 AS size_mb
        FROM sys.tables t
        JOIN sys.partitions p ON t.object_id = p.object_id
            AND p.index_id IN (0, 1)
        JOIN sys.allocation_units a ON p.partition_id = a.container_id
        GROUP BY t.name, p.rows
        ORDER BY t.name
    """)
    return [{'name': r[0], 'rows': r[1], 'size_mb': round(float(r[2]), 2)} for r in rows]


def _get_views() -> list[str]:
    cols, rows = db.run_select(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS ORDER BY TABLE_NAME"
    )
    return [r[0] for r in rows]


def _get_procedures() -> list[str]:
    cols, rows = db.run_select(
        "SELECT name FROM sys.procedures ORDER BY name"
    )
    return [r[0] for r in rows]


def get_table_columns(table_name: str) -> list[dict]:
    """Return column metadata for a table or view (name validated via whitelist check in route)."""
    cols, rows = db.run_select("""
        SELECT
            c.COLUMN_NAME,
            c.DATA_TYPE,
            c.CHARACTER_MAXIMUM_LENGTH,
            c.NUMERIC_PRECISION,
            c.NUMERIC_SCALE,
            c.IS_NULLABLE,
            c.COLUMN_DEFAULT,
            CASE WHEN pk.COLUMN_NAME IS NOT NULL THEN 1 ELSE 0 END AS is_pk
        FROM INFORMATION_SCHEMA.COLUMNS c
        LEFT JOIN (
            SELECT ku.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku
                ON tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
            WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
              AND tc.TABLE_NAME = ?
        ) pk ON pk.COLUMN_NAME = c.COLUMN_NAME
        WHERE c.TABLE_NAME = ?
        ORDER BY c.ORDINAL_POSITION
    """, [table_name, table_name])

    result = []
    for r in rows:
        col_name, dtype, char_max, num_prec, num_scale, nullable, default, is_pk = r
        if char_max:
            display_type = f'{dtype}({char_max if char_max != -1 else "max"})'
        elif num_prec and dtype in ('decimal', 'numeric'):
            display_type = f'{dtype}({num_prec},{num_scale})'
        else:
            display_type = dtype
        result.append({
            'name':     col_name,
            'type':     display_type,
            'nullable': nullable == 'YES',
            'default':  default,
            'is_pk':    bool(is_pk),
        })
    return result


def get_table_preview(table_name: str, limit: int = 100) -> tuple[list, list]:
    """Return (columns, rows) for a preview of the table."""
    safe_name = f'[{table_name.replace("]", "")}]'
    return db.run_select(f'SELECT TOP {int(limit)} * FROM {safe_name}')


def get_view_definition(view_name: str) -> str:
    cols, rows = db.run_select(
        "SELECT VIEW_DEFINITION FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_NAME = ?",
        [view_name]
    )
    return rows[0][0] if rows else ''


def get_proc_definition(proc_name: str) -> str:
    cols, rows = db.run_select(
        "SELECT OBJECT_DEFINITION(OBJECT_ID(?)) AS def",
        [proc_name]
    )
    return rows[0][0] if rows else ''


def get_db_stats() -> dict:
    """High-level database statistics shown in the header."""
    _, rows = db.run_select("""
        SELECT
            (SELECT COUNT(*) FROM sys.tables) AS table_count,
            (SELECT COUNT(*) FROM INFORMATION_SCHEMA.VIEWS) AS view_count,
            (SELECT COUNT(*) FROM sys.procedures) AS proc_count,
            (SELECT SUM(p.rows) FROM sys.tables t
             JOIN sys.partitions p ON t.object_id = p.object_id
             WHERE p.index_id IN (0,1)) AS total_rows,
            (SELECT SUM(a.total_pages) * 8 / 1024.0
             FROM sys.allocation_units a) AS total_mb
    """)
    if rows:
        r = rows[0]
        return {
            'tables': r[0], 'views': r[1], 'procs': r[2],
            'total_rows': r[3], 'total_mb': round(float(r[4] or 0), 1),
        }
    return {}
