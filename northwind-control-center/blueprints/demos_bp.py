"""
demos_bp.py — Visual Demo Lab blueprint.
"""
import json
import os
from flask import Blueprint, render_template, request, jsonify, current_app, Response
from auth import login_required
import meta_db
from services import demo_service
from services import graph_routing_service as grs
from services import graph_pagerank_service as gprs
from services import graph_lab_service as gl
from services import mapreduce_service as mrs
from services import pubsub_service as pss
from services import stream_service as sts
from services import cloud_functions_service as cfs
from services import batch_analytics_service as bas
from services import vm_service as vms
from services import montecarlo_service as mcs
from services import bigtable_service as bts
from services import rpc_service as rpcs
from services import microbatch_service as mbs
from services import kafka_service as kfs
from services import wordcount_service as wcs

demos_bp = Blueprint("demos", __name__, url_prefix="/demos")


def _conns_by_type(db_type):
    return [c for c in meta_db.list_connections() if c["db_type"] == db_type]


# ── Index ──────────────────────────────────────────────────────────────────────

@demos_bp.route("/")
@login_required
def index():
    sqlite_conns = _conns_by_type("sqlite")
    pg_conns = _conns_by_type("postgresql")
    return render_template("demos/index.html",
                           sqlite_conns=sqlite_conns, pg_conns=pg_conns)


# ── ACID Bank Transfer ─────────────────────────────────────────────────────────

@demos_bp.route("/acid")
@login_required
def acid():
    sqlite_conns = _conns_by_type("sqlite")
    return render_template("demos/acid.html", sqlite_conns=sqlite_conns)


@demos_bp.route("/acid/run", methods=["POST"])
@login_required
def acid_run():
    conn_id = int(request.form.get("conn_id", 0))
    from_id = int(request.form.get("from_id", 1))
    to_id = int(request.form.get("to_id", 2))
    amount = float(request.form.get("amount", 100))
    force_fail = request.form.get("force_fail") in ("on", "true", "1", "yes")
    result = demo_service.bank_transfer(conn_id, from_id, to_id, amount, force_fail)
    return jsonify(result)


@demos_bp.route("/acid/accounts")
@login_required
def acid_accounts():
    conn_id = int(request.args.get("conn_id", 0))
    accounts = demo_service.get_accounts(conn_id)
    return jsonify(accounts)


# ── Deadlock ───────────────────────────────────────────────────────────────────

@demos_bp.route("/deadlock")
@login_required
def deadlock():
    pg_conns = _conns_by_type("postgresql")
    return render_template("demos/deadlock.html", pg_conns=pg_conns)


@demos_bp.route("/deadlock/run", methods=["POST"])
@login_required
def deadlock_run():
    conn_id = int(request.form.get("conn_id", 0))
    try:
        result = demo_service.create_deadlock_scenario(conn_id)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Trigger Chain ──────────────────────────────────────────────────────────────

@demos_bp.route("/trigger-chain")
@login_required
def trigger_chain():
    sqlite_conns = _conns_by_type("sqlite")
    return render_template("demos/trigger_chain.html", sqlite_conns=sqlite_conns)


@demos_bp.route("/trigger-chain/insert", methods=["POST"])
@login_required
def trigger_chain_insert():
    conn_id = int(request.form.get("conn_id", 0))
    product = request.form.get("product", "Widget")
    qty = int(request.form.get("qty", 1))
    result = demo_service.insert_demo_order(conn_id, product, qty)
    return jsonify(result)


@demos_bp.route("/trigger-chain/data")
@login_required
def trigger_chain_data():
    conn_id = int(request.args.get("conn_id", 0))
    data = demo_service.get_trigger_chain_data(conn_id)
    return jsonify(data)


# ── Log Shipping ───────────────────────────────────────────────────────────────

@demos_bp.route("/log-shipping")
@login_required
def log_shipping():
    return render_template("demos/log_shipping.html")


@demos_bp.route("/log-shipping/state")
@login_required
def log_shipping_state():
    return jsonify(demo_service.ls_get_state())


