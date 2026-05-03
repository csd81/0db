import base64
import decimal
import datetime
import os
import time as _time

import pyodbc
from flask import Blueprint, render_template, jsonify, abort, request, current_app
from auth import login_required
import services.browser_service as bsvc
import db

browser_bp = Blueprint('browser_bp', __name__, url_prefix='/browser')


# ── Image detection ───────────────────────────────────────────────────────────

_IMAGE_MAGIC = [
    (b'\xff\xd8\xff',       'image/jpeg'),
    (b'\x89PNG\r\n\x1a\n', 'image/png'),
    (b'GIF89a',             'image/gif'),
    (b'GIF87a',             'image/gif'),
    (b'BM',                 'image/bmp'),
]


def _find_image(data: bytes):
    """Scan first 512 bytes for image magic, return (mime, offset) or (None, 0)."""
    for magic, mime in _IMAGE_MAGIC:
        idx = data.find(magic, 0, 512)
        if idx != -1:
            return mime, idx
    idx = data.find(b'RIFF', 0, 512)
    if idx != -1 and data[idx + 8:idx + 12] == b'WEBP':
        return 'image/webp', idx
    return None, 0


def _safe(v):
    if v is None:
        return None
    if isinstance(v, (datetime.datetime, datetime.date, datetime.time)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (bytes, bytearray)):
        raw = bytes(v)
        mime, offset = _find_image(raw)
        if mime:
            return 'data:' + mime + ';base64,' + base64.b64encode(raw[offset:]).decode('ascii')
        return raw.hex()
    return v


def _safe_rows(rows):
    return [[_safe(cell) for cell in row] for row in rows]


# ── Admin connection ──────────────────────────────────────────────────────────

