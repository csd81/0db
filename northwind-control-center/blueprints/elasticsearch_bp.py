from flask import Blueprint, render_template, request, flash, redirect, url_for
import meta_db
import services.elasticsearch_service as es_svc
from auth import login_required, admin_required

elasticsearch_bp = Blueprint('elasticsearch_bp', __name__, url_prefix='/elasticsearch')


def _es_conns():
    """Return only Elasticsearch-type connections."""
    return [c for c in meta_db.list_connections() if c['db_type'] == 'elasticsearch']


def _sql_conns():
    """Return only SQL-type connections (for import source selector)."""
    sql_types = {'sqlserver', 'postgresql', 'mysql', 'sqlite'}
    return [c for c in meta_db.list_connections() if c['db_type'] in sql_types]


# ── Index (home) ──────────────────────────────────────────────────────────────

@elasticsearch_bp.route('/')
@login_required
def index():
    conns = _es_conns()
    conn_id = request.args.get('conn_id', type=int)
    indices, idx_err = [], None
    if conn_id:
        indices, idx_err = es_svc.list_indices(conn_id)
    return render_template(
        'elasticsearch/index.html',
        conns=conns,
        conn_id=conn_id,
        all_conns=meta_db.list_connections(),
        sql_conns=_sql_conns(),
        indices=indices,
        idx_err=idx_err,
        selected_index=None,
        index_info=None,
        search_query='',
        fuzziness='AUTO',
        columns=None,
        rows=None,
        total_hits=0,
        search_error=None,
        agg_demos=es_svc.aggregation_demos(conn_id) if conn_id else [],
        agg_key='',
        agg_columns=None,
        agg_rows=None,
        agg_error=None,
        builtin_queries=es_svc.builtin_queries(),
    )


# ── Import Northwind ──────────────────────────────────────────────────────────

@elasticsearch_bp.route('/<int:conn_id>/import', methods=['POST'])
@admin_required
def import_northwind(conn_id):
    source_conn_id = request.form.get('source_conn_id', type=int)
    if not source_conn_id:
        flash('Select a source SQL connection.', 'danger')
        return redirect(url_for('elasticsearch_bp.index', conn_id=conn_id))

    stats, err = es_svc.import_northwind(conn_id, source_conn_id)
    if err:
        flash(f'Import failed: {err}', 'danger')
    else:
        flash(
            f'Import complete — products: {stats.get("products", 0)}, '
            f'categories: {stats.get("categories", 0)}.',
            'success',
        )
    return redirect(url_for('elasticsearch_bp.index', conn_id=conn_id))


# ── View index info ───────────────────────────────────────────────────────────

@elasticsearch_bp.route('/<int:conn_id>/index/<index_name>')
@login_required
def view_index(conn_id, index_name):
    conns = _es_conns()
    indices, idx_err = es_svc.list_indices(conn_id)
    index_info = es_svc.get_index_info(conn_id, index_name)
    return render_template(
        'elasticsearch/index.html',
        conns=conns,
        conn_id=conn_id,
        all_conns=meta_db.list_connections(),
        sql_conns=_sql_conns(),
        indices=indices,
        idx_err=idx_err,
        selected_index=index_name,
        index_info=index_info,
        search_query='',
        fuzziness='AUTO',
        columns=None,
        rows=None,
        total_hits=0,
        search_error=None,
        agg_demos=es_svc.aggregation_demos(conn_id),
        agg_key='',
        agg_columns=None,
        agg_rows=None,
        agg_error=None,
        builtin_queries=es_svc.builtin_queries(),
    )


# ── Search ────────────────────────────────────────────────────────────────────

@elasticsearch_bp.route('/<int:conn_id>/search', methods=['POST'])
@login_required
def search(conn_id):
    index_name = request.form.get('index_name', '')
    search_query = request.form.get('search_query', '').strip()
    fuzziness = request.form.get('fuzziness', 'AUTO')

    columns, rows, total_hits, search_error = [], [], 0, None
    index_info = None

    if index_name and search_query:
        columns, rows, total_hits, search_error = es_svc.search(
            conn_id, index_name, search_query, fuzziness
        )
        index_info = es_svc.get_index_info(conn_id, index_name)
    elif index_name:
        index_info = es_svc.get_index_info(conn_id, index_name)

    conns = _es_conns()
    indices, idx_err = es_svc.list_indices(conn_id)
    return render_template(
        'elasticsearch/index.html',
        conns=conns,
        conn_id=conn_id,
        all_conns=meta_db.list_connections(),
        sql_conns=_sql_conns(),
        indices=indices,
        idx_err=idx_err,
        selected_index=index_name,
        index_info=index_info,
        search_query=search_query,
        fuzziness=fuzziness,
        columns=columns,
        rows=rows,
        total_hits=total_hits,
        search_error=search_error,
        agg_demos=es_svc.aggregation_demos(conn_id),
        agg_key='',
        agg_columns=None,
        agg_rows=None,
        agg_error=None,
        builtin_queries=es_svc.builtin_queries(),
    )


# ── Delete index ──────────────────────────────────────────────────────────────

@elasticsearch_bp.route('/<int:conn_id>/delete/<index_name>', methods=['POST'])
@admin_required
def delete_index(conn_id, index_name):
    err = es_svc.delete_index(conn_id, index_name)
    if err:
        flash(f'Delete failed: {err}', 'danger')
    else:
        flash(f'Index "{index_name}" deleted.', 'success')
    return redirect(url_for('elasticsearch_bp.index', conn_id=conn_id))


# ── Aggregate ─────────────────────────────────────────────────────────────────

@elasticsearch_bp.route('/<int:conn_id>/aggregate', methods=['POST'])
@login_required
def aggregate(conn_id):
    agg_key = request.form.get('agg_key', '')
    agg_columns, agg_rows, agg_error = es_svc.run_aggregation(conn_id, agg_key)

    conns = _es_conns()
    indices, idx_err = es_svc.list_indices(conn_id)
    return render_template(
        'elasticsearch/index.html',
        conns=conns,
        conn_id=conn_id,
        all_conns=meta_db.list_connections(),
        sql_conns=_sql_conns(),
        indices=indices,
        idx_err=idx_err,
        selected_index=None,
        index_info=None,
        search_query='',
        fuzziness='AUTO',
        columns=None,
        rows=None,
        total_hits=0,
        search_error=None,
        agg_demos=es_svc.aggregation_demos(conn_id),
        agg_key=agg_key,
        agg_columns=agg_columns,
        agg_rows=agg_rows,
        agg_error=agg_error,
        builtin_queries=es_svc.builtin_queries(),
    )
