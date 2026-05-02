import sqlite3

from flask import Blueprint, render_template, request, redirect, url_for, flash

import meta_db
import db_adapter
from auth import login_required
from services import dqs_service as dqs

dqs_bp = Blueprint('dqs', __name__, url_prefix='/dqs')


@dqs_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    connections = meta_db.list_connections()
    # Handle the initial table selection form (conn + table in POST body)
    if request.method == 'POST':
        conn_id = int(request.form.get('conn_sel', 0) or 0)
        table = request.form.get('table_input', '').strip()
        if conn_id and table:
            return redirect(url_for('dqs.report', conn_id=conn_id, table=table))
    return render_template('dqs/index.html', connections=connections,
                           report=None, conn=None, table=None, text_cols=[])


@dqs_bp.route('/<int:conn_id>/<table>', methods=['GET', 'POST'])
@login_required
def report(conn_id, table):
    rec = meta_db.get_connection_by_id(conn_id)
    text_col = request.form.get('text_col') or request.args.get('text_col')
    threshold = int(request.form.get('threshold', 2))

    try:
        conn = db_adapter.get_adapter_connection(conn_id)
        if rec['db_type'] == 'sqlite':
            cur = conn.execute(f"PRAGMA table_info([{table}])")
            text_cols = [r[1] for r in cur.fetchall()
                         if 'TEXT' in (r[2] or '').upper() or r[2] == '']
        else:
            cols, _ = db_adapter.adapter_select(conn_id, f"SELECT TOP 0 * FROM [{table}]")
            text_cols = cols
    except Exception:
        text_cols = []

    dqs_report = dqs.run_full_dqs_report(conn_id, table, text_col, threshold)
    connections = meta_db.list_connections()
    return render_template('dqs/index.html',
                           connections=connections,
                           report=dqs_report,
                           conn=rec,
                           table=table,
                           text_cols=text_cols,
                           selected_text_col=text_col,
                           threshold=threshold)
