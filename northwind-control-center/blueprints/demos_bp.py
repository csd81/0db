"""
demos_bp.py — Visual Demo Lab blueprint.
"""
from flask import Blueprint, render_template, request, jsonify
from auth import login_required
import meta_db
from services import demo_service

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
    sqlite_conns = _conns_by_type("sqlite")
    return render_template("demos/log_shipping.html", sqlite_conns=sqlite_conns)


@demos_bp.route("/log-shipping/state")
@login_required
def log_shipping_state():
    master_conn_id = request.args.get("master_conn_id", 0)
    replica_conn_id = request.args.get("replica_conn_id", 0)
    try:
        state = demo_service.get_log_shipping_state(master_conn_id, replica_conn_id)
        return jsonify(state)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@demos_bp.route("/log-shipping/run", methods=["POST"])
@login_required
def log_shipping_run():
    master_conn_id = request.form.get("master_conn_id", 0)
    replica_conn_id = request.form.get("replica_conn_id", 0)
    try:
        result = demo_service.run_log_shipping_step(master_conn_id, replica_conn_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Snapshot ───────────────────────────────────────────────────────────────────

@demos_bp.route("/snapshot")
@login_required
def snapshot():
    return render_template("demos/snapshot.html")
