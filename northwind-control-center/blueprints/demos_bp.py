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
