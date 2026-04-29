import io
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, jsonify, make_response, session,
)
from config import Config
from db import close_connection, test_connection
import services.query_service as qs
import services.ops_service as ops
import services.events_service as es
import services.analytics_service as analytics
import services.graph_service as gs
import services.ml_service as ml

app = Flask(__name__)
app.config.from_object(Config)
app.teardown_appcontext(close_connection)


# ── Home ──────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    ok, err = test_connection()
    summary = ops.get_home_summary() if ok else {}
    return render_template('home.html', connected=ok, conn_error=err, summary=summary)


# ── Query Studio ──────────────────────────────────────────────────────────────

@app.route('/query')
def query_studio():
    saved = qs.list_saved_queries()
    return render_template('query_studio.html', saved_queries=saved,
                           sql_text='', columns=None, rows=None,
                           elapsed_ms=None, error=None)


@app.route('/query/run', methods=['POST'])
def run_query():
    sql_text = request.form.get('sql_text', '').strip()
    isolation = request.form.get('isolation', 'READ COMMITTED')
    readonly = request.form.get('readonly', '1') == '1'
    export = request.form.get('export', '0') == '1'

    saved_id = request.form.get('saved_query_id', '')
    if saved_id:
        loaded_sql, loaded_ro = qs.get_saved_query(int(saved_id))
        if loaded_sql:
            sql_text = loaded_sql
            readonly = loaded_ro

    columns, rows, elapsed_ms, error = qs.run_user_query(sql_text, isolation, readonly)

    if export and columns and rows and not error:
        csv_data = qs.rows_to_csv(columns, rows)
        resp = make_response(csv_data)
        resp.headers['Content-Type'] = 'text/csv'
        resp.headers['Content-Disposition'] = 'attachment; filename=query_result.csv'
        return resp

    saved = qs.list_saved_queries()
    return render_template(
        'query_studio.html',
        saved_queries=saved,
        sql_text=sql_text,
        columns=columns,
        rows=rows,
        elapsed_ms=elapsed_ms,
        error=error,
        isolation=isolation,
        readonly=readonly,
    )


# ── Operations ────────────────────────────────────────────────────────────────

@app.route('/operations')
def operations():
    db_cols, db_rows, db_err = ops.get_db_sizes()
    bk_cols, bk_rows, bk_err = ops.get_recent_backups()
    jb_cols, jb_rows, jb_err = ops.get_job_status()
    rc_cols, rc_rows, rc_err = ops.get_row_counts()
    ls_cols, ls_rows, ls_err = ops.get_low_stock()
    return render_template(
        'operations.html',
        db=(db_cols, db_rows, db_err),
        backups=(bk_cols, bk_rows, bk_err),
        jobs=(jb_cols, jb_rows, jb_err),
        row_counts=(rc_cols, rc_rows, rc_err),
        low_stock=(ls_cols, ls_rows, ls_err),
    )


# ── Events (Loose Coupling Monitor) ───────────────────────────────────────────

@app.route('/events')
def events():
    summary, sum_err = es.get_event_summary()
    cols, rows, list_err = es.get_recent_events()
    return render_template(
        'events.html',
        summary=summary,
        summary_error=sum_err,
        columns=cols,
        rows=rows,
        list_error=list_err,
    )


@app.route('/events/process', methods=['POST'])
def process_events():
    err = es.process_pending()
    if err:
        flash(f'Error during processing: {err}', 'danger')
    else:
        flash('Pending events processed.', 'success')
    return redirect(url_for('events'))


@app.route('/events/retry/<int:event_id>', methods=['POST'])
def retry_event(event_id):
    err = es.retry_event(event_id)
    if err:
        flash(f'Retry failed: {err}', 'danger')
    else:
        flash(f'Event {event_id} reset to pending.', 'success')
    return redirect(url_for('events'))


# ── Analytics ─────────────────────────────────────────────────────────────────

@app.route('/analytics')
def analytics_page():
    return render_template('analytics.html')


@app.route('/analytics/data/<chart_name>')
def analytics_data(chart_name):
    dispatch = {
        'sales_by_month': analytics.get_sales_by_month,
        'sales_by_category': analytics.get_sales_by_category,
        'top_products': analytics.get_top_products,
        'orders_by_country': analytics.get_orders_by_country,
        'ship_status': analytics.get_ship_status,
    }
    fn = dispatch.get(chart_name)
    if not fn:
        return jsonify({'error': 'Unknown chart'}), 404
    return jsonify(fn())