@demos_bp.route("/log-shipping/start", methods=["POST"])
@login_required
def log_shipping_start():
    demo_service.ls_start()
    return jsonify({'ok': True})


# ── Snapshot Replication ───────────────────────────────────────────────────────

@demos_bp.route("/snapshot")
@login_required
def snapshot():
    return render_template("demos/snapshot.html")


@demos_bp.route("/snapshot/state")
@login_required
def snapshot_state():
    return jsonify(demo_service.ss_get_state())


@demos_bp.route("/snapshot/start", methods=["POST"])
@login_required
def snapshot_start():
    demo_service.ss_start()
    return jsonify({'ok': True})


# ── Transactional Replication ──────────────────────────────────────────────────

@demos_bp.route("/transactional")
@login_required
def transactional():
    return render_template("demos/transactional.html")


@demos_bp.route("/transactional/state")
@login_required
def transactional_state():
    return jsonify(demo_service.tr_get_state())


@demos_bp.route("/transactional/start", methods=["POST"])
@login_required
def transactional_start():
    demo_service.tr_start()
    return jsonify({'ok': True})


@demos_bp.route("/transactional/stop", methods=["POST"])
@login_required
def transactional_stop():
    demo_service.tr_stop()
    return jsonify({'ok': True})


# ── Merge Replication ──────────────────────────────────────────────────────────

@demos_bp.route("/merge-replication")
@login_required
def merge_replication():
    return render_template("demos/merge_replication.html")


@demos_bp.route("/merge-replication/state")
@login_required
def merge_replication_state():
    return jsonify(demo_service.mr_get_state())


@demos_bp.route("/merge-replication/start", methods=["POST"])
@login_required
def merge_replication_start():
    demo_service.mr_start()
    return jsonify({'ok': True})


@demos_bp.route("/merge-replication/stop", methods=["POST"])
@login_required
def merge_replication_stop():
    demo_service.mr_stop()
    return jsonify({'ok': True})


# ── Blockchain Demo ────────────────────────────────────────────────────────────

@demos_bp.route("/blockchain")
@login_required
def blockchain():
    return render_template("demos/blockchain.html")


@demos_bp.route("/blockchain/state")
@login_required
def blockchain_state():
    return jsonify(demo_service.bc_get_state())


@demos_bp.route("/blockchain/start", methods=["POST"])
@login_required
def blockchain_start():
    demo_service.bc_start()
    return jsonify({'ok': True})


@demos_bp.route("/blockchain/stop", methods=["POST"])
@login_required
def blockchain_stop():
    demo_service.bc_stop()
    return jsonify({'ok': True})


# ── Crypto Exchange ────────────────────────────────────────────────────────────

@demos_bp.route("/crypto-exchange")
@login_required
def crypto_exchange():
    return render_template("demos/crypto_exchange.html")


@demos_bp.route("/crypto-exchange/state")
@login_required
def crypto_exchange_state():
    return jsonify(demo_service.ce_get_state())


@demos_bp.route("/crypto-exchange/start", methods=["POST"])
@login_required
def crypto_exchange_start():
    demo_service.ce_start()
    return jsonify({'ok': True})


@demos_bp.route("/crypto-exchange/stop", methods=["POST"])
@login_required
def crypto_exchange_stop():
    demo_service.ce_stop()
    return jsonify({'ok': True})


# ── NASDAQ ─────────────────────────────────────────────────────────────────────

@demos_bp.route("/nasdaq")
@login_required
def nasdaq():
    return render_template("demos/nasdaq.html")


@demos_bp.route("/nasdaq/state")
@login_required
def nasdaq_state():
    return jsonify(demo_service.nq_get_state())


@demos_bp.route("/nasdaq/start", methods=["POST"])
@login_required
def nasdaq_start():
    demo_service.nq_start()
    return jsonify({'ok': True})


@demos_bp.route("/nasdaq/stop", methods=["POST"])
@login_required
def nasdaq_stop():
    demo_service.nq_stop()
    return jsonify({'ok': True})


# ── NYSE ───────────────────────────────────────────────────────────────────────

@demos_bp.route("/nyse")
@login_required
def nyse():
    return render_template("demos/nyse.html")


