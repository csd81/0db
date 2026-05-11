"""
demos_bp.py — Visual Demo Lab blueprint.
"""
import json
import os
from flask import Blueprint, render_template, request, jsonify, current_app, Response, abort
from auth import login_required
import meta_db
from services import demo_service
from services import graph_routing_service as grs
from services import graph_pagerank_service as gprs
from services import graph_lab_service as gl
from services import energy_flow_service as efs
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


# ── Global Energy Flow ────────────────────────────────────────────────────────

@demos_bp.route('/energy-flow')
@login_required
def energy_flow_page():
    return render_template('demos/energy_flow.html')


@demos_bp.route('/energy-flow/nodes')
@login_required
def energy_flow_nodes():
    return jsonify(efs.get_all_nodes())


@demos_bp.route('/energy-flow/edges')
@login_required
def energy_flow_edges():
    month = request.args.get('month', '2021-01')
    return jsonify(efs.get_all_edges(month))


@demos_bp.route('/energy-flow/timeline')
@login_required
def energy_flow_timeline():
    return jsonify(efs.get_timeline())


@demos_bp.route('/energy-flow/chokepoints')
@login_required
def energy_flow_chokepoints():
    return jsonify(efs.get_chokepoints_ui())


@demos_bp.route('/energy-flow/compute', methods=['POST'])
@login_required
def energy_flow_compute():
    data          = request.json or {}
    month         = data.get('month', '2021-01')
    constrictions = data.get('constrictions', {})
    # Convert string keys/values coming from JSON
    constrictions = {str(k): float(v) for k, v in constrictions.items()}
    try:
        result = efs.compute_multi_flow(month, constrictions)
        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


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


# ── CAP Theorem ───────────────────────────────────────────────────────────────

@demos_bp.route('/cap-theorem')
@login_required
def cap_theorem_page():
    return render_template('demos/cap_theorem.html')


# ── Spotify on GCP Cloud Workflow ─────────────────────────────────────────────

@demos_bp.route('/spotify-cloud')
@login_required
def spotify_cloud_page():
    return render_template('demos/spotify_cloud.html')


# ── Polyglot Persistence ───────────────────────────────────────────────────────

@demos_bp.route('/polyglot')
@login_required
def polyglot_page():
    return render_template('demos/polyglot.html')


# ── Workflow Architecture Pages ────────────────────────────────────────────────

@demos_bp.route('/workflow/search-ai')
@login_required
def workflow_search_ai():
    return render_template('demos/workflow_search_ai.html')

@demos_bp.route('/workflow/video')
@login_required
def workflow_video():
    return render_template('demos/workflow_video.html')

@demos_bp.route('/workflow/social')
@login_required
def workflow_social():
    return render_template('demos/workflow_social.html')

@demos_bp.route('/workflow/ecommerce')
@login_required
def workflow_ecommerce():
    return render_template('demos/workflow_ecommerce.html')

@demos_bp.route('/workflow/messaging')
@login_required
def workflow_messaging():
    return render_template('demos/workflow_messaging.html')

@demos_bp.route('/workflow/fintech')
@login_required
def workflow_fintech():
    return render_template('demos/workflow_fintech.html')

@demos_bp.route('/workflow/iot')
@login_required
def workflow_iot():
    return render_template('demos/workflow_iot.html')

@demos_bp.route('/workflow/gaming')
@login_required
def workflow_gaming():
    return render_template('demos/workflow_gaming.html')

@demos_bp.route('/workflow/bigdata')
@login_required
def workflow_bigdata():
    return render_template('demos/workflow_bigdata.html')


# ── Breaking Points: Historical Case Studies ───────────────────────────────────

@demos_bp.route('/history/google')
@login_required
def history_google():
    return render_template('demos/history_google.html')

@demos_bp.route('/history/amazon')
@login_required
def history_amazon():
    return render_template('demos/history_amazon.html')

@demos_bp.route('/history/facebook')
@login_required
def history_facebook():
    return render_template('demos/history_facebook.html')

@demos_bp.route('/history/netflix')
@login_required
def history_netflix():
    return render_template('demos/history_netflix.html')

@demos_bp.route('/history/whatsapp')
@login_required
def history_whatsapp():
    return render_template('demos/history_whatsapp.html')

@demos_bp.route('/history/kafka')
@login_required
def history_kafka():
    return render_template('demos/history_kafka.html')

@demos_bp.route('/history/transformer')
@login_required
def history_transformer():
    return render_template('demos/history_transformer.html')

@demos_bp.route('/history/tiktok')
@login_required
def history_tiktok():
    return render_template('demos/history_tiktok.html')

@demos_bp.route('/history/figma')
@login_required
def history_figma():
    return render_template('demos/history_figma.html')

@demos_bp.route('/history/snowflake')
@login_required
def history_snowflake():
    return render_template('demos/history_snowflake.html')

@demos_bp.route('/history/cloudflare')
@login_required
def history_cloudflare():
    return render_template('demos/history_cloudflare.html')

@demos_bp.route('/era/web2')
@login_required
def era_web2():
    return render_template('demos/era_web2.html')

@demos_bp.route('/era/mobile-nosql')
@login_required
def era_mobile_nosql():
    return render_template('demos/era_mobile_nosql.html')

@demos_bp.route('/era/streaming')
@login_required
def era_streaming():
    return render_template('demos/era_streaming.html')

@demos_bp.route('/era/edge-iot')
@login_required
def era_edge_iot():
    return render_template('demos/era_edge_iot.html')

@demos_bp.route('/era/genai')
@login_required
def era_genai():
    return render_template('demos/era_genai.html')

@demos_bp.route('/cn/bytedance')
@login_required
def cn_bytedance():
    return render_template('demos/cn_bytedance.html')

@demos_bp.route('/cn/alibaba')
@login_required
def cn_alibaba():
    return render_template('demos/cn_alibaba.html')

@demos_bp.route('/cn/shein-temu')
@login_required
def cn_shein_temu():
    return render_template('demos/cn_shein_temu.html')

@demos_bp.route('/cn/byd')
@login_required
def cn_byd():
    return render_template('demos/cn_byd.html')

@demos_bp.route('/cn/tencent')
@login_required
def cn_tencent():
    return render_template('demos/cn_tencent.html')

@demos_bp.route('/bp/llm-moe')
@login_required
def bp_llm_moe():
    return render_template('demos/bp_llm_moe.html')

@demos_bp.route('/bp/db-convergence')
@login_required
def bp_db_convergence():
    return render_template('demos/bp_db_convergence.html')

@demos_bp.route('/bp/wasm-edge')
@login_required
def bp_wasm_edge():
    return render_template('demos/bp_wasm_edge.html')

@demos_bp.route('/bp/edge-ai')
@login_required
def bp_edge_ai():
    return render_template('demos/bp_edge_ai.html')

@demos_bp.route('/bp/space-cloud')
@login_required
def bp_space_cloud():
    return render_template('demos/bp_space_cloud.html')

@demos_bp.route('/i40/overview')
@login_required
def i40_overview():
    return render_template('demos/i40_overview.html')

@demos_bp.route('/i40/tesla')
@login_required
def i40_tesla():
    return render_template('demos/i40_tesla.html')

@demos_bp.route('/i40/spacex')
@login_required
def i40_spacex():
    return render_template('demos/i40_spacex.html')

@demos_bp.route('/i40/xai')
@login_required
def i40_xai():
    return render_template('demos/i40_xai.html')

@demos_bp.route('/data/paradigm')
@login_required
def data_paradigm():
    return render_template('demos/data_paradigm.html')


# ── T-SQL Script Lab ───────────────────────────────────────────────────────────

@demos_bp.route('/tsql-primer')
@login_required
def tsql_primer():
    return render_template('demos/tsql_primer.html')


@demos_bp.route('/tsql-primer/state')
@login_required
def tsql_primer_state():
    import pyodbc
    try:
        conn_str = _build_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=8) as conn:
            cur = conn.cursor()
            cur.execute("SELECT ISNULL(balance, 0) FROM Customers WHERE CustomerID='AROUT'")
            row = cur.fetchone()
            balance = float(row[0]) if row else None

            cur.execute("SELECT ProductName, UnitsInStock, UnitPrice FROM Products WHERE ProductID=40")
            row = cur.fetchone()
            product = {'name': row[0], 'stock': int(row[1]), 'price': float(row[2])} if row else None

            cur.execute("""
                SELECT TOP 5 o.OrderID,
                       CONVERT(varchar, o.OrderDate, 120) AS dt,
                       od.ProductID, od.Quantity, od.Discount
                FROM Orders o
                LEFT JOIN [Order Details] od ON o.OrderID = od.OrderID
                WHERE o.CustomerID = 'AROUT' AND o.EmployeeID IS NULL
                ORDER BY o.OrderDate DESC
            """)
            orders = [
                {'order_id': r[0], 'date': r[1], 'product_id': r[2],
                 'qty': r[3], 'discount': float(r[4]) if r[4] is not None else None}
                for r in cur.fetchall()
            ]
        return jsonify({'ok': True, 'balance': balance, 'product': product, 'orders': orders})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/tsql-primer/reset', methods=['POST'])
@login_required
def tsql_primer_reset():
    import pyodbc
    try:
        conn_str = _build_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=10) as conn:
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("UPDATE Products SET UnitsInStock=900 WHERE ProductID=40")
            cur.execute("UPDATE Customers SET balance=1000 WHERE CustomerID='AROUT'")
            cur.execute("""DELETE [Order Details] WHERE OrderID IN
                (SELECT OrderID FROM Orders WHERE CustomerID='AROUT' AND EmployeeID IS NULL)""")
            cur.execute("DELETE Orders WHERE CustomerID='AROUT' AND EmployeeID IS NULL")
        return jsonify({'ok': True, 'balance': 1000.0, 'stock': 900})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/tsql-primer/run', methods=['POST'])
@login_required
def tsql_primer_run():
    import pyodbc
    mode = (request.json or {}).get('mode', 'broken')
    log  = []

    PROD_NAME = 'boston'
    QUANTITY  = 10
    CUST_ID   = 'AROUT'
    PROD_ID   = 40

    def emit(step, msg, kind='info', sql=None):
        log.append({'step': step, 'msg': msg, 'kind': kind, 'sql': sql})

    try:
        conn_str = _build_conn_str(current_app.config)
        conn     = pyodbc.connect(conn_str, timeout=10)
        cur      = conn.cursor()

        if mode == 'broken':
            conn.autocommit = True
            emit(0, 'No BEGIN TRAN — each statement auto-commits immediately', 'header',
                 '-- ⚠ No explicit transaction\nSET NOCOUNT ON;\n-- autocommit = ON')

            cur.execute("SELECT COUNT(*) FROM Products WHERE ProductName LIKE '%'+?+'%'", PROD_NAME)
            res_no = cur.fetchone()[0]
            emit(1, f"Product lookup: {res_no} match(es) for '{PROD_NAME}'",
                 'ok' if res_no == 1 else 'warn',
                 f"SELECT COUNT(*) FROM Products\n  WHERE ProductName LIKE '%boston%'\n-- Result: {res_no} row(s)")
            if res_no != 1:
                emit(1, 'ERROR: Ambiguous product — aborting.', 'err')
                conn.close()
                return jsonify({'ok': True, 'log': log})

            cur.execute("SELECT UnitsInStock, UnitPrice FROM Products WHERE ProductID=?", PROD_ID)
            row = cur.fetchone()
            stock, unit_price = int(row[0]), float(row[1])
            emit(2, f"Stock check: {stock} units available, need {QUANTITY} → {'OK' if stock >= QUANTITY else 'INSUFFICIENT'}",
                 'ok' if stock >= QUANTITY else 'err',
                 f"SELECT UnitsInStock, UnitPrice FROM Products WHERE ProductID=40\n-- Stock: {stock}  Price: £{unit_price:.2f}")
            if stock < QUANTITY:
                conn.close()
                return jsonify({'ok': True, 'log': log})

            cur.execute("SELECT ISNULL(balance, 0) FROM Customers WHERE CustomerID=?", CUST_ID)
            balance = float(cur.fetchone()[0])
            cost    = QUANTITY * unit_price
            emit(3, f"Balance check: £{balance:.2f} available, order costs £{cost:.2f} → {'OK' if balance >= cost else 'INSUFFICIENT'}",
                 'ok' if balance >= cost else 'err',
                 f"SELECT balance FROM Customers WHERE CustomerID='AROUT'\n-- Balance: £{balance:.2f}  Cost: £{cost:.2f}")
            if balance < cost:
                conn.close()
                return jsonify({'ok': True, 'log': log})

            cur.execute("UPDATE Customers SET balance=balance-? WHERE CustomerID=?", cost, CUST_ID)
            emit(4, f"UPDATE Customers balance −£{cost:.2f}  ← AUTO-COMMITTED to disk", 'committed',
                 f"UPDATE Customers\n  SET balance = balance - {cost:.2f}\n  WHERE CustomerID = 'AROUT'\n-- ✓ 1 row affected — COMMITTED immediately")

            cur.execute("INSERT INTO Orders (CustomerID, OrderDate) VALUES (?, GETDATE())", CUST_ID)
            cur.execute("SELECT @@IDENTITY")
            order_id = int(cur.fetchone()[0])
            emit(5, f"INSERT Orders: OrderID={order_id}  ← AUTO-COMMITTED to disk", 'committed',
                 f"INSERT INTO Orders (CustomerID, OrderDate)\n  VALUES ('AROUT', GETDATE())\n-- ✓ OrderID = {order_id} — COMMITTED immediately")

            try:
                cur.execute("""INSERT INTO [Order Details] (OrderID, ProductID, Quantity, UnitPrice)
                               VALUES (?, ?, ?, ?)""", order_id, PROD_ID, QUANTITY, unit_price)
                emit(6, 'INSERT [Order Details]: succeeded (Discount column must be nullable here)', 'ok',
                     'INSERT [Order Details] (OrderID, ProductID, Quantity, UnitPrice) VALUES (...)')
            except Exception as ie:
                emit(6, f'INSERT [Order Details] FAILED: {ie}', 'err',
                     f"INSERT [Order Details] (OrderID, ProductID, Quantity, UnitPrice)\n  VALUES ({order_id}, 40, 10, {unit_price:.2f})\n-- ✗ FAILED — Discount column is NOT NULL\n-- Missing: Discount=0")
                emit(7, '⚠ No ROLLBACK possible — database is now INCONSISTENT', 'fatal',
                     f"-- CATCH block: cannot rollback — no transaction was open\n-- Orders row {order_id} exists (no matching Order Details)\n-- balance already deducted: -£{cost:.2f}\n-- State is CORRUPT")

        elif mode == 'fixed':
            conn.autocommit = False
            emit(0, 'BEGIN TRAN — all statements form one atomic unit', 'header',
                 'SET XACT_ABORT ON;\nBEGIN TRAN;\n-- All statements are pending until COMMIT or ROLLBACK')

            try:
                cur.execute("SELECT COUNT(*) FROM Products WHERE ProductName LIKE '%'+?+'%'", PROD_NAME)
                res_no = cur.fetchone()[0]
                emit(1, f"Product lookup: {res_no} match(es) for '{PROD_NAME}'", 'ok',
                     f"SELECT COUNT(*) FROM Products WHERE ProductName LIKE '%boston%'\n-- {res_no} row(s)")

                cur.execute("SELECT UnitsInStock, UnitPrice FROM Products WHERE ProductID=?", PROD_ID)
                row = cur.fetchone()
                stock, unit_price = int(row[0]), float(row[1])
                emit(2, f"Stock: {stock} units  Price: £{unit_price:.2f}", 'ok',
                     f"SELECT UnitsInStock, UnitPrice FROM Products WHERE ProductID=40\n-- Stock: {stock}  Price: £{unit_price:.2f}")

                cur.execute("SELECT ISNULL(balance, 0) FROM Customers WHERE CustomerID=?", CUST_ID)
                balance = float(cur.fetchone()[0])
                cost    = QUANTITY * unit_price
                emit(3, f"Balance: £{balance:.2f}  Cost: £{cost:.2f}", 'ok',
                     f"SELECT balance FROM Customers WHERE CustomerID='AROUT'\n-- £{balance:.2f}")

                cur.execute("UPDATE Customers SET balance=balance-? WHERE CustomerID=?", cost, CUST_ID)
                emit(4, f"UPDATE balance −£{cost:.2f}  ⏳ PENDING (not committed)", 'pending',
                     f"UPDATE Customers SET balance=balance-{cost:.2f} WHERE CustomerID='AROUT'\n-- 1 row affected — PENDING inside transaction")

                cur.execute("INSERT INTO Orders (CustomerID, OrderDate) VALUES (?, GETDATE())", CUST_ID)
                cur.execute("SELECT @@IDENTITY")
                order_id = int(cur.fetchone()[0])
                emit(5, f"INSERT Orders: OrderID={order_id}  ⏳ PENDING (not committed)", 'pending',
                     f"INSERT INTO Orders (CustomerID, OrderDate) VALUES ('AROUT', GETDATE())\n-- OrderID={order_id} — PENDING inside transaction")

                try:
                    cur.execute("""INSERT INTO [Order Details] (OrderID, ProductID, Quantity, UnitPrice)
                                   VALUES (?, ?, ?, ?)""", order_id, PROD_ID, QUANTITY, unit_price)
                    emit(6, 'INSERT [Order Details]: succeeded (Discount must be nullable)', 'ok',
                         'INSERT [Order Details] (...) VALUES (...) -- succeeded')
                    conn.commit()
                    emit(7, 'COMMIT TRAN — all 3 changes persisted atomically ✓', 'rollback',
                         'COMMIT TRAN\n-- ✓ balance updated\n-- ✓ Orders row saved\n-- ✓ Order Details row saved\n-- All or nothing: succeeded')
                except Exception as ie:
                    emit(6, f'INSERT [Order Details] FAILED: {ie}', 'err',
                         f"INSERT [Order Details] (OrderID, ProductID, Quantity, UnitPrice)\n  VALUES ({order_id}, 40, 10, {unit_price:.2f})\n-- ✗ FAILED — Discount is NOT NULL\n-- Entering CATCH block...")
                    conn.rollback()
                    emit(7, 'ROLLBACK TRAN — all pending changes undone atomically ✓', 'rollback',
                         "ROLLBACK TRAN\n-- ✓ balance restored (no change)\n-- ✓ Orders row removed\n-- ✓ Order Details: nothing to undo\n-- Database is CONSISTENT")

            except Exception as outer:
                conn.rollback()
                emit(8, f'ROLLBACK due to unexpected error: {outer}', 'err')

        conn.close()
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

    return jsonify({'ok': True, 'log': log})


# ── Isolation Level Visualizer ─────────────────────────────────────────────────

@demos_bp.route('/isolation')
@login_required
def isolation_demo():
    return render_template('demos/isolation.html')


# ── Loose Coupling Demo (Chapter 2) ───────────────────────────────────────────

@demos_bp.route('/loose-coupling')
@login_required
def loose_coupling():
    return render_template('demos/loose_coupling.html')


@demos_bp.route('/loose-coupling/state')
@login_required
def loose_coupling_state():
    import pyodbc
    try:
        conn_str = _build_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=8) as conn:
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='order_log'")
            has_table = cur.fetchone()[0] > 0

            cur.execute("SELECT COUNT(*) FROM sys.triggers WHERE name='tr_log_order'")
            has_trigger = cur.fetchone()[0] > 0

            log_rows = []
            if has_table:
                cur.execute("""
                    SELECT TOP 20 event_id, event_type, order_id, status,
                           CONVERT(varchar, time_created, 120) AS created,
                           CONVERT(varchar, time_process_begin, 120) AS t_begin,
                           CONVERT(varchar, time_process_end, 120) AS t_end,
                           process_duration
                    FROM order_log
                    WHERE order_id IN (
                        SELECT OrderID FROM Orders WHERE EmployeeID IS NULL
                    )
                    ORDER BY event_id DESC
                """)
                for r in cur.fetchall():
                    log_rows.append({
                        'event_id': r[0], 'event_type': r[1], 'order_id': r[2],
                        'status': r[3], 'created': r[4],
                        't_begin': r[5], 't_end': r[6], 'duration': r[7]
                    })

            cur.execute("""
                SELECT ProductID, ProductName, UnitsInStock, ReorderLevel
                FROM Products WHERE ProductID IN (9, 10, 40, 41)
                ORDER BY ProductID
            """)
            products = [{'id': r[0], 'name': r[1], 'stock': r[2], 'reorder': r[3]}
                        for r in cur.fetchall()]

            cur.execute("""
                SELECT TOP 5 OrderID,
                       CONVERT(varchar, OrderDate, 120) AS dt
                FROM Orders WHERE EmployeeID IS NULL
                ORDER BY OrderID DESC
            """)
            test_orders = [{'order_id': r[0], 'date': r[1]} for r in cur.fetchall()]

        return jsonify({'ok': True, 'has_table': has_table, 'has_trigger': has_trigger,
                        'log_rows': log_rows, 'products': products, 'test_orders': test_orders})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/loose-coupling/setup', methods=['POST'])
