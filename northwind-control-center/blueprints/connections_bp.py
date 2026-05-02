import sqlite3

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

import meta_db
import db_adapter
from auth import login_required, admin_required
from services import transaction_service as ts

connections = Blueprint('connections', __name__, url_prefix='/connections')

_DB_TYPES = ['sqlite', 'sqlserver', 'postgresql', 'mysql']


@connections.route('/')
@login_required
def list_connections():
    conns = meta_db.list_connections()
    return render_template('connections/list.html', connections=conns)


@connections.route('/new', methods=['GET', 'POST'])
@admin_required
def new_connection():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        db_type = request.form.get('db_type', 'sqlite')
        password = request.form.get('password', '')
        conn_params = _params_from_form(db_type, request.form)
        if not name:
            flash('Name is required.', 'danger')
        else:
            if db_type == 'sqlite':
                path = conn_params.get('database', '')
                if path:
                    import os
                    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                    # Touch the file so it exists before we register it
                    open(path, 'a').close()
            meta_db.create_connection(name, db_type, conn_params, password)
            flash(f"Connection '{name}' added.", 'success')
            return redirect(url_for('connections.list_connections'))
    from flask import current_app
    defaults = _env_defaults(current_app)
    return render_template('connections/form.html', conn=None, db_types=_DB_TYPES, defaults=defaults)