@demos_bp.route("/nyse/state")
@login_required
def nyse_state():
    return jsonify(demo_service.ny_get_state())


@demos_bp.route("/nyse/start", methods=["POST"])
@login_required
def nyse_start():
    demo_service.ny_start()
    return jsonify({'ok': True})


@demos_bp.route("/nyse/stop", methods=["POST"])
@login_required
def nyse_stop():
    demo_service.ny_stop()
    return jsonify({'ok': True})


@demos_bp.route("/nyse/flash-crash", methods=["POST"])
@login_required
def nyse_flash_crash():
    demo_service.ny_flash_crash()
    return jsonify({'ok': True})


# ── HFT ────────────────────────────────────────────────────────────────────────

@demos_bp.route("/hft")
@login_required
def hft():
    return render_template("demos/hft.html")


@demos_bp.route("/hft/state")
@login_required
def hft_state():
    return jsonify(demo_service.hft_get_state())


@demos_bp.route("/hft/trigger", methods=["POST"])
@login_required
def hft_trigger():
    network = request.form.get("network", "microwave")
    setup   = request.form.get("setup",   "cloud")
    result  = demo_service.hft_trigger(network, setup)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)


@demos_bp.route("/hft/reset", methods=["POST"])
@login_required
def hft_reset():
    demo_service.hft_reset()
    return jsonify({'ok': True})


# ── Order Fulfillment ──────────────────────────────────────────────────────────

