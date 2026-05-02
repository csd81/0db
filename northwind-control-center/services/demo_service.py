"""
demo_service.py — Backend logic for Visual Demo Lab.
"""
import json
import time
import threading
import sqlite3
import db_adapter
import meta_db
from services import transaction_service as ts


# ── ACID Bank Transfer ─────────────────────────────────────────────────────────

def _ensure_accounts(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS accounts "
        "(id INTEGER PRIMARY KEY, name TEXT, balance REAL)"
    )
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)",
            [(1, "Alice", 1000.0), (2, "Bob", 500.0), (3, "Carol", 750.0)],
        )
        conn.commit()


def bank_transfer(conn_id, from_id, to_id, amount, force_fail=False):
    conn = db_adapter.get_adapter_connection(conn_id)
    _ensure_accounts(conn)

    steps = []
    success = False
    error = None

    try:
        conn.execute("BEGIN")
        steps.append({"step": 1, "sql": "BEGIN", "ok": True,
                       "balance_from": None, "balance_to": None})

        row = conn.execute(
            "SELECT balance FROM accounts WHERE id = ?", (from_id,)
        ).fetchone()
        bal_from = float(row[0]) if row else None
        steps.append({
            "step": 2,
            "sql": f"SELECT balance FROM accounts WHERE id = {from_id}",
            "ok": row is not None,
            "balance_from": bal_from,
            "balance_to": None,
        })

        if bal_from is None or bal_from < amount:
            steps.append({
                "step": 3,
                "sql": f"CHECK balance ({bal_from}) >= amount ({amount})",
                "ok": False,
                "balance_from": bal_from,
                "balance_to": None,
            })
            raise RuntimeError(
                f"Insufficient funds: balance={bal_from}, requested={amount}"
            )
        steps.append({
            "step": 3,
            "sql": f"CHECK balance ({bal_from}) >= amount ({amount})",
            "ok": True,
            "balance_from": bal_from,
            "balance_to": None,
        })

        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id),
        )
        steps.append({
            "step": 4,
            "sql": f"UPDATE accounts SET balance = balance - {amount} WHERE id = {from_id}",
            "ok": True,
            "balance_from": bal_from - amount,
            "balance_to": None,
        })

        if force_fail:
            steps.append({
                "step": 5,
                "sql": "-- Simulated crash before second UPDATE",
                "ok": False,
                "balance_from": bal_from - amount,
                "balance_to": None,
            })
            raise RuntimeError("Simulated failure")

        row2 = conn.execute(
            "SELECT balance FROM accounts WHERE id = ?", (to_id,)
        ).fetchone()
        bal_to = float(row2[0]) if row2 else 0.0

        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id),
        )
        steps.append({
            "step": 5,
            "sql": f"UPDATE accounts SET balance = balance + {amount} WHERE id = {to_id}",
            "ok": True,
            "balance_from": bal_from - amount,
            "balance_to": bal_to + amount,
        })

        conn.execute("COMMIT")
        steps.append({"step": 6, "sql": "COMMIT", "ok": True,
                       "balance_from": bal_from - amount,
                       "balance_to": bal_to + amount})
        success = True

    except Exception as exc:
        error = str(exc)
        try:
            conn.execute("ROLLBACK")
        except Exception:
            pass
        steps.append({"step": len(steps) + 1, "sql": "ROLLBACK",
                       "ok": False, "balance_from": None, "balance_to": None})

    final_rows = conn.execute(
        "SELECT id, name, balance FROM accounts ORDER BY id"
    ).fetchall()
    final_balances = [
        {"id": r[0], "name": r[1], "balance": float(r[2])} for r in final_rows
    ]

    return {
        "success": success,
        "steps": steps,
        "final_balances": final_balances,
        "error": error,
    }


def get_accounts(conn_id):
    conn = db_adapter.get_adapter_connection(conn_id)
    _ensure_accounts(conn)
    rows = conn.execute(
        "SELECT id, name, balance FROM accounts ORDER BY id"
    ).fetchall()
    return [{"id": r[0], "name": r[1], "balance": float(r[2])} for r in rows]


# ── Deadlock Scenario ──────────────────────────────────────────────────────────