@login_required
def loose_coupling_setup():
    import pyodbc
    steps = []
    try:
        conn_str = _build_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=15) as conn:
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute("""
                IF OBJECT_ID('dbo.order_log', 'U') IS NULL
                CREATE TABLE order_log (
                    event_id            int IDENTITY(1,1) PRIMARY KEY,
                    event_type          varchar(50)  NOT NULL,
                    order_id            int          NOT NULL,
                    status              int          NOT NULL DEFAULT(0),
                    time_created        datetime     NOT NULL DEFAULT(GETDATE()),
                    time_process_begin  datetime     NULL,
                    time_process_end    datetime     NULL,
                    process_duration    AS DATEDIFF(second, time_process_begin, time_process_end)
                )
            """)
            steps.append({'msg': 'order_log table ready', 'kind': 'ok'})

            cur.execute("IF OBJECT_ID('dbo.tr_log_order', 'TR') IS NOT NULL DROP TRIGGER tr_log_order")
            cur.execute("""
                CREATE TRIGGER tr_log_order ON Orders FOR INSERT, UPDATE AS
                SET NOCOUNT ON;
                IF UPDATE(OrderID) BEGIN
                    INSERT order_log (event_type, order_id)
                    SELECT 'new order', OrderID FROM inserted
                END ELSE IF UPDATE(ShipAddress) OR UPDATE(ShipCity) BEGIN
                    INSERT order_log (event_type, order_id)
                    SELECT 'address changed', OrderID FROM inserted
                END ELSE BEGIN
                    INSERT order_log (event_type, order_id)
                    SELECT 'other change', OrderID FROM inserted
                END
            """)
            steps.append({'msg': 'tr_log_order trigger created on Orders', 'kind': 'ok'})

        return jsonify({'ok': True, 'steps': steps})
    except Exception as e:
        steps.append({'msg': f'Error: {e}', 'kind': 'err'})
        return jsonify({'ok': False, 'steps': steps, 'error': str(e)})


@demos_bp.route('/loose-coupling/insert-order', methods=['POST'])
@login_required
def loose_coupling_insert_order():
    import pyodbc
    scenario = (request.json or {}).get('scenario', 'good')
    try:
        conn_str = _build_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=10) as conn:
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute("INSERT INTO Orders (CustomerID, OrderDate) VALUES ('AROUT', GETDATE())")
            cur.execute("SELECT SCOPE_IDENTITY()")
            order_id = int(cur.fetchone()[0])

            if scenario == 'good':
                qty9, qty10 = 2, 3
            else:
                # quantities far exceed stock → will trigger CHECK constraint on UnitsInStock
                qty9, qty10 = 9999, 9999

            cur.execute("""
                INSERT INTO [Order Details] (OrderID, ProductID, Quantity, UnitPrice, Discount)
                VALUES (?, 9, ?, 10.0, 0), (?, 10, ?, 31.0, 0)
            """, order_id, qty9, order_id, qty10)

        return jsonify({'ok': True, 'order_id': order_id, 'scenario': scenario,
                        'note': f'Inserted OrderID={order_id} with qty {qty9}+{qty10}'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/loose-coupling/process', methods=['POST'])
@login_required
def loose_coupling_process():
    import pyodbc
    log = []
    try:
        conn_str = _build_conn_str(current_app.config)
        conn = pyodbc.connect(conn_str, timeout=15)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
            SELECT event_id, event_type, order_id FROM order_log
            WHERE status=0 AND order_id IN (SELECT OrderID FROM Orders WHERE EmployeeID IS NULL)
            ORDER BY event_id
        """)
        events = [(r[0], r[1], r[2]) for r in cur.fetchall()]

        if not events:
            return jsonify({'ok': True, 'log': [{'msg': 'No pending events (status=0).', 'kind': 'info'}]})

        for event_id, event_type, order_id in events:
            cur.execute("UPDATE order_log SET time_process_begin=GETDATE() WHERE event_id=?", event_id)
            log.append({'msg': f'Event #{event_id}  [{event_type}]  Order #{order_id}', 'kind': 'header'})

            result = 0
            if event_type == 'new order':
                try:
                    conn.autocommit = False
                    cur.execute("""
                        UPDATE Products
                        SET UnitsInStock = UnitsInStock - od.Quantity
                        FROM Products p
                        INNER JOIN [Order Details] od ON od.ProductID = p.ProductID
                        WHERE od.OrderID = ?
                    """, order_id)
                    conn.commit()
                    conn.autocommit = True
                    log.append({'msg': '  Inventory updated — UnitsInStock reduced', 'kind': 'ok'})
                except Exception as inv_err:
                    conn.rollback()
                    conn.autocommit = True
                    result = 1
                    log.append({'msg': f'  Inventory error: {inv_err}', 'kind': 'err'})
                    log.append({'msg': '  ROLLBACK — no stock changes committed', 'kind': 'rollback'})
            elif event_type in ('address changed', 'other change'):
                log.append({'msg': f'  Simulated processing for "{event_type}"', 'kind': 'ok'})
            else:
                result = 1
                log.append({'msg': f'  Unknown event type — skipped', 'kind': 'warn'})

            cur.execute("""
                UPDATE order_log SET time_process_end=GETDATE(),
                    status=? WHERE event_id=?
            """, (2 if result == 0 else 1), event_id)
            log.append({'msg': f'  status → {"2 (OK)" if result==0 else "1 (FAILED)"}', 'kind': 'ok' if result == 0 else 'err'})

        conn.close()
        return jsonify({'ok': True, 'log': log})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/loose-coupling/reset', methods=['POST'])
@login_required
def loose_coupling_reset():
    import pyodbc
    try:
        conn_str = _build_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=10) as conn:
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("""
                DELETE [Order Details] WHERE OrderID IN
                (SELECT OrderID FROM Orders WHERE EmployeeID IS NULL)
            """)
            cur.execute("DELETE Orders WHERE EmployeeID IS NULL")
            cur.execute("""
                IF OBJECT_ID('dbo.order_log','U') IS NOT NULL
                DELETE order_log
            """)
            # Restore stock for demo products
            cur.execute("UPDATE Products SET UnitsInStock=13  WHERE ProductID=9")
            cur.execute("UPDATE Products SET UnitsInStock=31  WHERE ProductID=10")
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ── Data Quality & Functional Dependency (Chapter 4) ───────────────────────────

# Whitelisted columns per table — never interpolate user input into SQL
_DQ_SCHEMA = {
    'DimSalesReason': ['SalesReasonName', 'SalesReasonReasonType'],
    'DimGeography':   ['City', 'StateProvinceCode', 'StateProvinceName',
                       'CountryRegionCode', 'EnglishCountryRegionName',
                       'PostalCode', 'SalesTerritoryKey'],
    'DimProduct':     ['Color', 'ProductLine', 'Size', 'Class', 'Style',
                       'WeightUnitMeasureCode', 'SizeUnitMeasureCode',
                       'DaysToManufacture', 'FinishedGoodsFlag'],
    'DimCustomer':    ['EnglishEducation', 'EnglishOccupation', 'Gender',
                       'MaritalStatus', 'CommuteDistance', 'NumberCarsOwned',
                       'NumberChildrenAtHome', 'HouseOwnerFlag', 'YearlyIncome'],
    'DimEmployee':    ['SalesTerritoryKey', 'Gender', 'MaritalStatus',
                       'Title', 'DepartmentName', 'SalariedFlag', 'PayFrequency'],
}

_DQ_ROW_COUNTS = {
    'DimSalesReason': 10,
    'DimGeography':   655,
    'DimProduct':     606,
    'DimCustomer':    18484,
    'DimEmployee':    296,
}


def _build_dw_conn_str(c):
    user = c.get('SQL_SA_USERNAME') or os.environ.get('SQL_SA_USERNAME') or ''
    pw   = c.get('SQL_SA_PASSWORD') or os.environ.get('SQL_SA_PASSWORD') or ''
    return (
        f"DRIVER={{{c['SQL_DRIVER']}}};SERVER={c['SQL_SERVER']};"
        f"DATABASE=AdventureWorksDW2019;UID={user};PWD={pw};"
        f"Encrypt={c['SQL_ENCRYPT']};TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )


@demos_bp.route('/data-quality')
@login_required
def data_quality():
    return render_template('demos/data_quality.html',
                           schema=_DQ_SCHEMA,
                           row_counts=_DQ_ROW_COUNTS)


@demos_bp.route('/data-quality/check-fd', methods=['POST'])
@login_required
def data_quality_check_fd():
    import pyodbc
    data  = request.get_json() or {}
    table = data.get('table', '')
    col_a = data.get('col_a', '')
    col_b = data.get('col_b', '')

    if table not in _DQ_SCHEMA:
        return jsonify({'ok': False, 'error': 'Invalid table'})
    allowed = _DQ_SCHEMA[table]
    if col_a not in allowed or col_b not in allowed:
        return jsonify({'ok': False, 'error': 'Invalid column'})
    if col_a == col_b:
        return jsonify({'ok': False, 'error': 'Choose two different columns'})

    try:
        conn_str = _build_dw_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=15) as conn:
            cur = conn.cursor()

            # N = distinct values of col_a (groups when grouping by col_a alone)
            cur.execute(
                f"SELECT COUNT(DISTINCT [{col_a}]) FROM [{table}]")
            n_alone = cur.fetchone()[0]

            # M = distinct (col_a, col_b) combinations
            cur.execute(
                f"SELECT COUNT(*) FROM "
                f"(SELECT DISTINCT [{col_a}],[{col_b}] FROM [{table}]) t")
            m_combined = cur.fetchone()[0]

            # Total row count
            cur.execute(f"SELECT COUNT(*) FROM [{table}]")
            total = cur.fetchone()[0]

            # Null counts for each column
            cur.execute(
                f"SELECT COUNT(*)-COUNT([{col_a}]), COUNT(*)-COUNT([{col_b}]) "
                f"FROM [{table}]")
            r = cur.fetchone()
            null_a, null_b = r[0], r[1]

            # Sample: up to 15 group combos ordered by col_a
            cur.execute(f"""
                SELECT TOP 15
                    CAST([{col_a}] AS NVARCHAR(200)) AS a_val,
                    CAST([{col_b}] AS NVARCHAR(200)) AS b_val,
                    COUNT(*) AS cnt
                FROM [{table}]
                WHERE [{col_a}] IS NOT NULL AND [{col_b}] IS NOT NULL
                GROUP BY CAST([{col_a}] AS NVARCHAR(200)),
                         CAST([{col_b}] AS NVARCHAR(200))
                ORDER BY CAST([{col_a}] AS NVARCHAR(200))
            """)
            samples = [{'a': r[0], 'b': r[1], 'cnt': r[2]}
                       for r in cur.fetchall()]

        return jsonify({
            'ok': True,
            'table': table, 'col_a': col_a, 'col_b': col_b,
            'n_alone': n_alone, 'm_combined': m_combined,
            'total': total, 'null_a': null_a, 'null_b': null_b,
            'dependent': (n_alone == m_combined),
            'samples': samples,
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/data-quality/profile', methods=['POST'])
@login_required
def data_quality_profile():
    import pyodbc
    data   = request.get_json() or {}
    table  = data.get('table', '')
    column = data.get('column', '')

    if table not in _DQ_SCHEMA or column not in _DQ_SCHEMA[table]:
        return jsonify({'ok': False, 'error': 'Invalid table/column'})

    try:
        conn_str = _build_dw_conn_str(current_app.config)
        with pyodbc.connect(conn_str, timeout=15) as conn:
            cur = conn.cursor()

            cur.execute(f"""
                SELECT COUNT(*) AS total,
                       COUNT([{column}]) AS non_null,
                       COUNT(DISTINCT [{column}]) AS distinct_count
                FROM [{table}]
            """)
            r = cur.fetchone()
            total, non_null, distinct_count = r[0], r[1], r[2]
            null_count = total - non_null
            null_pct   = round(100.0 * null_count / total, 1) if total else 0

            cur.execute(f"""
                SELECT TOP 10
                    CAST([{column}] AS NVARCHAR(255)) AS val,
                    COUNT(*) AS cnt
                FROM [{table}]
                WHERE [{column}] IS NOT NULL
                GROUP BY CAST([{column}] AS NVARCHAR(255))
                ORDER BY cnt DESC
            """)
            top_values = [{'val': r[0], 'cnt': r[1]} for r in cur.fetchall()]

        return jsonify({
            'ok': True,
            'table': table, 'column': column,
            'total': total, 'non_null': non_null,
            'null_count': null_count, 'null_pct': null_pct,
            'distinct_count': distinct_count,
            'top_values': top_values,
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ──────────────── Chapter 5: Columnstore & Partitioning ────────────────

_CS_TABLES = ['FactInternetSales_BTREE', 'FactInternetSales_PageComp', 'FactInternetSales_CCI']

_PART_STEPS = {
    1: "Create partition function & scheme",
    2: "Create InternetSales partitioned table",
    3: "Load data (years 2010–2012)",
    4: "Create aligned columnstore index",
    5: "Create staging table (InternetSalesNew, year=2013)",
    6: "Load 2013 data into staging + build CCI",
    7: "SWITCH staging → partition 4 (metadata-only!)",
}

_PART_SQLS = {
    1: [
        "IF EXISTS (SELECT 1 FROM sys.partition_schemes WHERE name='PsInternetSalesYear') DROP PARTITION SCHEME PsInternetSalesYear",
        "IF EXISTS (SELECT 1 FROM sys.partition_functions WHERE name='PfInternetSalesYear') DROP PARTITION FUNCTION PfInternetSalesYear",
        "CREATE PARTITION FUNCTION PfInternetSalesYear (TINYINT) AS RANGE LEFT FOR VALUES (10, 11, 12, 13)",
        "CREATE PARTITION SCHEME PsInternetSalesYear AS PARTITION PfInternetSalesYear ALL TO ([PRIMARY])",
    ],
    2: [
        "IF OBJECT_ID('dbo.InternetSales') IS NOT NULL DROP TABLE dbo.InternetSales",
        ("CREATE TABLE dbo.InternetSales ("
         " InternetSalesKey INT NOT NULL IDENTITY(1,1),"
         " PcInternetSalesYear TINYINT NOT NULL,"
         " ProductKey INT NOT NULL,"
         " DateKey INT NOT NULL,"
         " OrderQuantity SMALLINT NOT NULL DEFAULT 0,"
         " SalesAmount MONEY NOT NULL DEFAULT 0,"
         " UnitPrice MONEY NOT NULL DEFAULT 0,"
         " DiscountAmount FLOAT NOT NULL DEFAULT 0,"
         " CONSTRAINT PK_InternetSales PRIMARY KEY (InternetSalesKey, PcInternetSalesYear)"
         ") ON PsInternetSalesYear(PcInternetSalesYear)"),
        "ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_IS_Products FOREIGN KEY(ProductKey) REFERENCES dbo.DimProduct(ProductKey)",
        "ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_IS_Dates FOREIGN KEY(DateKey) REFERENCES dbo.DimDate(DateKey)",
        "ALTER TABLE dbo.InternetSales REBUILD WITH (DATA_COMPRESSION = PAGE)",
    ],
    3: [
        ("INSERT INTO dbo.InternetSales"
         " (PcInternetSalesYear, ProductKey, DateKey, OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)"
         " SELECT CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT),"
         " ProductKey, OrderDateKey, OrderQuantity, SalesAmount, UnitPrice, DiscountAmount"
         " FROM dbo.FactInternetSales"
         " WHERE CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) < 13"),
    ],
    4: [
        ("CREATE COLUMNSTORE INDEX CSI_InternetSales ON dbo.InternetSales"
         " (InternetSalesKey, PcInternetSalesYear, ProductKey, DateKey,"
         "  OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)"
         " ON PsInternetSalesYear(PcInternetSalesYear)"),
    ],
    5: [
        "IF OBJECT_ID('dbo.InternetSalesNew') IS NOT NULL DROP TABLE dbo.InternetSalesNew",
        ("CREATE TABLE dbo.InternetSalesNew ("
         " InternetSalesKey INT NOT NULL IDENTITY(1,1),"
         " PcInternetSalesYear TINYINT NOT NULL CHECK (PcInternetSalesYear = 13),"
         " ProductKey INT NOT NULL,"
         " DateKey INT NOT NULL,"
         " OrderQuantity SMALLINT NOT NULL DEFAULT 0,"
         " SalesAmount MONEY NOT NULL DEFAULT 0,"
         " UnitPrice MONEY NOT NULL DEFAULT 0,"
         " DiscountAmount FLOAT NOT NULL DEFAULT 0,"
         " CONSTRAINT PK_InternetSalesNew PRIMARY KEY (InternetSalesKey, PcInternetSalesYear)"
         ")"),
        "ALTER TABLE dbo.InternetSalesNew ADD CONSTRAINT FK_ISN_Products FOREIGN KEY(ProductKey) REFERENCES dbo.DimProduct(ProductKey)",
        "ALTER TABLE dbo.InternetSalesNew ADD CONSTRAINT FK_ISN_Dates FOREIGN KEY(DateKey) REFERENCES dbo.DimDate(DateKey)",
        "ALTER TABLE dbo.InternetSalesNew REBUILD WITH (DATA_COMPRESSION = PAGE)",
    ],
    6: [
        ("INSERT INTO dbo.InternetSalesNew"
         " (PcInternetSalesYear, ProductKey, DateKey, OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)"
         " SELECT CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT),"
         " ProductKey, OrderDateKey, OrderQuantity, SalesAmount, UnitPrice, DiscountAmount"
         " FROM dbo.FactInternetSales"
         " WHERE CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) = 13"),
        ("CREATE COLUMNSTORE INDEX CSI_InternetSalesNew ON dbo.InternetSalesNew"
         " (InternetSalesKey, PcInternetSalesYear, ProductKey, DateKey,"
         "  OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)"),
    ],
    7: [
        "ALTER TABLE dbo.InternetSalesNew SWITCH TO dbo.InternetSales PARTITION 4",
    ],
}


@demos_bp.route('/columnstore')
@login_required
def columnstore():
    return render_template('demos/columnstore.html')


@demos_bp.route('/columnstore/setup', methods=['POST'])
@login_required
def columnstore_setup():
    import pyodbc, time
    c = current_app.config
    conn_str = _build_dw_conn_str(c)
    results = []
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            steps = [
                ('FactInternetSales_BTREE', 'B-Tree (Heap)', [], [
                    "IF OBJECT_ID('dbo.FactInternetSales_BTREE') IS NOT NULL DROP TABLE dbo.FactInternetSales_BTREE",
                    "SELECT * INTO dbo.FactInternetSales_BTREE FROM dbo.FactInternetSales",
                ]),
                ('FactInternetSales_PageComp', 'Page Compression', [], [
                    "IF OBJECT_ID('dbo.FactInternetSales_PageComp') IS NOT NULL DROP TABLE dbo.FactInternetSales_PageComp",
                    "SELECT * INTO dbo.FactInternetSales_PageComp FROM dbo.FactInternetSales",
                    "ALTER TABLE dbo.FactInternetSales_PageComp REBUILD WITH (DATA_COMPRESSION = PAGE)",
                ]),
                ('FactInternetSales_CCI', 'Clustered Columnstore Index', [], [
                    "IF OBJECT_ID('dbo.FactInternetSales_CCI') IS NOT NULL DROP TABLE dbo.FactInternetSales_CCI",
                    "SELECT * INTO dbo.FactInternetSales_CCI FROM dbo.FactInternetSales",
                    "CREATE CLUSTERED COLUMNSTORE INDEX CCI_FIS ON dbo.FactInternetSales_CCI",
                ]),
            ]
            for tbl, typ, _, sqls in steps:
                t0 = time.perf_counter()
                for sql in sqls:
                    cur.execute(sql)
                elapsed = int((time.perf_counter() - t0) * 1000)
                results.append({'table': tbl, 'type': typ, 'ms': elapsed})
        return jsonify({'ok': True, 'results': results})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/columnstore/spaceused')
@login_required
def columnstore_spaceused():
    import pyodbc
    c = current_app.config
    conn_str = _build_dw_conn_str(c)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT OBJECT_NAME(p.object_id) AS tbl,
                       SUM(a.total_pages) * 8    AS total_kb,
                       SUM(a.used_pages)  * 8    AS used_kb
                FROM sys.partitions p
                JOIN sys.allocation_units a ON p.partition_id = a.container_id
                WHERE OBJECT_NAME(p.object_id) IN (
                    'FactInternetSales_BTREE',
                    'FactInternetSales_PageComp',
                    'FactInternetSales_CCI',
                    'FactInternetSales'
                )
                GROUP BY p.object_id
                ORDER BY used_kb DESC
            """)
            rows = [{'tbl': r[0], 'total_kb': r[1], 'used_kb': r[2]} for r in cur.fetchall()]
        return jsonify({'ok': True, 'rows': rows})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/columnstore/benchmark', methods=['POST'])
@login_required
def columnstore_benchmark():
    import pyodbc, time
    c = current_app.config
    conn_str = _build_dw_conn_str(c)
    QUERY = (
        "SELECT t.SalesTerritoryRegion, dt.CalendarYear,"
        " COUNT(s.SalesOrderNumber) AS NumSales,"
        " SUM(s.SalesAmount) AS TotalSalesAmt,"
        " AVG(s.SalesAmount) AS AvgSalesAmt,"
        " COUNT(DISTINCT s.SalesOrderNumber) AS NumOrders,"
        " COUNT(DISTINCT s.CustomerKey) AS NumCustomers"
        " FROM dbo.{table} s"
        " INNER JOIN dbo.DimSalesTerritory t  ON t.SalesTerritoryKey = s.SalesTerritoryKey"
        " INNER JOIN dbo.DimDate dt           ON dt.DateKey = s.OrderDateKey"
        " GROUP BY t.SalesTerritoryRegion, dt.CalendarYear"
    )
    results = []
    try:
        for tbl in _CS_TABLES:
            with pyodbc.connect(conn_str, autocommit=True) as conn:
                cur = conn.cursor()
                try:
                    cur.execute("DBCC DROPCLEANBUFFERS")
                    cur.execute("DBCC FREEPROCCACHE")
                except Exception:
                    pass
                t0 = time.perf_counter()
                cur.execute(QUERY.format(table=tbl))
                rows = cur.fetchall()
                elapsed = int((time.perf_counter() - t0) * 1000)
                results.append({'table': tbl, 'elapsed_ms': elapsed, 'row_count': len(rows)})
        return jsonify({'ok': True, 'results': results})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/columnstore/partition-status')
@login_required
def columnstore_partition_status():
    import pyodbc
    c = current_app.config
    conn_str = _build_dw_conn_str(c)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT OBJECT_ID('dbo.InternetSales')")
            table_exists = cur.fetchone()[0] is not None
            cur.execute("SELECT COUNT(*) FROM sys.partition_functions WHERE name='PfInternetSalesYear'")
            pf_exists = cur.fetchone()[0] > 0
            cur.execute("SELECT OBJECT_ID('dbo.InternetSalesNew')")
            staging_exists = cur.fetchone()[0] is not None
            partitions = []
            if table_exists and pf_exists:
                cur.execute(
                    "SELECT $PARTITION.PfInternetSalesYear(PcInternetSalesYear) AS PartNum,"
                    " COUNT(*) AS Rows"
                    " FROM dbo.InternetSales"
                    " GROUP BY $PARTITION.PfInternetSalesYear(PcInternetSalesYear)"
                    " ORDER BY PartNum"
                )
                year_map = {1: '2010', 2: '2011', 3: '2012', 4: '2013'}
                partitions = [{'partition': r[0], 'rows': r[1], 'year': year_map.get(r[0], str(r[0]))} for r in cur.fetchall()]
        return jsonify({'ok': True, 'table_exists': table_exists, 'pf_exists': pf_exists,
                        'staging_exists': staging_exists, 'partitions': partitions})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/columnstore/partition-build', methods=['POST'])
@login_required
def columnstore_partition_build():
    import pyodbc, time
    step = int((request.json or {}).get('step', 1))
    if step not in _PART_SQLS:
        return jsonify({'ok': False, 'error': f'Unknown step {step}'})
    c = current_app.config
    conn_str = _build_dw_conn_str(c)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            t0 = time.perf_counter()
            for sql in _PART_SQLS[step]:
                cur.execute(sql)
            elapsed = int((time.perf_counter() - t0) * 1000)
        return jsonify({'ok': True, 'step': step, 'label': _PART_STEPS[step], 'elapsed_ms': elapsed})
    except Exception as e:
        return jsonify({'ok': False, 'step': step, 'label': _PART_STEPS[step], 'error': str(e)})


@demos_bp.route('/columnstore/pg-partition', methods=['POST'])
@login_required
def columnstore_pg_partition():
    mode = (request.json or {}).get('mode', 'declarative')
    pg_conns = _conns_by_type('postgresql')
    if not pg_conns:
        return jsonify({'ok': False, 'error': 'No PostgreSQL connection configured'})
    conn_id = pg_conns[0]['id']
    try:
        from db_adapter import get_adapter_connection
        conn = get_adapter_connection(conn_id)
        cur = conn.cursor()
        if mode == 'declarative':
            for sql in [
                "DROP TABLE IF EXISTS products_p_a_m",
                "DROP TABLE IF EXISTS products_p_m_z",
                "DROP TABLE IF EXISTS products_p CASCADE",
                "CREATE TABLE products_p (productid int, productname varchar(40), part_key char(1), unitprice numeric(10,4)) PARTITION BY RANGE(part_key)",
                "CREATE TABLE products_p_a_m PARTITION OF products_p FOR VALUES FROM ('a') TO ('m')",
                "CREATE TABLE products_p_m_z PARTITION OF products_p FOR VALUES FROM ('m') TO ('z')",
                "INSERT INTO products_p (productid, productname, part_key, unitprice) SELECT productid, productname, LOWER(SUBSTRING(productname, 1, 1)), unitprice FROM products",
            ]:
                cur.execute(sql)
            cur.execute("SELECT 'A–L (products_p_a_m)' AS part, COUNT(*) FROM products_p_a_m UNION ALL SELECT 'M–Z (products_p_m_z)', COUNT(*) FROM products_p_m_z")
            counts = [{'part': r[0], 'count': r[1]} for r in cur.fetchall()]
            cur.execute("SELECT productname, part_key FROM products_p ORDER BY productname LIMIT 8")
            samples = [{'name': r[0], 'key': r[1]} for r in cur.fetchall()]
            return jsonify({'ok': True, 'mode': mode, 'counts': counts, 'samples': samples})
        else:
            for sql in [
                "DROP TABLE IF EXISTS products_i_a_m CASCADE",
                "DROP TABLE IF EXISTS products_i_n_z CASCADE",
                "DROP TABLE IF EXISTS products_i CASCADE",
                "CREATE TABLE products_i (productid int, productname varchar(40), unitprice numeric(10,4))",
                "CREATE TABLE products_i_a_m () INHERITS (products_i)",
                "ALTER TABLE products_i_a_m ADD CONSTRAINT df_a_m CHECK (lower(left(productname,1)) >= 'a' AND lower(left(productname,1)) <= 'm')",
                "CREATE TABLE products_i_n_z () INHERITS (products_i)",
                "ALTER TABLE products_i_n_z ADD CONSTRAINT df_n_z CHECK (lower(left(productname,1)) > 'm' AND lower(left(productname,1)) <= 'z')",
                ("CREATE RULE products_insert_a_m AS ON INSERT TO products_i"
                 " WHERE (lower(left(productname,1)) >= 'a' AND lower(left(productname,1)) <= 'm')"
                 " DO INSTEAD INSERT INTO products_i_a_m VALUES (new.*)"),
                ("CREATE RULE products_insert_n_z AS ON INSERT TO products_i"
                 " WHERE (lower(left(productname,1)) > 'm' AND lower(left(productname,1)) <= 'z')"
                 " DO INSTEAD INSERT INTO products_i_n_z VALUES (new.*)"),
                "INSERT INTO products_i (productid, productname, unitprice) SELECT productid, productname, unitprice FROM products",
            ]:
                cur.execute(sql)
            cur.execute(
                "SELECT 'A–M (products_i_a_m)' AS part, COUNT(*) FROM products_i_a_m"
                " UNION ALL SELECT 'N–Z (products_i_n_z)', COUNT(*) FROM products_i_n_z"
                " UNION ALL SELECT 'Parent only (ONLY products_i)', COUNT(*) FROM ONLY products_i"
            )
            counts = [{'part': r[0], 'count': r[1]} for r in cur.fetchall()]
            cur.execute("SELECT productname FROM products_i ORDER BY productname LIMIT 8")
            samples = [r[0] for r in cur.fetchall()]
            return jsonify({'ok': True, 'mode': mode, 'counts': counts, 'samples': samples})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ──────────────── Chapter 6: Database Migration ────────────────

def _pg_connect_direct(conn_id: int):
    """Return a psycopg2 connection (autocommit=False) for transaction demos."""
    import psycopg2
    rec = meta_db.get_connection_by_id(conn_id)
    p   = rec['conn_params']
    return psycopg2.connect(
        host=p.get('host', 'localhost'),
        port=int(p.get('port', 5432)),
        dbname=p.get('database', 'postgres'),
        user=p.get('username', 'postgres'),
        password=rec.get('password', ''),
    )


@demos_bp.route('/migration')
@login_required
def migration():
    pg_conns = _conns_by_type('postgresql')
    return render_template('demos/migration.html', has_pg=bool(pg_conns))


@demos_bp.route('/migration/setup', methods=['POST'])
@login_required
def migration_setup():
    import pyodbc
    pg_conns = _conns_by_type('postgresql')
    if not pg_conns:
        return jsonify({'ok': False, 'error': 'No PostgreSQL connection configured'})
    steps = []
    try:
        pg = _pg_connect_direct(pg_conns[0]['id'])
        pg.autocommit = True
        cur = pg.cursor()

        # Drop & recreate tables (migration DDL)
        for sql in [
            "DROP TABLE IF EXISTS orderdetails CASCADE",
            "DROP TABLE IF EXISTS orders CASCADE",
            "DROP TABLE IF EXISTS products CASCADE",
            "DROP TABLE IF EXISTS customers CASCADE",
            ("CREATE TABLE customers ("
             "  customerid CHAR(5) PRIMARY KEY,"
             "  companyname VARCHAR(40) NOT NULL,"
             "  contactname VARCHAR(30),"
             "  country VARCHAR(15),"
             "  balance NUMERIC(10,2) DEFAULT 10000)"),
            ("CREATE TABLE products ("
             "  productid INT PRIMARY KEY,"
             "  productname VARCHAR(40) NOT NULL,"
             "  unitprice NUMERIC(10,4) DEFAULT 0,"
             "  unitsinstock SMALLINT DEFAULT 0,"
             "  discontinued BOOLEAN DEFAULT FALSE)"),
            ("CREATE TABLE orders ("
             "  orderid INT PRIMARY KEY,"
             "  customerid CHAR(5) REFERENCES customers(customerid),"
             "  orderdate TIMESTAMP DEFAULT NOW())"),
            ("CREATE TABLE orderdetails ("
             "  orderid INT REFERENCES orders(orderid),"
             "  productid INT REFERENCES products(productid),"
             "  unitprice NUMERIC(10,4) DEFAULT 0,"
             "  quantity SMALLINT DEFAULT 1,"
             "  discount REAL DEFAULT 0,"
             "  PRIMARY KEY (orderid, productid))"),
        ]:
            cur.execute(sql)
        steps.append({'step': 'DDL — 4 tables created', 'ok': True})

        # Load from SQL Server Northwind
        c = current_app.config
        with pyodbc.connect(_build_conn_str(c), autocommit=True) as ss:
            sc = ss.cursor()

            sc.execute("SELECT CustomerID, CompanyName, ContactName, Country FROM Customers")
            rows = sc.fetchall()
            cur.executemany(
                "INSERT INTO customers (customerid,companyname,contactname,country) VALUES (%s,%s,%s,%s)",
                rows)
            steps.append({'step': f'Customers: {len(rows)} rows', 'ok': True})

            sc.execute("SELECT ProductID, ProductName, UnitPrice, UnitsInStock, Discontinued FROM Products")
            rows = sc.fetchall()
            cur.executemany(
                "INSERT INTO products (productid,productname,unitprice,unitsinstock,discontinued) VALUES (%s,%s,%s,%s,%s)",
                [(r[0], r[1], r[2], r[3], bool(r[4])) for r in rows])
            steps.append({'step': f'Products: {len(rows)} rows', 'ok': True})

            sc.execute("SELECT TOP 100 OrderID, CustomerID, OrderDate FROM Orders ORDER BY OrderDate DESC")
            orders = sc.fetchall()
            cur.executemany(
                "INSERT INTO orders (orderid,customerid,orderdate) VALUES (%s,%s,%s)",
                orders)
            steps.append({'step': f'Orders: {len(orders)} rows (top 100 latest)', 'ok': True})

            oids = [r[0] for r in orders]
            placeholders = ','.join('?' for _ in oids)
            sc.execute(
                f"SELECT OrderID,ProductID,UnitPrice,Quantity,Discount FROM [Order Details] WHERE OrderID IN ({placeholders})",
                oids)
            rows = sc.fetchall()
            cur.executemany(
                "INSERT INTO orderdetails (orderid,productid,unitprice,quantity,discount) VALUES (%s,%s,%s,%s,%s)",
                rows)
            steps.append({'step': f'Order details: {len(rows)} rows', 'ok': True})

        # Stored function new_order()
        cur.execute("""
            CREATE OR REPLACE FUNCTION new_order(
                var_custid CHAR(5), var_prodid INT, var_qty SMALLINT)
            RETURNS VOID LANGUAGE plpgsql AS $$
            DECLARE
                var_orderid  INT;
                var_price    NUMERIC(10,4);
                var_value    NUMERIC(10,4);
                var_balance  NUMERIC(10,2);
                var_stock    SMALLINT;
            BEGIN
                SELECT unitprice, unitsinstock INTO var_price, var_stock
                FROM products WHERE productid = var_prodid;
                var_value := var_price * var_qty;
                SELECT balance INTO var_balance FROM customers WHERE customerid = var_custid;
                IF var_balance < var_value THEN
                    RAISE EXCEPTION 'Insufficient balance: % < %', var_balance, var_value;
                END IF;
                IF var_stock < var_qty THEN
                    RAISE EXCEPTION 'Insufficient stock: % < %', var_stock, var_qty;
                END IF;
                SELECT COALESCE(MAX(orderid),0)+1 INTO var_orderid FROM orders;
                UPDATE customers SET balance = balance - var_value WHERE customerid = var_custid;
                UPDATE products  SET unitsinstock = unitsinstock - var_qty WHERE productid = var_prodid;
                INSERT INTO orders (orderid, customerid) VALUES (var_orderid, var_custid);
                INSERT INTO orderdetails (orderid,productid,unitprice,quantity)
                VALUES (var_orderid, var_prodid, var_price, var_qty);
            END; $$
        """)
        steps.append({'step': 'Stored function new_order() created', 'ok': True})

        pg.close()
        return jsonify({'ok': True, 'steps': steps})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'steps': steps})


