from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import meta_db
import services.redis_service as rs
from auth import login_required, admin_required

redis_bp = Blueprint('redis_bp', __name__, url_prefix='/redis')


@redis_bp.route('/')
@login_required
def index():
    conns = [c for c in meta_db.list_connections() if c['db_type'] == 'redis']
    conn_id = request.args.get('conn_id', type=int)
    info, info_err = {}, None
    keys, keys_err = [], None
    pattern = request.args.get('pattern', '*')

    if conn_id:
        info, info_err = rs.get_server_info(conn_id)
        keys, keys_err = rs.scan_keys(conn_id, pattern)

    return render_template('redis/index.html',
        conns=conns, conn_id=conn_id,
        info=info, info_err=info_err,
        keys=keys, keys_err=keys_err,
        pattern=pattern,
        selected_key=None, value=None, value_type=None, value_err=None,
        demo_queries=rs.demo_queries(), cache_result=None,
    )


@redis_bp.route('/<int:conn_id>/get')
@login_required
def get_key(conn_id):
    key = request.args.get('key', '')
    pattern = request.args.get('pattern', '*')
    conns = [c for c in meta_db.list_connections() if c['db_type'] == 'redis']
    info, info_err = rs.get_server_info(conn_id)
    keys, keys_err = rs.scan_keys(conn_id, pattern)
    value, value_type, value_err = rs.get_value(conn_id, key) if key else (None, None, None)
    return render_template('redis/index.html',
        conns=conns, conn_id=conn_id,
        info=info, info_err=info_err,
        keys=keys, keys_err=keys_err,
        pattern=pattern,
        selected_key=key, value=value, value_type=value_type, value_err=value_err,
        demo_queries=rs.demo_queries(), cache_result=None,
    )


@redis_bp.route('/<int:conn_id>/set', methods=['POST'])
@admin_required
def set_key(conn_id):
    key = request.form.get('key', '').strip()
    value = request.form.get('value', '')
    ttl = request.form.get('ttl', '0', type=str)
    try:
        ttl_int = int(ttl)
    except ValueError:
        ttl_int = 0
    err = rs.set_value(conn_id, key, value, ttl_int or None)
    if err:
        flash(f'Set failed: {err}', 'danger')
    else:
        flash(f'Key "{key}" set.', 'success')
    return redirect(url_for('redis_bp.get_key', conn_id=conn_id, key=key))


@redis_bp.route('/<int:conn_id>/delete', methods=['POST'])
@admin_required
def delete_key(conn_id):
    key = request.form.get('key', '')
    err = rs.delete_key(conn_id, key)
    if err:
        flash(f'Delete failed: {err}', 'danger')
    else:
        flash(f'Key "{key}" deleted.', 'success')
    return redirect(url_for('redis_bp.index', conn_id=conn_id))


@redis_bp.route('/<int:conn_id>/flush', methods=['POST'])
@admin_required
def flush(conn_id):
    err = rs.flush_db(conn_id)
    if err:
        flash(f'Flush failed: {err}', 'danger')
    else:
        flash('Database flushed.', 'success')
    return redirect(url_for('redis_bp.index', conn_id=conn_id))


@redis_bp.route('/<int:conn_id>/cache', methods=['POST'])
@login_required
def cache_demo(conn_id):
    query_key = request.form.get('query_key', '')
    ttl = int(request.form.get('ttl', 60))
    conns = [c for c in meta_db.list_connections() if c['db_type'] == 'redis']
    info, info_err = rs.get_server_info(conn_id)
    keys, keys_err = rs.scan_keys(conn_id, 'nwcc:*')
    cache_result = rs.run_cached_query(conn_id, query_key, ttl)
    return render_template('redis/index.html',
        conns=conns, conn_id=conn_id,
        info=info, info_err=info_err,
        keys=keys, keys_err=keys_err,
        pattern='nwcc:*',
        selected_key=None, value=None, value_type=None, value_err=None,
        demo_queries=rs.demo_queries(), cache_result=cache_result,
    )


# ── Benchmark ─────────────────────────────────────────────────────────────────

@redis_bp.route('/<int:conn_id>/benchmark')
@login_required
def benchmark(conn_id):
    rec = meta_db.get_connection_by_id(conn_id)
    if not rec:
        flash('Connection not found.', 'danger')
        return redirect(url_for('redis_bp.index'))
    all_conns = [c for c in meta_db.list_connections()
                 if c['db_type'] not in ('redis', 'rqlite', 'elasticsearch')]
    return render_template('redis/benchmark.html', conn=rec,
                           all_conns=all_conns,
                           result=None, sql_text='', sql_conn_id=None)


@redis_bp.route('/<int:conn_id>/benchmark/run', methods=['POST'])
@login_required
def benchmark_run(conn_id):
    sql_conn_id = request.form.get('sql_conn_id', type=int)
    sql = request.form.get('sql', '').strip()
    cache_ttl = request.form.get('cache_ttl', 60, type=int)
    rec = meta_db.get_connection_by_id(conn_id)
    all_conns = [c for c in meta_db.list_connections()
                 if c['db_type'] not in ('redis', 'rqlite', 'elasticsearch')]
    result = None
    if sql and sql_conn_id:
        result = rs.benchmark_query(sql_conn_id, conn_id, sql, cache_ttl)
    return render_template('redis/benchmark.html', conn=rec,
                           all_conns=all_conns,
                           result=result, sql_text=sql, sql_conn_id=sql_conn_id)


@redis_bp.route('/<int:conn_id>/benchmark/clear', methods=['POST'])
@login_required
def benchmark_clear(conn_id):
    n = rs.clear_benchmark_cache(conn_id)
    flash(f'Cleared {n} cached benchmark key(s).', 'success')
    return redirect(url_for('redis_bp.benchmark', conn_id=conn_id))