def create_deadlock_scenario(pg_conn_id):
    rec = meta_db.get_connection_by_id(pg_conn_id)
    if rec is None or rec["db_type"] != "postgresql":
        raise ValueError("Deadlock demo requires a PostgreSQL connection.")

    import psycopg2

    params = rec["conn_params"]
    password = rec.get("password", "")

    def _make_pg_conn():
        return psycopg2.connect(
            host=params.get("host", "localhost"),
            port=int(params.get("port", 5432)),
            dbname=params.get("database", "postgres"),
            user=params.get("username", "postgres"),
            password=password,
        )

    # Setup: ensure table + seed rows using a dedicated connection
    setup_conn = _make_pg_conn()
    setup_conn.autocommit = True
    cur = setup_conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deadlock_accounts
        (id INTEGER PRIMARY KEY, balance NUMERIC DEFAULT 1000)
    """)
    cur.execute("INSERT INTO deadlock_accounts (id, balance) VALUES (1, 1000) ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO deadlock_accounts (id, balance) VALUES (2, 1000) ON CONFLICT DO NOTHING")
    setup_conn.close()

    results = [None, None]

    def thread_a():
        conn_a = _make_pg_conn()
        conn_a.autocommit = False
        try:
            cur_a = conn_a.cursor()
            cur_a.execute("BEGIN")
            cur_a.execute("UPDATE deadlock_accounts SET balance = balance - 100 WHERE id = 1")
            time.sleep(0.15)
            cur_a.execute("UPDATE deadlock_accounts SET balance = balance + 100 WHERE id = 2")
            conn_a.commit()
            results[0] = {"ok": True, "error": None}
        except Exception as e:
            try:
                conn_a.rollback()
            except Exception:
                pass
            results[0] = {"ok": False, "error": str(e)}
        finally:
            try:
                conn_a.close()
            except Exception:
                pass

    def thread_b():
        conn_b = _make_pg_conn()
        conn_b.autocommit = False
        try:
            cur_b = conn_b.cursor()
            cur_b.execute("BEGIN")
            cur_b.execute("UPDATE deadlock_accounts SET balance = balance - 100 WHERE id = 2")
            time.sleep(0.15)
            cur_b.execute("UPDATE deadlock_accounts SET balance = balance + 100 WHERE id = 1")
            conn_b.commit()
            results[1] = {"ok": True, "error": None}
        except Exception as e:
            try:
                conn_b.rollback()
            except Exception:
                pass
            results[1] = {"ok": False, "error": str(e)}
        finally:
            try:
                conn_b.close()
            except Exception:
                pass

    t_start = time.time()
    ta = threading.Thread(target=thread_a)
    tb = threading.Thread(target=thread_b)
    ta.start()
    tb.start()
    ta.join(timeout=10)
    tb.join(timeout=10)
    elapsed_ms = int((time.time() - t_start) * 1000)

    r_a = results[0] or {"ok": False, "error": "Thread timed out"}
    r_b = results[1] or {"ok": False, "error": "Thread timed out"}

    victim = None
    if not r_a["ok"] and r_b["ok"]:
        victim = "A"
    elif r_a["ok"] and not r_b["ok"]:
        victim = "B"
    elif not r_a["ok"] and not r_b["ok"]:
        victim = "A"  # fallback

    return {
        "thread_a": r_a,
        "thread_b": r_b,
        "victim": victim,
        "elapsed_ms": elapsed_ms,
    }


# ── Trigger Chain ──────────────────────────────────────────────────────────────

def _ensure_trigger_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS demo_orders (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            qty     INTEGER,
            ts      TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS demo_audit (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            action     TEXT,
            table_name TEXT,
            row_data   TEXT,
            ts         TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()


def get_trigger_chain_data(conn_id):
    conn = db_adapter.get_adapter_connection(conn_id)
    _ensure_trigger_tables(conn)
    orders = [
        dict(zip(["id", "product", "qty", "ts"], row))
        for row in conn.execute(
            "SELECT id, product, qty, ts FROM demo_orders ORDER BY id DESC LIMIT 50"
        ).fetchall()
    ]
    audit = [
        dict(zip(["id", "action", "table_name", "row_data", "ts"], row))
        for row in conn.execute(
            "SELECT id, action, table_name, row_data, ts FROM demo_audit ORDER BY id DESC LIMIT 50"
        ).fetchall()
    ]
    return {"orders": orders, "audit_log": audit}


def insert_demo_order(conn_id, product, qty):
    conn = db_adapter.get_adapter_connection(conn_id)
    _ensure_trigger_tables(conn)

    cur = conn.execute(
        "INSERT INTO demo_orders (product, qty) VALUES (?, ?)", (product, int(qty))
    )
    order_id = cur.lastrowid
    conn.commit()

    row_data = json.dumps({"id": order_id, "product": product, "qty": int(qty)})
    cur2 = conn.execute(
        "INSERT INTO demo_audit (action, table_name, row_data) VALUES (?, ?, ?)",
        ("INSERT", "demo_orders", row_data),
    )
    audit_id = cur2.lastrowid
    conn.commit()

    return {"order_id": order_id, "audit_id": audit_id}


# ── Log Shipping ───────────────────────────────────────────────────────────────

def get_log_shipping_state(master_conn_id, replica_conn_id):
    master_conn = db_adapter.get_adapter_connection(int(master_conn_id))
    replica_conn = db_adapter.get_adapter_connection(int(replica_conn_id))

    ts.ensure_transaction_log(master_conn)
    ts.ensure_transaction_log(replica_conn)

    master_log = ts.get_transaction_log(master_conn)
    replica_log = ts.get_transaction_log(replica_conn)

    master_ids = {e["LogID"] for e in master_log}
    replica_ids = {e["LogID"] for e in replica_log}
    pending = master_ids - replica_ids
    pending_count = len(pending)

    in_sync = pending_count == 0 and len(master_log) > 0 and len(replica_log) > 0

    return {
        "master_log_count": len(master_log),
        "replica_log_count": len(replica_log),
        "pending_count": pending_count,
        "in_sync": in_sync,
    }


def run_log_shipping_step(master_conn_id, replica_conn_id):
    master_conn = db_adapter.get_adapter_connection(int(master_conn_id))
    replica_conn = db_adapter.get_adapter_connection(int(replica_conn_id))

    ts.ensure_transaction_log(master_conn)
    ts.ensure_transaction_log(replica_conn)

    master_log = ts.get_transaction_log(master_conn)
    replica_log = ts.get_transaction_log(replica_conn)

    replica_ids = {e["LogID"] for e in replica_log}
    pending = [e for e in master_log if e["LogID"] not in replica_ids]

    replicated = 0
    last_error = None
    for entry in pending:
        ok, err = ts.replay_log_entry(replica_conn, entry)
        if ok:
            # Also write the log entry itself into the replica's TransactionLog
            try:
                replica_conn.execute(
                    """INSERT INTO TransactionLog
                       (LogID, TableName, Operation, RecordID, OldData, NewData, Timestamp)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        entry["LogID"], entry["TableName"], entry["Operation"],
                        entry["RecordID"], entry["OldData"], entry["NewData"],
                        entry["Timestamp"],
                    ),
                )
                replica_conn.commit()
            except Exception:
                pass
            replicated += 1
        else:
            last_error = err

    return {"replicated_count": replicated, "error": last_error}