@demos_bp.route('/migration/status')
@login_required
def migration_status():
    pg_conns = _conns_by_type('postgresql')
    if not pg_conns:
        return jsonify({'ok': False, 'error': 'No PostgreSQL connection'})
    try:
        pg = _pg_connect_direct(pg_conns[0]['id'])
        pg.autocommit = True
        cur = pg.cursor()
        counts = {}
        for tbl in ('customers', 'products', 'orders', 'orderdetails'):
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            counts[tbl] = cur.fetchone()[0]
        cur.execute("""
            SELECT routine_name FROM information_schema.routines
            WHERE routine_type='FUNCTION' AND routine_name='new_order'
        """)
        counts['new_order_fn'] = cur.fetchone() is not None
        pg.close()
        return jsonify({'ok': True, 'counts': counts})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/migration/last-5-orders')
@login_required
def migration_last5():
    pg_conns = _conns_by_type('postgresql')
    if not pg_conns:
        return jsonify({'ok': False, 'error': 'No PostgreSQL connection'})
    sql = (
        "SELECT o.orderdate::timestamp(0) AS orderdate,"
        " c.companyname, c.country, c.balance,"
        " p.productname, od.quantity,"
        " od.quantity * od.unitprice AS value,"
        " p.unitsinstock"
        " FROM products p"
        " JOIN orderdetails od ON p.productid = od.productid"
        " JOIN orders o        ON o.orderid = od.orderid"
        " JOIN customers c     ON c.customerid = o.customerid"
        " ORDER BY orderdate DESC LIMIT 5"
    )
    try:
        pg = _pg_connect_direct(pg_conns[0]['id'])
        pg.autocommit = True
        cur = pg.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [[str(v) if v is not None else '' for v in r] for r in cur.fetchall()]
        pg.close()
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'sql': sql})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'sql': sql})


@demos_bp.route('/migration/transaction-demo', methods=['POST'])
@login_required
def migration_transaction_demo():
    inject_error = (request.json or {}).get('inject_error', False)
    pg_conns = _conns_by_type('postgresql')
    if not pg_conns:
        return jsonify({'ok': False, 'error': 'No PostgreSQL connection'})

    trace       = []
    cust_id     = None
    prod_id     = None
    prod_name   = None
    price       = None
    balance_before = None
    stock_before   = None
    pg = None

    try:
        pg = _pg_connect_direct(pg_conns[0]['id'])
        pg.autocommit = True
        cur = pg.cursor()

        # Read initial state (outside transaction, autocommit)
        cur.execute(
            "SELECT customerid, companyname, balance FROM customers"
            " ORDER BY customerid LIMIT 1")
        row = cur.fetchone()
        cust_id, cust_name, balance_before = row[0].strip(), row[1], float(row[2])

        cur.execute(
            "SELECT productid, productname, unitprice, unitsinstock"
            " FROM products WHERE unitsinstock > 5 ORDER BY productid LIMIT 1")
        row = cur.fetchone()
        prod_id, prod_name, price, stock_before = row[0], row[1], float(row[2]), int(row[3])

        trace.append({'sql': (
            f"-- Initial state\n"
            f"-- Customer:  {cust_id} ({cust_name}), balance = {balance_before:.2f}\n"
            f"-- Product:   {prod_id} ({prod_name}), stock = {stock_before}, price = {price:.4f}"
        ), 'status': 'info'})

        # Begin explicit transaction
        pg.autocommit = False
        trace.append({'sql': 'BEGIN; -- start transaction', 'status': 'begin'})

        # Step 1: deduct customer balance
        cur.execute(
            "UPDATE customers SET balance = balance - %s WHERE customerid = %s",
            (price, cust_id))
        trace.append({'sql': (
            f"UPDATE customers\n"
            f"  SET balance = balance - {price:.4f}\n"
            f"  WHERE customerid = '{cust_id}';\n"
            f"-- balance: {balance_before:.2f} → {balance_before - price:.2f}"
        ), 'status': 'ok'})

        # Step 2: deduct product stock
        cur.execute(
            "UPDATE products SET unitsinstock = unitsinstock - 1 WHERE productid = %s",
            (prod_id,))
        trace.append({'sql': (
            f"UPDATE products\n"
            f"  SET unitsinstock = unitsinstock - 1\n"
            f"  WHERE productid = {prod_id};\n"
            f"-- stock: {stock_before} → {stock_before - 1}"
        ), 'status': 'ok'})

        # Step 3: insert order (possibly with FK error)
        cur.execute("SELECT COALESCE(MAX(orderid),0)+1 FROM orders")
        next_id = cur.fetchone()[0]
        customer_to_insert = 'ERROR' if inject_error else cust_id
        try:
            cur.execute(
                "INSERT INTO orders (orderid, customerid) VALUES (%s, %s)",
                (next_id, customer_to_insert))
            trace.append({'sql': (
                f"INSERT INTO orders (orderid, customerid)\n"
                f"  VALUES ({next_id}, '{customer_to_insert}');"
            ), 'status': 'ok'})
        except Exception as insert_err:
            trace.append({'sql': (
                f"INSERT INTO orders (orderid, customerid)\n"
                f"  VALUES ({next_id}, '{customer_to_insert}');\n"
                f"-- FK violation: '{customer_to_insert}' not in customers!"
            ), 'status': 'error'})
            raise

        pg.commit()
        trace.append({'sql': 'COMMIT; -- ✓ all changes persisted', 'status': 'commit'})

        # Read post-commit state, then clean up
        pg.autocommit = True
        cur.execute("SELECT balance FROM customers WHERE customerid = %s", (cust_id,))
        balance_after = float(cur.fetchone()[0])
        cur.execute("SELECT unitsinstock FROM products WHERE productid = %s", (prod_id,))
        stock_after = int(cur.fetchone()[0])
        # Restore test data
        cur.execute("DELETE FROM orders WHERE orderid = %s", (next_id,))
        cur.execute("UPDATE customers SET balance = %s WHERE customerid = %s", (balance_before, cust_id))
        cur.execute("UPDATE products  SET unitsinstock = %s WHERE productid = %s", (stock_before, prod_id))
        trace.append({'sql': '-- (test data cleaned up — demo only)', 'status': 'info'})

        return jsonify({'ok': True, 'result': 'COMMITTED',
                        'cust_id': cust_id, 'prod_name': prod_name, 'price': price,
                        'balance_before': balance_before, 'balance_after': balance_after,
                        'stock_before': stock_before, 'stock_after': stock_after,
                        'trace': trace})
    except Exception as e:
        if pg and not pg.autocommit:
            try:
                pg.rollback()
            except Exception:
                pass
        trace.append({'sql': f'-- ✗ Error: {str(e)[:250]}', 'status': 'error'})
        trace.append({'sql': 'ROLLBACK; -- ↩ ALL changes automatically undone', 'status': 'rollback'})

        balance_after = None
        stock_after   = None
        if pg and cust_id:
            try:
                pg.autocommit = True
                cur2 = pg.cursor()
                cur2.execute("SELECT balance FROM customers WHERE customerid = %s", (cust_id,))
                r = cur2.fetchone()
                balance_after = float(r[0]) if r else None
                cur2.execute("SELECT unitsinstock FROM products WHERE productid = %s", (prod_id,))
                r = cur2.fetchone()
                stock_after = int(r[0]) if r else None
            except Exception:
                pass

        return jsonify({'ok': True, 'result': 'ROLLED BACK',
                        'cust_id': cust_id, 'prod_name': prod_name, 'price': price,
                        'balance_before': balance_before, 'balance_after': balance_after,
                        'stock_before': stock_before, 'stock_after': stock_after,
                        'trace': trace, 'error': str(e)[:300]})
    finally:
        if pg:
            try:
                pg.close()
            except Exception:
                pass


# ──────────────── Chapter 7: Cloud DB / BigQuery ML ────────────────

