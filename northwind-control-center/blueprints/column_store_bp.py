from flask import Blueprint, render_template, request, redirect, url_for, flash, session

import meta_db
from auth import login_required
from services import column_store_service as cs

column_store = Blueprint('column_store', __name__, url_prefix='/column-store')


def _session_key():
    return str(session.get('user_id', 'anon'))


@column_store.route('/')
@login_required
def index():
    sk = _session_key()
    stats = cs.get_store_stats(sk)
    connections = meta_db.list_connections()
    return render_template('column_store/index.html',
                           stats=stats,
                           connections=connections,
                           agg_labels=cs.AGGREGATION_LABELS,
                           result=None, agg_type=None)


@column_store.route('/load', methods=['POST'])
@login_required
def load():
    conn_id = int(request.form.get('conn_id', 0))
    if not conn_id:
        flash('Select a source connection.', 'danger')
        return redirect(url_for('column_store.index'))
    ok, err = cs.load_northwind_into_store(_session_key(), conn_id)
    if ok:
        flash('Northwind data loaded into in-memory column store.', 'success')
    else:
        flash(f'Load failed: {err}', 'danger')
    return redirect(url_for('column_store.index'))


@column_store.route('/query/<agg_type>')
@login_required
def query(agg_type):
    sk = _session_key()
    stats = cs.get_store_stats(sk)
    if not stats['loaded']:
        flash('Load data into the store first.', 'warning')
        return redirect(url_for('column_store.index'))

    cols, rows, err = cs.run_column_aggregation(sk, agg_type)
    connections = meta_db.list_connections()
    return render_template('column_store/index.html',
                           stats=stats,
                           connections=connections,
                           agg_labels=cs.AGGREGATION_LABELS,
                           result={'cols': cols, 'rows': rows, 'error': err},
                           agg_type=agg_type)


@column_store.route('/reset', methods=['POST'])
@login_required
def reset():
    cs.destroy_store(_session_key())
    flash('Column store cleared.', 'success')
    return redirect(url_for('column_store.index'))
