from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import meta_db
import services.rqlite_service as rs
from auth import login_required, admin_required

rqlite_bp = Blueprint('rqlite_bp', __name__, url_prefix='/rqlite')


def _conns():
    return [c for c in meta_db.list_connections() if c['db_type'] == 'rqlite']


@rqlite_bp.route('/')
@login_required
def index():
    conns = _conns()
    conn_id = request.args.get('conn_id', type=int)
    info = None
    if conn_id:
        try:
            info = rs.get_cluster_info(conn_id)
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('rqlite/index.html',
        conns=conns, conn_id=conn_id, info=info,
        cql_result=None, sql_text='',
    )


@rqlite_bp.route('/<int:conn_id>/run', methods=['POST'])
@login_required
def run(conn_id):
    sql_text = request.form.get('sql_text', '').strip()
    conns = _conns()
    try:
        info = rs.get_cluster_info(conn_id)
    except Exception as e:
        info = None
        flash(str(e), 'danger')

    cols, rows, elapsed_ms, error = rs.run_query(conn_id, sql_text)
    cql_result = {'columns': cols, 'rows': rows, 'elapsed_ms': elapsed_ms, 'error': error}
    return render_template('rqlite/index.html',
        conns=conns, conn_id=conn_id, info=info,
        cql_result=cql_result, sql_text=sql_text,
    )


@rqlite_bp.route('/<int:conn_id>/status.json')
@login_required
def status_json(conn_id):
    """JSON endpoint for live cluster polling."""
    try:
        info = rs.get_cluster_info(conn_id)
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