_NW_ML_SQL = """
    SELECT
        od.UnitPrice * od.Quantity * (1 - od.Discount) AS value_numeric,
        c.Country                                        AS country,
        CAST(p.CategoryID AS INT)                        AS categoryid,
        CAST(p.UnitPrice  AS FLOAT)                      AS p_unitprice,
        CAST(od.Discount  AS FLOAT)                      AS discount,
        CAST(YEAR(o.OrderDate) AS INT)                   AS pyear
    FROM Customers c
    JOIN Orders o             ON c.CustomerID  = o.CustomerID
    JOIN [Order Details] od   ON o.OrderID     = od.OrderID
    JOIN Products p           ON od.ProductID  = p.ProductID
    WHERE od.UnitPrice * od.Quantity * (1 - od.Discount) > 0
"""


def _fetch_nw_ml_df():
    """Return a pandas DataFrame of the Northwind ML denormalized view."""
    import pyodbc, pandas as pd
    c = current_app.config
    with pyodbc.connect(_build_conn_str(c), autocommit=True) as conn:
        import pandas as pd
        df = pd.read_sql(_NW_ML_SQL, conn)
    df = df.dropna()
    df['categoryid'] = df['categoryid'].astype(str)
    return df


def _build_pipeline(df):
    """Fit LinearRegression pipeline; return (pipe, X_test, y_test, y_pred_test)."""
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split

    X = df[['country', 'categoryid', 'p_unitprice', 'discount', 'pyear']]
    y = df['value_numeric'].astype(float)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    pre = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False),
         ['country', 'categoryid']),
        ('num', 'passthrough', ['p_unitprice', 'discount', 'pyear']),
    ])
    pipe = Pipeline([('pre', pre), ('lr', LinearRegression())])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    return pipe, X_test, y_test, y_pred


@demos_bp.route('/bqml')
@login_required
def bqml():
    return render_template('demos/bqml.html')


@demos_bp.route('/bqml/source-data')
@login_required
def bqml_source_data():
    try:
        import numpy as np
        df = _fetch_nw_ml_df()
        v = df['value_numeric'].astype(float)
        hist_vals, edges = np.histogram(v.clip(0, 5000), bins=20)
        sample = df.head(8)[['value_numeric', 'country', 'categoryid',
                               'p_unitprice', 'discount', 'pyear']].round(2)
        countries = sorted(df['country'].unique().tolist())
        return jsonify({
            'ok': True,
            'n_rows': len(df),
            'countries': len(countries),
            'years': sorted(df['pyear'].unique().tolist()),
            'categories': sorted(df['categoryid'].unique().tolist()),
            'value_min':   round(float(v.min()), 2),
            'value_max':   round(float(v.max()), 2),
            'value_mean':  round(float(v.mean()), 2),
            'value_median':round(float(v.median()), 2),
            'hist': {'counts': hist_vals.tolist(), 'edges': [round(e, 1) for e in edges.tolist()]},
            'sample': sample.values.tolist(),
            'sample_cols': list(sample.columns),
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/bqml/train', methods=['POST'])
@login_required
def bqml_train():
    try:
        import numpy as np
        from sklearn.metrics import (mean_absolute_error, r2_score,
                                     explained_variance_score)

        df   = _fetch_nw_ml_df()
        pipe, X_test, y_test, y_pred = _build_pipeline(df)

        mae = float(mean_absolute_error(y_test, y_pred))
        r2  = float(r2_score(y_test, y_pred))
        evs = float(explained_variance_score(y_test, y_pred))

        # Scatter: actual vs predicted (sample 300)
        rng = np.random.default_rng(7)
        idx = rng.choice(len(y_test), min(300, len(y_test)), replace=False)
        y_t_arr = y_test.to_numpy()
        scatter = {
            'actual':    y_t_arr[idx].tolist(),
            'predicted': y_pred[idx].tolist(),
        }

        # Coefficients
        pre  = pipe.named_steps['pre']
        lr   = pipe.named_steps['lr']
        feat = (list(pre.named_transformers_['cat']
                     .get_feature_names_out(['country', 'categoryid']))
                + ['p_unitprice', 'discount', 'pyear'])
        coefs = sorted(zip(feat, lr.coef_.tolist()),
                       key=lambda x: abs(x[1]), reverse=True)[:15]

        return jsonify({
            'ok': True,
            'n_total': len(df),
            'n_train': len(df) - len(X_test),
            'n_test':  len(X_test),
            'mae':     round(mae, 1),
            'r2':      round(r2 * 100, 1),
            'evs':     round(evs * 100, 1),
            'scatter': scatter,
            'coefs':   [(n, round(c, 2)) for n, c in coefs],
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/bqml/predict', methods=['POST'])
@login_required
def bqml_predict():
    try:
        import numpy as np
        threshold = float((request.json or {}).get('threshold', 0.4))

        df   = _fetch_nw_ml_df()
        pipe, X_test, y_test, y_pred = _build_pipeline(df)

        y_t = y_test.to_numpy()
        err_pct = np.abs(y_pred - y_t) / np.maximum(y_t, 1e-9)
        mask    = err_pct < threshold

        good = []
        countries = X_test['country'].to_numpy()
        for i in np.where(mask)[0][:10]:
            good.append({
                'actual':    round(float(y_t[i]), 2),
                'predicted': round(float(y_pred[i]), 2),
                'error_pct': round(float(err_pct[i]) * 100, 1),
                'country':   str(countries[i]),
            })

        # Worst predictions
        worst_idx = np.argsort(err_pct)[-8:][::-1]
        worst = []
        for i in worst_idx:
            worst.append({
                'actual':    round(float(y_t[i]), 2),
                'predicted': round(float(y_pred[i]), 2),
                'error_pct': round(float(err_pct[i]) * 100, 1),
                'country':   str(countries[i]),
            })

        return jsonify({
            'ok': True,
            'n_test': int(len(y_t)),
            'n_within': int(mask.sum()),
            'threshold_pct': int(threshold * 100),
            'good': good,
            'worst': worst,
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/bqml/train-nominal', methods=['POST'])
@login_required
def bqml_train_nominal():
    try:
        import numpy as np
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, classification_report

        df = _fetch_nw_ml_df()
        df['value_nominal'] = df['value_numeric'].apply(
            lambda v: 'L' if v < 200 else ('M' if v < 1200 else 'H'))

        X = df[['country', 'categoryid', 'p_unitprice', 'discount', 'pyear']]
        y = df['value_nominal']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y)

        pre = ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False),
             ['country', 'categoryid']),
            ('num', 'passthrough', ['p_unitprice', 'discount', 'pyear']),
        ])
        pipe = Pipeline([('pre', pre),
                          ('clf', LogisticRegression(max_iter=500, random_state=42))])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        rep = classification_report(y_test, y_pred, output_dict=True)

        dist = df['value_nominal'].value_counts().to_dict()

        # Confusion matrix counts
        from sklearn.metrics import confusion_matrix
        labels = ['L', 'M', 'H']
        cm = confusion_matrix(y_test, y_pred, labels=labels)

        return jsonify({
            'ok': True,
            'n_total': len(df), 'n_train': len(X_train), 'n_test': len(X_test),
            'accuracy': round(acc * 100, 1),
            'dist': dist,
            'per_class': {
                k: {'precision': round(v['precision']*100,1),
                    'recall':    round(v['recall']*100,1),
                    'f1':        round(v['f1-score']*100,1)}
                for k, v in rep.items() if k in ('L','M','H')
            },
            'cm': cm.tolist(),
            'cm_labels': labels,
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/bqml/natality-predict', methods=['POST'])
@login_required
def bqml_natality_predict():
    try:
        data       = request.json or {}
        is_male    = bool(data.get('is_male', True))
        gestation  = int(data.get('gestation_weeks', 40))
        mother_age = int(data.get('mother_age', 28))
        mother_race = str(data.get('mother_race', '1'))

        # Approximate formula derived from BQML natality model coefficients
        # (published in GCP documentation / course demos)
        base        = 7.302
        male_bonus  = 0.276 if is_male else 0.0
        gest_coef   = 0.460   # per week above/below 39
        age_coef    = 0.012   # per year of mother age (slight positive)
        race_adj    = {'1': 0.0, '2': -0.21, '3': -0.14, '6': -0.05,
                       '38': -0.04, '7': -0.10}
        pred = (base
                + male_bonus
                + gest_coef * (gestation - 39)
                + age_coef  * (mother_age - 28)
                + race_adj.get(mother_race, -0.05))
        pred = max(0.5, round(pred, 3))
        pred_kg = round(pred * 0.453592, 3)

        return jsonify({
            'ok': True,
            'weight_pounds': pred,
            'weight_kg':     pred_kg,
            'inputs': {
                'is_male': is_male,
                'gestation_weeks': gestation,
                'mother_age': mother_age,
                'mother_race': mother_race,
            }
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ── Chapter 8: Graph Tables, Neo4j, BLOB ──────────────────────────────────────

_C8_SETUP_SQLS = [
    # node tables
    "IF OBJECT_ID('likes','U') IS NOT NULL DROP TABLE likes",
    "IF OBJECT_ID('friendof','U') IS NOT NULL DROP TABLE friendof",
    "IF OBJECT_ID('livesin','U') IS NOT NULL DROP TABLE livesin",
    "IF OBJECT_ID('locatedin','U') IS NOT NULL DROP TABLE locatedin",
    "IF OBJECT_ID('person','U') IS NOT NULL DROP TABLE person",
    "IF OBJECT_ID('restaurant','U') IS NOT NULL DROP TABLE restaurant",
    "IF OBJECT_ID('city','U') IS NOT NULL DROP TABLE city",
    "CREATE TABLE person (id INTEGER PRIMARY KEY, name VARCHAR(100)) AS NODE",
    "CREATE TABLE restaurant (id INTEGER NOT NULL, name VARCHAR(100)) AS NODE",
    "CREATE TABLE city (id INTEGER PRIMARY KEY, name VARCHAR(100), statename VARCHAR(100)) AS NODE",
    # edge tables
    "CREATE TABLE likes (rating INTEGER) AS EDGE",
    "CREATE TABLE friendof AS EDGE",
    "ALTER TABLE friendof ADD CONSTRAINT ec_friendof_1 CONNECTION (person TO person)",
    "CREATE TABLE livesin AS EDGE",
    "CREATE TABLE locatedin AS EDGE",
    # person nodes
    "INSERT INTO person VALUES (1,'john')",
    "INSERT INTO person VALUES (2,'mary')",
    "INSERT INTO person VALUES (3,'alice')",
    "INSERT INTO person VALUES (4,'jacob')",
    "INSERT INTO person VALUES (5,'julie')",
    "INSERT INTO person VALUES (6,'tom')",
    # restaurant nodes
    "INSERT INTO restaurant VALUES (1,'taco dell')",
    "INSERT INTO restaurant VALUES (2,'ginger and spice')",
    "INSERT INTO restaurant VALUES (3,'noodle land')",
    # city nodes
    "INSERT INTO city VALUES (1,'bellevue','wa')",
    "INSERT INTO city VALUES (2,'seattle','wa')",
    "INSERT INTO city VALUES (3,'redmond','wa')",
    # likes edges
    "INSERT INTO likes VALUES ((SELECT $node_id FROM person WHERE id=1),(SELECT $node_id FROM restaurant WHERE id=1),9)",
    "INSERT INTO likes VALUES ((SELECT $node_id FROM person WHERE id=2),(SELECT $node_id FROM restaurant WHERE id=2),9)",
    "INSERT INTO likes VALUES ((SELECT $node_id FROM person WHERE id=3),(SELECT $node_id FROM restaurant WHERE id=3),9)",
    "INSERT INTO likes VALUES ((SELECT $node_id FROM person WHERE id=4),(SELECT $node_id FROM restaurant WHERE id=3),9)",
    "INSERT INTO likes VALUES ((SELECT $node_id FROM person WHERE id=5),(SELECT $node_id FROM restaurant WHERE id=3),9)",
    # livesin edges
    "INSERT INTO livesin VALUES ((SELECT $node_id FROM person WHERE id=1),(SELECT $node_id FROM city WHERE id=1))",
    "INSERT INTO livesin VALUES ((SELECT $node_id FROM person WHERE id=2),(SELECT $node_id FROM city WHERE id=2))",
    "INSERT INTO livesin VALUES ((SELECT $node_id FROM person WHERE id=3),(SELECT $node_id FROM city WHERE id=3))",
    "INSERT INTO livesin VALUES ((SELECT $node_id FROM person WHERE id=4),(SELECT $node_id FROM city WHERE id=3))",
    "INSERT INTO livesin VALUES ((SELECT $node_id FROM person WHERE id=5),(SELECT $node_id FROM city WHERE id=1))",
    # locatedin edges
    "INSERT INTO locatedin VALUES ((SELECT $node_id FROM restaurant WHERE id=1),(SELECT $node_id FROM city WHERE id=1))",
    "INSERT INTO locatedin VALUES ((SELECT $node_id FROM restaurant WHERE id=2),(SELECT $node_id FROM city WHERE id=2))",
    "INSERT INTO locatedin VALUES ((SELECT $node_id FROM restaurant WHERE id=3),(SELECT $node_id FROM city WHERE id=3))",
    # friendof edges (directed; undirected needs 2 edges per pair)
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=1),(SELECT $node_id FROM person WHERE id=2))",
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=1),(SELECT $node_id FROM person WHERE id=5))",
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=2),(SELECT $node_id FROM person WHERE id=3))",
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=3),(SELECT $node_id FROM person WHERE id=2))",
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=3),(SELECT $node_id FROM person WHERE id=5))",
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=3),(SELECT $node_id FROM person WHERE id=6))",
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=4),(SELECT $node_id FROM person WHERE id=2))",
    "INSERT INTO friendof VALUES ((SELECT $node_id FROM person WHERE id=5),(SELECT $node_id FROM person WHERE id=4))",
]

_C8_QUERIES = {
    1: {
        'title': "John's friends",
        'match': "MATCH(p1-(friendof)->p2)",
        'sql': """SELECT p2.name
FROM person p1, person p2, friendof
WHERE MATCH(p1-(friendof)->p2)
  AND p1.name = 'john'""",
    },
    2: {
        'title': "John's liked restaurants",
        'match': "MATCH(person-(likes)->restaurant)",
        'sql': """SELECT restaurant.name
FROM person, likes, restaurant
WHERE MATCH(person-(likes)->restaurant)
  AND person.name = 'john'""",
    },
    3: {
        'title': "Restaurants liked by John's friends",
        'match': "MATCH(p1-(friendof)->p2-(likes)->restaurant)",
        'sql': """SELECT restaurant.name
FROM person person1, person person2, likes, friendof, restaurant
WHERE MATCH(person1-(friendof)->person2-(likes)->restaurant)
  AND person1.name = 'john'""",
    },
    4: {
        'title': "Persons who like a restaurant in the city they live in",
        'match': "MATCH(person-(likes)->restaurant-(locatedin)->city AND person-(livesin)->city)",
        'sql': """SELECT person.id, person.name
FROM person, likes, restaurant, livesin, city, locatedin
WHERE MATCH(person-(likes)->restaurant-(locatedin)->city
        AND person-(livesin)->city)""",
    },
    5: {
        'title': "Persons whose friend likes a restaurant in the friend's own city",
        'match': "MATCH(p1-(friendof)->p2 AND p2-(likes)->restaurant-(locatedin)->city AND p2-(livesin)->city)",
        'sql': """SELECT DISTINCT p1.id, p1.name
FROM person p1, person p2, friendof, likes, restaurant, livesin, city, locatedin
WHERE MATCH(p1-(friendof)->p2
        AND p2-(likes)->restaurant-(locatedin)->city
        AND p2-(livesin)->city)""",
    },
    6: {
        'title': "Pairs of people with a common friend",
        'match': "MATCH(p1-(f1)->p0 AND p2-(f2)->p0)",
        'sql': """SELECT p0.name person, p1.name Friend1, p2.name Friend2
FROM person p1, friendof f1, person p2, friendof f2, person p0
WHERE MATCH(p1-(f1)->p0 AND p2-(f2)->p0)
  AND p1.id <> p2.id""",
    },
    7: {
        'title': "SHORTEST_PATH: all paths from John",
        'match': "SHORTEST_PATH(p1(-(friend)->p2)+)",
        'sql': """SELECT p1.name,
    p1.name + '->' + STRING_AGG(p2.name,'->') WITHIN GROUP (GRAPH PATH) paths,
    LAST_VALUE(p2.name) WITHIN GROUP (GRAPH PATH) last_name,
    COUNT(p2.name) WITHIN GROUP (GRAPH PATH) depth
FROM person p1, person FOR PATH AS p2,
    friendof FOR PATH AS friend
WHERE MATCH(SHORTEST_PATH(p1(-(friend)->p2)+))
  AND p1.name = 'john'""",
    },
}

_C8_REL_SETUP_SQLS = [
    "IF OBJECT_ID('r_friendof','U') IS NOT NULL DROP TABLE r_friendof",
    "IF OBJECT_ID('r_likes','U') IS NOT NULL DROP TABLE r_likes",
    "IF OBJECT_ID('r_person','U') IS NOT NULL DROP TABLE r_person",
    "IF OBJECT_ID('r_restaurant','U') IS NOT NULL DROP TABLE r_restaurant",
    "IF OBJECT_ID('r_city','U') IS NOT NULL DROP TABLE r_city",
    "CREATE TABLE r_city (id INT PRIMARY KEY, name VARCHAR(100), statename VARCHAR(100))",
    "CREATE TABLE r_person (id INT PRIMARY KEY, name VARCHAR(100), city_id INT REFERENCES r_city)",
    "CREATE TABLE r_restaurant (id INT PRIMARY KEY, name VARCHAR(100), city_id INT REFERENCES r_city)",
    "CREATE TABLE r_likes (person_id INT NOT NULL REFERENCES r_person, restaurant_id INT NOT NULL REFERENCES r_restaurant, rating INT, CONSTRAINT pk_r_likes PRIMARY KEY (person_id, restaurant_id))",
    "CREATE TABLE r_friendof (person1_id INT NOT NULL REFERENCES r_person, person2_id INT NOT NULL REFERENCES r_person, CONSTRAINT pk_r_friendof PRIMARY KEY (person1_id, person2_id))",
    "INSERT r_city VALUES (1,'bellevue','wa'),(2,'seattle','wa'),(3,'redmond','wa')",
    "INSERT r_person VALUES (1,'john',1),(5,'julie',1),(4,'jacob',3),(3,'alice',3),(2,'mary',2)",
    "INSERT r_restaurant VALUES (1,'taco dell',1),(2,'ginger and spice',2),(3,'noodle land',3)",
    "INSERT r_likes VALUES (1,1,9),(2,2,9),(3,3,9),(4,3,9),(5,3,9)",
    "INSERT r_friendof VALUES (1,2),(1,5),(2,3),(3,5),(4,2),(5,4)",
]

_C8_REL_QUERIES = {
    1: {
        'title': "John's friends (relational)",
        'sql': """SELECT p2.name
FROM r_person p1
  JOIN r_friendof f ON p1.id = f.person1_id
  JOIN r_person p2 ON p2.id = f.person2_id
WHERE p1.name = 'john'""",
    },
    2: {
        'title': "John's liked restaurants (relational)",
        'sql': """SELECT r.name
FROM r_restaurant r
  JOIN r_likes l ON r.id = l.restaurant_id
  JOIN r_person p ON p.id = l.person_id
WHERE p.name = 'john'""",
    },
    3: {
        'title': "Restaurants liked by John's friends (relational)",
        'sql': """SELECT r.name
FROM r_person p1
  JOIN r_friendof f ON p1.id = f.person1_id
  JOIN r_person p2 ON p2.id = f.person2_id
  JOIN r_likes l ON l.person_id = p2.id
  JOIN r_restaurant r ON r.id = l.restaurant_id
WHERE p1.name = 'john'""",
    },
    4: {
        'title': "Persons liking a restaurant in their own city (relational)",
        'sql': """SELECT p.name
FROM r_restaurant r
  JOIN r_likes l ON r.id = l.restaurant_id
  JOIN r_person p ON p.id = l.person_id
WHERE r.city_id = p.city_id""",
    },
    5: {
        'title': "Persons whose friend likes a restaurant in the friend's city (relational)",
        'sql': """SELECT DISTINCT p1.name
FROM r_person p1
  JOIN r_friendof f ON p1.id = f.person1_id
  JOIN r_person p2 ON p2.id = f.person2_id
  JOIN r_likes l ON l.person_id = p2.id
  JOIN r_restaurant r ON r.id = l.restaurant_id
WHERE r.city_id = p2.city_id""",
    },
}

_C8_NW_VIEWS_SQLS = [
    "IF OBJECT_ID('vi_orders_products','V') IS NOT NULL DROP VIEW vi_orders_products",
    "IF OBJECT_ID('vi_orders','V') IS NOT NULL DROP VIEW vi_orders",
    "IF OBJECT_ID('vi_products','V') IS NOT NULL DROP VIEW vi_products",
    """CREATE VIEW vi_products AS
SELECT productid, productname FROM Products""",
    """CREATE VIEW vi_orders AS
SELECT orderid, CAST(orderdate AS DATE) odate FROM Orders""",
    """CREATE VIEW vi_orders_products AS
SELECT o.orderid, p.productid, od.Quantity quantity,
    od.Quantity * od.UnitPrice * (1 - od.Discount) price
FROM Orders o
  JOIN [Order Details] od ON o.orderid = od.OrderID
  JOIN Products p ON od.ProductID = p.productid""",
]


