import csv
import io
import json
import sqlite3
import os
import zipfile
from datetime import datetime, timezone

from db import run_select


def export_to_sqlite(target_path: str) -> tuple[list[str], str | None]:
    """
    Export every user table from the connected SQL Server DB into a SQLite file.
    Returns (list_of_exported_table_names, error_or_None).
    """
    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)

    try:
        _, table_rows, err = _safe_select(
            """
            SELECT t.name
            FROM sys.tables t
            JOIN sys.partitions p ON t.object_id = p.object_id
            WHERE p.index_id IN (0,1) AND t.is_ms_shipped = 0
            GROUP BY t.name
            ORDER BY t.name
            """
        )
        if err:
            return [], err

        table_names = [r[0] for r in table_rows]
        exported = []

        lite = sqlite3.connect(target_path)

        for table in table_names:
            try:
                cols, rows, err = _safe_select(f"SELECT * FROM [{table}]")
                if err:
                    continue

                # Build CREATE TABLE with TEXT columns (SQLite is flexible)
                col_defs = ', '.join(f'[{c}] TEXT' for c in cols)
                lite.execute(f"DROP TABLE IF EXISTS [{table}]")
                lite.execute(f"CREATE TABLE [{table}] ({col_defs})")

                if rows:
                    placeholders = ', '.join('?' for _ in cols)
                    lite.executemany(
                        f"INSERT INTO [{table}] VALUES ({placeholders})",
                        [tuple(str(v) if v is not None else None for v in row) for row in rows],
                    )

                exported.append(table)
            except Exception:
                continue

        lite.commit()
        lite.close()
        return exported, None

    except Exception as e:
        return [], str(e)


def _get_table_schema(table: str) -> dict:
    """Fetch full schema metadata for a single table from SQL Server system catalogs."""
    schema = {'table': table, 'exported_at': datetime.now(timezone.utc).isoformat(), 'columns': [],
              'primary_key': [], 'foreign_keys': [], 'check_constraints': [], 'default_constraints': []}

    _, rows, _ = _safe_select(
        """
        SELECT
            c.column_id,
            c.name,
            t.name             AS type_name,
            c.max_length,
            c.precision,
            c.scale,
            c.is_nullable,
            c.is_identity,
            c.is_computed
        FROM sys.columns c
        JOIN sys.types t ON c.user_type_id = t.user_type_id
        WHERE c.object_id = OBJECT_ID(?)
        ORDER BY c.column_id
        """,
        (f'dbo.{table}',)
    )
    for r in rows:
        schema['columns'].append({
            'column_id': r[0], 'name': r[1], 'sql_type': r[2],
            'max_length': r[3], 'precision': r[4], 'scale': r[5],
            'nullable': bool(r[6]), 'is_identity': bool(r[7]), 'is_computed': bool(r[8]),
        })

    _, rows, _ = _safe_select(
        """
        SELECT c.name
        FROM sys.indexes i
        JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        WHERE i.object_id = OBJECT_ID(?) AND i.is_primary_key = 1
        ORDER BY ic.key_ordinal
        """,
        (f'dbo.{table}',)
    )
    schema['primary_key'] = [r[0] for r in rows]

    _, rows, _ = _safe_select(
        """
        SELECT
            fk.name,
            c.name,
            rt.name,
            rc.name
        FROM sys.foreign_keys fk
        JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        JOIN sys.columns c  ON fkc.parent_object_id   = c.object_id  AND fkc.parent_column_id   = c.column_id
        JOIN sys.tables  rt ON fkc.referenced_object_id = rt.object_id
        JOIN sys.columns rc ON fkc.referenced_object_id = rc.object_id AND fkc.referenced_column_id = rc.column_id
        WHERE fk.parent_object_id = OBJECT_ID(?)
        """,
        (f'dbo.{table}',)
    )
    schema['foreign_keys'] = [
        {'name': r[0], 'column': r[1], 'references_table': r[2], 'references_column': r[3]}
        for r in rows
    ]

    _, rows, _ = _safe_select(
        """
        SELECT cc.name, c.name, cc.definition
        FROM sys.check_constraints cc
        JOIN sys.columns c ON cc.parent_object_id = c.object_id AND cc.parent_column_id = c.column_id
        WHERE cc.parent_object_id = OBJECT_ID(?)
        """,
        (f'dbo.{table}',)
    )
    schema['check_constraints'] = [
        {'name': r[0], 'column': r[1], 'definition': r[2]} for r in rows
    ]

    _, rows, _ = _safe_select(
        """
        SELECT dc.name, c.name, dc.definition
        FROM sys.default_constraints dc
        JOIN sys.columns c ON dc.parent_object_id = c.object_id AND dc.parent_column_id = c.column_id
        WHERE dc.parent_object_id = OBJECT_ID(?)
        """,
        (f'dbo.{table}',)
    )
    schema['default_constraints'] = [
        {'name': r[0], 'column': r[1], 'definition': r[2]} for r in rows
    ]

    return schema