@connections.route('/<int:conn_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_connection(conn_id):
    rec = meta_db.get_connection_by_id(conn_id)
    if not rec:
        flash('Connection not found.', 'danger')
        return redirect(url_for('connections.list_connections'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        db_type = request.form.get('db_type', rec['db_type'])
        password = request.form.get('password', '')
        conn_params = _params_from_form(db_type, request.form)
        meta_db.update_connection(conn_id, name, db_type, conn_params, password)
        flash(f"Connection '{name}' updated.", 'success')
        return redirect(url_for('connections.list_connections'))

    from flask import current_app
    defaults = _env_defaults(current_app)
    return render_template('connections/form.html', conn=rec, db_types=_DB_TYPES, defaults=defaults)


@connections.route('/<int:conn_id>/delete', methods=['POST'])
@admin_required
def delete_connection(conn_id):
    meta_db.delete_connection(conn_id)
    flash('Connection deleted.', 'success')
    return redirect(url_for('connections.list_connections'))


@connections.route('/<int:conn_id>/test', methods=['POST'])
@login_required
def test_connection(conn_id):
    ok, err = db_adapter.adapter_test(conn_id)
    if ok:
        flash('Connection successful.', 'success')
    else:
        flash(f'Connection failed: {err}', 'danger')
    return redirect(url_for('connections.list_connections'))


# ── SQLite table browser ───────────────────────────────────────────────────────

@connections.route('/<int:conn_id>/browse')
@login_required
def browse(conn_id):
    rec = meta_db.get_connection_by_id(conn_id)
    if not rec or rec['db_type'] != 'sqlite':
        flash('Browser only available for SQLite connections.', 'warning')
        return redirect(url_for('connections.list_connections'))

    conn = db_adapter.get_adapter_connection(conn_id)
    ts.ensure_transaction_log(conn)
    tables = _list_tables(conn)
    return render_template('connections/browser.html', conn=rec, tables=tables,
                           selected_table=None, columns=None, rows=None)


@connections.route('/<int:conn_id>/browse/<table>')
@login_required
def browse_table(conn_id, table):
    rec = meta_db.get_connection_by_id(conn_id)
    if not rec or rec['db_type'] != 'sqlite':
        flash('Browser only available for SQLite connections.', 'warning')
        return redirect(url_for('connections.list_connections'))

    conn = db_adapter.get_adapter_connection(conn_id)
    ts.ensure_transaction_log(conn)
    tables = _list_tables(conn)

    if table not in tables:
        flash(f"Table '{table}' not found.", 'warning')
        return redirect(url_for('connections.browse', conn_id=conn_id))

    cols, rows = db_adapter.adapter_select(conn_id, f"SELECT * FROM [{table}] LIMIT 200")
    return render_template('connections/browser.html', conn=rec, tables=tables,
                           selected_table=table, columns=cols, rows=rows)


@connections.route('/<int:conn_id>/browse/<table>/insert', methods=['POST'])
@admin_required
def insert_row(conn_id, table):
    rec = meta_db.get_connection_by_id(conn_id)
    conn = db_adapter.get_adapter_connection(conn_id)
    ts.ensure_transaction_log(conn)

    data = {k: v for k, v in request.form.items() if k != 'csrf_token'}
    try:
        ts.tracked_insert(conn, table, data)
        flash('Row inserted.', 'success')
    except Exception as e:
        flash(f'Insert failed: {e}', 'danger')
    return redirect(url_for('connections.browse_table', conn_id=conn_id, table=table))


@connections.route('/<int:conn_id>/browse/<table>/update/<pk>', methods=['POST'])
@admin_required
def update_row(conn_id, table, pk):
    conn = db_adapter.get_adapter_connection(conn_id)
    ts.ensure_transaction_log(conn)

    pk_col = request.form.get('_pk_col', 'rowid')
    updates = {k: v for k, v in request.form.items()
               if k not in ('csrf_token', '_pk_col')}
    try:
        ts.tracked_update(conn, table, pk_col, pk, updates)
        flash('Row updated.', 'success')
    except Exception as e:
        flash(f'Update failed: {e}', 'danger')
    return redirect(url_for('connections.browse_table', conn_id=conn_id, table=table))


@connections.route('/<int:conn_id>/browse/<table>/delete/<pk>', methods=['POST'])
@admin_required
def delete_row(conn_id, table, pk):
    conn = db_adapter.get_adapter_connection(conn_id)
    ts.ensure_transaction_log(conn)

    pk_col = request.form.get('_pk_col', 'rowid')
    try:
        ts.tracked_delete(conn, table, pk_col, pk)
        flash('Row deleted.', 'success')
    except Exception as e:
        flash(f'Delete failed: {e}', 'danger')
    return redirect(url_for('connections.browse_table', conn_id=conn_id, table=table))


@connections.route('/<int:conn_id>/txlog')
@login_required
def txlog(conn_id):
    rec = meta_db.get_connection_by_id(conn_id)
    conn = db_adapter.get_adapter_connection(conn_id)
    ts.ensure_transaction_log(conn)
    log = ts.get_transaction_log(conn)
    return render_template('connections/txlog.html', conn=rec, log=log)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _list_tables(conn: sqlite3.Connection) -> list[str]:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name != 'TransactionLog' ORDER BY name"
    )
    return [r[0] for r in cur.fetchall()]


def _env_defaults(app) -> dict:
    """Pull current .env SQL Server values to pre-fill the new-connection form."""
    return {
        'server':           app.config.get('SQL_SERVER', ''),
        'database':         app.config.get('SQL_DATABASE', ''),
        'username':         app.config.get('SQL_USERNAME', ''),
        'driver':           app.config.get('SQL_DRIVER', 'ODBC Driver 18 for SQL Server'),
        'encrypt':          app.config.get('SQL_ENCRYPT', 'yes'),
        'trust_server_cert': app.config.get('SQL_TRUST_SERVER_CERT', 'yes'),
    }


def _params_from_form(db_type: str, form) -> dict:
    if db_type == 'sqlite':
        return {'database': form.get('sqlite_path', '').strip()}
    elif db_type == 'sqlserver':
        return {
            'server': form.get('ss_server', '').strip(),
            'database': form.get('ss_database', '').strip(),
            'username': form.get('ss_username', '').strip(),
            'driver': form.get('ss_driver', 'ODBC Driver 18 for SQL Server').strip(),
            'encrypt': form.get('ss_encrypt', 'yes'),
            'trust_server_cert': form.get('ss_trust_cert', 'yes'),
        }
    elif db_type == 'postgresql':
        return {
            'host': form.get('pg_host', 'localhost').strip(),
            'port': form.get('pg_port', '5432').strip(),
            'database': form.get('pg_database', 'postgres').strip(),
            'username': form.get('pg_username', 'postgres').strip(),
        }
    elif db_type == 'mysql':
        return {
            'host': form.get('my_host', 'localhost').strip(),
            'port': form.get('my_port', '3306').strip(),
            'database': form.get('my_database', '').strip(),
            'username': form.get('my_username', 'root').strip(),
        }
    return {}
