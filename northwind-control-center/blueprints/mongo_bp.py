from flask import Blueprint, render_template, request, flash, redirect, url_for
import meta_db
import services.mongo_service as ms
from auth import login_required, admin_required

mongo_bp = Blueprint('mongo_bp', __name__, url_prefix='/mongo')


def _conns():
    return [c for c in meta_db.list_connections() if c['db_type'] == 'mongodb']

def _all_conns():
    return meta_db.list_connections()


@mongo_bp.route('/')
@login_required
def index():
    conns = _conns()
    conn_id = request.args.get('conn_id', type=int)
    collections, col_err = [], None
    if conn_id:
        collections, col_err = ms.list_collections(conn_id)
    return render_template('mongo/index.html',
        conns=conns, conn_id=conn_id, all_conns=_all_conns(),
        collections=collections, col_err=col_err,
        selected=None, stats=None,
        columns=None, rows=None, find_error=None, filter_str='{}',
        agg_queries=ms.agg_queries(), agg_result=None,
    )


@mongo_bp.route('/<int:conn_id>/collection/<collection>')
@login_required
def view_collection(conn_id, collection):
    filter_str = request.args.get('filter', '{}')
    conns = _conns()
    collections, col_err = ms.list_collections(conn_id)
    stats = ms.get_collection_stats(conn_id, collection)
    columns, rows, find_error = ms.find_documents(conn_id, collection, filter_str)
    return render_template('mongo/index.html',
        conns=conns, conn_id=conn_id, all_conns=_all_conns(),
        collections=collections, col_err=col_err,
        selected=collection, stats=stats,
        columns=columns, rows=rows, find_error=find_error, filter_str=filter_str,
        agg_queries=ms.agg_queries(), agg_result=None,
    )


@mongo_bp.route('/<int:conn_id>/insert/<collection>', methods=['POST'])
@admin_required
def insert_doc(conn_id, collection):
    doc_str = request.form.get('document', '{}')
    err = ms.insert_document(conn_id, collection, doc_str)
    if err:
        flash(f'Insert failed: {err}', 'danger')
    else:
        flash('Document inserted.', 'success')
    return redirect(url_for('mongo_bp.view_collection', conn_id=conn_id, collection=collection))


@mongo_bp.route('/<int:conn_id>/drop/<collection>', methods=['POST'])
@admin_required
def drop_col(conn_id, collection):
    err = ms.drop_collection(conn_id, collection)
    if err:
        flash(f'Drop failed: {err}', 'danger')
    else:
        flash(f'Collection "{collection}" dropped.', 'success')
    return redirect(url_for('mongo_bp.index', conn_id=conn_id))


@mongo_bp.route('/<int:conn_id>/import', methods=['POST'])
@admin_required
def import_northwind(conn_id):
    source_conn_id = request.form.get('source_conn_id', type=int)
    if not source_conn_id:
        flash('Select a source SQL connection.', 'danger')
        return redirect(url_for('mongo_bp.index', conn_id=conn_id))
    stats, err = ms.import_northwind(conn_id, source_conn_id)
    if err:
        flash(f'Import failed: {err}', 'danger')
    else:
        flash(f'Imported — products: {stats.get("products",0)}, '
              f'customers: {stats.get("customers",0)}, '
              f'orders: {stats.get("orders",0)}.', 'success')
    return redirect(url_for('mongo_bp.index', conn_id=conn_id))


@mongo_bp.route('/<int:conn_id>/aggregate', methods=['POST'])
@login_required
def aggregate(conn_id):
    query_key = request.form.get('query_key', '')
    conns = _conns()
    collections, col_err = ms.list_collections(conn_id)
    columns, rows, agg_err = ms.run_aggregation(conn_id, query_key)
    agg_result = {'key': query_key, 'columns': columns, 'rows': rows, 'error': agg_err}
    return render_template('mongo/index.html',
        conns=conns, conn_id=conn_id, all_conns=_all_conns(),
        collections=collections, col_err=col_err,
        selected=None, stats=None,
        columns=None, rows=None, find_error=None, filter_str='{}',
        agg_queries=ms.agg_queries(), agg_result=agg_result,
    )