def export_to_csv_zip() -> tuple[bytes | None, list[str], str | None]:
    """
    Export every user table from the connected SQL Server DB as CSV files
    bundled into a ZIP archive returned as bytes.
    Returns (zip_bytes_or_None, list_of_exported_table_names, error_or_None).
    """
    try:
        _, table_rows, err = _safe_select(
            """
            SELECT t.name
            FROM sys.tables t
            JOIN sys.partitions p ON t.object_id = p.object_id
            WHERE p.index_id IN (0,1) AND t.is_ms_shipped = 0
            GROUP BY t.name
            ORDER BY t.name
            """
        )
        if err:
            return None, [], err

        table_names = [r[0] for r in table_rows]
        exported = []
        buf = io.BytesIO()

        with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for table in table_names:
                try:
                    cols, rows, err = _safe_select(f"SELECT * FROM [{table}]")
                    if err:
                        continue
                    csv_buf = io.StringIO()
                    writer = csv.writer(csv_buf)
                    writer.writerow(cols)
                    for row in rows:
                        writer.writerow(['' if v is None else str(v) for v in row])
                    zf.writestr(f"{table}.csv", csv_buf.getvalue())
                    schema = _get_table_schema(table)
                    zf.writestr(f"{table}.schema.json", json.dumps(schema, indent=2))
                    exported.append(table)
                except Exception:
                    continue

        return buf.getvalue(), exported, None

    except Exception as e:
        return None, [], str(e)


# ── SQL dump helpers ──────────────────────────────────────────────────────────

_MYSQL_BASE_TYPES = {
    'int': 'INT', 'bigint': 'BIGINT', 'smallint': 'SMALLINT',
    'tinyint': 'TINYINT UNSIGNED', 'bit': 'TINYINT(1)',
    'float': 'DOUBLE', 'real': 'FLOAT',
    'money': 'DECIMAL(19,4)', 'smallmoney': 'DECIMAL(10,4)',
    'text': 'LONGTEXT', 'ntext': 'LONGTEXT', 'image': 'LONGBLOB',
    'uniqueidentifier': 'CHAR(36)', 'xml': 'LONGTEXT',
    'hierarchyid': 'VARCHAR(4000)', 'sql_variant': 'LONGTEXT',
    'rowversion': 'BINARY(8)', 'timestamp': 'BINARY(8)',
    'date': 'DATE', 'smalldatetime': 'DATETIME', 'datetime': 'DATETIME',
    'geography': 'GEOMETRY', 'geometry': 'GEOMETRY',
}

_POSTGRES_BASE_TYPES = {
    'int': 'INTEGER', 'bigint': 'BIGINT', 'smallint': 'SMALLINT',
    'tinyint': 'SMALLINT', 'bit': 'BOOLEAN',
    'float': 'DOUBLE PRECISION', 'real': 'REAL',
    'money': 'NUMERIC(19,4)', 'smallmoney': 'NUMERIC(10,4)',
    'text': 'TEXT', 'ntext': 'TEXT', 'image': 'BYTEA',
    'uniqueidentifier': 'UUID', 'xml': 'XML',
    'hierarchyid': 'TEXT', 'sql_variant': 'TEXT',
    'rowversion': 'BYTEA', 'timestamp': 'BYTEA',
    'date': 'DATE', 'smalldatetime': 'TIMESTAMP', 'datetime': 'TIMESTAMP',
    'geography': 'TEXT', 'geometry': 'TEXT',
}


