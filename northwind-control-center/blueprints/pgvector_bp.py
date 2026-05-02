"""
pgvector_bp.py — Flask blueprint for pgvector semantic similarity search demo.

Blueprint name : pgvector
URL prefix     : /pgvector
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

import meta_db
from auth import login_required
from services import pgvector_service as pv

pgvector_bp = Blueprint('pgvector', __name__, url_prefix='/pgvector')


# ── Helpers ───────────────────────────────────────────────────────────────────

def _pg_conns():
    """Return only PostgreSQL-type connections."""
    return [c for c in meta_db.list_connections() if c['db_type'] == 'postgresql']


# ── Index ─────────────────────────────────────────────────────────────────────

@pgvector_bp.route('/')
@login_required
def index():
    pg_conns  = _pg_conns()
    all_conns = meta_db.list_connections()

    conn_id = request.args.get('conn_id', type=int)
    if not conn_id and pg_conns:
        conn_id = pg_conns[0]['id']

    stats = {}
    if conn_id:
        stats = pv.get_stats(conn_id)

    return render_template(
        'pgvector/index.html',
        pg_conns=pg_conns,
        all_conns=all_conns,
        selected_conn_id=conn_id,
        stats=stats,
        search_results=None,
        search_query='',
        search_k=10,
        compare=None,
    )


# ── Setup ─────────────────────────────────────────────────────────────────────

@pgvector_bp.route('/<int:conn_id>/setup', methods=['POST'])
@login_required
def setup(conn_id):
    err = pv.ensure_pgvector(conn_id)
    if err:
        flash(f'Failed to enable pgvector extension: {err}', 'danger')
        return redirect(url_for('pgvector.index', conn_id=conn_id))

    err = pv.setup_embeddings_table(conn_id)
    if err:
        flash(f'Failed to create embeddings table: {err}', 'danger')
    else:
        flash(
            'pgvector extension enabled and product_embeddings table created.',
            'success',
        )

    return redirect(url_for('pgvector.index', conn_id=conn_id))


# ── Import ────────────────────────────────────────────────────────────────────

@pgvector_bp.route('/<int:conn_id>/import', methods=['POST'])
@login_required
def import_products(conn_id):
    source_conn_id = request.form.get('source_conn_id', type=int)
    if not source_conn_id:
        flash('Select a source connection that contains the Northwind data.', 'danger')
        return redirect(url_for('pgvector.index', conn_id=conn_id))

    count, err = pv.import_products(conn_id, source_conn_id)
    if err:
        flash(f'Import failed: {err}', 'danger')
    else:
        flash(
            f'Successfully imported {count} products with {pv.VECTOR_DIM}-dim TF-IDF embeddings.',
            'success',
        )

    return redirect(url_for('pgvector.index', conn_id=conn_id))


# ── Search ────────────────────────────────────────────────────────────────────

@pgvector_bp.route('/<int:conn_id>/search', methods=['POST'])
@login_required
def search(conn_id):
    query_text = request.form.get('query_text', '').strip()
    k          = request.form.get('k', 10, type=int)
    k          = max(1, min(k, 50))

    pg_conns  = _pg_conns()
    all_conns = meta_db.list_connections()
    stats     = pv.get_stats(conn_id)

    if not query_text:
        flash('Enter a search query.', 'warning')
        return render_template(
            'pgvector/index.html',
            pg_conns=pg_conns,
            all_conns=all_conns,
            selected_conn_id=conn_id,
            stats=stats,
            search_results=None,
            search_query='',
            search_k=k,
            compare=None,
        )

    columns, rows, err = pv.similarity_search(conn_id, query_text, k=k)
    if err:
        flash(f'Search failed: {err}', 'danger')

    return render_template(
        'pgvector/index.html',
        pg_conns=pg_conns,
        all_conns=all_conns,
        selected_conn_id=conn_id,
        stats=stats,
        search_results={'columns': columns, 'rows': rows, 'error': err},
        search_query=query_text,
        search_k=k,
        compare=None,
    )


# ── Compare ───────────────────────────────────────────────────────────────────

@pgvector_bp.route('/<int:conn_id>/compare', methods=['POST'])
@login_required
def compare(conn_id):
    query_text     = request.form.get('query_text', '').strip()
    source_conn_id = request.form.get('source_conn_id', type=int)

    pg_conns  = _pg_conns()
    all_conns = meta_db.list_connections()
    stats     = pv.get_stats(conn_id)

    if not query_text or not source_conn_id:
        flash(
            'Enter a query and select a source connection for comparison.',
            'warning',
        )
        return render_template(
            'pgvector/index.html',
            pg_conns=pg_conns,
            all_conns=all_conns,
            selected_conn_id=conn_id,
            stats=stats,
            search_results=None,
            search_query=query_text,
            search_k=10,
            compare=None,
        )

    vec_cols, vec_rows, vec_err   = pv.similarity_search(conn_id, query_text, k=10)
    sql_cols, sql_rows, sql_err   = pv.sql_like_search(conn_id, source_conn_id, query_text)

    if sql_err:
        flash(f'SQL LIKE search error: {sql_err}', 'warning')
    if vec_err:
        flash(f'Vector search error: {vec_err}', 'warning')

    compare_result = {
        'query':        query_text,
        'vector':       (vec_cols, vec_rows),
        'sql_like':     (sql_cols, sql_rows),
        'vector_error': vec_err,
        'sql_error':    sql_err,
    }

    return render_template(
        'pgvector/index.html',
        pg_conns=pg_conns,
        all_conns=all_conns,
        selected_conn_id=conn_id,
        stats=stats,
        search_results=None,
        search_query=query_text,
        search_k=10,
        compare=compare_result,
    )
