import winrm
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, Response, stream_with_context, current_app, session

import meta_db
import services.ops_service as ops
import services.backup_service as bk
from auth import login_required

exports = Blueprint('exports', __name__, url_prefix='/exports')

_DB_TYPE_LABELS = {
    'sqlserver':  ('SQL Server', 'primary'),
    'sqlite':     ('SQLite',     'secondary'),
    'postgresql': ('PostgreSQL', 'info'),
    'mysql':      ('MySQL',      'warning'),
}


@exports.route('/')
@login_required
def index():
    db_type = session.get('active_db_type', 'sqlserver')
    sqlite_connections = [c for c in meta_db.list_connections() if c['db_type'] == 'sqlite']
    return render_template('exports/index.html',
                           db_type=db_type,
                           sqlite_connections=sqlite_connections,
                           export_result=None)


@exports.route('/sqlite', methods=['POST'])
@login_required
def export_sqlite():
    target_path = request.form.get('target_path', '').strip()
    conn_id = request.form.get('conn_id', '')
    if conn_id:
        rec = meta_db.get_connection_by_id(int(conn_id))
        target_path = rec['conn_params']['database']
    if not target_path:
        flash('Specify a target path or select a registered SQLite connection.', 'danger')
        return redirect(url_for('exports.index'))
    tables, err = ops.export_to_sqlite(target_path)
    sqlite_connections = [c for c in meta_db.list_connections() if c['db_type'] == 'sqlite']
    return render_template('exports/index.html',
                           db_type=session.get('active_db_type', 'sqlserver'),
                           sqlite_connections=sqlite_connections,
                           export_result={'tables': tables, 'error': err, 'path': target_path})


@exports.route('/csv', methods=['POST'])
@login_required
def export_csv():
    zip_bytes, tables, err = ops.export_to_csv_zip()
    if err or not zip_bytes:
        flash(f'CSV export failed: {err}', 'danger')
        return redirect(url_for('exports.index'))
    resp = make_response(zip_bytes)
    resp.headers['Content-Type'] = 'application/zip'
    resp.headers['Content-Disposition'] = 'attachment; filename=northwind_export.zip'
    return resp


@exports.route('/mysql', methods=['POST'])
@login_required
def export_mysql():
    sql_bytes, tables, err = ops.export_to_mysql_sql()
    if err or not sql_bytes:
        flash(f'MySQL export failed: {err}', 'danger')
        return redirect(url_for('exports.index'))
    resp = make_response(sql_bytes)
    resp.headers['Content-Type'] = 'application/sql'
    resp.headers['Content-Disposition'] = 'attachment; filename=northwind_mysql.sql'
    return resp


@exports.route('/postgres', methods=['POST'])
@login_required
def export_postgres():
    sql_bytes, tables, err = ops.export_to_postgres_sql()
    if err or not sql_bytes:
        flash(f'PostgreSQL export failed: {err}', 'danger')
        return redirect(url_for('exports.index'))
    resp = make_response(sql_bytes)
    resp.headers['Content-Type'] = 'application/sql'
    resp.headers['Content-Disposition'] = 'attachment; filename=northwind_postgres.sql'
    return resp


@exports.route('/backup', methods=['POST'])
@login_required
def backup_native():
    cfg = current_app.config
    host     = cfg['WINRM_HOST']
    username = cfg['WINRM_USERNAME']
    password = cfg['WINRM_PASSWORD']
    bak_path = cfg['WINRM_BAK_PATH']

    if not host:
        flash('WINRM_HOST not configured in .env.', 'danger')
        return redirect(url_for('exports.index'))

    bak_dir = bak_path.rsplit('\\', 1)[0]
    winrm.Session(host, auth=(username, password), transport='ntlm').run_ps(
        f'New-Item -ItemType Directory -Force -Path "{bak_dir}"'
    )

    err = bk.trigger_backup_to_disk(bak_path)
    if err:
        flash(f'Backup failed: {err}', 'danger')
        return redirect(url_for('exports.index'))

    file_size, err = bk.verify_file_winrm(host, username, password, bak_path)
    if err or file_size == 0:
        flash(f'Backup file not found on VM: {err}', 'danger')
        return redirect(url_for('exports.index'))

    filename = bak_path.rsplit('\\', 1)[-1]
    return Response(
        stream_with_context(bk.stream_from_winrm(host, username, password, bak_path, file_size)),
        mimetype='application/octet-stream',
        headers={
            'Content-Disposition': f'attachment; filename={filename}',
            'Content-Length': str(file_size),
        },
    )