def _map_mysql(col: dict) -> str:
    t, ml, p, s = col['sql_type'].lower(), col['max_length'], col['precision'], col['scale']
    if t in ('decimal', 'numeric'):   return f'DECIMAL({p},{s})'
    if t == 'char':                   return f'CHAR({ml})'
    if t == 'nchar':                  return f'CHAR({ml // 2})'
    if t == 'varchar':                return 'LONGTEXT' if ml == -1 else f'VARCHAR({ml})'
    if t == 'nvarchar':               return 'LONGTEXT' if ml == -1 else f'VARCHAR({ml // 2})'
    if t == 'binary':                 return f'BINARY({ml})'
    if t == 'varbinary':              return 'LONGBLOB' if ml == -1 else f'VARBINARY({ml})'
    if t == 'datetime2':              return f'DATETIME({min(s, 6)})'
    if t == 'datetimeoffset':         return 'VARCHAR(34)'
    if t == 'time':                   return f'TIME({min(s, 6)})'
    return _MYSQL_BASE_TYPES.get(t, 'LONGTEXT')


def _map_postgres(col: dict) -> str:
    t, ml, p, s = col['sql_type'].lower(), col['max_length'], col['precision'], col['scale']
    if t in ('decimal', 'numeric'):   return f'NUMERIC({p},{s})'
    if t == 'char':                   return f'CHAR({ml})'
    if t == 'nchar':                  return f'CHAR({ml // 2})'
    if t == 'varchar':                return 'TEXT' if ml == -1 else f'VARCHAR({ml})'
    if t == 'nvarchar':               return 'TEXT' if ml == -1 else f'VARCHAR({ml // 2})'
    if t in ('binary', 'varbinary'):  return 'BYTEA'
    if t == 'datetime2':              return f'TIMESTAMP({min(s, 6)})'
    if t == 'datetimeoffset':         return 'TIMESTAMPTZ'
    if t == 'time':                   return f'TIME({min(s, 6)})'
    return _POSTGRES_BASE_TYPES.get(t, 'TEXT')


def _esc_mysql(v, sql_type: str) -> str:
    if v is None:
        return 'NULL'
    if isinstance(v, bytes):
        return "X'" + v.hex() + "'"
    return "'" + str(v).replace('\\', '\\\\').replace("'", "\\'") + "'"


def _esc_postgres(v, sql_type: str) -> str:
    if v is None:
        return 'NULL'
    if isinstance(v, bytes):
        return "E'\\\\x" + v.hex() + "'"
    if sql_type.lower() == 'bit':
        return 'TRUE' if str(v) in ('1', 'True', 'true') else 'FALSE'
    return "'" + str(v).replace("'", "''") + "'"


def _user_tables() -> tuple[list[str], str | None]:
    _, rows, err = _safe_select(
        """
        SELECT t.name FROM sys.tables t
        JOIN sys.partitions p ON t.object_id = p.object_id
        WHERE p.index_id IN (0,1) AND t.is_ms_shipped = 0
        GROUP BY t.name ORDER BY t.name
        """
    )
    return ([r[0] for r in rows], err) if not err else ([], err)


def _build_insert_batches(table: str, cols: list, rows: list, esc_fn, batch=200) -> list[str]:
    if not rows:
        return []
    col_list = ', '.join(f'`{c}`' if '`' in esc_fn.__name__ + 'mysql' else f'"{c}"' for c in cols)
    # detect dialect from function name
    q = '`' if esc_fn == _esc_mysql else '"'
    col_list = ', '.join(f'{q}{c}{q}' for c in cols)
    tq = f'{q}{table}{q}'
    lines = []
    for i in range(0, len(rows), batch):
        chunk = rows[i:i + batch]
        values = ',\n  '.join(
            '(' + ', '.join(esc_fn(v, '') for v in row) + ')'
            for row in chunk
        )
        lines.append(f'INSERT INTO {tq} ({col_list}) VALUES\n  {values};')
    return lines