# ── Graph Explorer ────────────────────────────────────────────────────────────

@app.route('/graph')
def graph_explorer():
    queries = gs.list_graph_queries()
    descs = {q['key']: q.get('description', '') for q in queries if q.get('key')}
    return render_template('graph.html', queries=queries, descs=descs,
                           selected=None, columns=None, rows=None, error=None)


@app.route('/graph/run', methods=['POST'])
def run_graph():
    query_key = request.form.get('query_key', '')
    columns, rows, error = gs.run_graph_query(query_key)
    queries = gs.list_graph_queries()
    descs = {q['key']: q.get('description', '') for q in queries if q.get('key')}
    selected = next((q for q in queries if q['key'] == query_key), None)
    return render_template(
        'graph.html',
        queries=queries,
        descs=descs,
        selected=selected,
        columns=columns,
        rows=rows,
        error=error,
    )


@app.route('/graph/data/<query_key>')
def graph_data(query_key):
    elements = gs.get_cytoscape_data(query_key)
    if elements is None:
        return jsonify({'error': 'No Cytoscape data available for this query.'}), 404
    return jsonify({'elements': elements})


# ── Insights / ML ────────────────────────────────────────────────────────────

@app.route('/insights')
def insights():
    tab = request.args.get('tab', 'predict')
    options, opts_err = ml.get_form_options()
    status = ml.model_status()
    return render_template(
        'insights.html',
        active_tab=tab,
        options=options,
        opts_err=opts_err,
        status=status,
        prediction=None,
        pred_error=None,
        risk_items=None, risk_summary=None, risk_error=None,
        anomalies=None, anom_summary=None, anom_error=None,
        sklearn_available=ml.sklearn_available(),
    )


@app.route('/insights/train', methods=['POST'])
def train_model():
    ok, err = ml.train_model()
    if ok:
        flash('Model trained successfully.', 'success')
    else:
        flash(f'Training failed: {err}', 'danger')
    return redirect(url_for('insights', tab='predict'))


@app.route('/insights/predict', methods=['POST'])
def predict_value():
    options, opts_err = ml.get_form_options()
    status = ml.model_status()

    category = request.form.get('category', '')
    country  = request.form.get('country', '')
    try:
        unit_price = float(request.form.get('unit_price', 0))
        discount   = float(request.form.get('discount', 0))
        year       = int(request.form.get('year', 1997))
    except ValueError:
        flash('Invalid numeric input.', 'danger')
        return redirect(url_for('insights', tab='predict'))

    prediction, pred_error = ml.predict_order_value(
        category, country, unit_price, discount, year
    )
    return render_template(
        'insights.html',
        active_tab='predict',
        options=options,
        opts_err=opts_err,
        status=status,
        prediction=prediction,
        pred_error=pred_error,
        last_form={'category': category, 'country': country,
                   'unit_price': unit_price, 'discount': discount, 'year': year},
        risk_items=None, risk_summary=None, risk_error=None,
        anomalies=None, anom_summary=None, anom_error=None,
        sklearn_available=ml.sklearn_available(),
    )


@app.route('/insights/inventory-risk')
def inventory_risk():
    options, opts_err = ml.get_form_options()
    status = ml.model_status()
    risk_items, risk_error = ml.get_inventory_risk()
    rsummary = ml.risk_summary(risk_items) if risk_items else {}
    return render_template(
        'insights.html',
        active_tab='risk',
        options=options,
        opts_err=opts_err,
        status=status,
        prediction=None, pred_error=None,
        risk_items=risk_items,
        risk_summary=rsummary,
        risk_error=risk_error,
        anomalies=None, anom_summary=None, anom_error=None,
        sklearn_available=ml.sklearn_available(),
    )


@app.route('/insights/anomalies')
def anomalies():
    options, opts_err = ml.get_form_options()
    status = ml.model_status()
    anom_list, anom_error = ml.get_anomalies()
    asummary = ml.anomaly_summary(anom_list) if anom_list else {}
    return render_template(
        'insights.html',
        active_tab='anomalies',
        options=options,
        opts_err=opts_err,
        status=status,
        prediction=None, pred_error=None,
        risk_items=None, risk_summary=None, risk_error=None,
        anomalies=anom_list,
        anom_summary=asummary,
        anom_error=anom_error,
        sklearn_available=ml.sklearn_available(),
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