def _build_conn_str(c):
    # SA credentials and target database come from os.environ (.env) as the
    # authoritative source — the Settings UI / startup fallback can overwrite
    # app.config (and meta_db) with 'master', but the .env always has Northwind.
    user = (c.get('SQL_SA_USERNAME')
            or os.environ.get('SQL_SA_USERNAME')
            or c.get('SQL_USERNAME', ''))
    pw   = (c.get('SQL_SA_PASSWORD')
            or os.environ.get('SQL_SA_PASSWORD')
            or c.get('SQL_PASSWORD', ''))
    db   = os.environ.get('SQL_DATABASE') or c.get('SQL_DATABASE', 'Northwind')
    return (
        f"DRIVER={{{c['SQL_DRIVER']}}};SERVER={c['SQL_SERVER']};"
        f"DATABASE={db};UID={user};PWD={pw};"
        f"Encrypt={c['SQL_ENCRYPT']};TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )


@demos_bp.route('/fulfill')
@login_required
def fulfill():
    return render_template('demos/fulfill.html')


@demos_bp.route('/fulfill/state')
@login_required
def fulfill_state():
    return Response(
        json.dumps(demo_service.fulfill_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/fulfill/start', methods=['POST'])
@login_required
def fulfill_start():
    demo_service.fulfill_start(_build_conn_str(current_app.config))
    return jsonify({'ok': True})


@demos_bp.route('/fulfill/reset', methods=['POST'])
@login_required
def fulfill_reset():
    demo_service.fulfill_reset()
    return jsonify({'ok': True})


@demos_bp.route('/fulfill/step', methods=['POST'])
@login_required
def fulfill_step():
    demo_service.fulfill_step()
    return jsonify({'ok': True})


# ── Graph Routing ──────────────────────────────────────────────────────────────

@demos_bp.route('/graph_routing')
@login_required
def graph_routing_page():
    return render_template('demos/graph_routing.html')


@demos_bp.route('/graph_routing/state')
@login_required
def graph_routing_state():
    return Response(
        json.dumps(grs.graph_routing_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/graph_routing/start', methods=['POST'])
@login_required
def graph_routing_start():
    data     = request.json or {}
    start    = data.get('start', 'Paris')
    end      = data.get('end', 'Berlin')
    conn_str = _build_conn_str(current_app.config)
    grs.graph_routing_start(conn_str, start, end)
    return jsonify({'ok': True})


@demos_bp.route('/graph_routing/step', methods=['POST'])
@login_required
def graph_routing_step():
    grs.graph_routing_step()
    return jsonify({'ok': True})


@demos_bp.route('/graph_routing/reset', methods=['POST'])
@login_required
def graph_routing_reset():
    conn_str = _build_conn_str(current_app.config)
    grs.graph_routing_reset(conn_str)
    return jsonify({'ok': True})


@demos_bp.route('/graph_routing/cities')
@login_required
def graph_routing_cities():
    conn_str = _build_conn_str(current_app.config)
    return jsonify(grs.graph_routing_cities(conn_str))


@demos_bp.route('/graph_routing/fast', methods=['POST'])
@login_required
def graph_routing_fast():
    data     = request.json or {}
    start    = data.get('start', '')
    end      = data.get('end', '')
    conn_str = _build_conn_str(current_app.config)
    result   = grs.get_instant_route(conn_str, start, end)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)


# ── Graph Algorithm Laboratory ────────────────────────────────────────────────

@demos_bp.route('/graph_lab')
@login_required
def graph_lab_page():
    return render_template('demos/graph_lab.html')


@demos_bp.route('/graph_lab/algorithms')
@login_required
def graph_lab_algorithms():
    """Return problem → algorithm registry for the frontend dual-dropdown."""
    return jsonify(gl.get_registry())


@demos_bp.route('/graph_lab/solve', methods=['POST'])
@login_required
def graph_lab_solve():
    data      = request.json or {}
    problem   = data.get('problem', 'nav')
    algorithm = data.get('algorithm', 'astar')
    src       = data.get('src', '')
    dst       = data.get('dst', '')
    params    = data.get('params', {})
    conn_str  = _build_conn_str(current_app.config)
    result    = gl.solve(conn_str, problem, algorithm, src, dst, params=params)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)


# ── Graph PageRank ─────────────────────────────────────────────────────────────

@demos_bp.route('/graph_pagerank')
@login_required
def graph_pagerank_page():
    return render_template('demos/graph_pagerank.html')


@demos_bp.route('/graph_pagerank/data')
@login_required
def graph_pagerank_data():
    try:
        conn_str = _build_conn_str(current_app.config)
        return jsonify(gprs.get_pagerank_data(conn_str))
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


# ── MapReduce Batch Processing ─────────────────────────────────────────────────

@demos_bp.route('/mapreduce')
@login_required
def mapreduce_page():
    return render_template('demos/mapreduce.html')


@demos_bp.route('/mapreduce/run', methods=['POST'])
@login_required
def mapreduce_run():
    mrs.mr_start(_build_conn_str(current_app.config))
    return jsonify({'ok': True})


@demos_bp.route('/mapreduce/state')
@login_required
def mapreduce_state():
    return Response(
        json.dumps(mrs.mr_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/mapreduce/reset', methods=['POST'])
@login_required
def mapreduce_reset():
    mrs.mr_reset()
    return jsonify({'ok': True})


# ── Cloud Pub/Sub ──────────────────────────────────────────────────────────────

@demos_bp.route('/pubsub')
@login_required
def pubsub_page():
    return render_template('demos/pubsub.html')


@demos_bp.route('/pubsub/run', methods=['POST'])
@login_required
def pubsub_run():
    pss.ps_start(_build_conn_str(current_app.config))
    return jsonify({'ok': True})


@demos_bp.route('/pubsub/state')
@login_required
def pubsub_state():
    return Response(
        json.dumps(pss.ps_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/pubsub/reset', methods=['POST'])
@login_required
def pubsub_reset():
    pss.ps_reset()
    return jsonify({'ok': True})


# ── Data Stream Processing ────────────────────────────────────────────────────

@demos_bp.route('/stream')
@login_required
def stream_page():
    return render_template('demos/stream.html')


@demos_bp.route('/stream/start', methods=['POST'])
@login_required
def stream_start():
    sts.st_start()
    return jsonify({'ok': True})


@demos_bp.route('/stream/stop', methods=['POST'])
@login_required
def stream_stop():
    sts.st_stop()
    return jsonify({'ok': True})


@demos_bp.route('/stream/state')
@login_required
def stream_state():
    return Response(
        json.dumps(sts.st_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/stream/reset', methods=['POST'])
@login_required
def stream_reset():
    sts.st_reset()
    return jsonify({'ok': True})


# ── Cloud Functions ───────────────────────────────────────────────────────────

@demos_bp.route('/cloud_functions')
@login_required
def cloud_functions_page():
    return render_template('demos/cloud_functions.html')


@demos_bp.route('/cloud_functions/invoke', methods=['POST'])
@login_required
def cloud_functions_invoke():
    data    = request.json or {}
    fn_key  = data.get('fn_key', '')
    payload = data.get('payload', {})
    result  = cfs.cf_invoke(fn_key, payload)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)


@demos_bp.route('/cloud_functions/state')
@login_required
def cloud_functions_state():
    return Response(
        json.dumps(cfs.cf_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/cloud_functions/reset', methods=['POST'])
@login_required
def cloud_functions_reset():
    cfs.cf_reset()
    return jsonify({'ok': True})


# ── Batch Analytics ───────────────────────────────────────────────────────────

@demos_bp.route('/batch_analytics')
@login_required
def batch_analytics_page():
    return render_template('demos/batch_analytics.html')


@demos_bp.route('/batch_analytics/run', methods=['POST'])
@login_required
def batch_analytics_run():
    result = bas.ba_run(_build_conn_str(current_app.config))
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result)


# ── VM Lifecycle ──────────────────────────────────────────────────────────────

@demos_bp.route('/vm_lifecycle')
@login_required
def vm_lifecycle_page():
    vms.vm_start_cost_ticker()
    return render_template('demos/vm_lifecycle.html')


@demos_bp.route('/vm_lifecycle/state')
@login_required
def vm_lifecycle_state():
    return Response(
        json.dumps(vms.vm_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/vm_lifecycle/transition', methods=['POST'])
@login_required
def vm_lifecycle_transition():
    data   = request.json or {}
    target = data.get('target', '')
    result = vms.vm_transition(target)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)


@demos_bp.route('/vm_lifecycle/reset', methods=['POST'])
@login_required
def vm_lifecycle_reset():
    vms.vm_reset()
    return jsonify({'ok': True})


# ── Monte Carlo π ─────────────────────────────────────────────────────────────

@demos_bp.route('/montecarlo')
@login_required
def montecarlo_page():
    return render_template('demos/montecarlo.html')


@demos_bp.route('/montecarlo/start', methods=['POST'])
@login_required
def montecarlo_start():
    data = request.json or {}
    n    = max(1, min(16, int(data.get('n_workers', 4))))
    mcs.mc_start(n)
    return jsonify({'ok': True})


@demos_bp.route('/montecarlo/stop', methods=['POST'])
@login_required
def montecarlo_stop():
    mcs.mc_stop()
    return jsonify({'ok': True})


@demos_bp.route('/montecarlo/state')
@login_required
def montecarlo_state():
    return Response(
        json.dumps(mcs.mc_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/montecarlo/reset', methods=['POST'])
@login_required
def montecarlo_reset():
    mcs.mc_reset()
    return jsonify({'ok': True})


# ── Bigtable Wide-Column Store ────────────────────────────────────────────────

@demos_bp.route('/bigtable')
@login_required
def bigtable_page():
    return render_template('demos/bigtable.html')


@demos_bp.route('/bigtable/insert', methods=['POST'])
@login_required
def bigtable_insert():
    ping = request.json or {}
    row_key = bts.bt_insert_ping(ping)
    return jsonify({'ok': True, 'row_key': row_key})


@demos_bp.route('/bigtable/read', methods=['GET'])
@login_required
def bigtable_read():
    rk = request.args.get('row_key', '')
    return jsonify(bts.bt_read_row(rk) or {'error': 'not found'})


@demos_bp.route('/bigtable/versions', methods=['GET'])
@login_required
def bigtable_versions():
    rk  = request.args.get('row_key', '')
    cf  = request.args.get('cf', 'sensor')
    col = request.args.get('col', 'speed')
    return jsonify(bts.bt_get_versions(rk, cf, col))


@demos_bp.route('/bigtable/scan', methods=['GET'])
@login_required
def bigtable_scan():
    prefix = request.args.get('prefix', '')
    return jsonify(bts.bt_range_scan(prefix))


@demos_bp.route('/bigtable/state')
@login_required
def bigtable_state():
    return Response(
        json.dumps(bts.bt_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/bigtable/reset', methods=['POST'])
@login_required
def bigtable_reset():
    bts.bt_reset()
    return jsonify({'ok': True})


# ── RPC → REST Evolution ──────────────────────────────────────────────────────

@demos_bp.route('/rpc')
@login_required
def rpc_page():
    return render_template('demos/rpc.html')


@demos_bp.route('/rpc/invoke', methods=['POST'])
@login_required
def rpc_invoke():
    data     = request.json or {}
    order_id = int(data.get('order_id', 10248))
    return jsonify(rpcs.rpc_invoke(order_id))


# ── Micro-Batch vs True Stream ────────────────────────────────────────────────

@demos_bp.route('/microbatch')
@login_required
def microbatch_page():
    return render_template('demos/microbatch.html')


@demos_bp.route('/microbatch/start', methods=['POST'])
@login_required
def microbatch_start():
    data     = request.json or {}
    window_s = int(data.get('window_s', 1))
    mbs.mb_start(window_s)
    return jsonify({'ok': True})


@demos_bp.route('/microbatch/stop', methods=['POST'])
@login_required
def microbatch_stop():
    mbs.mb_stop()
    return jsonify({'ok': True})


@demos_bp.route('/microbatch/state')
@login_required
def microbatch_state():
    return Response(
        json.dumps(mbs.mb_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/microbatch/reset', methods=['POST'])
@login_required
def microbatch_reset():
    mbs.mb_reset()
    return jsonify({'ok': True})


# ── Kafka Consumer Groups ─────────────────────────────────────────────────────

@demos_bp.route('/kafka')
@login_required
def kafka_page():
    return render_template('demos/kafka.html')


@demos_bp.route('/kafka/start', methods=['POST'])
@login_required
def kafka_start():
    kfs.kafka_start(_build_conn_str(current_app.config))
    return jsonify({'ok': True})


@demos_bp.route('/kafka/state')
@login_required
def kafka_state():
    return Response(
        json.dumps(kfs.kafka_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/kafka/reset', methods=['POST'])
@login_required
def kafka_reset():
    kfs.kafka_reset()
    return jsonify({'ok': True})


# ── Word Count MapReduce ───────────────────────────────────────────────────────

@demos_bp.route('/wordcount')
@login_required
def wordcount_page():
    return render_template('demos/wordcount.html')


@demos_bp.route('/wordcount/run', methods=['POST'])
@login_required
def wordcount_run():
    wcs.wc_start(_build_conn_str(current_app.config))
    return jsonify({'ok': True})


@demos_bp.route('/wordcount/state')
@login_required
def wordcount_state():
    return Response(
        json.dumps(wcs.wc_get_state(), default=str),
        mimetype='application/json',
    )


@demos_bp.route('/wordcount/reset', methods=['POST'])
@login_required
def wordcount_reset():
    wcs.wc_reset()
    return jsonify({'ok': True})


# ── Storage Tiers ─────────────────────────────────────────────────────────────

@demos_bp.route('/storage_tiers')
@login_required
def storage_tiers_page():
    return render_template('demos/storage_tiers.html')


# ── Cloud Cost Calculator ─────────────────────────────────────────────────────

@demos_bp.route('/cloud_cost')
@login_required
def cloud_cost_page():
    return render_template('demos/cloud_cost.html')


# ── Apache Beam Portable Pipeline ─────────────────────────────────────────────

@demos_bp.route('/beam')
@login_required
def beam_page():
    return render_template('demos/beam.html')


# ── Geographic Latency / CDN Edge ─────────────────────────────────────────────

@demos_bp.route('/geo_latency')
@login_required
def geo_latency_page():
    return render_template('demos/geo_latency.html')


# ── BigQuery Column + Partition Pruning ───────────────────────────────────────

@demos_bp.route('/bigquery_pruning')
@login_required
def bigquery_pruning_page():
    return render_template('demos/bigquery_pruning.html')
