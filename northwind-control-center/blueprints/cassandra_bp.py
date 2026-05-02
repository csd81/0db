from flask import Blueprint, render_template, request, flash, redirect, url_for
import meta_db
import services.cassandra_service as cs
from auth import login_required, admin_required

cassandra_bp = Blueprint('cassandra_bp', __name__, url_prefix='/cassandra')


def _conns():
    return [c for c in meta_db.list_connections() if c['db_type'] == 'cassandra']

def _all_conns():
    return meta_db.list_connections()


@cassandra_bp.route('/')
@login_required
def index():
    conns = _conns()
    conn_id = request.args.get('conn_id', type=int)
    keyspace = request.args.get('keyspace')
    table = request.args.get('table')

    keyspaces, ks_err = [], None
    tables, tbl_err = [], None
    table_info = None
    cql_result = None

    if conn_id:
        keyspaces, ks_err = cs.list_keyspaces(conn_id)
    if conn_id and keyspace:
        tables, tbl_err = cs.list_tables(conn_id, keyspace)
    if conn_id and keyspace and table:
        table_info = cs.get_table_info(conn_id, keyspace, table)

    return render_template('cassandra/index.html',
        conns=conns, conn_id=conn_id, all_conns=_all_conns(),
        keyspaces=keyspaces, ks_err=ks_err,
        selected_ks=keyspace,
        tables=tables, tbl_err=tbl_err,
        selected_table=table,
        table_info=table_info,
        builtin_queries=cs.builtin_queries(),
        cql_result=None,
        cql_text='',
    )


@cassandra_bp.route('/<int:conn_id>/run', methods=['POST'])
@login_required
def run_cql(conn_id):
    cql_text = request.form.get('cql_text', '').strip()
    keyspace = request.form.get('keyspace') or None
    builtin_key = request.form.get('builtin_key', '')

    if builtin_key:
        match = next((q for q in cs.builtin_queries() if q['key'] == builtin_key), None)
        if match:
            cql_text = match['cql']

    columns, rows, error = cs.run_cql(conn_id, cql_text, keyspace)
    conns = _conns()
    keyspaces, ks_err = cs.list_keyspaces(conn_id)
    tables, tbl_err = [], None
    if keyspace:
        tables, tbl_err = cs.list_tables(conn_id, keyspace)

    cql_result = {'columns': columns, 'rows': rows, 'error': error}
    return render_template('cassandra/index.html',
        conns=conns, conn_id=conn_id, all_conns=_all_conns(),
        keyspaces=keyspaces, ks_err=ks_err,
        selected_ks=keyspace,
        tables=tables, tbl_err=tbl_err,
        selected_table=None,
        table_info=None,
        builtin_queries=cs.builtin_queries(),
        cql_result=cql_result,
        cql_text=cql_text,
    )


@cassandra_bp.route('/<int:conn_id>/import', methods=['POST'])
@admin_required
def import_northwind(conn_id):
    source_conn_id = request.form.get('source_conn_id', type=int)
    if not source_conn_id:
        flash('Select a source SQL connection.', 'danger')
        return redirect(url_for('cassandra_bp.index', conn_id=conn_id))
    stats, err = cs.import_northwind(conn_id, source_conn_id)
    if err:
        flash(f'Import failed: {err}', 'danger')
    else:
        flash(
            f'Imported — categories: {stats.get("categories", 0)}, '
            f'products: {stats.get("products", 0)}, '
            f'customers: {stats.get("customers", 0)}, '
            f'orders: {stats.get("orders", 0)}, '
            f'order_items: {stats.get("order_items", 0)}.',
            'success'
        )
    return redirect(url_for('cassandra_bp.index', conn_id=conn_id))