def export_to_mysql_sql() -> tuple[bytes | None, list[str], str | None]:
    table_names, err = _user_tables()
    if err:
        return None, [], err
    try:
        out = [
            '-- Northwind Control Center — MySQL dump',
            f'-- Generated: {datetime.now(timezone.utc).isoformat()}',
            '--',
            '-- ┌─ LOSSY CONVERSION WARNINGS ──────────────────────────────────────────────',
            '-- │  datetime2(7) → DATETIME(6)   : sub-microsecond (100 ns) precision lost',
            '-- │  datetimeoffset → VARCHAR(34)  : timezone offset information lost',
            '-- │  uniqueidentifier → CHAR(36)   : stored as string, no UUID enforcement',
            '-- │  hierarchyid / sql_variant      : stored as text approximations',
            '-- │  geography / geometry            : mapped to MySQL GEOMETRY (different impl.)',
            '-- │  T-SQL procedures/triggers/fns  : NOT exported — SQL dialect incompatible',
            '-- │  NULL is correctly preserved     (unlike the CSV export)',
            '-- └───────────────────────────────────────────────────────────────────────────',
            '',
            'SET NAMES utf8mb4;',
            'SET FOREIGN_KEY_CHECKS = 0;',
            '',
        ]

        all_fks = []
        exported = []

        for table in table_names:
            try:
                schema = _get_table_schema(table)
                cols_meta = schema['columns']
                pk = schema['primary_key']
                defaults = {d['column']: d['definition'] for d in schema['default_constraints']}

                col_lines = []
                for col in cols_meta:
                    mapped = _map_mysql(col)
                    if col['is_identity']:
                        mapped += ' AUTO_INCREMENT'
                    null_kw = 'NOT NULL' if not col['nullable'] else 'NULL'
                    default_clause = ''
                    defn = defaults.get(col['name'], '')
                    if defn:
                        # only emit literal defaults (digits or simple string literals)
                        stripped = defn.strip('()')
                        if stripped.lstrip('-').isdigit() or (stripped.startswith("'") and stripped.endswith("'")):
                            default_clause = f' DEFAULT {stripped}'
                    col_lines.append(f'  `{col["name"]}` {mapped} {null_kw}{default_clause}')

                if pk:
                    col_lines.append('  PRIMARY KEY (' + ', '.join(f'`{c}`' for c in pk) + ')')

                out.append(f'-- ─── {table} ───')
                out.append(f'DROP TABLE IF EXISTS `{table}`;')
                out.append(f'CREATE TABLE `{table}` (')
                out.append(',\n'.join(col_lines))
                out.append(') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')
                out.append('')

                data_cols, rows, data_err = _safe_select(f'SELECT * FROM [{table}]')
                if not data_err and rows:
                    batches = _build_insert_batches(table, data_cols, rows, _esc_mysql)
                    out.extend(batches)
                out.append('')

                for fk in schema['foreign_keys']:
                    all_fks.append(
                        f'ALTER TABLE `{table}` ADD CONSTRAINT `{fk["name"]}` '
                        f'FOREIGN KEY (`{fk["column"]}`) REFERENCES `{fk["references_table"]}` (`{fk["references_column"]}`) '
                        f'ON DELETE NO ACTION ON UPDATE NO ACTION;'
                    )

                exported.append(table)
            except Exception:
                continue

        if all_fks:
            out.append('-- ─── Foreign keys ───')
            out.extend(all_fks)
            out.append('')

        out.append('SET FOREIGN_KEY_CHECKS = 1;')

        return '\n'.join(out).encode('utf-8'), exported, None

    except Exception as e:
        return None, [], str(e)