def _admin_conn(target_db='master', autocommit=True):
    """Open a fresh pyodbc connection using SA credentials."""
    c = current_app.config
    sa_user = c.get('SQL_SA_USERNAME', '')
    sa_pass = c.get('SQL_SA_PASSWORD', '')
    if not sa_user:
        raise ValueError('SQL_SA_USERNAME not configured in .env')
    conn_str = (
        f"DRIVER={{{c['SQL_DRIVER']}}};"
        f"SERVER={c['SQL_SERVER']};"
        f"DATABASE={target_db};"
        f"UID={sa_user};"
        f"PWD={sa_pass};"
        f"Encrypt={c['SQL_ENCRYPT']};"
        f"TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )
    conn = pyodbc.connect(conn_str, timeout=15, autocommit=autocommit)
    return conn


def _user_conn(target_db):
    """Open a fresh pyodbc connection to target_db using regular (flask_user) credentials."""
    c = current_app.config
    conn_str = (
        f"DRIVER={{{c['SQL_DRIVER']}}};"
        f"SERVER={c['SQL_SERVER']};"
        f"DATABASE={target_db};"
        f"UID={c['SQL_USERNAME']};"
        f"PWD={c['SQL_PASSWORD']};"
        f"Encrypt={c['SQL_ENCRYPT']};"
        f"TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )
    return pyodbc.connect(conn_str, timeout=10)


# ── Schema helpers ────────────────────────────────────────────────────────────

def _valid_table(name):
    tree = bsvc.get_schema_tree()
    return name in ({t['name'] for t in tree['tables']} | set(tree['views']))


def _valid_proc(name):
    return name in bsvc.get_schema_tree()['procedures']


# ── Routes ────────────────────────────────────────────────────────────────────

def _schema_from_conn(conn) -> dict:
    """Fetch schema tree (tables, views, procs) from an arbitrary pyodbc connection."""
    cur = conn.cursor()

    cur.execute("""
        SELECT t.name, p.rows
        FROM sys.tables t
        JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0, 1)
        ORDER BY t.name
    """)
    tables = [{'name': r[0], 'rows': r[1]} for r in cur.fetchall()]

    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS ORDER BY TABLE_NAME")
    views = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT name FROM sys.procedures ORDER BY name")
    procs = [r[0] for r in cur.fetchall()]

    return {'tables': tables, 'views': views, 'procedures': procs}


def _columns_from_conn(conn, table_name: str) -> list:
    cur = conn.cursor()
    cur.execute("""
        SELECT c.COLUMN_NAME, c.DATA_TYPE, c.CHARACTER_MAXIMUM_LENGTH,
               c.NUMERIC_PRECISION, c.NUMERIC_SCALE, c.IS_NULLABLE, c.COLUMN_DEFAULT,
               CASE WHEN pk.COLUMN_NAME IS NOT NULL THEN 1 ELSE 0 END AS is_pk
        FROM INFORMATION_SCHEMA.COLUMNS c
        LEFT JOIN (
            SELECT ku.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku ON tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
            WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY' AND tc.TABLE_NAME = ?
        ) pk ON pk.COLUMN_NAME = c.COLUMN_NAME
        WHERE c.TABLE_NAME = ?
        ORDER BY c.ORDINAL_POSITION
    """, [table_name, table_name])
    result = []
    for r in cur.fetchall():
        col_name, dtype, char_max, num_prec, num_scale, nullable, default, is_pk = r
        if char_max:
            display_type = f'{dtype}({char_max if char_max != -1 else "max"})'
        elif num_prec and dtype in ('decimal', 'numeric'):
            display_type = f'{dtype}({num_prec},{num_scale})'
        else:
            display_type = dtype
        result.append({'name': col_name, 'type': display_type,
                        'nullable': nullable == 'YES', 'default': default, 'is_pk': bool(is_pk)})
    return result


@browser_bp.route('/')
@login_required
def index():
    from flask import session
    try:
        stats = bsvc.get_db_stats()
    except Exception:
        stats = {}
    active_db = session.get('active_db', current_app.config['SQL_DATABASE'])
    default_db = current_app.config['SQL_DATABASE']
    return render_template('browser/index.html', stats=stats,
                           active_db=active_db, default_db=default_db)


@browser_bp.route('/schema')
@login_required
def schema():
    """Return schema tree (tables/views/procs) for any database."""
    target_db = request.args.get('db', '').strip()
    default_db = current_app.config['SQL_DATABASE']
    if not target_db or target_db == default_db:
        try:
            return jsonify(bsvc.get_schema_tree())
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    try:
        conn = _admin_conn(target_db, autocommit=True)
        tree = _schema_from_conn(conn)
        conn.close()
        return jsonify(tree)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@browser_bp.route('/databases')
@login_required
def list_databases():
    """Return all databases on the server (requires SA credentials)."""
    try:
        conn = _admin_conn('master', autocommit=True)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sys.databases ORDER BY name")
        dbs = [row[0] for row in cur.fetchall()]
        conn.close()
        return jsonify({'databases': dbs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@browser_bp.route('/table/<path:name>')
@login_required
def table_detail(name):
    if name.startswith('#'):
        return jsonify({'error': 'Temp tables are session-scoped and cannot be previewed from a separate connection. Query #temp directly in Query Studio from the session that created it.'}), 400
    target_db = request.args.get('db', '').strip()
    default_db = current_app.config['SQL_DATABASE']
    if target_db and target_db != default_db:
        try:
            conn = _admin_conn(target_db, autocommit=True)
            columns = _columns_from_conn(conn, name)
            cur = conn.cursor()
            cur.execute(f'SELECT TOP 200 * FROM [{name.replace("]", "")}]')
            col_names = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()
            conn.close()
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        return jsonify({
            'name': name, 'is_view': False, 'columns': columns,
            'preview_columns': col_names,
            'preview_rows': _safe_rows(rows),
            'view_def': None,
        })
    try:
        if not _valid_table(name):
            abort(404)
        columns = bsvc.get_table_columns(name)
        cols, rows = bsvc.get_table_preview(name, limit=200)
        is_view = name in bsvc.get_schema_tree()['views']
        view_def = bsvc.get_view_definition(name) if is_view else None
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({
        'name': name, 'is_view': is_view, 'columns': columns,
        'preview_columns': cols, 'preview_rows': _safe_rows(rows),
        'view_def': view_def,
    })


@browser_bp.route('/proc/<path:name>')
@login_required
def proc_detail(name):
    target_db = request.args.get('db', '').strip()
    default_db = current_app.config['SQL_DATABASE']
    if target_db and target_db != default_db:
        try:
            conn = _admin_conn(target_db, autocommit=True)
            cur = conn.cursor()
            cur.execute("SELECT OBJECT_DEFINITION(OBJECT_ID(?)) AS def", [name])
            row = cur.fetchone()
            conn.close()
            return jsonify({'name': name, 'definition': row[0] if row else ''})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    try:
        if not _valid_proc(name):
            abort(404)
        definition = bsvc.get_proc_definition(name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'name': name, 'definition': definition})


@browser_bp.route('/run', methods=['POST'])
@login_required
def run_sql():
    sql = (request.form.get('sql') or '').strip()
    if not sql:
        return jsonify({'error': 'No SQL provided.'}), 400

    admin     = request.form.get('admin', '0') == '1'
    target_db = (request.form.get('target_db') or '').strip()

    t0 = _time.perf_counter()
    conn = None
    server_msgs = []
    try:
        if admin:
            conn = _admin_conn(target_db or 'master', autocommit=True)
            columns, rows, rowcount, error, server_msgs = db.run_any_on_conn(conn, sql)
        elif target_db:
            conn = _user_conn(target_db)
            columns, rows, rowcount, error, server_msgs = db.run_any_on_conn(conn, sql)
        else:
            columns, rows, rowcount, error, server_msgs = db.run_any(sql)
    except Exception as e:
        columns, rows, rowcount, error = [], [], 0, str(e)
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

    elapsed_ms = round((_time.perf_counter() - t0) * 1000, 1)
    return jsonify({
        'columns': columns,
        'rows': _safe_rows(rows),
        'row_count': rowcount,
        'elapsed_ms': elapsed_ms,
        'error': error,
        'server_msgs': server_msgs,
    })


@browser_bp.route('/read-file')
@login_required
def read_file_content():
    """Return the text content of a server-side file without executing it."""
    file_path = request.args.get('path', '').strip()
    if not file_path:
        return jsonify({'error': 'No path provided.'}), 400
    if not os.path.isfile(file_path):
        return jsonify({'error': f'File not found: {file_path}'}), 400
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@browser_bp.route('/save-file', methods=['POST'])
@login_required
def save_file():
    """Write editor content back to a server-side file."""
    file_path = (request.form.get('file_path') or '').strip()
    content   = request.form.get('content', '')
    if not file_path:
        return jsonify({'error': 'No file path provided.'}), 400
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@browser_bp.route('/run-file', methods=['POST'])
@login_required
def run_file():
    """Execute a .sql script file on the server, batch by batch (GO-separated).
    Uses SA credentials with autocommit=True — identical to SSMS behaviour."""
    file_path = (request.form.get('file_path') or '').strip()
    target_db = (request.form.get('target_db') or 'master').strip()

    if not file_path:
        return jsonify({'error': 'No file path provided.'}), 400
    if not os.path.isfile(file_path):
        return jsonify({'error': f'File not found: {file_path}'}), 400

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            sql_text = f.read()
    except Exception as e:
        return jsonify({'error': f'Cannot read file: {e}'}), 400

    batches = db._split_go_batches(sql_text)
    if not batches:
        return jsonify({'error': 'File contains no executable SQL batches.'}), 400

    t0 = _time.perf_counter()
    errors = []
    total_rowcount = 0
    last_columns, last_rows = [], []

    try:
        conn = _admin_conn(target_db, autocommit=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    try:
        for i, batch in enumerate(batches):
            try:
                cur = conn.cursor()
                cur.execute(batch)
                if cur.description:
                    last_columns = [col[0] for col in cur.description]
                    last_rows = [[_safe(cell) for cell in row] for row in cur.fetchall()]
                else:
                    rc = cur.rowcount if cur.rowcount is not None else 0
                    if rc > 0:
                        total_rowcount += rc
            except Exception as e:
                errors.append(f'Batch {i + 1}: {str(e)[:300]}')
    finally:
        try:
            conn.close()
        except Exception:
            pass

    elapsed_ms = round((_time.perf_counter() - t0) * 1000, 1)
    summary = (
        f'{len(batches)} batch(es) · {total_rowcount} row(s) affected'
        + (f' · {len(errors)} error(s)' if errors else '')
    )
    return jsonify({
        'columns':     last_columns,
        'rows':        last_rows,
        'row_count':   len(last_rows) if last_columns else total_rowcount,
        'elapsed_ms':  elapsed_ms,
        'error':       '\n'.join(errors) if errors else None,
        'summary':     summary,
        'batch_count': len(batches),
        'error_count': len(errors),
    })