@demos_bp.route('/c8-graph')
@login_required
def c8_graph():
    return render_template('demos/c8_graph.html')


@demos_bp.route('/c8-graph/setup', methods=['POST'])
@login_required
def c8_graph_setup():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    errors = []
    done   = []
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            for sql in _C8_SETUP_SQLS:
                try:
                    cur.execute(sql)
                    done.append(sql[:60])
                except Exception as e:
                    errors.append({'sql': sql[:60], 'error': str(e)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})
    return jsonify({'ok': True, 'steps': len(done), 'errors': errors})


@demos_bp.route('/c8-graph/query/<int:qnum>')
@login_required
def c8_graph_query(qnum):
    import pyodbc
    q = _C8_QUERIES.get(qnum)
    if not q:
        return jsonify({'ok': False, 'error': 'unknown query'}), 404
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute(q['sql'])
            cols = [d[0] for d in cur.description]
            rows = [list(r) for r in cur.fetchall()]
        return jsonify({'ok': True, 'title': q['title'], 'match': q.get('match',''),
                        'sql': q['sql'], 'cols': cols, 'rows': rows})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'sql': q['sql']})


@demos_bp.route('/c8-graph/relational-setup', methods=['POST'])
@login_required
def c8_graph_relational_setup():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    errors = []
    done   = []
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            for sql in _C8_REL_SETUP_SQLS:
                try:
                    cur.execute(sql)
                    done.append(sql[:60])
                except Exception as e:
                    errors.append({'sql': sql[:60], 'error': str(e)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})
    return jsonify({'ok': True, 'steps': len(done), 'errors': errors})


@demos_bp.route('/c8-graph/relational-query/<int:qnum>')
@login_required
def c8_graph_relational_query(qnum):
    import pyodbc
    q = _C8_REL_QUERIES.get(qnum)
    if not q:
        return jsonify({'ok': False, 'error': 'unknown query'}), 404
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute(q['sql'])
            cols = [d[0] for d in cur.description]
            rows = [list(r) for r in cur.fetchall()]
        return jsonify({'ok': True, 'title': q['title'], 'sql': q['sql'],
                        'cols': cols, 'rows': rows})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'sql': q['sql']})


@demos_bp.route('/c8-graph/northwind-views', methods=['POST'])
@login_required
def c8_graph_northwind_views():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    errors = []
    done   = []
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            for sql in _C8_NW_VIEWS_SQLS:
                try:
                    cur.execute(sql)
                    done.append(sql[:60])
                except Exception as e:
                    errors.append({'sql': sql[:60], 'error': str(e)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})
    return jsonify({'ok': True, 'steps': len(done), 'errors': errors})


@demos_bp.route('/c8-graph/northwind-orders')
@login_required
def c8_graph_northwind_orders():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT TOP 20 vop.orderid, vo.odate, vp.productname,
                    vop.quantity, ROUND(vop.price,2) price
                FROM vi_orders_products vop
                  JOIN vi_orders vo ON vo.orderid = vop.orderid
                  JOIN vi_products vp ON vp.productid = vop.productid
                ORDER BY vop.orderid DESC, vop.price DESC
            """)
            cols = [d[0] for d in cur.description]
            rows = [list(r) for r in cur.fetchall()]
            # convert date objects to string for JSON
            for row in rows:
                for i, v in enumerate(row):
                    if hasattr(v, 'isoformat'):
                        row[i] = v.isoformat()
        return jsonify({'ok': True, 'cols': cols, 'rows': rows})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ── Chapter 9: In-Memory OLTP (MOT) ──────────────────────────────────────────

def _mot_conn_str(c, db='master'):
    user = (c.get('SQL_SA_USERNAME') or os.environ.get('SQL_SA_USERNAME') or '')
    pw   = (c.get('SQL_SA_PASSWORD') or os.environ.get('SQL_SA_PASSWORD') or '')
    return (
        f"DRIVER={{{c['SQL_DRIVER']}}};SERVER={c['SQL_SERVER']};"
        f"DATABASE={db};UID={user};PWD={pw};"
        f"Encrypt={c['SQL_ENCRYPT']};TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )


def _mot_setup(c):
    """Create mot_bench database with MOT filegroup, disk table, MOT table, and natively compiled proc."""
    import pyodbc
    log = []

    # ── Step 1: create database (in master) ──────────────────────────────────
    with pyodbc.connect(_mot_conn_str(c, 'master'), autocommit=True) as conn:
        cur = conn.cursor()

        # Discover instance data directory
        cur.execute("SELECT SERVERPROPERTY('InstanceDefaultDataPath')")
        data_dir = (cur.fetchone() or [None])[0] or '/var/opt/mssql/data/'
        if not data_dir.endswith('/') and not data_dir.endswith('\\'):
            data_dir += '/'

        cur.execute("SELECT DB_ID('mot_bench')")
        if cur.fetchone()[0] is None:
            cur.execute("CREATE DATABASE mot_bench")
            log.append('Created database mot_bench')
        else:
            log.append('Database mot_bench already exists')

        # ── Step 2: add MOT filegroup ─────────────────────────────────────────
        cur.execute("SELECT COUNT(*) FROM mot_bench.sys.filegroups WHERE type='FX'")
        if cur.fetchone()[0] == 0:
            try:
                cur.execute("ALTER DATABASE mot_bench ADD FILEGROUP mot_fg CONTAINS MEMORY_OPTIMIZED_DATA")
                xtp_path = data_dir + 'mot_bench_xtp'
                cur.execute(
                    f"ALTER DATABASE mot_bench ADD FILE "
                    f"(NAME='mot_xtp', FILENAME='{xtp_path}') TO FILEGROUP mot_fg"
                )
                log.append(f'Added MOT filegroup → {xtp_path}')
            except Exception as e:
                log.append(f'WARNING: MOT filegroup failed ({e}) — MOT tests will be skipped')
        else:
            log.append('MOT filegroup already exists')

        # ELEVATE_TO_SNAPSHOT (required for MOT access from interpreted T-SQL)
        try:
            cur.execute("ALTER DATABASE mot_bench SET MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT = ON")
            log.append('ELEVATE_TO_SNAPSHOT = ON')
        except Exception as e:
            log.append(f'ELEVATE_TO_SNAPSHOT warning: {e}')

    # ── Step 3: create tables and proc (in mot_bench) ────────────────────────
    with pyodbc.connect(_mot_conn_str(c, 'mot_bench'), autocommit=True) as conn:
        cur = conn.cursor()

        # Disk-based table
        cur.execute("""
            IF OBJECT_ID('dbo.t_disk','U') IS NOT NULL DROP TABLE dbo.t_disk
        """)
        cur.execute("""
            CREATE TABLE dbo.t_disk (
                id  INT   NOT NULL PRIMARY KEY,
                val FLOAT NOT NULL
            )
        """)
        log.append('Created dbo.t_disk (disk-based)')

        # Check if MOT filegroup exists before creating MOT table
        cur.execute("""
            SELECT COUNT(*) FROM sys.filegroups WHERE type='FX'
        """)
        mot_ok = cur.fetchone()[0] > 0

        if mot_ok:
            # Drop existing MOT table (can't ALTER)
            cur.execute("""
                IF OBJECT_ID('dbo.t_mot','U') IS NOT NULL DROP TABLE dbo.t_mot
            """)
            cur.execute("""
                CREATE TABLE dbo.t_mot (
                    id  INT   NOT NULL,
                    val FLOAT NOT NULL,
                    CONSTRAINT pk_t_mot PRIMARY KEY NONCLUSTERED HASH (id)
                        WITH (BUCKET_COUNT = 1024)
                ) WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_AND_DATA)
            """)
            log.append('Created dbo.t_mot (memory-optimized, SCHEMA_AND_DATA)')

            # Non-durable cache table
            cur.execute("""
                IF OBJECT_ID('dbo.t_cache','U') IS NOT NULL DROP TABLE dbo.t_cache
            """)
            cur.execute("""
                CREATE TABLE dbo.t_cache (
                    key_col VARCHAR(200) COLLATE Latin1_General_100_BIN2 NOT NULL,
                    val_col NVARCHAR(MAX) NULL,
                    PRIMARY KEY NONCLUSTERED (key_col)
                ) WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY)
            """)
            log.append('Created dbo.t_cache (memory-optimized, SCHEMA_ONLY / non-durable)')

            # Natively compiled stored procedure
            cur.execute("""
                IF OBJECT_ID('dbo.p_insert_mot','P') IS NOT NULL DROP PROCEDURE dbo.p_insert_mot
            """)
            cur.execute("""
                CREATE PROCEDURE dbo.p_insert_mot @id INT, @val FLOAT
                WITH NATIVE_COMPILATION, SCHEMABINDING
                AS BEGIN ATOMIC WITH (
                    TRANSACTION ISOLATION LEVEL = SNAPSHOT,
                    LANGUAGE = N'english'
                )
                    INSERT INTO dbo.t_mot VALUES (@id, @val);
                END
            """)
            log.append('Created dbo.p_insert_mot (natively compiled)')
        else:
            log.append('SKIPPED: MOT table + proc (no MOT filegroup)')

    return {'ok': True, 'log': log, 'mot_available': mot_ok}


def _mot_benchmark(c, n):
    """Run 3-scenario benchmark. Returns ms timings per scenario."""
    import pyodbc, time
    results = {}

    with pyodbc.connect(_mot_conn_str(c, 'mot_bench'), autocommit=True) as conn:
        cur = conn.cursor()

        # ── Scenario 1: disk-based + interpreted T-SQL ────────────────────────
        cur.execute("TRUNCATE TABLE dbo.t_disk")
        sql_disk = f"""
DECLARE @i INT = 0;
WHILE @i < {n} BEGIN
    INSERT INTO dbo.t_disk VALUES (@i, CAST(@i AS FLOAT));
    SET @i += 1;
END
"""
        t0 = time.perf_counter()
        cur.execute(sql_disk)
        results['disk_ms'] = round((time.perf_counter() - t0) * 1000, 1)

        # ── Check MOT availability ────────────────────────────────────────────
        cur.execute("SELECT OBJECT_ID('dbo.t_mot','U')")
        mot_exists = cur.fetchone()[0] is not None

        if mot_exists:
            # ── Scenario 2: MOT + interpreted T-SQL ──────────────────────────
            cur.execute("DELETE FROM dbo.t_mot")
            sql_mot_interp = f"""
DECLARE @i INT = 0;
WHILE @i < {n} BEGIN
    INSERT INTO dbo.t_mot VALUES (@i, CAST(@i AS FLOAT));
    SET @i += 1;
END
"""
            t0 = time.perf_counter()
            cur.execute(sql_mot_interp)
            results['mot_interp_ms'] = round((time.perf_counter() - t0) * 1000, 1)

            # ── Scenario 3: MOT + natively compiled proc ──────────────────────
            cur.execute("DELETE FROM dbo.t_mot")
            sql_mot_native = f"""
DECLARE @i INT = 0;
WHILE @i < {n} BEGIN
    EXEC dbo.p_insert_mot @i, CAST(@i AS FLOAT);
    SET @i += 1;
END
"""
            t0 = time.perf_counter()
            cur.execute(sql_mot_native)
            results['mot_native_ms'] = round((time.perf_counter() - t0) * 1000, 1)
        else:
            results['mot_interp_ms'] = None
            results['mot_native_ms'] = None

    results['n'] = n
    results['mot_available'] = mot_exists
    return results


@demos_bp.route('/c9-inmemory')
@login_required
def c9_inmemory():
    return render_template('demos/c9_inmemory.html')


@demos_bp.route('/c9-inmemory/setup', methods=['POST'])
@login_required
def c9_inmemory_setup():
    try:
        result = _mot_setup(current_app.config)
        return jsonify(result)
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c9-inmemory/benchmark', methods=['POST'])
@login_required
def c9_inmemory_benchmark():
    try:
        n = int((request.json or {}).get('n', 1000))
        n = max(100, min(n, 10000))
        result = _mot_benchmark(current_app.config, n)
        return jsonify({'ok': True, **result})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c9-inmemory/status')
@login_required
def c9_inmemory_status():
    import pyodbc
    try:
        with pyodbc.connect(_mot_conn_str(current_app.config, 'master'),
                            autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT DB_ID('mot_bench')")
            db_exists = cur.fetchone()[0] is not None

        if not db_exists:
            return jsonify({'ok': True, 'db': False, 'mot': False, 'proc': False})

        with pyodbc.connect(_mot_conn_str(current_app.config, 'mot_bench'),
                            autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT OBJECT_ID('dbo.t_disk','U'), OBJECT_ID('dbo.t_mot','U'), OBJECT_ID('dbo.p_insert_mot','P')")
            row = cur.fetchone()
        return jsonify({
            'ok': True,
            'db': True,
            'disk_table': row[0] is not None,
            'mot_table':  row[1] is not None,
            'proc':       row[2] is not None,
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c9-inmemory/teardown', methods=['POST'])
@login_required
def c9_inmemory_teardown():
    import pyodbc
    try:
        with pyodbc.connect(_mot_conn_str(current_app.config, 'master'),
                            autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("""
                IF DB_ID('mot_bench') IS NOT NULL BEGIN
                    ALTER DATABASE mot_bench SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
                    DROP DATABASE mot_bench;
                END
            """)
        return jsonify({'ok': True, 'message': 'mot_bench database dropped'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ── Chapter 11: SQL DML Lab ───────────────────────────────────────────────────

_C11_QUERIES = {
    # ── Section 1: Basic SELECT ───────────────────────────────────────────────
    's1q1': {
        'title': 'All employees',
        'sql': "SELECT lastname, firstname, birthdate, city FROM employees",
    },
    's1q2': {
        'title': 'London customers (=)',
        'sql': "SELECT companyname, city FROM customers WHERE city = 'London'",
    },
    's1q3': {
        'title': "London customers (IN — multiple cities)",
        'sql': "SELECT companyname, city FROM customers WHERE city IN ('London', 'Lander')",
    },
    's1q4': {
        'title': "London customers (LIKE partial match)",
        'sql': "SELECT companyname, city FROM customers WHERE city LIKE 'L%' AND (city LIKE '%b%' OR city LIKE '%n%')",
    },

    # ── Section 2: Aggregate & Nested Queries ────────────────────────────────
    's2q1': {
        'title': 'MIN / MAX birthdate',
        'sql': "SELECT MAX(birthdate) as max_year, MIN(birthdate) as min_year FROM employees",
    },
    's2q2': {
        'title': 'Youngest employee (subquery)',
        'sql': """SELECT lastname, birthdate as [birth date]
FROM employees
WHERE birthdate = (
    SELECT MAX(birthdate) FROM employees
)""",
    },
    's2q3': {
        'title': 'ShipAddress of first order (MIN subquery)',
        'sql': """SELECT orderdate, shipaddress
FROM orders
WHERE orderdate = (
    SELECT MIN(orderdate) FROM orders
)""",
    },
    's2q4': {
        'title': "Youngest employee's ship addresses (3-level nesting)",
        'sql': """SELECT DISTINCT lastname, shipaddress
FROM orders o INNER JOIN employees e ON o.employeeid=e.employeeid
WHERE e.employeeid = (
    SELECT employeeid FROM employees
    WHERE birthdate = (
        SELECT MAX(birthdate) FROM employees
    )
)
ORDER BY shipaddress""",
    },

    # ── Section 3: JOINs ─────────────────────────────────────────────────────
    's3q1': {
        'title': 'Products ordered from youngest employee (4-table INNER JOIN)',
        'sql': """SELECT DISTINCT p.productname, e.lastname
FROM orders o
INNER JOIN employees e ON o.employeeid=e.employeeid
INNER JOIN [order details] od ON od.orderid=o.orderid
INNER JOIN products p ON p.productid=od.productid
WHERE e.employeeid = (
    SELECT TOP 1 employeeid FROM employees ORDER BY birthdate DESC
)
ORDER BY productname""",
    },
    's3q2': {
        'title': 'Ship cities of category-1 products',
        'sql': """SELECT DISTINCT o.shipcity
FROM orders o
INNER JOIN [order details] od ON od.orderid=o.orderid
INNER JOIN products p ON p.productid=od.productid
WHERE p.categoryid = 1
ORDER BY shipcity""",
    },

    # ── Section 4: GROUP BY (5-step progression) ─────────────────────────────
    's4q1': {
        'title': 'Step 1 — simple GROUP BY employeeid',
        'sql': "SELECT employeeid, COUNT(*) as order_count FROM orders GROUP BY employeeid ORDER BY order_count DESC",
    },
    's4q2': {
        'title': 'Step 2 — ⚠ Wrong: GROUP BY lastname only (logical error if same surname)',
        'sql': """SELECT e.lastname, COUNT(*) as order_count
FROM orders o INNER JOIN employees e ON o.employeeid=e.employeeid
GROUP BY e.lastname
ORDER BY order_count DESC""",
    },
    's4q3': {
        'title': 'Step 3 — ⚠ Still wrong: misses employee with no orders (INNER JOIN)',
        'sql': """SELECT e.lastname, e.firstname, COUNT(*) as order_count
FROM orders o INNER JOIN employees e ON o.employeeid=e.employeeid
GROUP BY e.employeeid, e.lastname, e.firstname
ORDER BY order_count DESC""",
    },
    's4q4': {
        'title': 'Step 4 — ⚠ LEFT JOIN but COUNT(*) fakes count=1 for idle employee',
        'sql': """SELECT e.employeeid, e.lastname, e.firstname, COUNT(*) as fake_count
FROM employees e LEFT OUTER JOIN orders o ON o.employeeid=e.employeeid
GROUP BY e.employeeid, e.lastname, e.firstname
ORDER BY fake_count DESC""",
    },
    's4q5': {
        'title': 'Step 5 — ✓ Correct: LEFT JOIN + COUNT(o.orderid)',
        'sql': """SELECT e.employeeid, e.lastname, e.firstname, COUNT(o.orderid) as no_ord
FROM employees e LEFT OUTER JOIN orders o ON o.employeeid=e.employeeid
GROUP BY e.employeeid, e.lastname, e.firstname
ORDER BY no_ord DESC""",
    },
    's4q6': {
        'title': 'Products per category (JOIN + GROUP BY)',
        'sql': """SELECT c.categoryid, c.categoryname, COUNT(*) as no_prod
FROM products p INNER JOIN categories c ON p.categoryid=c.categoryid
GROUP BY c.categoryid, c.categoryname
ORDER BY no_prod DESC""",
    },

    # ── Section 5: Self-Join ──────────────────────────────────────────────────
    's5q1': {
        'title': 'Reporting hierarchy (2-level self-join)',
        'sql': """SELECT e.lastname, boss.lastname as boss, bboss.lastname as boss_of_boss
FROM employees e
LEFT OUTER JOIN employees boss ON e.reportsto=boss.employeeid
LEFT OUTER JOIN employees bboss ON boss.reportsto=bboss.employeeid""",
    },
    's5q2': {
        'title': 'Orders per employee (self-join + GROUP BY)',
        'sql': """SELECT e.lastname, COUNT(o.orderid) as order_count
FROM employees e LEFT OUTER JOIN orders o ON e.employeeid=o.employeeid
GROUP BY e.employeeid, e.lastname
ORDER BY order_count DESC""",
    },
    's5q3': {
        'title': 'Who has NO orders? (LEFT JOIN + IS NULL)',
        'sql': """SELECT e.employeeid, e.lastname, e.firstname, e.title
FROM employees e LEFT OUTER JOIN orders o ON e.employeeid=o.employeeid
WHERE o.orderid IS NULL""",
    },

    # ── Section 6: Arithmetic & STR() ────────────────────────────────────────
    's6q1': {
        'title': 'Top-10 biggest orders by revenue (STR formatting)',
        'sql': """SELECT TOP 10 o.orderid,
    CAST(o.orderdate AS VARCHAR(50)) as order_date,
    STR(SUM((1-discount)*unitprice*quantity), 15, 2) as order_total,
    SUM(quantity) as no_of_units,
    COUNT(d.orderid) as no_of_items
FROM orders o INNER JOIN [order details] d ON o.orderid=d.orderid
GROUP BY o.orderid, o.orderdate
ORDER BY SUM((1-discount)*unitprice*quantity) DESC""",
    },

    # ── Section 7: HAVING & ISNULL ────────────────────────────────────────────
    's7q1': {
        'title': 'Top salesperson — INNER JOIN (9 rows, misses 0-order employee)',
        'sql': """SELECT u.titleofcourtesy+' '+u.lastname+' '+u.firstname+' ('+u.title+')' as name,
    STR(SUM((1-discount)*unitprice*quantity), 15, 2) as cash_income,
    COUNT(DISTINCT o.orderid) as no_of_orders,
    COUNT(productid) as no_of_items
FROM orders o
INNER JOIN [order details] d ON o.orderid=d.orderid
INNER JOIN employees u ON u.employeeid=o.employeeid
GROUP BY u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
ORDER BY SUM((1-discount)*unitprice*quantity) DESC""",
    },
    's7q2': {
        'title': 'All employees incl. 0-order — LEFT JOIN + ISNULL (10 rows)',
        'sql': """SELECT ISNULL(u.titleofcourtesy,'')+' '+ISNULL(u.lastname,'')+' '+
        ISNULL(u.firstname,'')+' ('+ISNULL(u.title,'')+')' as name,
    ISNULL(STR(SUM((1-discount)*unitprice*quantity), 15, 2), 'N/A') as cash_income,
    COUNT(DISTINCT o.orderid) as no_of_orders,
    COUNT(d.productid) as no_of_items