def export_to_postgres_sql() -> tuple[bytes | None, list[str], str | None]:
    table_names, err = _user_tables()
    if err:
        return None, [], err
    try:
        out = [
            '-- Northwind Control Center — PostgreSQL dump',
            f'-- Generated: {datetime.now(timezone.utc).isoformat()}',
            '--',
            '-- ┌─ LOSSY CONVERSION WARNINGS ──────────────────────────────────────────────',
            '-- │  datetime2(7) → TIMESTAMP(6)   : sub-microsecond (100 ns) precision lost',
            '-- │  datetimeoffset → TIMESTAMPTZ   : PostgreSQL normalises to UTC, offset lost',
            '-- │  tinyint → SMALLINT             : no unsigned 8-bit type in PostgreSQL',
            '-- │  money → NUMERIC(19,4)          : different locale semantics',
            '-- │  hierarchyid / sql_variant       : stored as TEXT',
            '-- │  geography / geometry             : stored as TEXT — use PostGIS for spatial',
            '-- │  T-SQL procedures/triggers/fns   : NOT exported — SQL dialect incompatible',
            '-- │  NULL is correctly preserved      (unlike the CSV export)',
            '-- │  After import: reset identity sequences with setval() where needed',
            '-- └───────────────────────────────────────────────────────────────────────────',
            '',
            'BEGIN;',
            '',
        ]

        all_fks = []
        identity_resets = []
        exported = []

        for table in table_names:
            try:
                schema = _get_table_schema(table)
                cols_meta = schema['columns']
                pk = schema['primary_key']
                defaults = {d['column']: d['definition'] for d in schema['default_constraints']}

                col_lines = []
                for col in cols_meta:
                    mapped = _map_postgres(col)
                    identity_clause = ''
                    if col['is_identity']:
                        identity_clause = ' GENERATED BY DEFAULT AS IDENTITY'
                    null_kw = 'NOT NULL' if not col['nullable'] else ''
                    default_clause = ''
                    defn = defaults.get(col['name'], '')
                    if defn and not col['is_identity']:
                        stripped = defn.strip('()')
                        if stripped.lstrip('-').isdigit() or (stripped.startswith("'") and stripped.endswith("'")):
                            default_clause = f' DEFAULT {stripped}'
                    parts = f'  "{col["name"]}" {mapped}{identity_clause}'
                    if null_kw:
                        parts += f' {null_kw}'
                    if default_clause:
                        parts += default_clause
                    col_lines.append(parts)

                if pk:
                    col_lines.append('  PRIMARY KEY (' + ', '.join(f'"{c}"' for c in pk) + ')')

                out.append(f'-- ─── {table} ───')
                out.append(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                out.append(f'CREATE TABLE "{table}" (')
                out.append(',\n'.join(col_lines))
                out.append(');')
                out.append('')

                data_cols, rows, data_err = _safe_select(f'SELECT * FROM [{table}]')
                type_map = {col['name']: col['sql_type'] for col in cols_meta}

                if not data_err and rows:
                    # build typed escape per column
                    q = '"'
                    col_list = ', '.join(f'{q}{c}{q}' for c in data_cols)
                    for i in range(0, len(rows), 200):
                        chunk = rows[i:i + 200]
                        values = ',\n  '.join(
                            '(' + ', '.join(_esc_postgres(v, type_map.get(data_cols[ci], '')) for ci, v in enumerate(row)) + ')'
                            for row in chunk
                        )
                        out.append(f'INSERT INTO "{table}" ({col_list}) VALUES\n  {values};')
                out.append('')

                for col in cols_meta:
                    if col['is_identity'] and pk:
                        seq = f'"{table}_{col["name"]}_seq"'
                        identity_resets.append(
                            f'SELECT setval(pg_get_serial_sequence(\'"{table}"\', \'{col["name"]}\'), '
                            f'COALESCE(MAX("{col["name"]}"), 0) + 1, false) FROM "{table}";'
                        )

                for fk in schema['foreign_keys']:
                    all_fks.append(
                        f'ALTER TABLE "{table}" ADD CONSTRAINT "{fk["name"]}" '
                        f'FOREIGN KEY ("{fk["column"]}") REFERENCES "{fk["references_table"]}" ("{fk["references_column"]}");'
                    )

                exported.append(table)
            except Exception:
                continue

        if all_fks:
            out.append('-- ─── Foreign keys ───')
            out.extend(all_fks)
            out.append('')

        if identity_resets:
            out.append('-- ─── Reset identity sequences ───')
            out.extend(identity_resets)
            out.append('')

        out.append('COMMIT;')

        return '\n'.join(out).encode('utf-8'), exported, None

    except Exception as e:
        return None, [], str(e)


def _safe_select(sql, params=None):
    try:
        cols, rows = run_select(sql, params)
        return cols, rows, None
    except Exception as e:
        return [], [], str(e)


def get_home_summary():
    summary = {
        'today_orders': 0,
        'pending_events': 0,
        'failed_events': 0,
        'low_stock_count': 0,
        'db_size_mb': 0,
        'events_available': False,
    }

    _, rows, _ = _safe_select(
        "SELECT COUNT(*) FROM Orders WHERE CAST(OrderDate AS DATE) = CAST(GETDATE() AS DATE)"
    )
    if rows:
        summary['today_orders'] = rows[0][0]

    _, rows, _ = _safe_select(
        "SELECT COUNT(*) FROM Products WHERE UnitsInStock <= ReorderLevel"
    )
    if rows:
        summary['low_stock_count'] = rows[0][0]

    try:
        _, rows, err = _safe_select(
            "SELECT COUNT(*) FROM dbo.order_log WHERE status = 0"
        )
        if not err and rows:
            summary['pending_events'] = rows[0][0]
            summary['events_available'] = True
        _, rows, _ = _safe_select(
            "SELECT COUNT(*) FROM dbo.order_log WHERE status = 3"
        )
        if rows:
            summary['failed_events'] = rows[0][0]
    except Exception:
        pass

    _, rows, _ = _safe_select(
        "SELECT CAST(SUM(size) * 8.0 / 1024 AS DECIMAL(10,1)) FROM sys.database_files"
    )
    if rows and rows[0][0] is not None:
        summary['db_size_mb'] = float(rows[0][0])

    return summary


def get_db_sizes():
    cols, rows, err = _safe_select(
        """
        SELECT
            name,
            type_desc,
            CAST(size * 8.0 / 1024 AS DECIMAL(10,1)) AS size_mb,
            CAST(FILEPROPERTY(name, 'SpaceUsed') * 8.0 / 1024 AS DECIMAL(10,1)) AS used_mb,
            physical_name
        FROM sys.database_files
        """
    )
    return cols, rows, err


def get_recent_backups():
    cols, rows, err = _safe_select(
        """
        SELECT TOP 10
            database_name,
            backup_start_date,
            backup_finish_date,
            CASE type
                WHEN 'D' THEN 'Full'
                WHEN 'L' THEN 'Log'
                WHEN 'I' THEN 'Differential'
                ELSE type
            END AS backup_type,
            CAST(backup_size / 1048576.0 AS DECIMAL(10,2)) AS size_mb
        FROM msdb.dbo.backupset
        WHERE database_name = DB_NAME()
        ORDER BY backup_finish_date DESC
        """
    )
    return cols, rows, err


def get_job_status():
    cols, rows, err = _safe_select(
        """
        SELECT TOP 20
            j.name AS job_name,
            CONVERT(datetime,
                CAST(h.run_date AS varchar(8)) + ' ' +
                STUFF(STUFF(RIGHT('000000' + CAST(h.run_time AS varchar(6)), 6), 5, 0, ':'), 3, 0, ':')
            ) AS run_datetime,
            CASE h.run_status
                WHEN 0 THEN 'Failed'
                WHEN 1 THEN 'Succeeded'
                WHEN 2 THEN 'Retry'
                WHEN 3 THEN 'Cancelled'
                WHEN 4 THEN 'In Progress'
                ELSE 'Unknown'
            END AS status,
            h.message
        FROM msdb.dbo.sysjobs j
        JOIN msdb.dbo.sysjobhistory h ON j.job_id = h.job_id
        WHERE h.step_id = 0
        ORDER BY h.run_date DESC, h.run_time DESC
        """
    )
    return cols, rows, err


def get_row_counts():
    cols, rows, err = _safe_select(
        """
        SELECT
            t.name AS table_name,
            SUM(p.rows) AS row_count
        FROM sys.tables t
        JOIN sys.partitions p ON t.object_id = p.object_id
        WHERE p.index_id IN (0, 1)
          AND t.is_ms_shipped = 0
        GROUP BY t.name
        ORDER BY SUM(p.rows) DESC
        """
    )
    return cols, rows, err


def get_low_stock():
    cols, rows, err = _safe_select(
        """
        SELECT
            ProductID, ProductName,
            UnitsInStock, ReorderLevel, UnitsOnOrder,
            CASE WHEN Discontinued = 1 THEN 'Yes' ELSE 'No' END AS Discontinued
        FROM Products
        WHERE UnitsInStock <= ReorderLevel
        ORDER BY UnitsInStock
        """
    )
    return cols, rows, err
