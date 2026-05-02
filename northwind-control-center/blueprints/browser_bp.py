import decimal
import datetime

from flask import Blueprint, render_template, jsonify, abort
from auth import login_required
import services.browser_service as bsvc

browser_bp = Blueprint('browser_bp', __name__, url_prefix='/browser')


def _safe(v):
    """Convert pyodbc-returned values to JSON-safe types."""
    if v is None:
        return None
    if isinstance(v, (datetime.datetime, datetime.date, datetime.time)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (bytes, bytearray)):
        return v.hex()
    return v


def _safe_rows(rows):
    return [[_safe(cell) for cell in row] for row in rows]


def _valid_table(name):
    tree = bsvc.get_schema_tree()
    valid = {t['name'] for t in tree['tables']} | set(tree['views'])
    return name in valid


def _valid_proc(name):
    return name in bsvc.get_schema_tree()['procedures']


@browser_bp.route('/')
@login_required
def index():
    try:
        tree = bsvc.get_schema_tree()
        stats = bsvc.get_db_stats()
    except Exception:
        tree = {'tables': [], 'views': [], 'procedures': []}
        stats = {}
    return render_template('browser/index.html', tree=tree, stats=stats)


@browser_bp.route('/table/<path:name>')
@login_required
def table_detail(name):
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
        'name': name,
        'is_view': is_view,
        'columns': columns,
        'preview_columns': cols,
        'preview_rows': _safe_rows(rows),
        'view_def': view_def,
    })


@browser_bp.route('/proc/<path:name>')
@login_required
def proc_detail(name):
    try:
        if not _valid_proc(name):
            abort(404)
        definition = bsvc.get_proc_definition(name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'name': name, 'definition': definition})