FROM employees u
LEFT OUTER JOIN (orders o INNER JOIN [order details] d ON o.orderid=d.orderid)
    ON u.employeeid=o.employeeid
GROUP BY u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
ORDER BY SUM((1-discount)*unitprice*quantity) DESC""",
    },
    's7q3': {
        'title': 'HAVING — only employees with >200 orders',
        'sql': """SELECT u.lastname, COUNT(DISTINCT o.orderid) as no_of_orders
FROM orders o
INNER JOIN [order details] d ON o.orderid=d.orderid
INNER JOIN employees u ON u.employeeid=o.employeeid
GROUP BY u.employeeid, u.lastname
HAVING COUNT(o.orderid) > 200
ORDER BY no_of_orders DESC""",
    },

    # ── Section 8: TOP ────────────────────────────────────────────────────────
    's8q1': {
        'title': 'Most popular product (TOP 1 by order count)',
        'sql': """SELECT TOP 1 p.productid, p.productname,
    COUNT(*) as no_appearances,
    SUM(quantity) as total_pieces
FROM products p LEFT OUTER JOIN [order details] d ON p.productid=d.productid
GROUP BY p.productid, p.productname
ORDER BY no_appearances DESC""",
    },
    's8q2': {
        'title': "Who sold the most of the most popular product? (nested TOP 1 subquery)",
        'sql': """SELECT TOP 1
    u.titleofcourtesy+' '+u.lastname+' '+u.firstname+' ('+u.title+')' as name,
    SUM(quantity) as no_pieces_sold
FROM orders o
INNER JOIN [order details] d ON o.orderid=d.orderid
INNER JOIN employees u ON u.employeeid=o.employeeid
WHERE d.productid = (
    SELECT TOP 1 p.productid
    FROM products p LEFT OUTER JOIN [order details] d2 ON p.productid=d2.productid
    GROUP BY p.productid, p.productname
    ORDER BY COUNT(*) DESC
)
GROUP BY u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
ORDER BY SUM(quantity) DESC""",
    },

    # ── Section 9: Date Functions ─────────────────────────────────────────────
    's9q1': {
        'title': 'Date function demos (GETDATE, DATEDIFF, DATEADD, YEAR, MONTH)',
        'sql': """SELECT
    GETDATE() as now,
    DATEDIFF(second,'2013-10-10 12:13:50','2013-10-10 14:16:50') as diff_seconds,
    DATEADD(second, 1000, '2013-10-10 14:16:50') as plus_1000s,
    YEAR(GETDATE()) as cur_year,
    MONTH(GETDATE()) as cur_month""",
    },
    's9q2': {
        'title': 'Orders by employee × year × month',
        'sql': """SELECT e.employeeid, e.lastname,
    YEAR(o.orderdate) as [year],
    MONTH(o.orderdate) as [month],
    COUNT(o.orderid) as no_of_orders
FROM employees e LEFT OUTER JOIN orders o ON e.employeeid=o.employeeid
GROUP BY e.employeeid, e.lastname, YEAR(o.orderdate), MONTH(o.orderdate)
ORDER BY e.lastname, [year], [month]""",
    },

    # ── Section 10: CASE Expression ───────────────────────────────────────────
    's10q1': {
        'title': 'Zero-padded month label with CASE (YYYY_MM format)',
        'sql': """SELECT e.employeeid, e.lastname,
    CASE
        WHEN MONTH(o.orderdate) < 10
            THEN CAST(YEAR(o.orderdate) AS VARCHAR(4))+'_0'+CAST(MONTH(o.orderdate) AS CHAR(2))
        WHEN MONTH(o.orderdate) >= 10
            THEN CAST(YEAR(o.orderdate) AS VARCHAR(4))+'_'+CAST(MONTH(o.orderdate) AS CHAR(2))
        ELSE 'N.A'
    END as month_label,
    COUNT(o.orderid) as no_of_orders
FROM employees e LEFT OUTER JOIN orders o ON e.employeeid=o.employeeid
GROUP BY e.employeeid, e.lastname,
    CASE
        WHEN MONTH(o.orderdate) < 10
            THEN CAST(YEAR(o.orderdate) AS VARCHAR(4))+'_0'+CAST(MONTH(o.orderdate) AS CHAR(2))
        WHEN MONTH(o.orderdate) >= 10
            THEN CAST(YEAR(o.orderdate) AS VARCHAR(4))+'_'+CAST(MONTH(o.orderdate) AS CHAR(2))
        ELSE 'N.A'
    END
ORDER BY e.lastname, month_label""",
    },

    # ── Section 11: Temp Tables (derived-table equivalent) ───────────────────
    's11q1': {
        'title': 'Avg monthly orders per employee (derived table instead of #temp)',
        'sql': """SELECT src.lastname,
    STR(AVG(CAST(src.no_of_orders AS FLOAT)), 15, 2) as avg_monthly_orders
FROM (
    SELECT e.employeeid, e.lastname,
        YEAR(o.orderdate) as ev,
        MONTH(o.orderdate) as mo,
        COUNT(o.orderid) as no_of_orders
    FROM employees e LEFT OUTER JOIN orders o ON e.employeeid=o.employeeid
    GROUP BY e.employeeid, e.lastname, YEAR(o.orderdate), MONTH(o.orderdate)
) AS src
GROUP BY src.employeeid, src.lastname
ORDER BY avg_monthly_orders DESC""",
    },

    # ── Section 12: Homework Solutions ───────────────────────────────────────
    's12q1': {
        'title': 'HW1: Avg monthly order count per product',
        'sql': """SELECT p.productname,
    STR(AVG(CAST(mo.cnt AS FLOAT)), 15, 2) as avg_monthly_orders
FROM products p
JOIN (
    SELECT od.productid,
        YEAR(o.orderdate) as yr,
        MONTH(o.orderdate) as mo,
        COUNT(DISTINCT o.orderid) as cnt
    FROM orders o JOIN [order details] od ON o.orderid=od.orderid
    GROUP BY od.productid, YEAR(o.orderdate), MONTH(o.orderdate)
) mo ON p.productid = mo.productid
GROUP BY p.productid, p.productname
ORDER BY avg_monthly_orders DESC""",
    },
    's12q2': {
        'title': 'HW2: Who sold more than 2× their boss\'s total revenue?',
        'sql': """WITH emp_totals AS (
    SELECT o.employeeid,
        SUM(od.unitprice * od.quantity * (1 - od.discount)) as total
    FROM orders o JOIN [order details] od ON o.orderid=od.orderid
    GROUP BY o.employeeid
)
SELECT e.lastname as employee,
    STR(et.total, 15, 2) as emp_revenue,
    b.lastname as boss,
    STR(bt.total, 15, 2) as boss_revenue,
    STR(et.total / bt.total, 6, 2) as ratio
FROM employees e
JOIN emp_totals et ON e.employeeid = et.employeeid
JOIN employees b ON e.reportsto = b.employeeid
JOIN emp_totals bt ON b.employeeid = bt.employeeid
WHERE et.total > 2 * bt.total
ORDER BY ratio DESC""",
    },
}


@demos_bp.route('/c11-sql-lab')
@login_required
def c11_sql_lab():
    return render_template('demos/c11_sql_lab.html')


@demos_bp.route('/c11-sql-lab/run')
@login_required
def c11_sql_lab_run():
    import pyodbc
    qid = request.args.get('qid', '')
    q   = _C11_QUERIES.get(qid)
    if not q:
        return jsonify({'ok': False, 'error': f'Unknown query id: {qid}'}), 404
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute(q['sql'])
            cols = [d[0] for d in cur.description]
            rows = [list(r) for r in cur.fetchall()]
            for row in rows:
                for i, v in enumerate(row):
                    if hasattr(v, 'isoformat'):
                        row[i] = v.isoformat()
                    elif v is None:
                        row[i] = None
        return jsonify({'ok': True, 'title': q['title'], 'cols': cols, 'rows': rows, 'n': len(rows)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'sql': q['sql']})


# ── Chapter 12: Database Administration & Security ───────────────────────────

@demos_bp.route('/c12-dba')
@login_required
def c12_dba():
    return render_template('demos/c12_dba.html')


def _c12_fetch(cur):
    """Return (cols, rows) from cursor; handles no-result DDL/DML statements."""
    if cur.description is None:
        return [], []
    cols = [d[0] for d in cur.description]
    rows = []
    for r in cur.fetchall():
        row = list(r)
        for i, v in enumerate(row):
            if hasattr(v, 'isoformat'):
                row[i] = v.isoformat()
            elif v is None:
                row[i] = None
        rows.append(row)
    return cols, rows


@demos_bp.route('/c12-dba/checkdb')
@login_required
def c12_dba_checkdb():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("DBCC CHECKDB('northwind') WITH TABLERESULTS, NO_INFOMSGS, ALL_ERRORMSGS")
            cols, rows = _c12_fetch(cur)
        if not rows:
            return jsonify({'ok': True, 'clean': True,
                            'cols': ['Result'], 'rows': [['✓ No corruption detected — database is healthy']], 'n': 0})
        return jsonify({'ok': True, 'clean': False, 'cols': cols, 'rows': rows, 'n': len(rows)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/page-alloc')
@login_required
def c12_dba_page_alloc():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("""
SELECT OBJECT_NAME(i.object_id) AS tablename,
       SUM(a.total_pages) AS totalpages,
       SUM(a.total_pages - a.used_pages) AS unusedPages,
       SUM(a.used_pages) AS usedPages
FROM sys.indexes i
JOIN sys.partitions p
    ON i.object_id = p.object_id AND i.index_id = p.index_id
JOIN sys.allocation_units a
    ON p.partition_id = a.container_id
WHERE OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1
GROUP BY OBJECT_NAME(i.object_id)
ORDER BY totalpages DESC""")
            cols, rows = _c12_fetch(cur)
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/role-members')
@login_required
def c12_dba_role_members():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("""
SELECT DP1.name AS DatabaseRoleName,
       ISNULL(DP2.name, '(No members)') AS DatabaseUserName
FROM sys.database_role_members AS DRM
    RIGHT OUTER JOIN sys.database_principals AS DP1
        ON DRM.role_principal_id = DP1.principal_id
    LEFT OUTER JOIN sys.database_principals AS DP2
        ON DRM.member_principal_id = DP2.principal_id
WHERE DP1.type = 'R'
ORDER BY DP1.name, DP2.name""")
            cols, rows = _c12_fetch(cur)
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/mask/setup', methods=['POST'])
@login_required
def c12_dba_mask_setup():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    log = []
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM sys.columns WHERE object_id=OBJECT_ID('Employees') AND name='ssn'")
            ssn_exists = cur.fetchone()[0] > 0
            if not ssn_exists:
                cur.execute("ALTER TABLE Employees ADD ssn char(10) NULL")
                log.append('Added ssn column to Employees')
                cur.execute("ALTER TABLE Employees ADD email varchar(200) NULL")
                log.append('Added email column to Employees')
            else:
                log.append('Columns already exist — re-applying masks')
            cur.execute("ALTER TABLE Employees ALTER COLUMN ssn char(10) MASKED WITH (FUNCTION = 'partial(1,\".....\",4)')")
            log.append('Applied partial(1,".....",4) mask → ssn: 1.....7890')
            cur.execute("ALTER TABLE Employees ALTER COLUMN email varchar(200) MASKED WITH (FUNCTION = 'email()')")
            log.append('Applied email() mask → email: sXXX@XXXX.com')
            cur.execute("UPDATE Employees SET ssn='1234567890'")
            cur.execute("UPDATE Employees SET email='sohase_mondd@citromail.hu'")
            log.append('Populated with test data: SSN=1234567890, email=sohase_mondd@citromail.hu')
            log.append('✓ Setup complete')
        return jsonify({'ok': True, 'log': log})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'log': log})


@demos_bp.route('/c12-dba/mask/query-admin')
@login_required
def c12_dba_mask_query_admin():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT lastname, firstname, ssn, email FROM Employees")
            cols, rows = _c12_fetch(cur)
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows),
                        'label': 'sysadmin — always sees real unmasked values'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/mask/create-user', methods=['POST'])
@login_required
def c12_dba_mask_create_user():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    log = []
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM master.sys.server_principals WHERE name='c12_test_user'")
            if cur.fetchone()[0] == 0:
                cur.execute("CREATE LOGIN c12_test_user WITH PASSWORD='h6twqPNO!A', DEFAULT_DATABASE=northwind")
                log.append('Created server login c12_test_user')
            else:
                log.append('Server login c12_test_user already exists')
            cur.execute("SELECT COUNT(*) FROM sys.database_principals WHERE name='c12_test_user'")
            if cur.fetchone()[0] == 0:
                cur.execute("CREATE USER c12_test_user FOR LOGIN c12_test_user")
                cur.execute("ALTER ROLE db_datareader ADD MEMBER c12_test_user")
                cur.execute("ALTER ROLE db_datawriter ADD MEMBER c12_test_user")
                log.append('Created DB user c12_test_user → db_datareader + db_datawriter')
            else:
                log.append('DB user c12_test_user already exists')
            log.append('✓ Test user ready (no UNMASK privilege yet)')
        return jsonify({'ok': True, 'log': log})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'log': log})


@demos_bp.route('/c12-dba/mask/query-masked')
@login_required
def c12_dba_mask_query_masked():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("EXECUTE AS USER = 'c12_test_user'")
            cur.execute("SELECT lastname, firstname, ssn, email FROM Employees")
            cols, rows = _c12_fetch(cur)
            cur.execute("REVERT")
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows),
                        'label': 'EXECUTE AS c12_test_user — Dynamic Data Masking active'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/mask/grant-unmask', methods=['POST'])
@login_required
def c12_dba_mask_grant_unmask():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("GRANT UNMASK TO c12_test_user")
        return jsonify({'ok': True, 'message': 'GRANT UNMASK TO c12_test_user — privilege applied'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/mask/query-unmasked')
@login_required
def c12_dba_mask_query_unmasked():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("EXECUTE AS USER = 'c12_test_user'")
            cur.execute("SELECT lastname, firstname, ssn, email FROM Employees")
            cols, rows = _c12_fetch(cur)
            cur.execute("REVERT")
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows),
                        'label': 'EXECUTE AS c12_test_user WITH UNMASK — real values now visible'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/mask/cleanup', methods=['POST'])
@login_required
def c12_dba_mask_cleanup():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    log = []
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            try:
                cur.execute("REVOKE UNMASK FROM c12_test_user")
                log.append('Revoked UNMASK from c12_test_user')
            except Exception:
                pass
            cur.execute("SELECT COUNT(*) FROM sys.database_principals WHERE name='c12_test_user'")
            if cur.fetchone()[0] > 0:
                cur.execute("DROP USER c12_test_user")
                log.append('Dropped DB user c12_test_user')
            cur.execute("SELECT COUNT(*) FROM master.sys.server_principals WHERE name='c12_test_user'")
            if cur.fetchone()[0] > 0:
                cur.execute("DROP LOGIN c12_test_user")
                log.append('Dropped server login c12_test_user')
            cur.execute("SELECT COUNT(*) FROM sys.columns WHERE object_id=OBJECT_ID('Employees') AND name='ssn'")
            if cur.fetchone()[0] > 0:
                cur.execute("ALTER TABLE Employees DROP COLUMN ssn")
                cur.execute("ALTER TABLE Employees DROP COLUMN email")
                log.append('Dropped ssn and email columns from Employees')
            log.append('✓ Cleanup complete — Employees table restored to original schema')
        return jsonify({'ok': True, 'log': log})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'log': log})


@demos_bp.route('/c12-dba/sp/create', methods=['POST'])
@login_required
def c12_dba_sp_create():
    import pyodbc
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            try:
                cur.execute("DROP PROCEDURE sp_c12_list_employees")
            except Exception:
                pass
            cur.execute("""
CREATE PROCEDURE sp_c12_list_employees
    @city varchar(50) = 'London'
AS
    SELECT EmployeeID, LastName, FirstName, Title, City, Country
    FROM Employees
    WHERE City = @city""")
        return jsonify({'ok': True, 'message': 'Procedure sp_c12_list_employees created successfully'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c12-dba/sp/exec')
@login_required
def c12_dba_sp_exec():
    import pyodbc
    city = request.args.get('city', 'London')
    conn_str = _build_conn_str(current_app.config)
    try:
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cur = conn.cursor()
            cur.execute("EXEC sp_c12_list_employees ?", city)
            cols, rows = _c12_fetch(cur)
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows), 'city': city})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ── Chapter 13: Neo4j — Native Graph Database ────────────────────────────────

import services.neo4j_service as _nj_svc


def _get_neo4j_conn_id():
    conns = [c for c in meta_db.list_connections() if c['db_type'] == 'neo4j']
    return conns[0]['id'] if conns else None


_C13_GRAPH_STMTS = [
    "MATCH (n) DETACH DELETE n",
    "CREATE (:Person {id: 1, name: 'john'})",
    "CREATE (:Person {id: 2, name: 'mary'})",
    "CREATE (:Person {id: 3, name: 'alice'})",
    "CREATE (:Person {id: 4, name: 'jacob'})",
    "CREATE (:Person {id: 5, name: 'julie'})",
    "CREATE (:Person {id: 6, name: 'tom'})",
    "CREATE (:Restaurant {id: 1, name: 'taco dell'})",
    "CREATE (:Restaurant {id: 2, name: 'ginger and spice'})",
    "CREATE (:Restaurant {id: 3, name: 'noodle land'})",
    "CREATE (:City {id: 1, name: 'bellevue', state: 'wa'})",
    "CREATE (:City {id: 2, name: 'seattle',  state: 'wa'})",
    "CREATE (:City {id: 3, name: 'redmond',  state: 'wa'})",
    "MATCH (p:Person {id:1}), (r:Restaurant {id:1}) CREATE (p)-[:LIKES {rating:9}]->(r)",
    "MATCH (p:Person {id:2}), (r:Restaurant {id:2}) CREATE (p)-[:LIKES {rating:9}]->(r)",
    "MATCH (p:Person {id:3}), (r:Restaurant {id:3}) CREATE (p)-[:LIKES {rating:9}]->(r)",
    "MATCH (p:Person {id:4}), (r:Restaurant {id:3}) CREATE (p)-[:LIKES {rating:9}]->(r)",
    "MATCH (p:Person {id:5}), (r:Restaurant {id:3}) CREATE (p)-[:LIKES {rating:9}]->(r)",
    "MATCH (p:Person {id:1}), (c:City {id:1}) CREATE (p)-[:LIVES_IN]->(c)",
    "MATCH (p:Person {id:2}), (c:City {id:2}) CREATE (p)-[:LIVES_IN]->(c)",
    "MATCH (p:Person {id:3}), (c:City {id:3}) CREATE (p)-[:LIVES_IN]->(c)",
    "MATCH (p:Person {id:4}), (c:City {id:3}) CREATE (p)-[:LIVES_IN]->(c)",
    "MATCH (p:Person {id:5}), (c:City {id:1}) CREATE (p)-[:LIVES_IN]->(c)",
    "MATCH (r:Restaurant {id:1}), (c:City {id:1}) CREATE (r)-[:LOCATED_IN]->(c)",
    "MATCH (r:Restaurant {id:2}), (c:City {id:2}) CREATE (r)-[:LOCATED_IN]->(c)",
    "MATCH (r:Restaurant {id:3}), (c:City {id:3}) CREATE (r)-[:LOCATED_IN]->(c)",
    "MATCH (p1:Person {id:1}), (p2:Person {id:2}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "MATCH (p1:Person {id:1}), (p2:Person {id:5}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "MATCH (p1:Person {id:2}), (p2:Person {id:3}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "MATCH (p1:Person {id:3}), (p2:Person {id:2}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "MATCH (p1:Person {id:3}), (p2:Person {id:5}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "MATCH (p1:Person {id:3}), (p2:Person {id:6}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "MATCH (p1:Person {id:4}), (p2:Person {id:2}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "MATCH (p1:Person {id:5}), (p2:Person {id:4}) CREATE (p1)-[:FRIEND_OF]->(p2)",
    "CREATE (:Product {id: 1,  name: 'Chai',                  price: 18.00, category: 'Beverages'})",
    "CREATE (:Product {id: 2,  name: 'Chang',                 price: 19.00, category: 'Beverages'})",
    "CREATE (:Product {id: 11, name: 'Queso Cabrales',         price: 21.00, category: 'Dairy Products'})",
    "CREATE (:Product {id: 72, name: 'Mozzarella di Giovanni', price: 34.80, category: 'Dairy Products'})",
    "CREATE (:Order {id: 10248, date: '1996-07-04'})",
    "CREATE (:Order {id: 10249, date: '1996-07-05'})",
    "MATCH (o:Order {id:10248}), (p:Product {id:11})  CREATE (o)-[:CONTAINS {quantity:12, discount:0.0}]->(p)",
    "MATCH (o:Order {id:10248}), (p:Product {id:72})  CREATE (o)-[:CONTAINS {quantity:10, discount:0.0}]->(p)",
    "MATCH (o:Order {id:10249}), (p:Product {id:1})   CREATE (o)-[:CONTAINS {quantity:9,  discount:0.0}]->(p)",
    "MATCH (o:Order {id:10249}), (p:Product {id:2})   CREATE (o)-[:CONTAINS {quantity:40, discount:0.0}]->(p)",
]

_C13_ALL_QUERIES = {
    # ── Basic (7) — direct translations of c8 SQL Server MATCH queries ──────
    'q1': {
        'title': "John's direct friends",
        'group': 'basic',
        'sql': "SELECT p2.name\nFROM person p1, person p2, friendof\nWHERE MATCH(p1-(friendof)->p2)\n  AND p1.name = 'john'",
        'cypher': "MATCH (:Person {name: 'john'})-[:FRIEND_OF]->(friend:Person)\nRETURN friend.name AS friend",
        'note': "Pattern replaces 3-table FROM; relationship type is part of the arrow, not a separate table.",
    },
    'q2': {
        'title': "Restaurants john likes",
        'group': 'basic',
        'sql': "SELECT restaurant.name\nFROM person, likes, restaurant\nWHERE MATCH(person-(likes)->restaurant)\n  AND person.name = 'john'",
        'cypher': "MATCH (:Person {name: 'john'})-[l:LIKES]->(r:Restaurant)\nRETURN r.name AS restaurant, l.rating AS rating",
        'note': "Edge property (rating) accessed via the relationship variable [l:LIKES].",
    },
    'q3': {
        'title': "Restaurants liked by john's friends",
        'group': 'basic',
        'sql': "SELECT restaurant.name\nFROM person p1, person p2,\n     friendof, likes, restaurant\nWHERE MATCH(p1-(friendof)->p2-(likes)->restaurant)\n  AND p1.name = 'john'",
        'cypher': "MATCH (:Person {name: 'john'})-[:FRIEND_OF]->(p2:Person)-[:LIKES]->(r:Restaurant)\nRETURN p2.name AS friend, r.name AS restaurant",
        'note': "Two-hop chain — Cypher reads left-to-right like a path description.",
    },
    'q4': {
        'title': "People who like a local restaurant",
        'group': 'basic',
        'sql': "SELECT person.name\nFROM person, likes, restaurant,\n     livesin, city, locatedin\nWHERE MATCH(\n  person-(likes)->restaurant-(locatedin)->city\n  AND person-(livesin)->city)",
        'cypher': "MATCH (p:Person)-[:LIKES]->(r:Restaurant)-[:LOCATED_IN]->(c:City),\n      (p)-[:LIVES_IN]->(c)\nRETURN p.name AS person, r.name AS restaurant, c.name AS city",
        'note': "AND pattern: two paths converge on the same city node 'c'.",
    },
    'q5': {
        'title': "Friends with local taste",
        'group': 'basic',
        'sql': "SELECT DISTINCT p1.name\nFROM person p1, person p2, friendof, likes,\n     restaurant, livesin, city, locatedin\nWHERE MATCH(\n  p1-(friendof)->p2\n  AND p2-(likes)->restaurant-(locatedin)->city\n  AND p2-(livesin)->city)",
        'cypher': "MATCH (p1:Person)-[:FRIEND_OF]->(p2:Person)-[:LIKES]\n      ->(r:Restaurant)-[:LOCATED_IN]->(c:City),\n      (p2)-[:LIVES_IN]->(c)\nRETURN DISTINCT p1.name AS person,\n       p2.name AS friend, r.name AS restaurant",
        'note': "Three paths share p2 and c — compound AND convergence.",
    },
    'q6': {
        'title': "Pairs sharing a mutual friend",
        'group': 'basic',
        'sql': "SELECT p0.name, p1.name, p2.name\nFROM person p1, friendof f1, person p2,\n     friendof f2, person p0\nWHERE MATCH(p1-(f1)->p0 AND p2-(f2)->p0)\n  AND p1.id <> p2.id",
        'cypher': "MATCH (p1:Person)-[:FRIEND_OF]->(p0:Person)<-[:FRIEND_OF]-(p2:Person)\nWHERE p1.id <> p2.id AND p1.name < p2.name\nRETURN p0.name AS mutual_friend,\n       p1.name AS person1, p2.name AS person2",
        'note': "Both p1 and p2 point INTO p0 — arrow reversed on right side (no > on p0 side).",
    },
    'q7': {
        'title': "Shortest paths from john",
        'group': 'basic',
        'sql': "SELECT p1.name+'->'+ STRING_AGG(p2.name,'->')\n       WITHIN GROUP (GRAPH PATH) AS paths,\n       COUNT(p2.name) WITHIN GROUP (GRAPH PATH) AS depth\nFROM person p1,\n     person FOR PATH AS p2,\n     friendof FOR PATH AS friend\nWHERE MATCH(SHORTEST_PATH(p1(-(friend)->p2)+))\n  AND p1.name = 'john'",
        'cypher': "MATCH path = shortestPath(\n  (:Person {name:'john'})-[:FRIEND_OF*]->(dest:Person))\nWHERE dest.name <> 'john'\nRETURN dest.name AS reaches,\n       length(path) AS hops,\n       [n IN nodes(path) | n.name] AS route\nORDER BY hops",
        'note': "shortestPath() built-in; [:FRIEND_OF*] = any depth; list comprehension [n IN nodes(path) | n.name] replaces STRING_AGG … WITHIN GROUP (GRAPH PATH).",
    },
    # ── Advanced (10) ────────────────────────────────────────────────────────
    'a1': {
        'title': "Friend count per person",
        'group': 'adv',
        'cypher': "MATCH (p:Person)-[:FRIEND_OF]->(friend:Person)\nRETURN p.name AS person, count(friend) AS friend_count\nORDER BY friend_count DESC",
        'note': "No GROUP BY needed — aggregation is implicit on non-aggregated RETURN columns.",
    },
    'a2': {
        'title': "Average rating per restaurant",
        'group': 'adv',
        'cypher': "MATCH (p:Person)-[l:LIKES]->(r:Restaurant)\nRETURN r.name AS restaurant,\n       avg(l.rating) AS avg_rating, count(p) AS fans\nORDER BY fans DESC",
        'note': "avg() on a relationship property (l.rating) — no JOIN to an aggregate table needed.",
    },
    'a3': {
        'title': "Restaurants per city with fan count",
        'group': 'adv',
        'cypher': "MATCH (r:Restaurant)-[:LOCATED_IN]->(c:City)\nOPTIONAL MATCH (p:Person)-[:LIKES]->(r)\nRETURN c.name AS city, r.name AS restaurant, count(p) AS fans\nORDER BY city, fans DESC",
        'note': "OPTIONAL MATCH = LEFT JOIN — restaurants with 0 fans still appear with count=0.",
    },
    'a4': {
        'title': "All persons reachable from john (≤2 hops)",
        'group': 'adv',
        'cypher': "MATCH (:Person {name: 'john'})-[:FRIEND_OF*1..2]->(p:Person)\nRETURN DISTINCT p.name AS reachable",
        'note': "[:TYPE*min..max] = variable-length — equivalent to SHORTEST_PATH{1,2} range in SQL Server.",
    },
    'a5': {
        'title': "All paths: john → alice (up to 4 hops)",
        'group': 'adv',
        'cypher': "MATCH path = (:Person {name: 'john'})-[:FRIEND_OF*1..4]->(:Person {name: 'alice'})\nRETURN [n IN nodes(path) | n.name] AS route, length(path) AS hops\nORDER BY hops",
        'note': "ALL paths, not just shortest — list comprehension builds the route array.",
    },
    'a6': {
        'title': "Network diameter (5 most-distant pairs)",
        'group': 'adv',
        'cypher': "MATCH (a:Person), (b:Person)\nWHERE a.id < b.id\nMATCH path = shortestPath((a)-[:FRIEND_OF*]-(b))\nRETURN a.name, b.name, length(path) AS distance\nORDER BY distance DESC\nLIMIT 5",
        'note': "Undirected traversal (no >) — finds longest shortest-path pairs, i.e. the diameter.",
    },
    'a7': {
        'title': "Order contents with line totals",
        'group': 'adv',
        'cypher': "MATCH (o:Order)-[c:CONTAINS]->(p:Product)\nRETURN o.id AS order_id, p.name AS product,\n       c.quantity AS qty, p.price AS unit_price,\n       round(c.quantity * p.price * (1 - coalesce(c.discount,0.0)), 2) AS line_total\nORDER BY order_id",
        'note': "Relationship properties (quantity, discount) combined with node property (price) — no JOIN.",
    },
    'a8': {
        'title': "Product co-occurrence in orders",
        'group': 'adv',
        'cypher': "MATCH (o:Order)-[:CONTAINS]->(p1:Product),\n      (o)-[:CONTAINS]->(p2:Product)\nWHERE p1.id < p2.id\nRETURN p1.name AS product_a, p2.name AS product_b,\n       count(o) AS shared_orders\nORDER BY shared_orders DESC",
        'note': "Self-join on Order — same co-purchase logic as the Northwind SQL but no JOIN keyword.",
    },
    'a9': {
        'title': "Revenue by category",
        'group': 'adv',
        'cypher': "MATCH (o:Order)-[c:CONTAINS]->(p:Product)\nRETURN p.category AS category,\n       round(sum(c.quantity * p.price * (1 - coalesce(c.discount,0.0))), 2) AS revenue\nORDER BY revenue DESC",
        'note': "Same SUM(UnitPrice*Quantity*(1-Discount)) formula as Northwind SQL — no intermediate JOIN table.",
    },
    'a10': {
        'title': "In-degree centrality (proxy PageRank)",
        'group': 'adv',
        'cypher': "MATCH (p:Person)\nOPTIONAL MATCH (other:Person)-[:FRIEND_OF]->(p)\nRETURN p.name AS person, count(other) AS in_degree\nORDER BY in_degree DESC",
        'note': "Counts incoming FRIEND_OF edges — approximates importance. Full PageRank needs GDS plugin.",
    },
}


@demos_bp.route('/c13-neo4j')
@login_required
def c13_neo4j():
    conn_id = _get_neo4j_conn_id()
    return render_template('demos/c13_neo4j.html', conn_id=conn_id)


@demos_bp.route('/c13-neo4j/schema')
@login_required
def c13_neo4j_schema():
    conn_id = _get_neo4j_conn_id()
    if not conn_id:
        return jsonify({'ok': False, 'error': 'No Neo4j connection registered — add one in Control Plane → Connections.'})
    schema = _nj_svc.get_schema(conn_id)
    if schema['error']:
        return jsonify({'ok': False, 'error': schema['error']})
    return jsonify({'ok': True, 'labels': schema['labels'], 'rel_types': schema['rel_types']})


@demos_bp.route('/c13-neo4j/load-graph', methods=['POST'])
@login_required
def c13_neo4j_load_graph():
    conn_id = _get_neo4j_conn_id()
    if not conn_id:
        return jsonify({'ok': False, 'error': 'No Neo4j connection registered.'})
    log = []
    try:
        for stmt in _C13_GRAPH_STMTS:
            _, _, err = _nj_svc.run_cypher(conn_id, stmt)
            if err:
                return jsonify({'ok': False, 'error': f'Failed: {stmt[:70]}… — {err}', 'log': log})
            short = stmt[:70] + ('…' if len(stmt) > 70 else '')
            log.append(f'✓ {short}')
        log.append(f'Graph loaded — {len(_C13_GRAPH_STMTS)} statements executed successfully')
        return jsonify({'ok': True, 'log': log})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'log': log})


@demos_bp.route('/c13-neo4j/query')
@login_required
def c13_neo4j_query():
    key = request.args.get('key', '')
    q = _C13_ALL_QUERIES.get(key)
    if not q:
        return jsonify({'ok': False, 'error': f'Unknown query key: {key}'})
    conn_id = _get_neo4j_conn_id()
    if not conn_id:
        return jsonify({'ok': False, 'error': 'No Neo4j connection registered.'})
    cols, rows, err = _nj_svc.run_cypher(conn_id, q['cypher'])
    if err:
        return jsonify({'ok': False, 'error': err, 'title': q['title']})
    # Serialize any non-primitive values (lists, dicts from Neo4j)
    def _ser(v):
        if isinstance(v, (list, dict)):
            import json as _json
            return _json.dumps(v)
        return v
    rows = [[_ser(v) for v in row] for row in rows]
    return jsonify({'ok': True, 'title': q['title'], 'cols': cols, 'rows': rows, 'n': len(rows)})


@demos_bp.route('/c13-neo4j/cypher', methods=['POST'])
@login_required
def c13_neo4j_cypher():
    data = request.get_json(silent=True) or {}
    cypher = data.get('cypher', '').strip()
    if not cypher:
        return jsonify({'ok': False, 'error': 'No Cypher provided'})
    conn_id = _get_neo4j_conn_id()
    if not conn_id:
        return jsonify({'ok': False, 'error': 'No Neo4j connection registered.'})
    cols, rows, err = _nj_svc.run_cypher(conn_id, cypher)
    if err:
        return jsonify({'ok': False, 'error': err})
    def _ser(v):
        if isinstance(v, (list, dict)):
            import json as _json
            return _json.dumps(v)
        return v
    rows = [[_ser(v) for v in row] for row in rows]
    return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows)})


# ── Chapter 16: CDC, Kafka, Flyway, ACID Test Lab ────────────────────────────

@demos_bp.route('/c16-cdc')
@login_required
def c16_cdc():
    return render_template('demos/c16_cdc.html')


@demos_bp.route('/c16-cdc/check-cdc')
@login_required
def c16_check_cdc():
    try:
        import pyodbc
        conn_str = _build_conn_str(current_app.config)
        conn = pyodbc.connect(conn_str, autocommit=True)
        cur = conn.cursor()
        cur.execute("SELECT name, is_cdc_enabled FROM sys.databases WHERE name = 'Northwind'")
        row = cur.fetchone()
        conn.close()
        if row:
            enabled = bool(row[1])
            return jsonify({'ok': True, 'db': row[0], 'cdc_enabled': enabled})
        return jsonify({'ok': False, 'error': 'Northwind database not found'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c16-cdc/enable-cdc', methods=['POST'])
@login_required
def c16_enable_cdc():
    log = []
    try:
        import pyodbc
        conn_str = _build_conn_str(current_app.config)
        conn = pyodbc.connect(conn_str, autocommit=True)
        cur = conn.cursor()
        # Enable CDC at DB level
        try:
            cur.execute("EXEC sys.sp_cdc_enable_db")
            log.append('✓ sp_cdc_enable_db — database-level CDC enabled')
        except Exception as e:
            msg = str(e)
            if 'already enabled' in msg.lower() or '22830' in msg:
                log.append('ℹ CDC already enabled at database level')
            else:
                log.append(f'⚠ sp_cdc_enable_db: {msg}')
        # Enable CDC on Orders table
        try:
            cur.execute("""
                EXEC sys.sp_cdc_enable_table
                    @source_schema = N'dbo',
                    @source_name   = N'Orders',
                    @role_name     = NULL
            """)
            log.append('✓ sp_cdc_enable_table — CDC enabled on dbo.Orders')
        except Exception as e:
            msg = str(e)
            if 'already enabled' in msg.lower() or '22832' in msg:
                log.append('ℹ CDC already enabled on dbo.Orders')
            else:
                log.append(f'⚠ sp_cdc_enable_table: {msg}')
        conn.close()
        return jsonify({'ok': True, 'log': log})
    except Exception as e:
        log.append(f'✗ Connection error: {str(e)}')
        return jsonify({'ok': False, 'error': str(e), 'log': log})


@demos_bp.route('/c16-cdc/cdc-rows')
@login_required
def c16_cdc_rows():
    try:
        import pyodbc
        conn_str = _build_conn_str(current_app.config)
        conn = pyodbc.connect(conn_str, autocommit=True)
        cur = conn.cursor()
        # Check if CDC change table exists
        cur.execute("""
            SELECT COUNT(*) FROM sys.tables
            WHERE name = 'dbo_Orders_CT' AND SCHEMA_NAME(schema_id) = 'cdc'
        """)
        cnt = cur.fetchone()[0]
        if cnt == 0:
            conn.close()
            return jsonify({'ok': False, 'error': 'CDC change table not found. Enable CDC first.'})
        cur.execute("SELECT TOP 10 * FROM cdc.dbo_Orders_CT ORDER BY __$start_lsn DESC")
        cols = [d[0] for d in cur.description]
        rows = []
        for r in cur.fetchall():
            row = []
            for v in r:
                if hasattr(v, 'isoformat'):
                    row.append(v.isoformat())
                elif isinstance(v, (bytes, bytearray)):
                    row.append(v.hex())
                else:
                    row.append(v)
            rows.append(row)
        conn.close()
        return jsonify({'ok': True, 'cols': cols, 'rows': rows, 'n': len(rows)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@demos_bp.route('/c16-cdc/acid-test', methods=['POST'])
@login_required
def c16_acid_test():
    import subprocess, sys as _sys, os as _os
    data = request.get_json(silent=True) or {}
    isolation = data.get('isolation', 'SERIALIZABLE')
    threads   = int(data.get('threads', 20))
    allowed = {'READ_UNCOMMITTED', 'READ_COMMITTED', 'REPEATABLE_READ', 'SERIALIZABLE'}
    if isolation not in allowed:
        isolation = 'SERIALIZABLE'
    script = _os.path.join(current_app.root_path, 'scripts', 'acid_test.py')
    cmd = [_sys.executable, script, '--db', 'sqlite', '--threads', str(threads)]
    if isolation != 'SERIALIZABLE':
        cmd += ['--isolation', isolation]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        output = result.stdout + (result.stderr or '')
        lines  = [l for l in output.splitlines() if l.strip()]
        verdict = 'PASS' if 'PASS' in output else ('FAIL' if 'FAIL' in output else 'UNKNOWN')
        return jsonify({'ok': True, 'output': lines, 'verdict': verdict,
                        'isolation': isolation, 'threads': threads})
    except subprocess.TimeoutExpired:
        return jsonify({'ok': False, 'error': 'Test timed out after 60 seconds'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


# ── Chapter 17: MongoDB Schema Validation, CQRS, pgvector ────────────────────

@demos_bp.route('/c17-mongo')
@login_required
def c17_mongo():
    return render_template('demos/c17_mongo.html')


# ── Chapter 18: Cloud Database Ecosystems ────────────────────────────────────

@demos_bp.route('/c18-cloud')
@login_required
def c18_cloud():
    return render_template('demos/c18_cloud.html')


# ── Cloud Book Chapter 3: Cloud Technology Fundamentals ──────────────────────

@demos_bp.route('/cloud-fundamentals')
@login_required
def cloud_fundamentals():
    return render_template('demos/cloud_fundamentals.html')


# ── Chapter 3: Replication, Log Shipping & Failover ──────────────────────────

@demos_bp.route('/c3-replication')
@login_required
def c3_replication():
    return render_template('demos/c3_replication.html')


# ── Chapter 14: Distributed Consensus — PoW vs Raft ──────────────────────────

@demos_bp.route('/c14-raft')
@login_required
def c14_raft():
    return render_template('demos/c14_raft.html')


# ── Chapter 15: Full-Text Search with Elasticsearch ──────────────────────────

@demos_bp.route('/c15-elasticsearch')
@login_required
def c15_elasticsearch():
    return render_template('demos/c15_elasticsearch.html')


# ── Cloud Book Chapter 2: The Road to Cloud Computing ────────────────────────

@demos_bp.route('/cloud-ch2')
@login_required
def cloud_ch2():
    return render_template('demos/cloud_ch2.html')


# ── Cloud Book Chapter 4: Amazon AWS ─────────────────────────────────────────

@demos_bp.route('/cloud-ch4')
@login_required
def cloud_ch4():
    return render_template('demos/cloud_ch4.html')


# ── Cloud Book Chapters 5–6: Google Cloud Platform ───────────────────────────

@demos_bp.route('/cloud-ch5')
@login_required
def cloud_ch5():
    return render_template('demos/cloud_ch5.html')


# ── Cloud Book Chapter 7: MapReduce, Spark & GCP Dataproc ────────────────────

@demos_bp.route('/cloud-ch7')
@login_required
def cloud_ch7():
    return render_template('demos/cloud_ch7.html')


# ── Cloud Book Chapter 8: Stream Data Processing ─────────────────────────────

@demos_bp.route('/cloud-ch8')
@login_required
def cloud_ch8():
    return render_template('demos/cloud_ch8.html')


# ── Cloud Book Chapter 9: Cloud Functions / FaaS ─────────────────────────────

@demos_bp.route('/cloud-ch9')
@login_required
def cloud_ch9():
    return render_template('demos/cloud_ch9.html')


# ── Cloud Book Chapter 10: Service Communication — Pub/Sub ───────────────────

@demos_bp.route('/cloud-ch10')
@login_required
def cloud_ch10():
    return render_template('demos/cloud_ch10.html')


# ── Cloud Book Chapter 11: GCP AI Service Examples ───────────────────────────

@demos_bp.route('/cloud-ch11')
@login_required
def cloud_ch11():
    return render_template('demos/cloud_ch11.html')


# ── Cloud Book Chapter 12: Cloud Service Orchestration ───────────────────────

@demos_bp.route('/cloud-ch12')
@login_required
def cloud_ch12():
    return render_template('demos/cloud_ch12.html')


# ── Learn — chapter index pages ───────────────────────────────────────────────

@demos_bp.route('/learn/databases')
@login_required
def learn_databases():
    return render_template('learn/databases.html')

@demos_bp.route('/learn/cloud')
@login_required
def learn_cloud():
    return render_template('learn/cloud.html')

@demos_bp.route('/learn/ila')
@login_required
def learn_ila():
    return render_template('learn/ila.html')

@demos_bp.route('/learn/dimat')
@login_required
def learn_dimat():
    return render_template('learn/dimat.html')

@demos_bp.route('/dimat/ch0')
@login_required
def dimat_ch0():
    return render_template('demos/dimat_ch0.html')

@demos_bp.route('/dimat/ch1')
@login_required
def dimat_ch1():
    return render_template('demos/dimat_ch1.html')

@demos_bp.route('/dimat/ch2')
@login_required
def dimat_ch2():
    return render_template('demos/dimat_ch2.html')

@demos_bp.route('/dimat/ch3')
@login_required
def dimat_ch3():
    return render_template('demos/dimat_ch3.html')

@demos_bp.route('/dimat/ch4')
@login_required
def dimat_ch4():
    return render_template('demos/dimat_ch4.html')

@demos_bp.route('/dimat/ch5')
@login_required
def dimat_ch5():
    return render_template('demos/dimat_ch5.html')

@demos_bp.route('/dimat/ch6')
@login_required
def dimat_ch6():
    return render_template('demos/dimat_ch6.html')

@demos_bp.route('/dimat/ch7')
@login_required
def dimat_ch7():
    return render_template('demos/dimat_ch7.html')

@demos_bp.route('/dimat/ch8')
@login_required
def dimat_ch8():
    return render_template('demos/dimat_ch8.html')

@demos_bp.route('/dimat/ch9')
@login_required
def dimat_ch9():
    return render_template('demos/dimat_ch9.html')

@demos_bp.route('/dimat/ch10')
@login_required
def dimat_ch10():
    return render_template('demos/dimat_ch10.html')

@demos_bp.route('/dimat/ch11')
@login_required
def dimat_ch11():
    return render_template('demos/dimat_ch11.html')

@demos_bp.route('/dimat/ch12')
@login_required
def dimat_ch12():
    return render_template('demos/dimat_ch12.html')

@demos_bp.route('/dimat/ch13')
@login_required
def dimat_ch13():
    return render_template('demos/dimat_ch13.html')

@demos_bp.route('/dimat/ch14')
@login_required
def dimat_ch14():
    return render_template('demos/dimat_ch14.html')

@demos_bp.route('/dimat/ch15')
@login_required
def dimat_ch15():
    return render_template('demos/dimat_ch15.html')

@demos_bp.route('/dimat/ch16')
@login_required
def dimat_ch16():
    return render_template('demos/dimat_ch16.html')

@demos_bp.route('/dimat/ch17')
@login_required
def dimat_ch17():
    return render_template('demos/dimat_ch17.html')

@demos_bp.route('/dimat/ch18')
@login_required
def dimat_ch18():
    return render_template('demos/dimat_ch18.html')

@demos_bp.route('/dimat/ch19')
@login_required
def dimat_ch19():
    return render_template('demos/dimat_ch19.html')

@demos_bp.route('/dimat/ch20')
@login_required
def dimat_ch20():
    return render_template('demos/dimat_ch20.html')

@demos_bp.route('/dimat/ch21')
@login_required
def dimat_ch21():
    return render_template('demos/dimat_ch21.html')

@demos_bp.route('/dimat/ch22')
@login_required
def dimat_ch22():
    return render_template('demos/dimat_ch22.html')

@demos_bp.route('/dimat/ch23')
@login_required
def dimat_ch23():
    return render_template('demos/dimat_ch23.html')

@demos_bp.route('/dimat/appendix')
@login_required
def dimat_appendix():
    return render_template('demos/dimat_appendix.html')


# ── Dimat: gamification API ──────────────────────────────────────────────────
# All read endpoints permit anonymous access (returning empty progress/leaderboards)
# so the page is browsable; only POSTs require login (decorator below applies session check).

from flask import session as _session
from services import dimat_data as _dimat_data
from services import dimat_quiz_gen as _dimat_quiz
from services import dimat_progress as _dimat_progress
from services import dimat_srs as _dimat_srs
from services import dimat_achievements as _dimat_ach
from services import dimat_community as _dimat_comm


def _uid():
    return _session.get('user_id', 0)


@demos_bp.route('/dimat/api/exercises/<ch>')
def api_dimat_exercises(ch):
    data = _dimat_data.get_chapter(ch)
    return jsonify({
        'ch': ch,
        'title': data.get('title', ch),
        'count': len(data.get('exercises', [])),
        'exercises': data.get('exercises', []),
    })


@demos_bp.route('/dimat/api/exercise_status/<ch>')
def api_dimat_exercise_status(ch):
    """Returns {exercise_id: status} for the current user, for one chapter."""
    uid = _uid()
    if not uid:
        return jsonify({'ch': ch, 'statuses': {}})
    conn = meta_db.dimat_conn()
    rows = conn.execute(
        "SELECT exercise_id, status FROM dimat_progress WHERE user_id=? AND ch=?",
        (uid, ch),
    ).fetchall()
    return jsonify({'ch': ch, 'statuses': {r[0]: r[1] for r in rows}})


@demos_bp.route('/dimat/api/quiz/<ch>')
def api_dimat_quiz(ch):
    diff = request.args.get('d', 'normal')
    if diff not in ('easy', 'normal', 'hard'):
        diff = 'normal'
    items = _dimat_quiz.generate_for_chapter(ch, diff)
    return jsonify({'ch': ch, 'difficulty': diff, 'questions': items})


@demos_bp.route('/dimat/api/daily_challenge')
def api_dimat_daily():
    from datetime import datetime
    seed = datetime.utcnow().strftime('%Y-%m-%d')
    return jsonify({
        'date': seed,
        'questions': _dimat_quiz.daily_challenge(seed_extra=seed),
    })


@demos_bp.route('/dimat/api/progress', methods=['POST'])
@login_required
def api_dimat_progress():
    body = request.get_json(force=True) or {}
    ch = body.get('ch', '')
    ex_id = body.get('exercise_id', '')
    status = body.get('status', '')
    res = _dimat_progress.record_progress(_uid(), ch, ex_id, status)
    newly = _dimat_ach.check(_uid())
    return jsonify({**res, 'newly_earned': newly})


@demos_bp.route('/dimat/api/quiz_result', methods=['POST'])
@login_required
def api_dimat_quiz_result():
    body = request.get_json(force=True) or {}
    res = _dimat_progress.record_quiz(
        _uid(),
        body.get('ch', ''),
        int(body.get('score', 0)),
        int(body.get('total', 0)),
        int(body.get('duration_sec', 0)),
        body.get('difficulty', 'normal'),
        body.get('wrong_qids') or [],
    )
    newly = _dimat_ach.check(_uid())
    return jsonify({**res, 'newly_earned': newly})


@demos_bp.route('/dimat/api/game_result', methods=['POST'])
@login_required
def api_dimat_game_result():
    body = request.get_json(force=True) or {}
    res = _dimat_progress.record_game(
        _uid(),
        body.get('ch', ''),
        int(body.get('score', 0)),
        int(body.get('max_score', 100)),
    )
    newly = _dimat_ach.check(_uid())
    return jsonify({**res, 'newly_earned': newly})


@demos_bp.route('/dimat/api/srs_due')
def api_dimat_srs_due():
    return jsonify({'due': _dimat_srs.list_due(_uid(), limit=20)})


@demos_bp.route('/dimat/api/srs_grade', methods=['POST'])
@login_required
def api_dimat_srs_grade():
    body = request.get_json(force=True) or {}
    return jsonify(_dimat_srs.grade(
        _uid(),
        body.get('ch', ''),
        body.get('question_id', ''),
        int(body.get('grade', 3)),
    ))


@demos_bp.route('/dimat/api/me')
def api_dimat_me():
    return jsonify(_dimat_progress.me(_uid()))


@demos_bp.route('/dimat/api/leaderboard')
def api_dimat_leaderboard():
    ch = request.args.get('ch') or None
    period = request.args.get('period', 'all')
    if period not in ('week', 'month', 'all'):
        period = 'all'
    return jsonify({
        'period': period, 'ch': ch,
        'rows': _dimat_progress.leaderboard(ch=ch, period=period, limit=20),
    })


@demos_bp.route('/dimat/api/achievements')
def api_dimat_achievements():
    return jsonify({
        'all': _dimat_ach.list_all(),
        'earned': _dimat_ach.list_earned(_uid()),
    })


@demos_bp.route('/dimat/api/community_goal')
def api_dimat_community():
    return jsonify(_dimat_comm.status())


@demos_bp.route('/dimat/api/skill_tree')
def api_dimat_skill_tree():
    return jsonify(_dimat_data.get_skill_tree())


@demos_bp.route('/dimat/challenges')
@login_required
def dimat_challenges():
    return render_template('demos/dimat_challenges.html')


@demos_bp.route('/ila/ch1')
@login_required
def ila_ch1():
    return render_template('demos/ila_ch1.html')

@demos_bp.route('/ila/ch2')
@login_required
def ila_ch2():
    return render_template('demos/ila_ch2.html')

@demos_bp.route('/ila/ch3')
@login_required
def ila_ch3():
    return render_template('demos/ila_ch3.html')

@demos_bp.route('/ila/ch4')
@login_required
def ila_ch4():
    return render_template('demos/ila_ch4.html')

@demos_bp.route('/ila/ch5')
@login_required
def ila_ch5():
    return render_template('demos/ila_ch5.html')

@demos_bp.route('/ila/ch6')
@login_required
def ila_ch6():
    return render_template('demos/ila_ch6.html')

@demos_bp.route('/ila/ch7')
@login_required
def ila_ch7():
    return render_template('demos/ila_ch7.html')

@demos_bp.route('/ila/ch8')
@login_required
def ila_ch8():
    return render_template('demos/ila_ch8.html')

@demos_bp.route('/ila/ch9')
@login_required
def ila_ch9():
    return render_template('demos/ila_ch9.html')

@demos_bp.route('/ila/ch10')
@login_required
def ila_ch10():
    return render_template('demos/ila_ch10.html')

@demos_bp.route('/ila/ch11')
@login_required
def ila_ch11():
    return render_template('demos/ila_ch11.html')

@demos_bp.route('/ila/ch12')
@login_required
def ila_ch12():
    return render_template('demos/ila_ch12.html')

@demos_bp.route('/ila/ch13')
@login_required
def ila_ch13():
    return render_template('demos/ila_ch13.html')

@demos_bp.route('/ila/ch14')
@login_required
def ila_ch14():
    return render_template('demos/ila_ch14.html')

@demos_bp.route('/ila/ch15')
@login_required
def ila_ch15():
    return render_template('demos/ila_ch15.html')

@demos_bp.route('/ila/ch16')
@login_required
def ila_ch16():
    return render_template('demos/ila_ch16.html')


@demos_bp.route('/ila/ch17')
@login_required
def ila_ch17():
    return render_template('demos/ila_ch17.html')


@demos_bp.route('/ila/ch18')
@login_required
def ila_ch18():
    return render_template('demos/ila_ch18.html')


# ── Demo subpages by subject ──────────────────────────────────────────────────

@demos_bp.route('/cloud')
@login_required
def demos_cloud():
    return render_template('demos/index_cloud.html')

@demos_bp.route('/graph')
@login_required
def demos_graph():
    return render_template('demos/index_graph.html')

@demos_bp.route('/database')
@login_required
def demos_database():
    return render_template('demos/index_database.html')

@demos_bp.route('/other')
@login_required
def demos_other():
    return render_template('demos/index_other.html')


# ── DBMS Encyclopedia ─────────────────────────────────────────────────────────

@demos_bp.route('/databases')
@login_required
def db_index():
    return render_template('demos/db_index.html')

@demos_bp.route('/db-postgresql')
@login_required
def db_postgresql():
    return render_template('demos/db_postgresql.html')

@demos_bp.route('/db-mysql')
@login_required
def db_mysql():
    return render_template('demos/db_mysql.html')

@demos_bp.route('/db-redis')
@login_required
def db_redis():
    return render_template('demos/db_redis.html')

@demos_bp.route('/db-cassandra')
@login_required
def db_cassandra():
    return render_template('demos/db_cassandra.html')

@demos_bp.route('/db-snowflake')
@login_required
def db_snowflake():
    return render_template('demos/db_snowflake.html')

@demos_bp.route('/db-dynamodb')
@login_required
def db_dynamodb():
    return render_template('demos/db_dynamodb.html')

@demos_bp.route('/db-clickhouse')
@login_required
def db_clickhouse():
    return render_template('demos/db_clickhouse.html')

@demos_bp.route('/db-influxdb')
@login_required
def db_influxdb():
    return render_template('demos/db_influxdb.html')

@demos_bp.route('/db-pinecone')
@login_required
def db_pinecone():
    return render_template('demos/db_pinecone.html')

@demos_bp.route('/db-cockroachdb')
@login_required
def db_cockroachdb():
    return render_template('demos/db_cockroachdb.html')

# Phase 2 — Enterprise Relational Giants

@demos_bp.route('/db-oracle')
@login_required
def db_oracle():
    return render_template('demos/db_oracle.html')

@demos_bp.route('/db-sqlserver')
@login_required
def db_sqlserver():
    return render_template('demos/db_sqlserver.html')

@demos_bp.route('/db-sqlite')
@login_required
def db_sqlite():
    return render_template('demos/db_sqlite.html')

@demos_bp.route('/db-mariadb')
@login_required
def db_mariadb():
    return render_template('demos/db_mariadb.html')

@demos_bp.route('/db-db2')
@login_required
def db_db2():
    return render_template('demos/db_db2.html')

# Phase 3 — Additional NoSQL & Cache

@demos_bp.route('/db-memcached')
@login_required
def db_memcached():
    return render_template('demos/db_memcached.html')

@demos_bp.route('/db-couchbase')
@login_required
def db_couchbase():
    return render_template('demos/db_couchbase.html')

@demos_bp.route('/db-firestore')
@login_required
def db_firestore():
    return render_template('demos/db_firestore.html')

# Phase 4 — NewSQL / Distributed SQL Completion

@demos_bp.route('/db-spanner')
@login_required
def db_spanner():
    return render_template('demos/db_spanner.html')

@demos_bp.route('/db-tidb')
@login_required
def db_tidb():
    return render_template('demos/db_tidb.html')

@demos_bp.route('/db-oceanbase')
@login_required
def db_oceanbase():
    return render_template('demos/db_oceanbase.html')

# Phase 5 — Additional Search & Vector

@demos_bp.route('/db-opensearch')
@login_required
def db_opensearch():
    return render_template('demos/db_opensearch.html')

@demos_bp.route('/db-milvus')
@login_required
def db_milvus():
    return render_template('demos/db_milvus.html')

@demos_bp.route('/db-qdrant')
@login_required
def db_qdrant():
    return render_template('demos/db_qdrant.html')

# Phase 6 — Additional Time-Series

@demos_bp.route('/db-prometheus')
@login_required
def db_prometheus():
    return render_template('demos/db_prometheus.html')

@demos_bp.route('/db-timescaledb')
@login_required
def db_timescaledb():
    return render_template('demos/db_timescaledb.html')

# Phase 7 — Cloud-Native Managed Services

@demos_bp.route('/db-aurora')
@login_required
def db_aurora():
    return render_template('demos/db_aurora.html')

@demos_bp.route('/db-redshift')
@login_required
def db_redshift():
    return render_template('demos/db_redshift.html')

@demos_bp.route('/db-cosmosdb')
@login_required
def db_cosmosdb():
    return render_template('demos/db_cosmosdb.html')

@demos_bp.route('/db-azure-sql')
@login_required
def db_azure_sql():
    return render_template('demos/db_azure_sql.html')

@demos_bp.route('/db-synapse')
@login_required
def db_synapse():
    return render_template('demos/db_synapse.html')

@demos_bp.route('/db-polardb')
@login_required
def db_polardb():
    return render_template('demos/db_polardb.html')

# Phase 8 — Chinese Cloud Databases

@demos_bp.route('/db-gaussdb')
@login_required
def db_gaussdb():
    return render_template('demos/db_gaussdb.html')

@demos_bp.route('/db-tdsql')
@login_required
def db_tdsql():
    return render_template('demos/db_tdsql.html')


# ── Global Infrastructure Digital Twin ───────────────────────────────────────

@demos_bp.route('/global-infra')
@login_required
def global_infra_page():
    return render_template('demos/global_infra.html')


@demos_bp.route('/global-infra/nodes')
@login_required
def global_infra_nodes():
    from services.global_infra_service import get_all_nodes, get_cloud_nodes
    conn_str = _build_conn_str(current_app.config)
    return jsonify({
        'all':   get_all_nodes(conn_str),
        'cloud': get_cloud_nodes(conn_str),
    })


@demos_bp.route('/global-infra/edges')
@login_required
def global_infra_edges():
    from services.global_infra_service import get_edges_for_display
    return jsonify(get_edges_for_display(_build_conn_str(current_app.config)))


@demos_bp.route('/global-infra/route')
@login_required
def global_infra_route():
    from services.global_infra_service import route as gi_route
    src      = request.args.get('src', '').strip()
    dst      = request.args.get('dst', '').strip()
    disabled = request.args.get('disabled_edge', '').strip()
    if not src or not dst:
        return jsonify({'error': 'src and dst are required'}), 400
    edge = tuple(disabled.split(',')) if ',' in disabled else None

    # ?t= is minute-of-day (0–1439) — enables SQL orbital snapshot routing
    # ?hour= is legacy UTC hour (0–23) — used only when ?t= is absent
    t_raw    = request.args.get('t', '').strip()
    hour_raw = request.args.get('hour', '').strip()
    minute   = int(t_raw)    if t_raw.isdigit()    and 0 <= int(t_raw)    <= 1439 else None
    hour     = int(hour_raw) if hour_raw.isdigit() and 0 <= int(hour_raw) <= 23   \
               and minute is None else None

    result = gi_route(src, dst, edge,
                      conn_str=_build_conn_str(current_app.config),
                      hour_utc=hour, minute=minute)
    if 'error' in result and not result.get('terrestrial'):
        return jsonify(result), 400
    return jsonify(result)


@demos_bp.route('/global-infra/topology')
@login_required
def global_infra_topology():
    """Return 2 000 satellite positions for a given minute-of-day (0–1439)."""
    from services.global_infra_service import get_dynamic_topology
    raw = request.args.get('t', '').strip()
    minute = int(raw) if raw.isdigit() and 0 <= int(raw) <= 1439 else 0
    return jsonify(get_dynamic_topology(minute, _build_conn_str(current_app.config)))


@demos_bp.route('/global-infra/route-dynamic')
@login_required
def global_infra_route_dynamic():
    """Route through the pre-computed dynamic satellite topology for a given minute."""
    from services.global_infra_service import route_dynamic as gi_dyn
    src      = request.args.get('src', '').strip()
    dst      = request.args.get('dst', '').strip()
    disabled = request.args.get('disabled_edge', '').strip()
    raw      = request.args.get('t', '').strip()
    if not src or not dst:
        return jsonify({'error': 'src and dst are required'}), 400
    minute = int(raw) if raw.isdigit() and 0 <= int(raw) <= 1439 else 0
    edge   = tuple(disabled.split(',')) if ',' in disabled else None
    result = gi_dyn(src, dst, minute, conn_str=_build_conn_str(current_app.config),
                    disabled_edge=edge)
    if 'error' in result and not result.get('terrestrial'):
        return jsonify(result), 400
    return jsonify(result)


# =============================================================================
# Tételsor — 39-topic exam syllabus overlay
# =============================================================================
from services import dimat_exam


@demos_bp.route('/dimat/exam/<nn>')
def dimat_exam_topic(nn):
    try:
        n = int(nn)
    except (TypeError, ValueError):
        abort(404)
    if not 1 <= n <= 39:
        abort(404)
    topic = dimat_exam.get_topic(n)
    if topic is None:
        meta = dimat_exam.PATH_META[dimat_exam.PATH_OF_N[n]]
        prev_n = n - 1 if n - 1 >= meta['range'][0] else None
        next_n = n + 1 if n + 1 <= meta['range'][1] else None
        topic = {
            'n': n, 'title': f'Tétel {n} (még nincs feltöltve)',
            'glossary': 'Ez a tétel még nem rendelkezik feltöltött tartalommal.',
            'path': dimat_exam.PATH_OF_N[n], 'path_meta': meta,
            'related_dimat': [], 'related_ila': [], 'related_exercises': [],
            'formulas': [], 'body_html': '<p><em>Hamarosan…</em></p>',
            'prev': prev_n, 'next': next_n,
        }
    return render_template('demos/exam/page.html', topic=topic)


@demos_bp.route('/dimat/path/<slug>')
def dimat_path_index(slug):
    if slug not in ('combo', 'graph', 'szamelm'):
        abort(404)
    topics = dimat_exam.list_topics_in_path(slug)
    meta = dimat_exam.path_meta(slug)
    return render_template('demos/exam/path.html', slug=slug, topics=topics, meta=meta)


@demos_bp.route('/ila/path/foundations')
def ila_path_foundations():
    return render_template('demos/exam/path_foundations.html')


@demos_bp.route('/learn/tetelsor')
def learn_tetelsor():
    return render_template('learn/tetelsor.html',
                           combo=dimat_exam.list_topics_in_path('combo'),
                           graph=dimat_exam.list_topics_in_path('graph'),
                           szamelm=dimat_exam.list_topics_in_path('szamelm'))
