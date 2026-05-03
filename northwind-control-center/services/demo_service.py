"""
demo_service.py — Backend logic for Visual Demo Lab.
"""
import copy
import re
import decimal
import datetime
import hashlib
import json
import os
import queue as _queue_mod
import random
import time
import threading
import sqlite3
import pyodbc
import requests as _requests
import db_adapter
import meta_db


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
    """
    Three-way cyclic deadlock: A locks row 1 then wants row 2,
    B locks row 2 then wants row 3, C locks row 3 then wants row 1.
    PostgreSQL detects the cycle and chooses one victim to roll back.
    """
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

    # Ensure table with 3 rows
    setup_conn = _make_pg_conn()
    setup_conn.autocommit = True
    cur = setup_conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deadlock_accounts
        (id INTEGER PRIMARY KEY, balance NUMERIC DEFAULT 1000)
    """)
    for i in (1, 2, 3):
        cur.execute(
            "INSERT INTO deadlock_accounts (id, balance) VALUES (%s, 1000) ON CONFLICT DO NOTHING",
            (i,)
        )
    setup_conn.close()

    results = [None, None, None]

    def _thread(idx, lock_first, lock_second):
        conn = _make_pg_conn()
        conn.autocommit = False
        try:
            c = conn.cursor()
            c.execute("BEGIN")
            c.execute("UPDATE deadlock_accounts SET balance = balance - 10 WHERE id = %s", (lock_first,))
            time.sleep(0.15)  # give other threads time to acquire their first lock
            c.execute("UPDATE deadlock_accounts SET balance = balance + 10 WHERE id = %s", (lock_second,))
            conn.commit()
            results[idx] = {"ok": True, "error": None}
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            results[idx] = {"ok": False, "error": str(e)}
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # Cyclic wait: A→1,2  B→2,3  C→3,1
    t_start = time.time()
    threads = [
        threading.Thread(target=_thread, args=(0, 1, 2)),
        threading.Thread(target=_thread, args=(1, 2, 3)),
        threading.Thread(target=_thread, args=(2, 3, 1)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)
    elapsed_ms = int((time.time() - t_start) * 1000)

    r = [results[i] or {"ok": False, "error": "Thread timed out"} for i in range(3)]
    labels = ["A", "B", "C"]

    victims = [labels[i] for i in range(3) if not r[i]["ok"]]
    committed = [labels[i] for i in range(3) if r[i]["ok"]]
    # PostgreSQL rolls back exactly one transaction in a deadlock
    victim = victims[0] if victims else None

    return {
        "thread_a": r[0],
        "thread_b": r[1],
        "thread_c": r[2],
        "victim": victim,
        "committed": committed,
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

_LS_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'log_shipping.db')
_LS_LOCK = threading.Lock()
_LS_STATE: dict = {
    'phase': 'idle', 'cycle': 0, 'total_cycles': 0, 'countdown': 0,
    'current_sql': '', 'replayed': 0, 'log_count': 0,
}

_CUSTOMERS = ['Alice', 'Bob', 'Carol', 'David', 'Eve']
_PRODUCTS  = ['Widget', 'Gadget', 'Doohickey', 'Thingamajig', 'Gizmo', 'Sprocket']
_STATUSES  = ['processing', 'shipped', 'cancelled']


def _ls_conn():
    conn = sqlite3.connect(_LS_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _ls_init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS orders_master (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            product  TEXT,
            qty      INTEGER,
            price    REAL,
            status   TEXT DEFAULT 'pending',
            ts       TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS shipment_log (
            seq       INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT,
            row_id    INTEGER,
            data_json TEXT,
            sql_text  TEXT,
            ts        TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS orders_replica (
            id       INTEGER PRIMARY KEY,
            customer TEXT,
            product  TEXT,
            qty      INTEGER,
            price    REAL,
            status   TEXT,
            ts       TEXT
        );
    """)
    conn.commit()


def _ls_reset(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS orders_master;
        DROP TABLE IF EXISTS shipment_log;
        DROP TABLE IF EXISTS orders_replica;
    """)
    conn.commit()
    _ls_init_db(conn)


def ls_get_state() -> dict:
    with _LS_LOCK:
        snapshot = dict(_LS_STATE)
    try:
        conn = _ls_conn()
        _ls_init_db(conn)
        master_rows = [dict(r) for r in conn.execute(
            "SELECT id, customer, product, qty, price, status, ts FROM orders_master ORDER BY id"
        ).fetchall()]
        log_entries = [dict(r) for r in conn.execute(
            "SELECT seq, operation, row_id, sql_text, ts FROM shipment_log ORDER BY seq"
        ).fetchall()]
        replica_rows = [dict(r) for r in conn.execute(
            "SELECT id, customer, product, qty, price, status, ts FROM orders_replica ORDER BY id"
        ).fetchall()]
        conn.close()
    except Exception:
        master_rows, log_entries, replica_rows = [], [], []
    snapshot['master_rows'] = master_rows
    snapshot['log_entries'] = log_entries
    snapshot['replica_rows'] = replica_rows
    return snapshot


def ls_start():
    with _LS_LOCK:
        if _LS_STATE['phase'] in ('active', 'gap', 'replay'):
            return
        _LS_STATE.update({
            'phase': 'active', 'cycle': 0, 'total_cycles': 0, 'countdown': 0,
            'current_sql': '', 'replayed': 0, 'log_count': 0,
        })
    threading.Thread(target=_ls_worker, daemon=True).start()


def _ls_worker():
    try:
        conn = _ls_conn()
        _ls_reset(conn)

        total_cycles = random.randint(10, 15)
        with _LS_LOCK:
            _LS_STATE['total_cycles'] = total_cycles

        # Phase active: run INSERT/UPDATE/DELETE cycles on master
        for cycle in range(1, total_cycles + 1):
            existing_ids = [r[0] for r in conn.execute("SELECT id FROM orders_master").fetchall()]

            if not existing_ids:
                op = 'INSERT'
            else:
                op = random.choices(['INSERT', 'UPDATE', 'DELETE'], weights=[60, 25, 15])[0]

            row_id = None
            data_json = None
            sql_text = ''

            if op == 'INSERT':
                c = random.choice(_CUSTOMERS)
                p = random.choice(_PRODUCTS)
                q = random.randint(1, 20)
                pr = round(random.uniform(9.99, 199.99), 2)
                sql_text = f"INSERT INTO orders_master (customer, product, qty, price) VALUES ('{c}', '{p}', {q}, {pr})"
                cur = conn.execute(
                    "INSERT INTO orders_master (customer, product, qty, price) VALUES (?, ?, ?, ?)",
                    (c, p, q, pr)
                )
                conn.commit()
                row_id = cur.lastrowid
                row = conn.execute(
                    "SELECT id, customer, product, qty, price, status, ts FROM orders_master WHERE id = ?",
                    (row_id,)
                ).fetchone()
                data_json = json.dumps(dict(row))

            elif op == 'UPDATE':
                row_id = random.choice(existing_ids)
                if random.random() < 0.5:
                    new_val = random.choice(_STATUSES)
                    sql_text = f"UPDATE orders_master SET status = '{new_val}' WHERE id = {row_id}"
                    conn.execute("UPDATE orders_master SET status = ? WHERE id = ?", (new_val, row_id))
                else:
                    new_val = random.randint(1, 50)
                    sql_text = f"UPDATE orders_master SET qty = {new_val} WHERE id = {row_id}"
                    conn.execute("UPDATE orders_master SET qty = ? WHERE id = ?", (new_val, row_id))
                conn.commit()
                row = conn.execute(
                    "SELECT id, customer, product, qty, price, status, ts FROM orders_master WHERE id = ?",
                    (row_id,)
                ).fetchone()
                data_json = json.dumps(dict(row)) if row else '{}'

            else:  # DELETE
                row_id = random.choice(existing_ids)
                row = conn.execute(
                    "SELECT id, customer, product, qty, price, status, ts FROM orders_master WHERE id = ?",
                    (row_id,)
                ).fetchone()
                data_json = json.dumps(dict(row)) if row else '{}'
                sql_text = f"DELETE FROM orders_master WHERE id = {row_id}"
                conn.execute("DELETE FROM orders_master WHERE id = ?", (row_id,))
                conn.commit()

            conn.execute(
                "INSERT INTO shipment_log (operation, row_id, data_json, sql_text) VALUES (?, ?, ?, ?)",
                (op, row_id, data_json, sql_text)
            )
            conn.commit()
            log_count = conn.execute("SELECT COUNT(*) FROM shipment_log").fetchone()[0]

            with _LS_LOCK:
                _LS_STATE['cycle'] = cycle
                _LS_STATE['current_sql'] = sql_text
                _LS_STATE['log_count'] = log_count

            time.sleep(1.0)

        # Phase gap: 15s countdown, replica stays empty
        with _LS_LOCK:
            _LS_STATE['phase'] = 'gap'
            _LS_STATE['current_sql'] = ''
        for remaining in range(15, 0, -1):
            with _LS_LOCK:
                _LS_STATE['countdown'] = remaining
            time.sleep(1.0)

        # Phase replay: apply each log entry to replica at 400ms intervals
        with _LS_LOCK:
            _LS_STATE['phase'] = 'replay'
            _LS_STATE['countdown'] = 0

        entries = conn.execute(
            "SELECT seq, operation, row_id, data_json, sql_text FROM shipment_log ORDER BY seq"
        ).fetchall()

        for i, entry in enumerate(entries, 1):
            op = entry[1]
            row_id = entry[2]
            data = json.loads(entry[3] or '{}')
            sql_text = entry[4]

            with _LS_LOCK:
                _LS_STATE['current_sql'] = sql_text
                _LS_STATE['replayed'] = i

            if op in ('INSERT', 'UPDATE') and data:
                conn.execute(
                    "INSERT OR REPLACE INTO orders_replica "
                    "(id, customer, product, qty, price, status, ts) "
                    "VALUES (:id, :customer, :product, :qty, :price, :status, :ts)",
                    data
                )
            elif op == 'DELETE':
                conn.execute("DELETE FROM orders_replica WHERE id = ?", (row_id,))
            conn.commit()
            time.sleep(0.4)

        conn.close()
        with _LS_LOCK:
            _LS_STATE['phase'] = 'done'
            _LS_STATE['current_sql'] = ''

    except Exception as exc:
        with _LS_LOCK:
            _LS_STATE['phase'] = 'error'
            _LS_STATE['current_sql'] = str(exc)


# ── Snapshot Replication ──────────────────────────────────────────────────────

_SS_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'snapshot.db')
_SS_LOCK = threading.Lock()
_SS_STATE: dict = {
    'phase': 'idle', 'filled': 0, 'total': 9, 'countdown': 0,
    'current_sql': '',
    'dist_ready': False, 'sub_a_ready': False, 'sub_b_ready': False, 'sub_c_ready': False,
}

_CURRENCY_RATES = [
    ('USD', 'HUF', 350.50),
    ('EUR', 'HUF', 385.20),
    ('GBP', 'HUF', 445.00),
    ('CHF', 'HUF', 398.30),
    ('JPY', 'HUF',   2.35),
    ('CAD', 'HUF', 258.40),
    ('AUD', 'HUF', 231.60),
    ('DKK', 'HUF',  51.80),
    ('SEK', 'HUF',  33.10),
]


def _ss_conn():
    conn = sqlite3.connect(_SS_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _ss_init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS publisher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_from TEXT, currency_to TEXT, rate REAL,
            ts TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS distributor (
            id INTEGER PRIMARY KEY, currency_from TEXT, currency_to TEXT, rate REAL, ts TEXT
        );
        CREATE TABLE IF NOT EXISTS subscriber_a (
            id INTEGER PRIMARY KEY, currency_from TEXT, currency_to TEXT, rate REAL, ts TEXT
        );
        CREATE TABLE IF NOT EXISTS subscriber_b (
            id INTEGER PRIMARY KEY, currency_from TEXT, currency_to TEXT, rate REAL, ts TEXT
        );
        CREATE TABLE IF NOT EXISTS subscriber_c (
            id INTEGER PRIMARY KEY, currency_from TEXT, currency_to TEXT, rate REAL, ts TEXT
        );
    """)
    conn.commit()


def _ss_reset(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS publisher;
        DROP TABLE IF EXISTS distributor;
        DROP TABLE IF EXISTS subscriber_a;
        DROP TABLE IF EXISTS subscriber_b;
        DROP TABLE IF EXISTS subscriber_c;
    """)
    conn.commit()
    _ss_init_db(conn)


def ss_get_state() -> dict:
    with _SS_LOCK:
        snapshot = dict(_SS_STATE)
    try:
        conn = _ss_conn()
        _ss_init_db(conn)
        cols = "id, currency_from, currency_to, rate, ts"
        snapshot['publisher_rows']   = [dict(r) for r in conn.execute(f"SELECT {cols} FROM publisher   ORDER BY id").fetchall()]
        snapshot['distributor_rows'] = [dict(r) for r in conn.execute(f"SELECT {cols} FROM distributor ORDER BY id").fetchall()]
        snapshot['sub_a_rows']       = [dict(r) for r in conn.execute(f"SELECT {cols} FROM subscriber_a ORDER BY id").fetchall()]
        snapshot['sub_b_rows']       = [dict(r) for r in conn.execute(f"SELECT {cols} FROM subscriber_b ORDER BY id").fetchall()]
        snapshot['sub_c_rows']       = [dict(r) for r in conn.execute(f"SELECT {cols} FROM subscriber_c ORDER BY id").fetchall()]
        conn.close()
    except Exception:
        for k in ('publisher_rows', 'distributor_rows', 'sub_a_rows', 'sub_b_rows', 'sub_c_rows'):
            snapshot[k] = []
    return snapshot


def ss_start():
    with _SS_LOCK:
        if _SS_STATE['phase'] in ('filling', 'gap', 'snapshot', 'push_a', 'push_b', 'push_c'):
            return
        _SS_STATE.update({
            'phase': 'filling', 'filled': 0, 'total': len(_CURRENCY_RATES),
            'countdown': 0, 'current_sql': '',
            'dist_ready': False, 'sub_a_ready': False, 'sub_b_ready': False, 'sub_c_ready': False,
        })
    threading.Thread(target=_ss_worker, daemon=True).start()


def _ss_worker():
    try:
        conn = _ss_conn()
        _ss_reset(conn)

        # Phase filling: INSERT currency rates one by one at 0.35s intervals
        for i, (frm, to, rate) in enumerate(_CURRENCY_RATES, 1):
            sql = f"INSERT INTO publisher (currency_from, currency_to, rate) VALUES ('{frm}', '{to}', {rate})"
            conn.execute(
                "INSERT INTO publisher (currency_from, currency_to, rate) VALUES (?, ?, ?)",
                (frm, to, rate)
            )
            conn.commit()
            with _SS_LOCK:
                _SS_STATE['filled'] = i
                _SS_STATE['current_sql'] = sql
            time.sleep(0.35)

        # Phase gap: 5s countdown — simulate snapshot agent waking up
        with _SS_LOCK:
            _SS_STATE['phase'] = 'gap'
            _SS_STATE['current_sql'] = '-- Snapshot agent sleeping... waiting for scheduled run'
        for remaining in range(5, 0, -1):
            with _SS_LOCK:
                _SS_STATE['countdown'] = remaining
            time.sleep(1.0)

        # Phase snapshot: BCP publisher → distributor (bulk, no transaction log)
        with _SS_LOCK:
            _SS_STATE['phase'] = 'snapshot'
            _SS_STATE['countdown'] = 0
            _SS_STATE['current_sql'] = '-- BCP OUT: Bulk Copy publisher → distributor (no transaction log)'

        pub_rows = conn.execute(
            "SELECT id, currency_from, currency_to, rate, ts FROM publisher ORDER BY id"
        ).fetchall()
        conn.executemany(
            "INSERT OR REPLACE INTO distributor (id, currency_from, currency_to, rate, ts) VALUES (?, ?, ?, ?, ?)",
            [tuple(r) for r in pub_rows]
        )
        conn.commit()
        with _SS_LOCK:
            _SS_STATE['dist_ready'] = True
        time.sleep(1.2)

        # Phase push_a/b/c: distributor → each subscriber (0.6s apart)
        dist_rows = conn.execute(
            "SELECT id, currency_from, currency_to, rate, ts FROM distributor ORDER BY id"
        ).fetchall()

        for sub_table, sub_key, phase_name in [
            ('subscriber_a', 'sub_a_ready', 'push_a'),
            ('subscriber_b', 'sub_b_ready', 'push_b'),
            ('subscriber_c', 'sub_c_ready', 'push_c'),
        ]:
            with _SS_LOCK:
                _SS_STATE['phase'] = phase_name
                _SS_STATE['current_sql'] = f'-- PUSH: distributor → {sub_table.replace("_", " ").title()}'
            conn.executemany(
                f"INSERT OR REPLACE INTO {sub_table} (id, currency_from, currency_to, rate, ts) VALUES (?, ?, ?, ?, ?)",
                [tuple(r) for r in dist_rows]
            )
            conn.commit()
            with _SS_LOCK:
                _SS_STATE[sub_key] = True
            time.sleep(1.0)

        conn.close()
        with _SS_LOCK:
            _SS_STATE['phase'] = 'done'
            _SS_STATE['current_sql'] = '-- Snapshot replication complete. All 3 subscribers in sync.'

    except Exception as exc:
        with _SS_LOCK:
            _SS_STATE['phase'] = 'error'
            _SS_STATE['current_sql'] = str(exc)


# ── Transactional Replication ─────────────────────────────────────────────────

_TR_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'transactional.db')
_TR_LOCK = threading.Lock()
_TR_STATE: dict = {
    'running': False, 'tx_count': 0, 'success_count': 0, 'fail_count': 0,
    'current_sql': '', 'agent': '',
}

_TR_CUSTOMERS = [
    ('Alice', 1500.0), ('Bob', 800.0), ('Carol', 2200.0),
    ('David', 450.0),  ('Eve', 1200.0),
]
_TR_ITEMS = [
    ('Widget',    30, 25.0),
    ('Gadget',    15, 89.0),
    ('Doohickey', 50, 12.0),
    ('Sprocket',  20, 45.0),
    ('Gizmo',      8, 150.0),
]


def _tr_conn():
    conn = sqlite3.connect(_TR_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None  # autocommit; we manage transactions explicitly
    return conn


def _tr_init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS pub_balances (
            customer TEXT PRIMARY KEY,
            balance  REAL,
            ts       TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS pub_inventory (
            item  TEXT PRIMARY KEY,
            stock INTEGER,
            price REAL,
            ts    TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS pub_orders (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            item     TEXT,
            qty      INTEGER,
            amount   REAL,
            status   TEXT,
            ts       TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS pub_company (
            name    TEXT PRIMARY KEY,
            balance REAL,
            ts      TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS dist_log (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            op_sql  TEXT,
            status  TEXT DEFAULT 'pending',
            ts      TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS sub_balances (
            customer TEXT PRIMARY KEY,
            balance  REAL,
            ts       TEXT
        );
        CREATE TABLE IF NOT EXISTS sub_inventory (
            item  TEXT PRIMARY KEY,
            stock INTEGER,
            price REAL,
            ts    TEXT
        );
        CREATE TABLE IF NOT EXISTS sub_orders (
            id       INTEGER PRIMARY KEY,
            customer TEXT,
            item     TEXT,
            qty      INTEGER,
            amount   REAL,
            status   TEXT,
            ts       TEXT
        );
        CREATE TABLE IF NOT EXISTS sub_company (
            name    TEXT PRIMARY KEY,
            balance REAL,
            ts      TEXT
        );
    """)


def _tr_reset(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS pub_balances;
        DROP TABLE IF EXISTS pub_inventory;
        DROP TABLE IF EXISTS pub_orders;
        DROP TABLE IF EXISTS pub_company;
        DROP TABLE IF EXISTS dist_log;
        DROP TABLE IF EXISTS sub_balances;
        DROP TABLE IF EXISTS sub_inventory;
        DROP TABLE IF EXISTS sub_orders;
        DROP TABLE IF EXISTS sub_company;
    """)
    _tr_init_db(conn)
    conn.execute("BEGIN")
    for customer, balance in _TR_CUSTOMERS:
        conn.execute("INSERT INTO pub_balances (customer, balance) VALUES (?, ?)", (customer, balance))
        conn.execute("INSERT INTO sub_balances (customer, balance, ts) VALUES (?, ?, datetime('now','localtime'))", (customer, balance))
    for item, stock, price in _TR_ITEMS:
        conn.execute("INSERT INTO pub_inventory (item, stock, price) VALUES (?, ?, ?)", (item, stock, price))
        conn.execute("INSERT INTO sub_inventory (item, stock, price, ts) VALUES (?, ?, ?, datetime('now','localtime'))", (item, stock, price))
    conn.execute("INSERT INTO pub_company (name, balance) VALUES ('HQ', 0.0)")
    conn.execute("INSERT INTO sub_company (name, balance, ts) VALUES ('HQ', 0.0, datetime('now','localtime'))")
    conn.execute("COMMIT")


def tr_get_state() -> dict:
    with _TR_LOCK:
        snapshot = dict(_TR_STATE)
    try:
        conn = _tr_conn()
        _tr_init_db(conn)
        snapshot['pub_orders']    = [dict(r) for r in conn.execute(
            "SELECT id, customer, item, qty, amount, status, ts FROM pub_orders ORDER BY id DESC LIMIT 8"
        ).fetchall()]
        snapshot['pub_balances']  = [dict(r) for r in conn.execute(
            "SELECT customer, balance, ts FROM pub_balances ORDER BY customer"
        ).fetchall()]
        snapshot['pub_inventory'] = [dict(r) for r in conn.execute(
            "SELECT item, stock, price, ts FROM pub_inventory ORDER BY item"
        ).fetchall()]
        snapshot['dist_log']      = [dict(r) for r in conn.execute(
            "SELECT id, op_sql, status, ts FROM dist_log ORDER BY id DESC LIMIT 10"
        ).fetchall()]
        snapshot['sub_orders']    = [dict(r) for r in conn.execute(
            "SELECT id, customer, item, qty, amount, status, ts FROM sub_orders ORDER BY id DESC LIMIT 8"
        ).fetchall()]
        snapshot['pub_company']   = [dict(r) for r in conn.execute(
            "SELECT name, balance, ts FROM pub_company"
        ).fetchall()]
        snapshot['sub_balances']  = [dict(r) for r in conn.execute(
            "SELECT customer, balance, ts FROM sub_balances ORDER BY customer"
        ).fetchall()]
        snapshot['sub_inventory'] = [dict(r) for r in conn.execute(
            "SELECT item, stock, price, ts FROM sub_inventory ORDER BY item"
        ).fetchall()]
        snapshot['sub_company']   = [dict(r) for r in conn.execute(
            "SELECT name, balance, ts FROM sub_company"
        ).fetchall()]
        conn.close()
    except Exception:
        for key in ('pub_orders','pub_balances','pub_inventory','pub_company',
                    'dist_log','sub_orders','sub_balances','sub_inventory','sub_company'):
            snapshot[key] = []
    return snapshot


def tr_start():
    with _TR_LOCK:
        if _TR_STATE['running']:
            return
        _TR_STATE.update({
            'running': True, 'tx_count': 0, 'success_count': 0,
            'fail_count': 0, 'current_sql': '', 'agent': '',
        })
    threading.Thread(target=_tr_worker, daemon=True).start()


def tr_stop():
    with _TR_LOCK:
        _TR_STATE['running'] = False


def _tr_interruptible_sleep(seconds):
    deadline = time.time() + seconds
    while time.time() < deadline:
        with _TR_LOCK:
            if not _TR_STATE['running']:
                return
        time.sleep(0.05)


def _tr_worker():
    try:
        conn = _tr_conn()
        _tr_reset(conn)

        while True:
            with _TR_LOCK:
                if not _TR_STATE['running']:
                    break

            # ── Replenish customer balances so the demo doesn't stall ─────────
            for customer, init_bal in _TR_CUSTOMERS:
                row = conn.execute("SELECT balance FROM pub_balances WHERE customer = ?", (customer,)).fetchone()
                if row and row['balance'] < 50:
                    conn.execute("BEGIN")
                    conn.execute("UPDATE pub_balances SET balance = ?, ts = datetime('now','localtime') WHERE customer = ?", (init_bal, customer))
                    conn.execute("UPDATE sub_balances SET balance = ?, ts = datetime('now','localtime') WHERE customer = ?", (init_bal, customer))
                    conn.execute("COMMIT")

            # ── Pick random order ─────────────────────────────────────────────
            customer, _ = random.choice(_TR_CUSTOMERS)
            item, _, price = random.choice(_TR_ITEMS)
            qty    = random.randint(1, 5)
            amount = round(price * qty, 2)

            inv_row = conn.execute("SELECT stock FROM pub_inventory WHERE item = ?", (item,)).fetchone()
            bal_row = conn.execute("SELECT balance FROM pub_balances WHERE customer = ?", (customer,)).fetchone()
            stock   = inv_row['stock']   if inv_row else 0
            balance = bal_row['balance'] if bal_row else 0.0

            can_fulfill = stock >= qty and balance >= amount

            if can_fulfill:
                sql_order  = (f"INSERT INTO orders (customer,item,qty,amount,status) "
                              f"VALUES ('{customer}','{item}',{qty},{amount:.2f},'fulfilled')")
                sql_inv    = f"UPDATE inventory SET stock = stock - {qty} WHERE item = '{item}'"
                sql_bal    = f"UPDATE balances SET balance = balance - {amount:.2f} WHERE customer = '{customer}'"
                sql_co     = f"UPDATE company SET balance = balance + {amount:.2f} WHERE name = 'HQ'"

                with _TR_LOCK:
                    _TR_STATE['current_sql'] = f'BEGIN; {sql_order}'
                    _TR_STATE['agent'] = 'log_reader'

                conn.execute("BEGIN")
                cur = conn.execute(
                    "INSERT INTO pub_orders (customer, item, qty, amount, status) VALUES (?,?,?,?,'fulfilled')",
                    (customer, item, qty, amount)
                )
                order_id = cur.lastrowid
                conn.execute(
                    "UPDATE pub_inventory SET stock = stock - ?, ts = datetime('now','localtime') WHERE item = ?",
                    (qty, item)
                )
                conn.execute(
                    "UPDATE pub_balances SET balance = balance - ?, ts = datetime('now','localtime') WHERE customer = ?",
                    (amount, customer)
                )
                conn.execute(
                    "UPDATE pub_company SET balance = balance + ?, ts = datetime('now','localtime') WHERE name = 'HQ'",
                    (amount,)
                )
                conn.execute("COMMIT")

                with _TR_LOCK:
                    _TR_STATE['current_sql'] = f'COMMIT  -- order #{order_id}: {qty}x {item} for {customer}'
                    _TR_STATE['tx_count']     += 1
                    _TR_STATE['success_count'] += 1

                # ── Log Reader: 4 change entries to distributor ───────────────
                conn.execute("BEGIN")
                for sql_line in (sql_order, sql_inv, sql_bal, sql_co):
                    conn.execute("INSERT INTO dist_log (op_sql, status) VALUES (?, 'pending')", (sql_line,))
                conn.execute("COMMIT")

                _tr_interruptible_sleep(0.35)
                with _TR_LOCK:
                    if not _TR_STATE['running']:
                        break

                # ── Distribution Agent: apply all 4 changes to subscriber ─────
                with _TR_LOCK:
                    _TR_STATE['agent'] = 'distribution'
                    _TR_STATE['current_sql'] = f'[Distribution Agent] → Subscriber: {sql_order}'

                pub_order   = conn.execute(
                    "SELECT id, customer, item, qty, amount, status, ts FROM pub_orders WHERE id = ?",
                    (order_id,)
                ).fetchone()
                new_inv     = conn.execute("SELECT stock, price, ts FROM pub_inventory WHERE item = ?", (item,)).fetchone()
                new_bal     = conn.execute("SELECT balance, ts FROM pub_balances WHERE customer = ?", (customer,)).fetchone()
                new_company = conn.execute("SELECT balance, ts FROM pub_company WHERE name = 'HQ'").fetchone()

                conn.execute("BEGIN")
                if pub_order:
                    conn.execute(
                        "INSERT OR REPLACE INTO sub_orders (id,customer,item,qty,amount,status,ts) VALUES (?,?,?,?,?,?,?)",
                        tuple(pub_order)
                    )
                if new_inv:
                    conn.execute("UPDATE sub_inventory SET stock = ?, ts = ? WHERE item = ?",
                                 (new_inv['stock'], new_inv['ts'], item))
                if new_bal:
                    conn.execute("UPDATE sub_balances SET balance = ?, ts = ? WHERE customer = ?",
                                 (new_bal['balance'], new_bal['ts'], customer))
                if new_company:
                    conn.execute("UPDATE sub_company SET balance = ?, ts = ? WHERE name = 'HQ'",
                                 (new_company['balance'], new_company['ts']))
                conn.execute("COMMIT")

                # Mark applied; trim log
                conn.execute("BEGIN")
                conn.execute("UPDATE dist_log SET status = 'applied' WHERE status = 'pending'")
                conn.execute("DELETE FROM dist_log WHERE id NOT IN "
                             "(SELECT id FROM dist_log ORDER BY id DESC LIMIT 10)")
                conn.execute("COMMIT")

            else:
                stock_out = stock < qty
                reason    = 'insufficient stock' if stock_out else 'insufficient balance'
                sql_fail  = (f"ROLLBACK  -- {customer} wants {qty}x {item} "
                             f"({amount:.2f}) — {reason}")

                conn.execute("BEGIN")
                conn.execute(
                    "INSERT INTO pub_orders (customer, item, qty, amount, status) VALUES (?,?,?,?,'failed')",
                    (customer, item, qty, amount)
                )
                conn.execute("INSERT INTO dist_log (op_sql, status) VALUES (?, 'applied')", (sql_fail,))
                conn.execute("DELETE FROM dist_log WHERE id NOT IN "
                             "(SELECT id FROM dist_log ORDER BY id DESC LIMIT 10)")
                conn.execute("COMMIT")

                with _TR_LOCK:
                    _TR_STATE['current_sql'] = sql_fail
                    _TR_STATE['agent']        = 'log_reader'
                    _TR_STATE['tx_count']     += 1
                    _TR_STATE['fail_count']   += 1

                # ── Restock trigger: fires only on a stock-out rollback ────────
                if stock_out:
                    inv_row     = conn.execute("SELECT price FROM pub_inventory WHERE item = ?", (item,)).fetchone()
                    company_row = conn.execute("SELECT balance FROM pub_company WHERE name = 'HQ'").fetchone()
                    if inv_row and company_row:
                        restock_cost = round(inv_row['price'] * 0.5 * 20, 2)
                        hq_balance   = company_row['balance']

                        if hq_balance >= restock_cost:
                            sql_tri_inv = (f"UPDATE inventory SET stock = stock + 20 "
                                          f"WHERE item = '{item}'  -- AFTER UPDATE TRIGGER")
                            sql_tri_co  = (f"UPDATE company SET balance = balance - {restock_cost:.2f} "
                                          f"WHERE name = 'HQ'  -- AFTER UPDATE TRIGGER")

                            conn.execute("BEGIN")
                            conn.execute(
                                "UPDATE pub_inventory SET stock = stock + 20, ts = datetime('now','localtime') WHERE item = ?",
                                (item,)
                            )
                            conn.execute(
                                "UPDATE pub_company SET balance = balance - ?, ts = datetime('now','localtime') WHERE name = 'HQ'",
                                (restock_cost,)
                            )
                            conn.execute("COMMIT")

                            conn.execute("BEGIN")
                            conn.execute("INSERT INTO dist_log (op_sql, status) VALUES (?, 'pending')", (sql_tri_inv,))
                            conn.execute("INSERT INTO dist_log (op_sql, status) VALUES (?, 'pending')", (sql_tri_co,))
                            conn.execute("COMMIT")

                            with _TR_LOCK:
                                _TR_STATE['current_sql'] = (
                                    f'[TRIGGER] RESTOCK 20x {item} — '
                                    f'HQ debited {restock_cost:.2f}'
                                )

                            _tr_interruptible_sleep(0.4)

                            new_inv     = conn.execute("SELECT stock, price, ts FROM pub_inventory WHERE item = ?", (item,)).fetchone()
                            new_company = conn.execute("SELECT balance, ts FROM pub_company WHERE name = 'HQ'").fetchone()
                            conn.execute("BEGIN")
                            if new_inv:
                                conn.execute("UPDATE sub_inventory SET stock = ?, ts = ? WHERE item = ?",
                                             (new_inv['stock'], new_inv['ts'], item))
                            if new_company:
                                conn.execute("UPDATE sub_company SET balance = ?, ts = ? WHERE name = 'HQ'",
                                             (new_company['balance'], new_company['ts']))
                            conn.execute("UPDATE dist_log SET status = 'applied' WHERE status = 'pending'")
                            conn.execute("DELETE FROM dist_log WHERE id NOT IN "
                                         "(SELECT id FROM dist_log ORDER BY id DESC LIMIT 10)")
                            conn.execute("COMMIT")

                        else:
                            sql_warn = (f"-- WARNING [TRIGGER]: low stock on '{item}', "
                                        f"HQ balance {hq_balance:.2f} < restock cost {restock_cost:.2f}")
                            conn.execute("BEGIN")
                            conn.execute("INSERT INTO dist_log (op_sql, status) VALUES (?, 'applied')", (sql_warn,))
                            conn.execute("DELETE FROM dist_log WHERE id NOT IN "
                                         "(SELECT id FROM dist_log ORDER BY id DESC LIMIT 10)")
                            conn.execute("COMMIT")
                            with _TR_LOCK:
                                _TR_STATE['current_sql'] = sql_warn

            _tr_interruptible_sleep(random.uniform(0.6, 2.2))

        conn.close()
        with _TR_LOCK:
            _TR_STATE['running'] = False
            _TR_STATE['agent']   = ''

    except Exception as exc:
        with _TR_LOCK:
            _TR_STATE['running']     = False
            _TR_STATE['current_sql'] = f'[ERROR] {exc}'


# ── Merge Replication ─────────────────────────────────────────────────────────

_MR_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'merge_replication.db')
_MR_LOCK    = threading.Lock()
_MR_STATE   = {
    'running': False, 'phase': 'idle',
    'current_sql': '', 'sync_count': 0, 'conflict_count': 0, 'offline_countdown': 0,
}

_MR_PACKAGES = [
    (1, 'PKG-001', 'Alice Brown',   '14 Oak Street'),
    (2, 'PKG-002', 'Bob Clark',     '7 Maple Ave'),
    (3, 'PKG-003', 'Carol Davis',   '33 Pine Road'),
    (4, 'PKG-004', 'David Evans',   '8 Cedar Lane'),
    (5, 'PKG-005', 'Eve Foster',    '21 Birch Blvd'),
    (6, 'PKG-006', 'Frank Green',   '5 Elm Drive'),
    (7, 'PKG-007', 'Grace Harris',  '17 Spruce Way'),
    (8, 'PKG-008', 'Hank Irving',   '3 Walnut Court'),
]

_MR_ALT_ADDRESSES = {
    'PKG-001': '14 Oak St, Apt 2B',
    'PKG-002': '7 Maple Ave, rear entrance',
    'PKG-003': '33 Pine Rd (leave w/ neighbor)',
    'PKG-004': '8 Cedar Lane, back door',
    'PKG-005': '21 Birch Blvd, Floor 3',
    'PKG-006': '5 Elm Drive, loading dock',
    'PKG-007': '17 Spruce Way (ring doorbell)',
    'PKG-008': '3 Walnut Ct, gate code: 4829',
}


def _mr_conn():
    conn = sqlite3.connect(_MR_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None
    return conn


def _mr_init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS central_deliveries (
            id         INTEGER PRIMARY KEY,
            package_id TEXT,
            customer   TEXT,
            address    TEXT,
            status     TEXT DEFAULT 'pending',
            notes      TEXT DEFAULT '',
            ts         TEXT DEFAULT (datetime('now','localtime')),
            dirty      INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS driver_deliveries (
            id         INTEGER PRIMARY KEY,
            package_id TEXT,
            customer   TEXT,
            address    TEXT,
            status     TEXT DEFAULT 'pending',
            notes      TEXT DEFAULT '',
            ts         TEXT DEFAULT (datetime('now','localtime')),
            dirty      INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS merge_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type  TEXT,
            package_id  TEXT,
            description TEXT,
            ts          TEXT DEFAULT (datetime('now','localtime'))
        );
    """)


def _mr_reset(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS central_deliveries;
        DROP TABLE IF EXISTS driver_deliveries;
        DROP TABLE IF EXISTS merge_log;
    """)
    _mr_init_db(conn)
    conn.execute("BEGIN")
    for pkg_id, package_id, customer, address in _MR_PACKAGES:
        conn.execute(
            "INSERT INTO central_deliveries (id, package_id, customer, address) VALUES (?,?,?,?)",
            (pkg_id, package_id, customer, address)
        )
        conn.execute(
            "INSERT INTO driver_deliveries (id, package_id, customer, address) VALUES (?,?,?,?)",
            (pkg_id, package_id, customer, address)
        )
    conn.execute("COMMIT")


def mr_get_state() -> dict:
    with _MR_LOCK:
        snapshot = dict(_MR_STATE)
    try:
        conn = _mr_conn()
        _mr_init_db(conn)
        snapshot['central_rows'] = [dict(r) for r in conn.execute(
            "SELECT id, package_id, customer, address, status, notes, ts, dirty "
            "FROM central_deliveries ORDER BY id"
        ).fetchall()]
        snapshot['merge_log'] = [dict(r) for r in conn.execute(
            "SELECT id, event_type, package_id, description, ts "
            "FROM merge_log ORDER BY id DESC LIMIT 15"
        ).fetchall()]
        snapshot['driver_rows'] = [dict(r) for r in conn.execute(
            "SELECT id, package_id, customer, address, status, notes, ts, dirty "
            "FROM driver_deliveries ORDER BY id"
        ).fetchall()]
        conn.close()
    except Exception:
        snapshot['central_rows'] = snapshot['merge_log'] = snapshot['driver_rows'] = []
    return snapshot


def mr_start():
    with _MR_LOCK:
        if _MR_STATE['running']:
            return
        _MR_STATE.update({
            'running': True, 'phase': 'starting', 'current_sql': '',
            'sync_count': 0, 'conflict_count': 0, 'offline_countdown': 0,
        })
    threading.Thread(target=_mr_worker, daemon=True).start()


def mr_stop():
    with _MR_LOCK:
        _MR_STATE['running'] = False


def _mr_interruptible_sleep(seconds):
    deadline = time.time() + seconds
    while time.time() < deadline:
        with _MR_LOCK:
            if not _MR_STATE['running']:
                return
        time.sleep(0.05)


def _mr_log(conn, event_type, package_id, description):
    conn.execute("BEGIN")
    conn.execute(
        "INSERT INTO merge_log (event_type, package_id, description) VALUES (?,?,?)",
        (event_type, package_id, description)
    )
    conn.execute(
        "DELETE FROM merge_log WHERE id NOT IN (SELECT id FROM merge_log ORDER BY id DESC LIMIT 15)"
    )
    conn.execute("COMMIT")


def _mr_worker():
    try:
        conn = _mr_conn()
        _mr_reset(conn)
        cycle = 0

        while True:
            with _MR_LOCK:
                if not _MR_STATE['running']:
                    break

            # Reset statuses every 3 cycles so demo keeps generating fresh events
            if cycle > 0 and cycle % 3 == 0:
                conn.execute("BEGIN")
                conn.execute("UPDATE central_deliveries SET status='pending', notes='', address=?, dirty=0 WHERE id=?",
                             ('14 Oak Street', 1))
                conn.execute("UPDATE driver_deliveries  SET status='pending', notes='', dirty=0")
                conn.execute("UPDATE central_deliveries SET status='pending', notes='', dirty=0")
                for _, package_id, _, address in _MR_PACKAGES:
                    conn.execute("UPDATE central_deliveries SET address=? WHERE package_id=?", (address, package_id))
                    conn.execute("UPDATE driver_deliveries  SET address=? WHERE package_id=?", (address, package_id))
                conn.execute("COMMIT")

            # ── Phase: Central Office makes changes ───────────────────────────
            with _MR_LOCK:
                _MR_STATE['phase'] = 'central_update'

            for pkg_id in random.sample(range(1, 9), k=random.randint(2, 3)):
                with _MR_LOCK:
                    if not _MR_STATE['running']:
                        break

                row = conn.execute(
                    "SELECT id, package_id, status, address FROM central_deliveries WHERE id=?", (pkg_id,)
                ).fetchone()
                if not row:
                    continue

                pkg, current_status = row['package_id'], row['status']

                if current_status == 'delivered':
                    action = 'address'
                elif current_status == 'cancelled':
                    action = 'priority'
                else:
                    action = random.choices(['cancel', 'address', 'priority'], weights=[30, 40, 30])[0]

                if action == 'cancel':
                    sql = f"UPDATE deliveries SET status='cancelled' WHERE package_id='{pkg}'"
                    conn.execute("BEGIN")
                    conn.execute(
                        "UPDATE central_deliveries SET status='cancelled', dirty=1, ts=datetime('now','localtime') WHERE id=?",
                        (pkg_id,)
                    )
                    conn.execute("COMMIT")
                elif action == 'address':
                    new_addr = _MR_ALT_ADDRESSES.get(pkg, row['address'] + ' (updated)')
                    sql = f"UPDATE deliveries SET address='...' WHERE package_id='{pkg}'"
                    conn.execute("BEGIN")
                    conn.execute(
                        "UPDATE central_deliveries SET address=?, dirty=1, ts=datetime('now','localtime') WHERE id=?",
                        (new_addr, pkg_id)
                    )
                    conn.execute("COMMIT")
                else:
                    sql = f"UPDATE deliveries SET notes='PRIORITY' WHERE package_id='{pkg}'"
                    conn.execute("BEGIN")
                    conn.execute(
                        "UPDATE central_deliveries SET notes='PRIORITY delivery', dirty=1, ts=datetime('now','localtime') WHERE id=?",
                        (pkg_id,)
                    )
                    conn.execute("COMMIT")

                with _MR_LOCK:
                    _MR_STATE['current_sql'] = f'[Central Office] {sql}'
                _mr_interruptible_sleep(1.0)

            with _MR_LOCK:
                if not _MR_STATE['running']:
                    break

            # ── Phase: Driver updates (offline) ───────────────────────────────
            with _MR_LOCK:
                _MR_STATE['phase'] = 'driver_update'

            for pkg_id in random.sample(range(1, 9), k=random.randint(2, 3)):
                with _MR_LOCK:
                    if not _MR_STATE['running']:
                        break

                row = conn.execute(
                    "SELECT id, package_id, status FROM driver_deliveries WHERE id=?", (pkg_id,)
                ).fetchone()
                if not row:
                    continue

                pkg, current_status = row['package_id'], row['status']

                if current_status in ('delivered', 'cancelled'):
                    action = 'note'
                else:
                    action = random.choices(['delivered', 'failed', 'note'], weights=[55, 15, 30])[0]

                if action == 'delivered':
                    sql = f"UPDATE deliveries SET status='delivered', notes='Signed' WHERE package_id='{pkg}'"
                    conn.execute("BEGIN")
                    conn.execute(
                        "UPDATE driver_deliveries SET status='delivered', notes='Signed by recipient', dirty=1, ts=datetime('now','localtime') WHERE id=?",
                        (pkg_id,)
                    )
                    conn.execute("COMMIT")
                elif action == 'failed':
                    sql = f"UPDATE deliveries SET status='failed', notes='No answer' WHERE package_id='{pkg}'"
                    conn.execute("BEGIN")
                    conn.execute(
                        "UPDATE driver_deliveries SET status='failed', notes='No answer at door', dirty=1, ts=datetime('now','localtime') WHERE id=?",
                        (pkg_id,)
                    )
                    conn.execute("COMMIT")
                else:
                    sql = f"UPDATE deliveries SET notes='Left at door' WHERE package_id='{pkg}'"
                    conn.execute("BEGIN")
                    conn.execute(
                        "UPDATE driver_deliveries SET notes='Left at front door', dirty=1, ts=datetime('now','localtime') WHERE id=?",
                        (pkg_id,)
                    )
                    conn.execute("COMMIT")

                with _MR_LOCK:
                    _MR_STATE['current_sql'] = f'[Driver Device] {sql}'
                _mr_interruptible_sleep(1.0)

            with _MR_LOCK:
                if not _MR_STATE['running']:
                    break

            # ── Offline countdown ─────────────────────────────────────────────
            with _MR_LOCK:
                _MR_STATE['phase'] = 'offline'

            for t in range(random.randint(4, 6), 0, -1):
                with _MR_LOCK:
                    if not _MR_STATE['running']:
                        break
                    _MR_STATE['offline_countdown'] = t
                    _MR_STATE['current_sql'] = f'-- Driver device offline — no signal ({t}s until sync)'
                _mr_interruptible_sleep(1.0)

            with _MR_LOCK:
                if not _MR_STATE['running']:
                    break
                _MR_STATE['offline_countdown'] = 0

            # ── Merge sync ────────────────────────────────────────────────────
            with _MR_LOCK:
                _MR_STATE['phase'] = 'syncing'
                _MR_STATE['current_sql'] = '-- Merge Agent: 4G signal acquired — starting sync…'

            _mr_log(conn, 'sync_start', '', 'Merge Agent connected — scanning dirty rows')
            _mr_interruptible_sleep(0.4)

            central_dirty = conn.execute(
                "SELECT id, package_id, status, address, notes FROM central_deliveries WHERE dirty=1"
            ).fetchall()
            driver_dirty = conn.execute(
                "SELECT id, package_id, status, address, notes FROM driver_deliveries WHERE dirty=1"
            ).fetchall()

            central_map = {r['id']: dict(r) for r in central_dirty}
            driver_map  = {r['id']: dict(r) for r in driver_dirty}

            conflict_ids = set(central_map) & set(driver_map)
            push_ids     = set(driver_map)   - conflict_ids
            pull_ids     = set(central_map)  - conflict_ids

            # PUSH: driver → central
            for pkg_id in sorted(push_ids):
                with _MR_LOCK:
                    if not _MR_STATE['running']:
                        break
                dr   = driver_map[pkg_id]
                desc = f"PUSH driver→central: {dr['package_id']} status={dr['status']}"
                conn.execute("BEGIN")
                conn.execute(
                    "UPDATE central_deliveries SET status=?, notes=?, dirty=0, ts=datetime('now','localtime') WHERE id=?",
                    (dr['status'], dr['notes'], pkg_id)
                )
                conn.execute("UPDATE driver_deliveries SET dirty=0 WHERE id=?", (pkg_id,))
                conn.execute("COMMIT")
                _mr_log(conn, 'push', dr['package_id'], desc)
                with _MR_LOCK:
                    _MR_STATE['current_sql'] = f'[Merge Agent] {desc}'
                _mr_interruptible_sleep(0.5)

            # PULL: central → driver
            for pkg_id in sorted(pull_ids):
                with _MR_LOCK:
                    if not _MR_STATE['running']:
                        break
                cr   = central_map[pkg_id]
                desc = f"PULL central→driver: {cr['package_id']} status={cr['status']}"
                conn.execute("BEGIN")
                conn.execute(
                    "UPDATE driver_deliveries SET status=?, address=?, notes=?, dirty=0, ts=datetime('now','localtime') WHERE id=?",
                    (cr['status'], cr['address'], cr['notes'], pkg_id)
                )
                conn.execute("UPDATE central_deliveries SET dirty=0 WHERE id=?", (pkg_id,))
                conn.execute("COMMIT")
                _mr_log(conn, 'pull', cr['package_id'], desc)
                with _MR_LOCK:
                    _MR_STATE['current_sql'] = f'[Merge Agent] {desc}'
                _mr_interruptible_sleep(0.5)

            # CONFLICTS: central wins
            for pkg_id in sorted(conflict_ids):
                with _MR_LOCK:
                    if not _MR_STATE['running']:
                        break
                cr, dr = central_map[pkg_id], driver_map[pkg_id]
                desc_c = f"CONFLICT {cr['package_id']}: Central={cr['status']} vs Driver={dr['status']}"
                _mr_log(conn, 'conflict', cr['package_id'], desc_c)
                with _MR_LOCK:
                    _MR_STATE['current_sql'] = f'[Merge Agent] {desc_c}'
                _mr_interruptible_sleep(0.7)

                conn.execute("BEGIN")
                conn.execute(
                    "UPDATE driver_deliveries SET status=?, address=?, notes=?, dirty=0, ts=datetime('now','localtime') WHERE id=?",
                    (cr['status'], cr['address'], cr['notes'], pkg_id)
                )
                conn.execute("UPDATE central_deliveries SET dirty=0 WHERE id=?", (pkg_id,))
                conn.execute("COMMIT")
                desc_r = f"RESOLVED {cr['package_id']}: Central wins → {cr['status']}"
                _mr_log(conn, 'resolved', cr['package_id'], desc_r)
                with _MR_LOCK:
                    _MR_STATE['current_sql'] = f'[Merge Agent] {desc_r}'
                    _MR_STATE['conflict_count'] += 1
                _mr_interruptible_sleep(0.5)

            with _MR_LOCK:
                next_num = _MR_STATE['sync_count'] + 1
            summary = (f"Sync #{next_num} done — "
                       f"{len(push_ids)} pushed, {len(pull_ids)} pulled, {len(conflict_ids)} conflicts")
            _mr_log(conn, 'sync_done', '', summary)
            with _MR_LOCK:
                _MR_STATE['sync_count']  += 1
                _MR_STATE['current_sql'] = f'[Merge Agent] {summary}'
                _MR_STATE['phase']       = 'synced'

            _mr_interruptible_sleep(2.5)
            cycle += 1

        conn.close()
        with _MR_LOCK:
            _MR_STATE['running'] = False
            _MR_STATE['phase']   = 'idle'

    except Exception as exc:
        with _MR_LOCK:
            _MR_STATE['running']     = False
            _MR_STATE['current_sql'] = f'[ERROR] {exc}'


# ── Blockchain Demo (rqlite-backed) ──────────────────────────────────────────

_BC_RQLITE = "http://127.0.0.1:4001"
_BC_LOCK   = threading.Lock()
_BC_STATE  = {
    'running': False, 'phase': 'idle',
    'current_sql': '', 'block_count': 0, 'fork_count': 0,
    'peers': {
        'Peer A': {'status': 'idle', 'nonce': 0, 'last_hash': ''},
        'Peer B': {'status': 'idle', 'nonce': 0, 'last_hash': ''},
        'Peer C': {'status': 'idle', 'nonce': 0, 'last_hash': ''},
    },
}

_BC_TXS = [
    'Alice→Bob: 1.5 BTC',   'Carol→Dave: 0.3 BTC',  'Eve→Frank: 5.0 BTC',
    'Grace→Hank: 0.01 BTC', 'Ivan→Judy: 2.2 BTC',   'Kate→Leo: 0.5 BTC',
    'Mike→Nina: 3.7 BTC',   'Oscar→Pam: 0.8 BTC',   'Quinn→Ray: 1.0 BTC',
    'Sara→Ted: 4.5 BTC',    'Uma→Vic: 0.2 BTC',      'Wendy→Xav: 6.0 BTC',
]


# ── rqlite helpers ────────────────────────────────────────────────────────────

def _bc_exec(sql, *args):
    payload = [[sql] + list(args)]
    r = _requests.post(f"{_BC_RQLITE}/db/execute", json=payload, timeout=5)
    return r.json()


def _bc_query(sql):
    r = _requests.get(f"{_BC_RQLITE}/db/query", params={'q': sql, 'level': 'weak'}, timeout=5)
    data = r.json()
    result = data.get('results', [{}])[0]
    cols = result.get('columns', [])
    rows = result.get('values', [])
    return [dict(zip(cols, row)) for row in rows]


# ── DB init / reset ───────────────────────────────────────────────────────────

def _bc_init():
    _bc_exec("""CREATE TABLE IF NOT EXISTS bc_blocks (
        height    INTEGER,
        hash      TEXT,
        prev_hash TEXT,
        miner     TEXT,
        nonce     INTEGER,
        txs       TEXT,
        orphan    INTEGER DEFAULT 0,
        ts        TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
    )""")
    _bc_exec("""CREATE TABLE IF NOT EXISTS bc_events (
        id     INTEGER PRIMARY KEY,
        event  TEXT,
        detail TEXT,
        ts     TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
    )""")


def _bc_reset():
    _bc_exec("DROP TABLE IF EXISTS bc_blocks")
    _bc_exec("DROP TABLE IF EXISTS bc_events")
    _bc_init()
    genesis_hash = "0000" + hashlib.sha256(b"genesis").hexdigest()[4:]
    _bc_exec(
        "INSERT INTO bc_blocks (height, hash, prev_hash, miner, nonce, txs) VALUES (?,?,?,?,?,?)",
        0, genesis_hash, "0" * 64, "Satoshi", 0, "Genesis — Bitcoin: A Peer-to-Peer Electronic Cash System"
    )
    _bc_exec("INSERT INTO bc_events (event, detail) VALUES (?,?)",
             "GENESIS", "Block #0 created — chain begins")


# ── Public API ────────────────────────────────────────────────────────────────

def bc_get_state() -> dict:
    with _BC_LOCK:
        snapshot = dict(_BC_STATE)
        snapshot['peers'] = {k: dict(v) for k, v in _BC_STATE['peers'].items()}
    try:
        snapshot['blocks'] = _bc_query(
            "SELECT height, hash, prev_hash, miner, nonce, txs, orphan, ts "
            "FROM bc_blocks ORDER BY height DESC, orphan ASC LIMIT 12"
        )
        snapshot['events'] = _bc_query(
            "SELECT id, event, detail, ts FROM bc_events ORDER BY id DESC LIMIT 15"
        )
        r = _requests.get(f"{_BC_RQLITE}/nodes", timeout=2)
        snapshot['nodes'] = r.json()
    except Exception:
        snapshot['blocks'] = snapshot['events'] = []
        snapshot['nodes'] = {}
    return snapshot


def bc_start():
    with _BC_LOCK:
        if _BC_STATE['running']:
            return
        _BC_STATE.update({
            'running': True, 'phase': 'starting', 'current_sql': '',
            'block_count': 0, 'fork_count': 0,
        })
        for p in _BC_STATE['peers'].values():
            p.update({'status': 'idle', 'nonce': 0, 'last_hash': ''})
    threading.Thread(target=_bc_worker, daemon=True).start()


def bc_stop():
    with _BC_LOCK:
        _BC_STATE['running'] = False


# ── Mining simulation ─────────────────────────────────────────────────────────

def _bc_mine_peer(peer_name, prev_hash, txs, result_q, stop_evt):
    """
    Simulates a miner: visually counts nonces for a random duration,
    then computes a real SHA-256 hash (low difficulty) for chain integrity.
    """
    mine_secs = random.uniform(2.0, 6.0)   # each peer takes 2–6s
    deadline  = time.time() + mine_secs
    nonce     = random.randint(10_000, 99_999)

    while not stop_evt.is_set() and time.time() < deadline:
        with _BC_LOCK:
            if not _BC_STATE['running']:
                return
            _BC_STATE['peers'][peer_name]['nonce']  = nonce
            _BC_STATE['peers'][peer_name]['status'] = 'mining'
        nonce += random.randint(80, 300)
        time.sleep(0.15)

    if stop_evt.is_set():
        return  # another peer won before timer expired

    # Real PoW (low difficulty "00" so it resolves instantly for chain integrity)
    data = f"{prev_hash}|{txs}|{peer_name}"
    real_nonce = nonce
    while not stop_evt.is_set():
        candidate = hashlib.sha256(f"{data}{real_nonce}".encode()).hexdigest()
        if candidate.startswith("00"):
            result_q.put((peer_name, real_nonce, candidate))
            return
        real_nonce += 1


# ── Main worker ───────────────────────────────────────────────────────────────

def _bc_worker():
    try:
        _bc_reset()
        with _BC_LOCK:
            _BC_STATE['phase'] = 'mining'

        while True:
            with _BC_LOCK:
                if not _BC_STATE['running']:
                    break

            # Get current canonical tip
            tip = _bc_query(
                "SELECT height, hash FROM bc_blocks WHERE orphan=0 ORDER BY height DESC LIMIT 1"
            )
            if not tip:
                break
            tip_height  = tip[0]['height']
            prev_hash   = tip[0]['hash']
            next_height = tip_height + 1

            peer_txs = {
                'Peer A': ' | '.join(random.sample(_BC_TXS, 2)),
                'Peer B': ' | '.join(random.sample(_BC_TXS, 2)),
                'Peer C': ' | '.join(random.sample(_BC_TXS, 2)),
            }

            with _BC_LOCK:
                for peer in _BC_STATE['peers']:
                    _BC_STATE['peers'][peer].update({'status': 'mining', 'nonce': 0})
                _BC_STATE['current_sql'] = (
                    f'-- Block #{next_height}: Peer A/B/C racing '
                    f'(PoW difficulty: hash must start with "00")'
                )

            result_q = _queue_mod.Queue()
            stop_evt  = threading.Event()

            for peer_name in ('Peer A', 'Peer B', 'Peer C'):
                threading.Thread(
                    target=_bc_mine_peer,
                    args=(peer_name, prev_hash, peer_txs[peer_name], result_q, stop_evt),
                    daemon=True
                ).start()

            # Wait for first winner
            try:
                winner, w_nonce, w_hash = result_q.get(timeout=30)
            except _queue_mod.Empty:
                stop_evt.set()
                break

            with _BC_LOCK:
                _BC_STATE['peers'][winner]['status']    = 'found'
                _BC_STATE['peers'][winner]['last_hash'] = w_hash[:12]
                _BC_STATE['current_sql'] = (
                    f'[{winner}] FOUND nonce={w_nonce} '
                    f'hash={w_hash[:12]}… — broadcasting to network'
                )

            # Simulate propagation delay — other peers keep mining during this
            time.sleep(random.uniform(0.5, 1.8))

            # Check if a second peer also finished during propagation → FORK
            fork_result = None
            try:
                fork_result = result_q.get_nowait()
            except _queue_mod.Empty:
                pass

            stop_evt.set()  # stop all remaining miners

            # Write winner's block to rqlite (the network ledger)
            sql = (f"INSERT INTO bc_blocks (height,hash,prev_hash,miner,nonce,txs) "
                   f"VALUES ({next_height},'{w_hash}','{prev_hash}','{winner}',{w_nonce},'...')")
            _bc_exec(
                "INSERT INTO bc_blocks (height,hash,prev_hash,miner,nonce,txs) VALUES (?,?,?,?,?,?)",
                next_height, w_hash, prev_hash, winner, w_nonce, peer_txs[winner]
            )
            _bc_exec("INSERT INTO bc_events (event,detail) VALUES (?,?)",
                     "BLOCK",
                     f"Block #{next_height} — miner: {winner} | hash: {w_hash[:12]}…")
            _bc_exec("DELETE FROM bc_events WHERE id NOT IN "
                     "(SELECT id FROM bc_events ORDER BY id DESC LIMIT 15)")

            with _BC_LOCK:
                _BC_STATE['block_count'] += 1
                _BC_STATE['current_sql']  = sql
                _BC_STATE['peers'][winner]['status'] = 'committed'

            # Handle fork
            if fork_result:
                f_peer, f_nonce, f_hash = fork_result
                fork_sql = (f"-- {f_peer} also found block #{next_height} "
                            f"hash={f_hash[:12]}… — ORPHANED (first-seen rule)")
                _bc_exec(
                    "INSERT INTO bc_blocks (height,hash,prev_hash,miner,nonce,txs,orphan) VALUES (?,?,?,?,?,?,1)",
                    next_height, f_hash, prev_hash, f_peer, f_nonce, peer_txs[f_peer]
                )
                _bc_exec("INSERT INTO bc_events (event,detail) VALUES (?,?)",
                         "FORK",
                         f"FORK at #{next_height}: {f_peer} orphaned ({f_hash[:12]}…) — "
                         f"{winner} wins (first-seen rule)")
                with _BC_LOCK:
                    _BC_STATE['fork_count']           += 1
                    _BC_STATE['peers'][f_peer]['status'] = 'orphaned'
                    _BC_STATE['current_sql']            = fork_sql

            time.sleep(0.8)
            with _BC_LOCK:
                for peer in _BC_STATE['peers']:
                    if _BC_STATE['peers'][peer]['status'] not in ('committed',):
                        _BC_STATE['peers'][peer]['status'] = 'idle'

            time.sleep(random.uniform(0.3, 1.0))

        with _BC_LOCK:
            _BC_STATE['running'] = False
            _BC_STATE['phase']   = 'idle'
            for p in _BC_STATE['peers'].values():
                p['status'] = 'idle'

    except Exception as exc:
        with _BC_LOCK:
            _BC_STATE['running']     = False
            _BC_STATE['current_sql'] = f'[ERROR] {exc}'


# ── Crypto Exchange (CEX) Demo ─────────────────────────────────────────────────

_CE_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'crypto_exchange.db')
_CE_LOCK    = threading.Lock()
_CE_STATE   = {
    'running': False, 'phase': 'idle',
    'current_sql': '', 'trade_count': 0,
    'last_price': 50000.0, 'spread': 0.0,
}

_CE_TRADERS = [
    ('Alice', 60000.0, 2.0),
    ('Bob',   45000.0, 1.5),
    ('Carol', 90000.0, 3.0),
    ('Dave',  25000.0, 0.5),
    ('Eve',   75000.0, 2.5),
]


def _ce_conn():
    conn = sqlite3.connect(_CE_DB_PATH, check_same_thread=False)
    conn.isolation_level = None
    return conn


def _ce_init_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS order_book (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        side    TEXT,
        price   REAL,
        qty     REAL,
        trader  TEXT,
        status  TEXT DEFAULT 'open',
        ts      TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS ledger (
        trader  TEXT PRIMARY KEY,
        usdt    REAL,
        btc     REAL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS event_stream (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        topic   TEXT,
        detail  TEXT,
        ts      TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS trades (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        price   REAL,
        qty     REAL,
        buyer   TEXT,
        seller  TEXT,
        ts      TEXT DEFAULT (datetime('now','localtime'))
    )""")


def _ce_reset(conn):
    for tbl in ('order_book', 'ledger', 'event_stream', 'trades'):
        conn.execute(f"DROP TABLE IF EXISTS {tbl}")
    _ce_init_db(conn)
    for trader, usdt, btc in _CE_TRADERS:
        conn.execute("INSERT INTO ledger (trader,usdt,btc) VALUES (?,?,?)", (trader, usdt, btc))


def ce_get_state():
    with _CE_LOCK:
        state = dict(_CE_STATE)
    try:
        conn = _ce_conn()
        state['order_book_asks'] = [
            dict(id=r[0], price=r[1], qty=r[2], trader=r[3])
            for r in conn.execute(
                "SELECT id,price,qty,trader FROM order_book WHERE side='sell' AND status='open' ORDER BY price ASC LIMIT 8"
            ).fetchall()
        ]
        state['order_book_bids'] = [
            dict(id=r[0], price=r[1], qty=r[2], trader=r[3])
            for r in conn.execute(
                "SELECT id,price,qty,trader FROM order_book WHERE side='buy' AND status='open' ORDER BY price DESC LIMIT 8"
            ).fetchall()
        ]
        state['events'] = [
            dict(id=r[0], topic=r[1], detail=r[2], ts=r[3])
            for r in conn.execute(
                "SELECT id,topic,detail,ts FROM event_stream ORDER BY id DESC LIMIT 12"
            ).fetchall()
        ]
        state['ledger'] = [
            dict(trader=r[0], usdt=r[1], btc=r[2])
            for r in conn.execute(
                "SELECT trader,usdt,btc FROM ledger ORDER BY trader"
            ).fetchall()
        ]
        state['recent_trades'] = [
            dict(id=r[0], price=r[1], qty=r[2], buyer=r[3], seller=r[4], ts=r[5])
            for r in conn.execute(
                "SELECT id,price,qty,buyer,seller,ts FROM trades ORDER BY id DESC LIMIT 8"
            ).fetchall()
        ]
        conn.close()
    except Exception:
        state.setdefault('order_book_asks', [])
        state.setdefault('order_book_bids', [])
        state.setdefault('events', [])
        state.setdefault('ledger', [])
        state.setdefault('recent_trades', [])
    return state


def ce_start():
    with _CE_LOCK:
        if _CE_STATE['running']:
            return
        _CE_STATE['running']     = True
        _CE_STATE['phase']       = 'starting'
        _CE_STATE['trade_count'] = 0
        _CE_STATE['spread']      = 0.0
        _CE_STATE['current_sql'] = ''
    threading.Thread(target=_ce_worker, daemon=True).start()


def ce_stop():
    with _CE_LOCK:
        _CE_STATE['running'] = False


def _ce_interruptible_sleep(seconds):
    end = time.time() + seconds
    while time.time() < end:
        with _CE_LOCK:
            if not _CE_STATE['running']:
                return
        time.sleep(0.05)


def _ce_worker():
    try:
        conn = _ce_conn()
        _ce_reset(conn)

        with _CE_LOCK:
            _CE_STATE['phase']       = 'running'
            _CE_STATE['last_price']  = 50000.0
            _CE_STATE['trade_count'] = 0
            _CE_STATE['spread']      = 0.0

        order_count = 0

        while True:
            with _CE_LOCK:
                if not _CE_STATE['running']:
                    break
                mkt_price = _CE_STATE['last_price']

            # ── STEP 1: GENERATE ORDER ─────────────────────────────────────────
            # Shuffle candidates and try up to 5 to find one with sufficient funds
            candidates = [(t, s) for t in [r[0] for r in _CE_TRADERS] for s in ['buy', 'sell']]
            random.shuffle(candidates)

            placed = False
            for trader, side in candidates[:5]:
                price = round(mkt_price * random.uniform(0.997, 1.003), 2)
                qty   = round(random.uniform(0.05, 0.4), 3)

                # FIX 2 — Locked-fund validation
                if side == 'buy':
                    locked = conn.execute(
                        "SELECT COALESCE(SUM(price*qty),0) FROM order_book "
                        "WHERE trader=? AND side='buy' AND status='open'",
                        (trader,)
                    ).fetchone()[0]
                    row = conn.execute("SELECT usdt FROM ledger WHERE trader=?", (trader,)).fetchone()
                    if not row or row[0] - locked < price * qty:
                        continue
                else:
                    locked = conn.execute(
                        "SELECT COALESCE(SUM(qty),0) FROM order_book "
                        "WHERE trader=? AND side='sell' AND status='open'",
                        (trader,)
                    ).fetchone()[0]
                    row = conn.execute("SELECT btc FROM ledger WHERE trader=?", (trader,)).fetchone()
                    if not row or row[0] - locked < qty:
                        continue

                sql_str = (f"INSERT INTO order_book (side,price,qty,trader) "
                           f"VALUES ('{side}',{price},{qty},'{trader}')")
                with _CE_LOCK:
                    _CE_STATE['current_sql'] = sql_str
                conn.execute("INSERT INTO order_book (side,price,qty,trader) VALUES (?,?,?,?)",
                             (side, price, qty, trader))
                conn.execute("INSERT INTO event_stream (topic,detail) VALUES (?,?)",
                             ('ORDER_PLACED',
                              f"{trader} {side} {qty} BTC @ {price:.2f} USDT"))
                order_count += 1
                placed = True
                break

            if not placed:
                _ce_interruptible_sleep(0.5)
                continue

            _ce_interruptible_sleep(0.3)

            with _CE_LOCK:
                if not _CE_STATE['running']:
                    break

            # ── STEP 2: MATCH CHECK ────────────────────────────────────────────
            best_bid = conn.execute(
                "SELECT id,price,qty,trader FROM order_book "
                "WHERE side='buy' AND status='open' ORDER BY price DESC, id ASC LIMIT 1"
            ).fetchone()
            best_ask = conn.execute(
                "SELECT id,price,qty,trader FROM order_book "
                "WHERE side='sell' AND status='open' ORDER BY price ASC, id ASC LIMIT 1"
            ).fetchone()

            if best_bid and best_ask:
                bid_id, bid_price, bid_qty, bid_trader = best_bid
                ask_id, ask_price, ask_qty, ask_trader = best_ask
                spread = ask_price - bid_price
                with _CE_LOCK:
                    _CE_STATE['spread'] = round(spread, 2)

                if bid_price >= ask_price and bid_trader != ask_trader:
                    # FIX 3 — Maker price (older order sets the price)
                    trade_price = bid_price if bid_id < ask_id else ask_price

                    # FIX 1 — Partial fill
                    trade_qty   = round(min(bid_qty, ask_qty), 8)
                    new_bid_qty = round(bid_qty - trade_qty, 8)
                    new_ask_qty = round(ask_qty - trade_qty, 8)

                    trade_sql = (f"BEGIN; UPDATE order_book (partial fill); "
                                 f"INSERT INTO trades VALUES "
                                 f"({trade_price},{trade_qty},'{bid_trader}','{ask_trader}'); "
                                 f"UPDATE ledger buyer/seller; COMMIT")
                    with _CE_LOCK:
                        _CE_STATE['current_sql'] = trade_sql

                    conn.execute("BEGIN")
                    try:
                        if new_bid_qty <= 0.0001:
                            conn.execute("UPDATE order_book SET status='matched' WHERE id=?", (bid_id,))
                        else:
                            conn.execute("UPDATE order_book SET qty=? WHERE id=?", (new_bid_qty, bid_id))

                        if new_ask_qty <= 0.0001:
                            conn.execute("UPDATE order_book SET status='matched' WHERE id=?", (ask_id,))
                        else:
                            conn.execute("UPDATE order_book SET qty=? WHERE id=?", (new_ask_qty, ask_id))

                        conn.execute("INSERT INTO trades (price,qty,buyer,seller) VALUES (?,?,?,?)",
                                     (trade_price, trade_qty, bid_trader, ask_trader))
                        conn.execute("UPDATE ledger SET btc=btc+?,usdt=usdt-? WHERE trader=?",
                                     (trade_qty, trade_price * trade_qty, bid_trader))
                        conn.execute("UPDATE ledger SET btc=btc-?,usdt=usdt+? WHERE trader=?",
                                     (trade_qty, trade_price * trade_qty, ask_trader))
                        conn.execute("COMMIT")
                    except Exception:
                        conn.execute("ROLLBACK")
                        raise

                    conn.execute("INSERT INTO event_stream (topic,detail) VALUES (?,?)",
                                 ('TRADE_EXECUTED',
                                  f"{bid_trader}→{ask_trader}: {trade_qty:.4f} BTC @ {trade_price:.2f}"))
                    conn.execute("INSERT INTO event_stream (topic,detail) VALUES (?,?)",
                                 ('BALANCE_UPDATED',
                                  f"{bid_trader}: +{trade_qty:.4f} BTC, "
                                  f"-{trade_price * trade_qty:.2f} USDT"))
                    conn.execute("INSERT INTO event_stream (topic,detail) VALUES (?,?)",
                                 ('BALANCE_UPDATED',
                                  f"{ask_trader}: -{trade_qty:.4f} BTC, "
                                  f"+{trade_price * trade_qty:.2f} USDT"))

                    with _CE_LOCK:
                        _CE_STATE['last_price']  = trade_price
                        _CE_STATE['trade_count'] += 1

            # ── STEP 3: CLEANUP every 10 orders ───────────────────────────────
            if order_count % 10 == 0:
                expired = conn.execute(
                    "SELECT id,trader,side,price,qty FROM order_book WHERE status='open' "
                    "AND ts < datetime('now','localtime','-20 seconds')"
                ).fetchall()
                for c in expired:
                    conn.execute("UPDATE order_book SET status='cancelled' WHERE id=?", (c[0],))
                    conn.execute("INSERT INTO event_stream (topic,detail) VALUES (?,?)",
                                 ('ORDER_CANCELLED',
                                  f"{c[1]} {c[2]} {c[4]:.4f} BTC @ {c[3]:.2f} (expired)"))
                conn.execute(
                    "DELETE FROM event_stream WHERE id NOT IN "
                    "(SELECT id FROM event_stream ORDER BY id DESC LIMIT 50)"
                )
                conn.execute(
                    "DELETE FROM order_book WHERE status != 'open' AND id NOT IN "
                    "(SELECT id FROM order_book WHERE status != 'open' ORDER BY id DESC LIMIT 50)"
                )

            _ce_interruptible_sleep(random.uniform(0.4, 1.2))

        with _CE_LOCK:
            _CE_STATE['running'] = False
            _CE_STATE['phase']   = 'idle'

    except Exception as exc:
        with _CE_LOCK:
            _CE_STATE['running']     = False
            _CE_STATE['current_sql'] = f'[ERROR] {exc}'


# ── NASDAQ Simulation Demo ─────────────────────────────────────────────────────

_NQ_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'nasdaq.db')
_NQ_LOCK    = threading.Lock()
_NQ_STATE   = {
    'running': False, 'phase': 'idle', 'current_sql': '',
    'trade_count': 0, 'last_price': 150.0, 'spread': 0.0,
    'pending_settlements': 0, 'market_status': 'CLOSED', 'cycle': 0,
}

_NQ_BROKERS = [
    # (name, broker_type, shares, cash)
    ('Schwab',    'retail',  500,  80000.0),
    ('Robinhood', 'retail',  200,  30000.0),
    ('E*Trade',   'retail',  350,  55000.0),
    ('AlgoFast',  'hft',   1000, 200000.0),
    ('QuantBot',  'hft',    800, 160000.0),
]


def _nq_conn():
    conn = sqlite3.connect(_NQ_DB_PATH, check_same_thread=False)
    conn.isolation_level = None
    return conn


def _nq_init_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS orders (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        broker      TEXT,
        broker_type TEXT,
        side        TEXT,
        price       REAL,
        qty         INTEGER,
        status      TEXT DEFAULT 'open',
        latency_ms  REAL,
        ts          TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS trades (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        price         REAL,
        qty           INTEGER,
        buyer_broker  TEXT,
        seller_broker TEXT,
        settled       INTEGER DEFAULT 0,
        ts            TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS settlement_queue (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id  INTEGER,
        qty       INTEGER,
        price     REAL,
        buyer     TEXT,
        seller    TEXT,
        status    TEXT DEFAULT 'pending',
        ts        TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS custodian_holdings (
        broker  TEXT PRIMARY KEY,
        shares  INTEGER DEFAULT 0,
        cash    REAL DEFAULT 0.0
    )""")


def _nq_reset(conn):
    for tbl in ('orders', 'trades', 'settlement_queue', 'custodian_holdings'):
        conn.execute(f"DROP TABLE IF EXISTS {tbl}")
    _nq_init_db(conn)
    for name, btype, shares, cash in _NQ_BROKERS:
        conn.execute("INSERT INTO custodian_holdings (broker,shares,cash) VALUES (?,?,?)",
                     (name, shares, cash))


def nq_get_state():
    with _NQ_LOCK:
        state = dict(_NQ_STATE)
    try:
        conn = _nq_conn()
        state['orders'] = [
            dict(id=r[0], broker=r[1], broker_type=r[2], side=r[3],
                 price=r[4], qty=r[5], latency_ms=r[6], ts=r[7])
            for r in conn.execute(
                "SELECT id,broker,broker_type,side,price,qty,latency_ms,ts "
                "FROM orders ORDER BY id DESC LIMIT 12"
            ).fetchall()
        ]
        state['asks'] = [
            dict(id=r[0], price=r[1], qty=r[2], broker=r[3])
            for r in conn.execute(
                "SELECT id,price,qty,broker FROM orders WHERE side='sell' AND status='open' "
                "ORDER BY price ASC LIMIT 8"
            ).fetchall()
        ]
        state['bids'] = [
            dict(id=r[0], price=r[1], qty=r[2], broker=r[3])
            for r in conn.execute(
                "SELECT id,price,qty,broker FROM orders WHERE side='buy' AND status='open' "
                "ORDER BY price DESC LIMIT 8"
            ).fetchall()
        ]
        state['trades'] = [
            dict(id=r[0], price=r[1], qty=r[2], buyer=r[3], seller=r[4], ts=r[5])
            for r in conn.execute(
                "SELECT id,price,qty,buyer_broker,seller_broker,ts FROM trades ORDER BY id DESC LIMIT 8"
            ).fetchall()
        ]
        state['settlement_queue'] = [
            dict(id=r[0], trade_id=r[1], qty=r[2], price=r[3],
                 buyer=r[4], seller=r[5], status=r[6], ts=r[7])
            for r in conn.execute(
                "SELECT id,trade_id,qty,price,buyer,seller,status,ts "
                "FROM settlement_queue ORDER BY id DESC LIMIT 15"
            ).fetchall()
        ]
        state['custodian_holdings'] = [
            dict(broker=r[0], shares=r[1], cash=r[2])
            for r in conn.execute(
                "SELECT broker,shares,cash FROM custodian_holdings ORDER BY broker"
            ).fetchall()
        ]
        conn.close()
    except Exception:
        for key in ('orders', 'asks', 'bids', 'trades', 'settlement_queue', 'custodian_holdings'):
            state.setdefault(key, [])
    return state


def nq_start():
    with _NQ_LOCK:
        if _NQ_STATE['running']:
            return
        _NQ_STATE['running']             = True
        _NQ_STATE['phase']               = 'starting'
        _NQ_STATE['trade_count']         = 0
        _NQ_STATE['pending_settlements'] = 0
        _NQ_STATE['cycle']               = 0
        _NQ_STATE['current_sql']         = ''
    threading.Thread(target=_nq_worker, daemon=True).start()


def nq_stop():
    with _NQ_LOCK:
        _NQ_STATE['running'] = False


def _nq_interruptible_sleep(seconds):
    end = time.time() + seconds
    while time.time() < end:
        with _NQ_LOCK:
            if not _NQ_STATE['running']:
                return
        time.sleep(0.05)


def _nq_batch_auction(conn):
    """Find the clearing price that maximises matched volume and execute all eligible orders."""
    buys  = conn.execute(
        "SELECT id,price,qty,broker FROM orders WHERE side='buy'  AND status='open' ORDER BY price DESC, id ASC"
    ).fetchall()
    sells = conn.execute(
        "SELECT id,price,qty,broker FROM orders WHERE side='sell' AND status='open' ORDER BY price ASC,  id ASC"
    ).fetchall()

    if not buys or not sells:
        return None

    # Walk all candidate prices to find the one that maximises min(buy_vol, sell_vol)
    candidate_prices = sorted(set([b[1] for b in buys] + [s[1] for s in sells]))
    clearing_price, max_vol = None, 0
    for p in candidate_prices:
        buy_vol  = sum(b[2] for b in buys  if b[1] >= p)
        sell_vol = sum(s[2] for s in sells if s[1] <= p)
        vol = min(buy_vol, sell_vol)
        if vol > max_vol:
            max_vol, clearing_price = vol, p

    if clearing_price is None or max_vol == 0:
        return None

    eligible_buys  = [[b[0], b[1], b[2], b[3]] for b in buys  if b[1] >= clearing_price]
    eligible_sells = [[s[0], s[1], s[2], s[3]] for s in sells if s[1] <= clearing_price]

    bi = si = 0
    total_matched = 0
    while bi < len(eligible_buys) and si < len(eligible_sells):
        b = eligible_buys[bi]
        s = eligible_sells[si]
        if b[3] == s[3]:
            bi += 1
            continue

        trade_qty = min(b[2], s[2])
        b[2] -= trade_qty
        s[2] -= trade_qty

        conn.execute("BEGIN")
        try:
            if b[2] <= 0:
                conn.execute("UPDATE orders SET status='matched' WHERE id=?", (b[0],))
            else:
                conn.execute("UPDATE orders SET qty=? WHERE id=?", (b[2], b[0]))
            if s[2] <= 0:
                conn.execute("UPDATE orders SET status='matched' WHERE id=?", (s[0],))
            else:
                conn.execute("UPDATE orders SET qty=? WHERE id=?", (s[2], s[0]))
            trade_id = conn.execute(
                "INSERT INTO trades (price,qty,buyer_broker,seller_broker) VALUES (?,?,?,?)",
                (clearing_price, trade_qty, b[3], s[3])
            ).lastrowid
            conn.execute(
                "INSERT INTO settlement_queue (trade_id,qty,price,buyer,seller) VALUES (?,?,?,?,?)",
                (trade_id, trade_qty, clearing_price, b[3], s[3])
            )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

        total_matched += trade_qty
        with _NQ_LOCK:
            _NQ_STATE['trade_count']         += 1
            _NQ_STATE['pending_settlements'] += 1
            _NQ_STATE['last_price']           = clearing_price

        if b[2] <= 0: bi += 1
        if s[2] <= 0: si += 1

    return clearing_price, total_matched


def _nq_worker():
    try:
        conn = _nq_conn()
        _nq_reset(conn)

        with _NQ_LOCK:
            _NQ_STATE['last_price']          = 150.0
            _NQ_STATE['trade_count']         = 0
            _NQ_STATE['pending_settlements'] = 0
            _NQ_STATE['cycle']               = 0

        retail_brokers = [b[0] for b in _NQ_BROKERS if b[1] == 'retail']
        all_broker_names = [(b[0], b[1]) for b in _NQ_BROKERS]

        while True:
            with _NQ_LOCK:
                if not _NQ_STATE['running']:
                    break

            # ── PHASE: closed ─────────────────────────────────────────────────
            with _NQ_LOCK:
                _NQ_STATE['phase']         = 'closed'
                _NQ_STATE['market_status'] = 'CLOSED'
                _NQ_STATE['current_sql']   = '-- Market CLOSED. Retail orders queuing. No matching active.'

            closed_end = time.time() + 8.0
            while time.time() < closed_end:
                with _NQ_LOCK:
                    if not _NQ_STATE['running']:
                        break
                    mkt_price = _NQ_STATE['last_price']

                for _ in range(random.randint(1, 2)):
                    broker_name = random.choice(retail_brokers)
                    side        = random.choice(['buy', 'sell'])
                    price       = round(mkt_price * random.uniform(0.985, 1.015), 2)
                    qty         = random.randint(1, 20)
                    latency_ms  = round(random.uniform(30, 80), 1)
                    sql_str = (f"INSERT INTO orders (broker,broker_type,side,price,qty) "
                               f"VALUES ('{broker_name}','retail','{side}',{price},{qty})")
                    with _NQ_LOCK:
                        _NQ_STATE['current_sql'] = sql_str
                    conn.execute(
                        "INSERT INTO orders (broker,broker_type,side,price,qty,latency_ms) VALUES (?,?,?,?,?,?)",
                        (broker_name, 'retail', side, price, qty, latency_ms)
                    )

                _nq_interruptible_sleep(1.5)

            with _NQ_LOCK:
                if not _NQ_STATE['running']:
                    break

            # ── PHASE: opening_auction ────────────────────────────────────────
            with _NQ_LOCK:
                _NQ_STATE['phase']         = 'opening_auction'
                _NQ_STATE['market_status'] = 'AUCTION'
                _NQ_STATE['current_sql']   = '-- Opening Bell! Batch auction — finding clearing price...'

            result = _nq_batch_auction(conn)
            if result:
                clr_price, clr_qty = result
                with _NQ_LOCK:
                    _NQ_STATE['current_sql'] = (
                        f"-- AUCTION CLEARED @ ${clr_price:.2f}: {clr_qty} shares matched. "
                        f"All eligible orders execute at single price. "
                        f"INSERT INTO settlement_queue (T+1 pending)"
                    )
            else:
                with _NQ_LOCK:
                    _NQ_STATE['current_sql'] = '-- Auction: no crossing orders. Opening at reference price.'

            _nq_interruptible_sleep(6.0)

            with _NQ_LOCK:
                if not _NQ_STATE['running']:
                    break

            # ── PHASE: trading ────────────────────────────────────────────────
            with _NQ_LOCK:
                _NQ_STATE['phase']         = 'trading'
                _NQ_STATE['market_status'] = 'OPEN'

            trading_end = time.time() + 35.0
            while time.time() < trading_end:
                with _NQ_LOCK:
                    if not _NQ_STATE['running']:
                        break
                    mkt_price = _NQ_STATE['last_price']

                broker_name, broker_type = random.choice(all_broker_names)
                side = random.choice(['buy', 'sell'])

                if broker_type == 'hft':
                    latency_ms = round(random.uniform(0.1, 0.5), 2)
                    qty        = random.randint(10, 100)
                    price      = round(mkt_price * random.uniform(0.997, 1.003), 2)
                else:
                    latency_ms = round(random.uniform(30, 80), 1)
                    qty        = random.randint(1, 20)
                    price      = round(mkt_price * random.uniform(0.985, 1.015), 2)

                sql_str = (f"-- [{broker_name}] [{latency_ms}ms] "
                           f"{side.upper()} {qty}sh NCC @ ${price:.2f}")
                with _NQ_LOCK:
                    _NQ_STATE['current_sql'] = sql_str
                conn.execute(
                    "INSERT INTO orders (broker,broker_type,side,price,qty,latency_ms) VALUES (?,?,?,?,?,?)",
                    (broker_name, broker_type, side, price, qty, latency_ms)
                )

                # Match check (maker-price + partial-fill, same as CEX)
                best_bid = conn.execute(
                    "SELECT id,price,qty,broker FROM orders WHERE side='buy' AND status='open' "
                    "ORDER BY price DESC, id ASC LIMIT 1"
                ).fetchone()
                best_ask = conn.execute(
                    "SELECT id,price,qty,broker FROM orders WHERE side='sell' AND status='open' "
                    "ORDER BY price ASC, id ASC LIMIT 1"
                ).fetchone()

                if best_bid and best_ask:
                    bid_id, bid_price, bid_qty, bid_broker = best_bid
                    ask_id, ask_price, ask_qty, ask_broker = best_ask
                    spread = ask_price - bid_price
                    with _NQ_LOCK:
                        _NQ_STATE['spread'] = round(spread, 2)

                    if bid_price >= ask_price and bid_broker != ask_broker:
                        trade_price = bid_price if bid_id < ask_id else ask_price
                        trade_qty   = min(bid_qty, ask_qty)
                        new_bid_qty = bid_qty - trade_qty
                        new_ask_qty = ask_qty - trade_qty

                        trade_sql = (f"BEGIN; partial fill {trade_qty}sh NCC @ ${trade_price:.2f}; "
                                     f"INSERT INTO settlement_queue (status='pending') -- T+1; COMMIT")
                        with _NQ_LOCK:
                            _NQ_STATE['current_sql'] = trade_sql

                        conn.execute("BEGIN")
                        try:
                            if new_bid_qty <= 0:
                                conn.execute("UPDATE orders SET status='matched' WHERE id=?", (bid_id,))
                            else:
                                conn.execute("UPDATE orders SET qty=? WHERE id=?", (new_bid_qty, bid_id))
                            if new_ask_qty <= 0:
                                conn.execute("UPDATE orders SET status='matched' WHERE id=?", (ask_id,))
                            else:
                                conn.execute("UPDATE orders SET qty=? WHERE id=?", (new_ask_qty, ask_id))
                            trade_id = conn.execute(
                                "INSERT INTO trades (price,qty,buyer_broker,seller_broker) VALUES (?,?,?,?)",
                                (trade_price, trade_qty, bid_broker, ask_broker)
                            ).lastrowid
                            conn.execute(
                                "INSERT INTO settlement_queue (trade_id,qty,price,buyer,seller) VALUES (?,?,?,?,?)",
                                (trade_id, trade_qty, trade_price, bid_broker, ask_broker)
                            )
                            conn.execute("COMMIT")
                        except Exception:
                            conn.execute("ROLLBACK")
                            raise

                        with _NQ_LOCK:
                            _NQ_STATE['last_price']          = trade_price
                            _NQ_STATE['trade_count']         += 1
                            _NQ_STATE['pending_settlements'] += 1

                _nq_interruptible_sleep(random.uniform(0.6, 1.2))

            with _NQ_LOCK:
                if not _NQ_STATE['running']:
                    break

            # ── PHASE: closing_auction ────────────────────────────────────────
            with _NQ_LOCK:
                _NQ_STATE['phase']         = 'closing_auction'
                _NQ_STATE['market_status'] = 'AUCTION'
                _NQ_STATE['current_sql']   = '-- Closing Bell! Batch auction running...'

            result = _nq_batch_auction(conn)
            if result:
                clr_price, clr_qty = result
                with _NQ_LOCK:
                    _NQ_STATE['current_sql'] = (
                        f"-- CLOSING AUCTION @ ${clr_price:.2f}: {clr_qty} shares cleared."
                    )

            _nq_interruptible_sleep(6.0)

            with _NQ_LOCK:
                if not _NQ_STATE['running']:
                    break

            # ── PHASE: settlement ─────────────────────────────────────────────
            with _NQ_LOCK:
                _NQ_STATE['phase']         = 'settlement'
                _NQ_STATE['market_status'] = 'AFTER-HOURS'
                _NQ_STATE['current_sql']   = '-- DTCC EOD Batch Settlement running...'

            pending = conn.execute(
                "SELECT id,trade_id,qty,price,buyer,seller FROM settlement_queue "
                "WHERE status='pending' ORDER BY id ASC"
            ).fetchall()

            for row in pending:
                sq_id, trade_id, qty, price, buyer, seller = row
                with _NQ_LOCK:
                    if not _NQ_STATE['running']:
                        break

                settle_sql = (f"BEGIN; UPDATE settlement_queue SET status='settled' WHERE id={sq_id}; "
                              f"UPDATE custodian_holdings SET shares=shares+{qty} WHERE broker='{buyer}'; "
                              f"UPDATE custodian_holdings SET shares=shares-{qty} WHERE broker='{seller}'; COMMIT")
                with _NQ_LOCK:
                    _NQ_STATE['current_sql'] = settle_sql

                conn.execute("BEGIN")
                try:
                    conn.execute("UPDATE settlement_queue SET status='settled' WHERE id=?", (sq_id,))
                    conn.execute(
                        "UPDATE custodian_holdings SET shares=shares+?,cash=cash-? WHERE broker=?",
                        (qty, price * qty, buyer)
                    )
                    conn.execute(
                        "UPDATE custodian_holdings SET shares=shares-?,cash=cash+? WHERE broker=?",
                        (qty, price * qty, seller)
                    )
                    conn.execute("COMMIT")
                except Exception:
                    conn.execute("ROLLBACK")
                    raise

                with _NQ_LOCK:
                    _NQ_STATE['pending_settlements'] = max(0, _NQ_STATE['pending_settlements'] - 1)

                _nq_interruptible_sleep(0.6)

            # Trim tables
            conn.execute("DELETE FROM orders WHERE id NOT IN (SELECT id FROM orders ORDER BY id DESC LIMIT 50)")
            conn.execute("DELETE FROM trades WHERE id NOT IN (SELECT id FROM trades ORDER BY id DESC LIMIT 50)")
            conn.execute(
                "DELETE FROM settlement_queue WHERE id NOT IN "
                "(SELECT id FROM settlement_queue ORDER BY id DESC LIMIT 30)"
            )

            with _NQ_LOCK:
                _NQ_STATE['cycle'] += 1
                if not _NQ_STATE['running']:
                    break

        with _NQ_LOCK:
            _NQ_STATE['running'] = False
            _NQ_STATE['phase']   = 'idle'

    except Exception as exc:
        with _NQ_LOCK:
            _NQ_STATE['running']     = False
            _NQ_STATE['current_sql'] = f'[ERROR] {exc}'


# ── NYSE Simulation Demo (Auction Market + DMM) ────────────────────────────────

_NY_DB_PATH        = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'nyse.db')
_NY_LOCK           = threading.Lock()
_NY_STATE          = {
    'running': False, 'phase': 'idle', 'current_sql': '',
    'trade_count': 0, 'last_price': 100.0, 'spread': 0.0,
    'dmm_cash': 500000.0, 'dmm_shares': 5000,
    'dmm_interventions': 0, 'flash_crash_pending': False,
}

_NY_TRADERS        = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank']
_NY_DMM_MAX_SPREAD = 2.00   # DMM intervenes when spread exceeds this
_NY_DMM_QUOTE_HALF = 0.05   # DMM quotes ± this around the fair price
_NY_TICKER         = 'WMT'


def _ny_conn():
    conn = sqlite3.connect(_NY_DB_PATH, check_same_thread=False)
    conn.isolation_level = None
    return conn


def _ny_init_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS order_book (
        order_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        trader_id TEXT,
        ticker    TEXT DEFAULT 'WMT',
        side      TEXT,
        price     REAL,
        qty       INTEGER,
        status    TEXT DEFAULT 'OPEN',
        is_dmm    INTEGER DEFAULT 0,
        ts        TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS trades (
        trade_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker          TEXT DEFAULT 'WMT',
        price           REAL,
        qty             INTEGER,
        buyer_order_id  INTEGER,
        seller_order_id INTEGER,
        is_dmm_involved INTEGER DEFAULT 0,
        ts              TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS dmm_inventory (
        ticker        TEXT PRIMARY KEY,
        cash_balance  REAL,
        stock_balance INTEGER
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS event_log (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        detail     TEXT,
        ts         TEXT DEFAULT (datetime('now','localtime'))
    )""")


def _ny_reset(conn):
    for tbl in ('order_book', 'trades', 'dmm_inventory', 'event_log'):
        conn.execute(f"DROP TABLE IF EXISTS {tbl}")
    _ny_init_db(conn)
    conn.execute("INSERT INTO dmm_inventory (ticker,cash_balance,stock_balance) VALUES (?,?,?)",
                 (_NY_TICKER, 500000.0, 5000))
    # Seed initial order book: 5 bids + 5 asks around $100
    for i, price in enumerate([99.50, 99.60, 99.70, 99.80, 99.90]):
        trader = _NY_TRADERS[i % len(_NY_TRADERS)]
        conn.execute("INSERT INTO order_book (trader_id,side,price,qty) VALUES (?,?,?,?)",
                     (trader, 'BUY', price, random.randint(50, 200)))
    for i, price in enumerate([100.10, 100.20, 100.30, 100.40, 100.50]):
        trader = _NY_TRADERS[(i + 3) % len(_NY_TRADERS)]
        conn.execute("INSERT INTO order_book (trader_id,side,price,qty) VALUES (?,?,?,?)",
                     (trader, 'SELL', price, random.randint(50, 200)))


def ny_get_state():
    with _NY_LOCK:
        state = dict(_NY_STATE)
    try:
        conn = _ny_conn()
        state['bids'] = [
            dict(order_id=r[0], trader_id=r[1], price=r[2], qty=r[3], is_dmm=r[4])
            for r in conn.execute(
                "SELECT order_id,trader_id,price,qty,is_dmm FROM order_book "
                "WHERE side='BUY' AND status IN ('OPEN','PARTIAL') ORDER BY price DESC LIMIT 10"
            ).fetchall()
        ]
        state['asks'] = [
            dict(order_id=r[0], trader_id=r[1], price=r[2], qty=r[3], is_dmm=r[4])
            for r in conn.execute(
                "SELECT order_id,trader_id,price,qty,is_dmm FROM order_book "
                "WHERE side='SELL' AND status IN ('OPEN','PARTIAL') ORDER BY price ASC LIMIT 10"
            ).fetchall()
        ]
        state['trades'] = [
            dict(trade_id=r[0], price=r[1], qty=r[2],
                 buyer_order_id=r[3], seller_order_id=r[4], is_dmm_involved=r[5], ts=r[6])
            for r in conn.execute(
                "SELECT trade_id,price,qty,buyer_order_id,seller_order_id,is_dmm_involved,ts "
                "FROM trades ORDER BY trade_id DESC LIMIT 10"
            ).fetchall()
        ]
        state['events'] = [
            dict(id=r[0], event_type=r[1], detail=r[2], ts=r[3])
            for r in conn.execute(
                "SELECT id,event_type,detail,ts FROM event_log ORDER BY id DESC LIMIT 12"
            ).fetchall()
        ]
        inv = conn.execute(
            "SELECT cash_balance,stock_balance FROM dmm_inventory WHERE ticker=?", (_NY_TICKER,)
        ).fetchone()
        if inv:
            state['dmm_cash']   = inv[0]
            state['dmm_shares'] = inv[1]
        conn.close()
    except Exception:
        for key in ('bids', 'asks', 'trades', 'events'):
            state.setdefault(key, [])
    return state


def ny_start():
    with _NY_LOCK:
        if _NY_STATE['running']:
            return
        _NY_STATE['running']           = True
        _NY_STATE['phase']             = 'open'
        _NY_STATE['trade_count']       = 0
        _NY_STATE['dmm_cash']          = 500000.0
        _NY_STATE['dmm_shares']        = 5000
        _NY_STATE['dmm_interventions'] = 0
        _NY_STATE['flash_crash_pending'] = False
        _NY_STATE['current_sql']       = ''
    threading.Thread(target=_ny_worker, daemon=True).start()


def ny_stop():
    with _NY_LOCK:
        _NY_STATE['running'] = False


def ny_flash_crash():
    with _NY_LOCK:
        _NY_STATE['flash_crash_pending'] = True


def _ny_interruptible_sleep(seconds):
    end = time.time() + seconds
    while time.time() < end:
        with _NY_LOCK:
            if not _NY_STATE['running']:
                return
        time.sleep(0.05)


def _ny_match(conn):
    """Try to match best bid vs best ask. Returns True if a trade executed."""
    best_bid = conn.execute(
        "SELECT order_id,price,qty,trader_id,is_dmm FROM order_book "
        "WHERE side='BUY' AND status IN ('OPEN','PARTIAL') ORDER BY price DESC, order_id ASC LIMIT 1"
    ).fetchone()
    best_ask = conn.execute(
        "SELECT order_id,price,qty,trader_id,is_dmm FROM order_book "
        "WHERE side='SELL' AND status IN ('OPEN','PARTIAL') ORDER BY price ASC, order_id ASC LIMIT 1"
    ).fetchone()

    if not best_bid or not best_ask:
        return False
    bid_id, bid_price, bid_qty, bid_trader, bid_dmm = best_bid
    ask_id, ask_price, ask_qty, ask_trader, ask_dmm = best_ask

    if bid_price < ask_price or bid_trader == ask_trader:
        return False

    # Maker price: older order wins
    trade_price = bid_price if bid_id < ask_id else ask_price
    trade_qty   = min(bid_qty, ask_qty)
    new_bid_qty = bid_qty - trade_qty
    new_ask_qty = ask_qty - trade_qty
    is_dmm_trade = 1 if (bid_dmm or ask_dmm) else 0

    sql_str = (f"BEGIN; partial fill {trade_qty}sh {_NY_TICKER} @ ${trade_price:.2f}"
               + (" [DMM involved]" if is_dmm_trade else "") + "; COMMIT")
    with _NY_LOCK:
        _NY_STATE['current_sql'] = sql_str

    conn.execute("BEGIN")
    try:
        if new_bid_qty <= 0:
            conn.execute("UPDATE order_book SET status='FILLED' WHERE order_id=?", (bid_id,))
        else:
            conn.execute("UPDATE order_book SET qty=?,status='PARTIAL' WHERE order_id=?",
                         (new_bid_qty, bid_id))
        if new_ask_qty <= 0:
            conn.execute("UPDATE order_book SET status='FILLED' WHERE order_id=?", (ask_id,))
        else:
            conn.execute("UPDATE order_book SET qty=?,status='PARTIAL' WHERE order_id=?",
                         (new_ask_qty, ask_id))
        conn.execute(
            "INSERT INTO trades (price,qty,buyer_order_id,seller_order_id,is_dmm_involved) "
            "VALUES (?,?,?,?,?)",
            (trade_price, trade_qty, bid_id, ask_id, is_dmm_trade)
        )
        # Update DMM inventory if DMM was involved
        if bid_dmm:  # DMM bought: receives shares, spent cash
            conn.execute("UPDATE dmm_inventory SET stock_balance=stock_balance+?,cash_balance=cash_balance-? WHERE ticker=?",
                         (trade_qty, trade_price * trade_qty, _NY_TICKER))
        if ask_dmm:  # DMM sold: loses shares, gains cash
            conn.execute("UPDATE dmm_inventory SET stock_balance=stock_balance-?,cash_balance=cash_balance+? WHERE ticker=?",
                         (trade_qty, trade_price * trade_qty, _NY_TICKER))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise

    detail = f"{trade_qty}sh {_NY_TICKER} @ ${trade_price:.2f}"
    if is_dmm_trade:
        detail += " [DMM]"
    conn.execute("INSERT INTO event_log (event_type,detail) VALUES (?,?)", ('TRADE', detail))

    with _NY_LOCK:
        _NY_STATE['last_price']  = trade_price
        _NY_STATE['trade_count'] += 1
        # Sync DMM inventory to state
    inv = conn.execute(
        "SELECT cash_balance,stock_balance FROM dmm_inventory WHERE ticker=?", (_NY_TICKER,)
    ).fetchone()
    if inv:
        with _NY_LOCK:
            _NY_STATE['dmm_cash']   = inv[0]
            _NY_STATE['dmm_shares'] = inv[1]
    return True


def _ny_dmm_check(conn):
    """Monitor spread; inject liquidity if it exceeds threshold or bid side is empty."""
    # Check if DMM already has enough active quotes
    existing = conn.execute(
        "SELECT COUNT(*) FROM order_book WHERE trader_id='DMM' AND status IN ('OPEN','PARTIAL')"
    ).fetchone()[0]
    if existing >= 4:
        return  # DMM already providing liquidity

    best_bid = conn.execute(
        "SELECT MAX(price) FROM order_book WHERE side='BUY' AND status IN ('OPEN','PARTIAL')"
    ).fetchone()[0]
    best_ask = conn.execute(
        "SELECT MIN(price) FROM order_book WHERE side='SELL' AND status IN ('OPEN','PARTIAL')"
    ).fetchone()[0]

    with _NY_LOCK:
        last_price = _NY_STATE['last_price']
        dmm_cash   = _NY_STATE['dmm_cash']
        dmm_shares = _NY_STATE['dmm_shares']

    # Calculate spread
    if best_bid is not None and best_ask is not None:
        spread = best_ask - best_bid
        with _NY_LOCK:
            _NY_STATE['spread'] = round(spread, 2)
        if spread <= _NY_DMM_MAX_SPREAD:
            return  # Spread is fine, no intervention needed
        fair_price = (best_bid + best_ask) / 2.0
    elif best_bid is None and best_ask is None:
        fair_price = last_price
        with _NY_LOCK:
            _NY_STATE['spread'] = 0.0
    elif best_bid is None:
        fair_price = best_ask - 0.50
        with _NY_LOCK:
            _NY_STATE['spread'] = 999.0
    else:  # best_ask is None
        fair_price = best_bid + 0.50
        with _NY_LOCK:
            _NY_STATE['spread'] = 999.0

    # DMM injects orders on both sides
    buy_price  = round(fair_price - _NY_DMM_QUOTE_HALF, 2)
    sell_price = round(fair_price + _NY_DMM_QUOTE_HALF, 2)
    qty        = 500

    intervened = False
    if dmm_cash >= buy_price * qty:
        conn.execute(
            "INSERT INTO order_book (trader_id,side,price,qty,is_dmm) VALUES (?,?,?,?,1)",
            ('DMM', 'BUY', buy_price, qty)
        )
        intervened = True

    if dmm_shares >= qty:
        conn.execute(
            "INSERT INTO order_book (trader_id,side,price,qty,is_dmm) VALUES (?,?,?,?,1)",
            ('DMM', 'SELL', sell_price, qty)
        )
        intervened = True

    if intervened:
        detail = (f"Spread ${round(best_ask - best_bid if best_bid and best_ask else 999, 2):.2f} > "
                  f"${_NY_DMM_MAX_SPREAD:.2f} — DMM quoting "
                  f"${buy_price:.2f}×{sell_price:.2f} qty={qty}")
        sql_str = (f"INSERT INTO order_book (trader_id='DMM', side='BUY/SELL', "
                   f"price={buy_price}/{sell_price}, qty={qty}, is_dmm=1)")
        with _NY_LOCK:
            _NY_STATE['current_sql']      = sql_str
            _NY_STATE['dmm_interventions'] += 1
        conn.execute("INSERT INTO event_log (event_type,detail) VALUES (?,?)",
                     ('DMM_INTERVENE', detail))


def _ny_worker():
    try:
        conn = _ny_conn()
        _ny_reset(conn)

        with _NY_LOCK:
            _NY_STATE['last_price']        = 100.0
            _NY_STATE['trade_count']       = 0
            _NY_STATE['dmm_cash']          = 500000.0
            _NY_STATE['dmm_shares']        = 5000
            _NY_STATE['dmm_interventions'] = 0

        order_count = 0

        while True:
            with _NY_LOCK:
                if not _NY_STATE['running']:
                    break
                mkt_price          = _NY_STATE['last_price']
                crash_pending      = _NY_STATE['flash_crash_pending']

            # ── Flash Crash ───────────────────────────────────────────────────
            if crash_pending:
                # Cancel the top 5 bids (remove human liquidity)
                top_bids = conn.execute(
                    "SELECT order_id FROM order_book WHERE side='BUY' AND status IN ('OPEN','PARTIAL') "
                    "ORDER BY price DESC LIMIT 5"
                ).fetchall()
                for (oid,) in top_bids:
                    conn.execute("UPDATE order_book SET status='CANCELED' WHERE order_id=?", (oid,))

                # Cancel existing DMM buy orders too (simulate panic)
                conn.execute(
                    "UPDATE order_book SET status='CANCELED' WHERE trader_id='DMM' AND side='BUY' "
                    "AND status IN ('OPEN','PARTIAL')"
                )

                # Inject massive panic sells at deeply discounted prices
                for crash_price, crash_qty in [(85.0, 2000), (80.0, 2000), (75.0, 2000)]:
                    conn.execute(
                        "INSERT INTO order_book (trader_id,side,price,qty) VALUES (?,?,?,?)",
                        ('PANIC', 'SELL', crash_price, crash_qty)
                    )
                conn.execute("INSERT INTO event_log (event_type,detail) VALUES (?,?)",
                             ('FLASH_CRASH',
                              f'Liquidity crisis! Top bids cancelled. '
                              f'Panic sells injected at $85/$80/$75 (6000 shares total). '
                              f'DMM must intervene!'))
                with _NY_LOCK:
                    _NY_STATE['flash_crash_pending'] = False
                    _NY_STATE['current_sql'] = (
                        "-- FLASH CRASH: UPDATE order_book SET status='CANCELED' (top bids); "
                        "INSERT panic SELL orders @ $85/$80/$75"
                    )

            # ── Generate human order ──────────────────────────────────────────
            trader = random.choice(_NY_TRADERS)
            side   = random.choice(['BUY', 'SELL'])
            price  = round(mkt_price * random.uniform(0.995, 1.005), 2)
            qty    = random.randint(10, 200)

            sql_str = (f"INSERT INTO order_book (trader_id,side,price,qty) "
                       f"VALUES ('{trader}','{side}',{price},{qty})")
            with _NY_LOCK:
                _NY_STATE['current_sql'] = sql_str
            conn.execute("INSERT INTO order_book (trader_id,side,price,qty) VALUES (?,?,?,?)",
                         (trader, side, price, qty))
            conn.execute("INSERT INTO event_log (event_type,detail) VALUES (?,?)",
                         ('ORDER_PLACED', f"{trader} {side} {qty}sh @ ${price:.2f}"))
            order_count += 1

            # ── Match ─────────────────────────────────────────────────────────
            # Run up to 3 match cycles per order insertion
            for _ in range(3):
                if not _ny_match(conn):
                    break

            # ── DMM check ─────────────────────────────────────────────────────
            _ny_dmm_check(conn)

            # ── Trim ──────────────────────────────────────────────────────────
            if order_count % 15 == 0:
                conn.execute(
                    "DELETE FROM order_book WHERE status NOT IN ('OPEN','PARTIAL') AND order_id NOT IN "
                    "(SELECT order_id FROM order_book WHERE status NOT IN ('OPEN','PARTIAL') "
                    "ORDER BY order_id DESC LIMIT 50)"
                )
                conn.execute(
                    "DELETE FROM event_log WHERE id NOT IN "
                    "(SELECT id FROM event_log ORDER BY id DESC LIMIT 50)"
                )

            _ny_interruptible_sleep(random.uniform(0.5, 1.5))

        with _NY_LOCK:
            _NY_STATE['running'] = False
            _NY_STATE['phase']   = 'idle'

    except Exception as exc:
        with _NY_LOCK:
            _NY_STATE['running']     = False
            _NY_STATE['current_sql'] = f'[ERROR] {exc}'


# ── HFT Latency Arbitrage Race Demo ───────────────────────────────────────────

_HFT_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'demos', 'hft.db')
_HFT_LOCK    = threading.Lock()

# Only ephemeral UI hints live here — business data stays in SQLite (Fix 1)
_HFT_STATE = {
    'phase': 'idle',
    'current_sql': '',
    'last_hft_latency_ms': None,
    'last_ret_latency_ms': None,
    'last_race_result': None,
}

_HFT_BASE_LATENCIES = {
    ('microwave', 'cloud'):     (4.1,  67.0),
    ('fiber',     'cloud'):     (6.1,  67.0),
    ('microwave', 'colocated'): (4.1,   8.5),
    ('fiber',     'colocated'): (6.1,   8.5),
}


def _hft_conn():
    conn = sqlite3.connect(_HFT_DB_PATH, check_same_thread=False)
    conn.isolation_level = None
    return conn


def _hft_init_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS races (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        hft_network    TEXT,
        retail_setup   TEXT,
        hft_latency_ms REAL,
        ret_latency_ms REAL,
        winner         TEXT,
        profit         REAL,
        ts             TEXT DEFAULT (datetime('now','localtime'))
    )""")


def _hft_computed_state(conn, extra=None):
    """Build the full state dict entirely from SQLite — no cached global P&L (Fix 1)."""
    hft_pnl    = conn.execute("SELECT COALESCE(SUM(profit),0) FROM races WHERE winner='hft'").fetchone()[0]
    retail_pnl = conn.execute("SELECT COALESCE(SUM(profit),0) FROM races WHERE winner='retail'").fetchone()[0]
    hft_wins   = conn.execute("SELECT COUNT(*) FROM races WHERE winner='hft'").fetchone()[0]
    retail_wins= conn.execute("SELECT COUNT(*) FROM races WHERE winner='retail'").fetchone()[0]
    race_count = conn.execute("SELECT COUNT(*) FROM races").fetchone()[0]

    races = [
        dict(id=r[0], hft_network=r[1], retail_setup=r[2],
             hft_ms=round(r[3], 2), ret_ms=round(r[4], 2),
             winner=r[5], profit=r[6], ts=r[7])
        for r in conn.execute(
            "SELECT id,hft_network,retail_setup,hft_latency_ms,ret_latency_ms,winner,profit,ts "
            "FROM races ORDER BY id DESC LIMIT 10"
        ).fetchall()
    ]

    with _HFT_LOCK:
        s = dict(_HFT_STATE)
    s.update({
        'hft_pnl':    round(hft_pnl, 2),
        'retail_pnl': round(retail_pnl, 2),
        'hft_wins':   hft_wins,
        'retail_wins': retail_wins,
        'race_count': race_count,
        'ny_price':   99.95 if race_count > 0 else 100.00,
        'chi_price':  99.95 if race_count > 0 else 100.00,
        'races':      races,
    })
    if extra:
        s.update(extra)
    return s


def hft_get_state():
    try:
        conn = _hft_conn()
        _hft_init_db(conn)
        state = _hft_computed_state(conn)
        conn.close()
    except Exception as exc:
        with _HFT_LOCK:
            state = dict(_HFT_STATE)
        state.update({'error': str(exc), 'races': [],
                      'hft_pnl': 0, 'retail_pnl': 0, 'hft_wins': 0,
                      'retail_wins': 0, 'race_count': 0,
                      'ny_price': 100.0, 'chi_price': 100.0})
    return state


def hft_trigger(network, setup):
    # Fix 3: Validate inputs before touching the DB
    if (network, setup) not in _HFT_BASE_LATENCIES:
        return {'error': f'invalid config: network={network!r} setup={setup!r}'}

    base_hft, base_ret = _HFT_BASE_LATENCIES[(network, setup)]
    hft_ms = round(base_hft * random.uniform(0.85, 1.15), 2)
    ret_ms = round(base_ret * random.uniform(0.85, 1.15), 2)
    winner = 'hft' if hft_ms < ret_ms else 'retail'
    loser  = 'retail' if winner == 'hft' else 'hft'
    margin = round(abs(ret_ms - hft_ms), 2)

    net_label   = 'Microwave' if network == 'microwave' else 'Fiber'
    setup_label = 'Cloud'     if setup   == 'cloud'     else 'Co-located'

    sql_narrative = (
        f"-- [EVENT] NYSE WMT: $100.00 -> $99.95  spread=$0.05  potential=$5.00/100sh\n"
        f"-- [HFT-{net_label}] {hft_ms:.2f}ms: SELECT MIN(ask) FROM chi_orderbook; "
        f"INSERT INTO chi_orders (SELL 100sh @ $100.00)\n"
        f"-- [Retail-{setup_label}] {ret_ms:.2f}ms: SELECT MIN(ask) FROM chi_orderbook; "
        f"INSERT INTO chi_orders (SELL 100sh @ ...) -- price already moved\n"
        f"-- [{winner.upper()} WINS] ORDER FILLED @ $100.00 +$5.00 | "
        f"[{loser.upper()} REJECTED] {margin:.2f}ms late -- CHI price now $99.95"
    )

    try:
        conn = _hft_conn()
        _hft_init_db(conn)
        conn.execute(
            "INSERT INTO races (hft_network,retail_setup,hft_latency_ms,ret_latency_ms,winner,profit) "
            "VALUES (?,?,?,?,?,?)",
            (network, setup, hft_ms, ret_ms, winner, 5.00)
        )

        with _HFT_LOCK:
            _HFT_STATE['phase']               = 'result'
            _HFT_STATE['current_sql']         = sql_narrative
            _HFT_STATE['last_hft_latency_ms'] = hft_ms
            _HFT_STATE['last_ret_latency_ms'] = ret_ms
            _HFT_STATE['last_race_result']    = winner

        state = _hft_computed_state(conn, extra={
            'hft_latency_ms': hft_ms,
            'ret_latency_ms': ret_ms,
        })
        conn.close()
        return state
    except Exception as exc:
        return {'error': str(exc)}


def hft_reset():
    try:
        conn = _hft_conn()
        _hft_init_db(conn)
        conn.execute("DELETE FROM races")
        conn.close()
    except Exception:
        pass
    with _HFT_LOCK:
        _HFT_STATE['phase']               = 'idle'
        _HFT_STATE['current_sql']         = ''
        _HFT_STATE['last_hft_latency_ms'] = None
        _HFT_STATE['last_ret_latency_ms'] = None
        _HFT_STATE['last_race_result']    = None



# ── Order Fulfillment Demo ─────────────────────────────────────────────────────

_FULFILL_LOCK       = threading.Lock()
_FULFILL_STEP_EVENT = threading.Event()
_FULFILL_ABORTED    = False
_FULFILL_LOG_CONN   = None   # persistent autocommit connection for SQL logging

_FULFILL_ORDER_COLS = [
    'OrderID', 'CustomerID', 'EmployeeID', 'OrderDate', 'RequiredDate',
    'ShipVia', 'Freight', 'ShipName', 'ShipAddress', 'ShipCity',
    'ShipRegion', 'ShipPostalCode', 'ShipCountry',
]
_FULFILL_CUSTOMER_COLS = [
    'CustomerID', 'CompanyName', 'ContactName', 'ContactTitle',
    'Phone', 'Fax', 'City', 'Country',
]
_FULFILL_EMPLOYEE_COLS = [
    'EmployeeID', 'FirstName', 'LastName', 'Title',
    'TitleOfCourtesy', 'HomePhone', 'City', 'Country',
]
_FULFILL_SHIPPER_COLS  = ['ShipperID', 'CompanyName', 'Phone']
_FULFILL_PRODUCT_COLS  = [
    'ProductID', 'ProductName', 'QuantityPerUnit', 'UnitPrice',
    'UnitsInStock', 'UnitsOnOrder', 'ReorderLevel', 'Discontinued', 'SupplierID',
]
_FULFILL_SUPPLIER_COLS = [
    'SupplierID', 'CompanyName', 'ContactName', 'ContactTitle',
    'Phone', 'Fax', 'HomePage', 'City', 'Country',
]
_FULFILL_FK_MAP = {
    'CustomerID': ('Customers', 'CustomerID', _FULFILL_CUSTOMER_COLS, 'customer_card'),
    'EmployeeID': ('Employees', 'EmployeeID', _FULFILL_EMPLOYEE_COLS, 'employee_card'),
    'ShipVia':    ('Shippers',  'ShipperID',  _FULFILL_SHIPPER_COLS,  'shipper_card'),
}
# Orders columns that feed directly into package metadata
_FULFILL_META_FIELDS = {
    'OrderID', 'OrderDate', 'RequiredDate', 'Freight',
    'ShipName', 'ShipAddress', 'ShipCity', 'ShipRegion',
    'ShipPostalCode', 'ShipCountry',
}

_FULFILL_STATE_DEFAULTS: dict = {
    'phase': 'idle',
    'phase_label': '',
    'waiting_for_step': False,
    # Orders table
    'orders': [],
    'order_idx': 0,
    'orders_total': 0,
    'order_cols': [],
    'order_col_idx': -1,
    # Universal sub-table viewer
    'sub_table': None,
    # Order Details
    'items': [],
    'item_idx': -1,
    # Context cards (fill incrementally, cell by cell)
    'customer_card': {},
    'employee_card': {},
    'shipper_card': {},
    'supplier_card': {},
    'product_card': {},
    # Order queue (visual stack of in-flight orders)
    'order_queue': [],    # [{order_id, status: active|partial|shipped, customer}]
    # Refill order card (open while scanning Products/Suppliers for restock)
    'refill_order': None,  # None | {status:'open'|'sent', fields...}
    # Package
    'package_id': None,
    'package_items': [],
    'package_meta': {},   # accumulates order metadata field by field as it is read
    # SQL log
    'sql_log': [],
    'current_sql': '',
    # P&L running totals (updated in-memory as events fire)
    'pnl': {
        'initial_capital': 500000.0,
        'revenue':         0.0,
        'cogs':            0.0,
        'freight':         0.0,
        'restock':         0.0,
        'salaries':        0.0,
        'overhead':        0.0,
    },
    # DB changes (for reset)
    'changes': {
        'package_ids': [],
        'shipped_order_ids': [],
        'deleted_details': [],
        'stock_decremented': [],
        'stock_incremented': [],
    },
    'error': None,
    'conn_str': '',
}
_FULFILL_STATE: dict = copy.deepcopy(_FULFILL_STATE_DEFAULTS)


# ── Low-level helpers ─────────────────────────────────────────────────────────

def _fulfill_fix_val(v):
    if v is None:
        return None
    if isinstance(v, (datetime.datetime, datetime.date, datetime.time)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, str):
        try:
            return v.encode('latin-1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return v
    return v


def _queue_set(order_id, status, customer=''):
    with _FULFILL_LOCK:
        for q in _FULFILL_STATE['order_queue']:
            if q['order_id'] == order_id and q.get('type') != 'refill':
                q['status'] = status
                return
        _FULFILL_STATE['order_queue'].append(
            {'order_id': order_id, 'status': status, 'customer': customer}
        )


def _fulfill_sql_log(line):
    with _FULFILL_LOCK:
        _FULFILL_STATE['sql_log'].append(line)
        _FULFILL_STATE['current_sql'] = line
        conn_str = _FULFILL_STATE.get('conn_str', '')
    global _FULFILL_LOG_CONN
    if not conn_str:
        return
    # Try existing connection; reconnect once on failure
    for attempt in range(2):
        if _FULFILL_LOG_CONN is None:
            try:
                _FULFILL_LOG_CONN = pyodbc.connect(conn_str, autocommit=True, timeout=5)
            except Exception:
                return
        try:
            _FULFILL_LOG_CONN.execute("INSERT INTO log_(sql_text) VALUES (?)", [line])
            return
        except Exception:
            try: _FULFILL_LOG_CONN.close()
            except Exception: pass
            _FULFILL_LOG_CONN = None


def _ledger_insert(conn_str: str, event_type: str, amount: float,
                   description: str, order_id=None, product_id=None, employee_id=None):
    """Insert one row into CompanyLedger and update the in-memory pnl dict."""
    pnl_key = {
        'revenue': 'revenue', 'cogs': 'cogs', 'freight': 'freight',
        'restock': 'restock', 'salary': 'salaries', 'overhead': 'overhead',
    }.get(event_type)
    if pnl_key:
        with _FULFILL_LOCK:
            if event_type == 'revenue':
                _FULFILL_STATE['pnl'][pnl_key] += amount
            else:
                _FULFILL_STATE['pnl'][pnl_key] += abs(amount)

    _fulfill_sql_log(
        f"INSERT CompanyLedger({event_type}): {description}  [{amount:+.2f}]"
    )
    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=5)
        conn.execute(
            "INSERT INTO CompanyLedger(EventType,OrderID,ProductID,EmployeeID,Amount,Description)"
            " VALUES (?,?,?,?,?,?)",
            [event_type, order_id, product_id, employee_id, amount, description],
        )
        conn.close()
    except Exception:
        pass


def _step(**updates) -> bool:
    """Atomically update state fields and pause until Next Step is clicked.
    Returns True if the demo was aborted (reset)."""
    with _FULFILL_LOCK:
        _FULFILL_STATE.update(updates)
        _FULFILL_STATE['waiting_for_step'] = True
    _FULFILL_STEP_EVENT.wait()
    _FULFILL_STEP_EVENT.clear()
    with _FULFILL_LOCK:
        _FULFILL_STATE['waiting_for_step'] = False
    return _FULFILL_ABORTED


def _scan_subtable(conn_str: str, table_name: str, id_col: str, id_val,
                   scan_cols: list, card_key: str, refill_key: str = None) -> bool:
    """Physically 'open' table in the sub-table viewer, highlight the target row,
    then scan each column cell-by-cell, filling state[card_key] incrementally.
    Returns True if completed normally, False if aborted."""

    # Log the SELECT being executed
    col_list = ', '.join(scan_cols)
    _fulfill_sql_log(
        f"SELECT {col_list}\n"
        f"FROM [{table_name}]\n"
        f"WHERE [{id_col}] = '{id_val}'"
    )

    # Fetch full table ordered by PK
    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=10)
        try:
            cur = conn.cursor()
            col_list_sq = ', '.join(f'[{c}]' for c in scan_cols)
            cur.execute(f'SELECT {col_list_sq} FROM [{table_name}] ORDER BY [{id_col}]')
            all_rows = [
                {scan_cols[j]: _fulfill_fix_val(v) for j, v in enumerate(r)}
                for r in cur.fetchall()
            ]
        finally:
            conn.close()
    except Exception:
        all_rows = []

    # Locate target row
    str_val       = str(id_val)
    target_global = next(
        (i for i, r in enumerate(all_rows) if str(r.get(id_col, '')) == str_val),
        None,
    )
    if target_global is None:
        if _step(phase='sub_table_open',
                 phase_label=f'{table_name}: {id_col}={id_val} not found',
                 sub_table=None, **{card_key: {}}):
            return False
        return True

    # 5-row context window centred on target
    win_start  = max(0, target_global - 2)
    win_end    = min(len(all_rows), target_global + 3)
    ctx_rows   = all_rows[win_start:win_end]
    target_win = target_global - win_start

    # Step 1 — open table, highlight row (no column selected yet)
    if _step(
        phase='sub_table_open',
        phase_label=f'Opening {table_name} → searching {id_col} = {id_val}',
        sub_table={
            'table_name':     table_name,
            'columns':        scan_cols,
            'rows':           ctx_rows,
            'active_row_idx': target_win,
            'active_col_idx': -1,
        },
        **{card_key: {}},
    ): return False

    # Step 2 — scan each column, fill card (and optionally refill_order) incrementally
    card = {}
    for col_idx, col in enumerate(scan_cols):
        card[col] = all_rows[target_global][col]
        _fulfill_sql_log(f"  ↳ [{col}] = {repr(card[col])}")

        extra = {}
        if refill_key:
            with _FULFILL_LOCK:
                current_refill = dict(_FULFILL_STATE.get(refill_key, {}) or {})
            current_refill[col] = card[col]
            extra[refill_key] = current_refill

        if _step(
            phase='sub_table_scan',
            phase_label=f'{table_name}.{col} = {card[col]}',
            sub_table={
                'table_name':     table_name,
                'columns':        scan_cols,
                'rows':           ctx_rows,
                'active_row_idx': target_win,
                'active_col_idx': col_idx,
            },
            **{card_key: dict(card)},
            **extra,
        ): return False

    # Step 3 — close sub-table
    if _step(
        phase='sub_table_done',
        phase_label=f'{table_name} scan complete',
        sub_table=None,
    ): return False

    return True


def _fulfill_reset_state():
    with _FULFILL_LOCK:
        cs = _FULFILL_STATE.get('conn_str', '')
        _FULFILL_STATE.clear()
        _FULFILL_STATE.update(copy.deepcopy(_FULFILL_STATE_DEFAULTS))
        _FULFILL_STATE['conn_str'] = cs


# ── Public API ────────────────────────────────────────────────────────────────

def fulfill_get_state() -> dict:
    with _FULFILL_LOCK:
        return copy.deepcopy(_FULFILL_STATE)


def fulfill_step():
    """Advance the worker by one step (called from the Next Step button)."""
    _FULFILL_STEP_EVENT.set()


def _fulfill_ensure_tables(conn_str: str):
    """Create Packages / PackageItems if missing, run one-time 1996 init and wrap-around.
    Idempotent — safe to call on every Start and Reset."""
    _db_m    = re.search(r'DATABASE=([^;]+)', conn_str, re.I)
    _db_name = _db_m.group(1).strip() if _db_m else 'Northwind'
    conn = pyodbc.connect(conn_str, autocommit=True, timeout=10)
    conn.execute(f'USE [{_db_name}]')
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='Packages')
            CREATE TABLE Packages (
                PackageID INT IDENTITY(1,1) PRIMARY KEY,
                OrderID   INT NOT NULL,
                CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
                Status    NVARCHAR(20) NOT NULL DEFAULT 'packing'
            )
    """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='PackageItems')
            CREATE TABLE PackageItems (
                ItemID      INT IDENTITY(1,1) PRIMARY KEY,
                PackageID   INT NOT NULL REFERENCES Packages(PackageID),
                ProductID   INT NOT NULL,
                ProductName NVARCHAR(100),
                Quantity    INT NOT NULL,
                Status      NVARCHAR(20) NOT NULL DEFAULT 'packed'
            )
    """)
    conn.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM sys.columns
            WHERE object_id = OBJECT_ID('PackageItems') AND name = 'Status'
        )
            ALTER TABLE PackageItems ADD Status NVARCHAR(20) NOT NULL DEFAULT 'packed'
    """)
    # CREATE TRIGGER must be the first statement in its batch — check separately.
    _cur = conn.cursor()
    _cur.execute("SELECT COUNT(*) FROM sys.triggers WHERE name='trg_PackageItems_DecrStock'")
    if _cur.fetchone()[0] == 0:
        conn.execute("""
            CREATE TRIGGER trg_PackageItems_DecrStock
            ON PackageItems AFTER INSERT AS
            BEGIN
                SET NOCOUNT ON;
                UPDATE p
                SET    p.UnitsInStock = p.UnitsInStock - i.Quantity
                FROM   Products p
                JOIN   inserted i ON i.ProductID = p.ProductID
                WHERE  i.Status = 'packed'
            END
        """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='log_')
            CREATE TABLE log_ (
                id       INT IDENTITY(1,1) PRIMARY KEY,
                ts       DATETIME      NOT NULL DEFAULT GETDATE(),
                sql_text NVARCHAR(MAX) NOT NULL
            )
    """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='RefillOrders')
            CREATE TABLE RefillOrders (
                RefillID    INT IDENTITY(1,1) PRIMARY KEY,
                OrderID     INT NOT NULL,
                ProductID   INT NOT NULL,
                ProductName NVARCHAR(100),
                NeededQty   INT NOT NULL,
                RestockQty  INT NOT NULL DEFAULT 100,
                SupplierID  INT,
                Supplier    NVARCHAR(100),
                SentAt              DATETIME NOT NULL DEFAULT GETDATE(),
                Status              NVARCHAR(20) NOT NULL DEFAULT 'sent',
                TicksUntilDelivery  INT NOT NULL DEFAULT 3
            )
    """)
    # Migration: add TicksUntilDelivery to existing RefillOrders table
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.columns
                       WHERE object_id=OBJECT_ID('RefillOrders') AND name='TicksUntilDelivery')
            ALTER TABLE RefillOrders ADD TicksUntilDelivery INT NOT NULL DEFAULT 3
    """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='CompanySettings')
        BEGIN
            CREATE TABLE CompanySettings (
                SettingKey   NVARCHAR(50)  NOT NULL PRIMARY KEY,
                SettingValue NVARCHAR(200) NOT NULL
            )
            INSERT INTO CompanySettings VALUES ('InitialCapital','500000')
            INSERT INTO CompanySettings VALUES ('SimulationYear','1996')
            INSERT INTO CompanySettings VALUES ('MonthlyOverhead','5000')
        END
    """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='CompanyLedger')
            CREATE TABLE CompanyLedger (
                LedgerID    INT IDENTITY(1,1) PRIMARY KEY,
                EventType   NVARCHAR(30)  NOT NULL,
                OrderID     INT           NULL,
                ProductID   INT           NULL,
                EmployeeID  INT           NULL,
                Amount      MONEY         NOT NULL,
                Description NVARCHAR(200) NULL,
                EventDate   DATETIME      NOT NULL DEFAULT GETDATE()
            )
    """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.columns
                       WHERE object_id=OBJECT_ID('Products') AND name='UnitCost')
        BEGIN
            ALTER TABLE Products ADD UnitCost MONEY NULL
            UPDATE Products SET UnitCost = ROUND(UnitPrice * 0.60, 2)
        END
    """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.columns
                       WHERE object_id=OBJECT_ID('Employees') AND name='MonthlySalary')
        BEGIN
            ALTER TABLE Employees ADD MonthlySalary MONEY NULL
            UPDATE Employees SET MonthlySalary =
                CASE EmployeeID
                    WHEN 1 THEN 2800 WHEN 2 THEN 5500 WHEN 3 THEN 2600
                    WHEN 4 THEN 2700 WHEN 5 THEN 4200 WHEN 6 THEN 2500
                    WHEN 7 THEN 2500 WHEN 8 THEN 3100 WHEN 9 THEN 2400
                    ELSE 2500
                END
        END
    """)
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'FulfillDemoInit')
        BEGIN
            CREATE TABLE FulfillDemoInit (InitAt DATETIME NOT NULL DEFAULT GETDATE())
            INSERT INTO FulfillDemoInit DEFAULT VALUES
            DELETE FROM PackageItems
            DELETE FROM Packages
            UPDATE Orders SET ShippedDate = NULL
        END
    """)
    conn.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM Orders
            WHERE ShippedDate IS NULL
              AND NOT EXISTS (SELECT 1 FROM Packages WHERE OrderID = Orders.OrderID)
        )
        BEGIN
            DELETE FROM PackageItems
            DELETE FROM Packages
            UPDATE Orders SET ShippedDate = NULL
        END
    """)
    conn.close()


def fulfill_start(conn_str: str):
    global _FULFILL_ABORTED
    with _FULFILL_LOCK:
        if _FULFILL_STATE['phase'] != 'idle':
            return
        _FULFILL_STATE.update(copy.deepcopy(_FULFILL_STATE_DEFAULTS))
        _FULFILL_STATE['phase']       = 'loading'
        _FULFILL_STATE['phase_label'] = 'Loading orders…'
        _FULFILL_STATE['conn_str']    = conn_str

    _FULFILL_ABORTED = False
    _FULFILL_STEP_EVENT.clear()

    _db_m    = re.search(r'DATABASE=([^;]+)', conn_str, re.I)
    _db_name = _db_m.group(1).strip() if _db_m else 'Northwind'

    try:
        setup = pyodbc.connect(conn_str, autocommit=True, timeout=10)
        setup.execute(f'USE [{_db_name}]')
        setup.execute("""
            IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='Packages')
                CREATE TABLE Packages (
                    PackageID INT IDENTITY(1,1) PRIMARY KEY,
                    OrderID   INT NOT NULL,
                    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
                    Status    NVARCHAR(20) NOT NULL DEFAULT 'packing'
                )
        """)
        setup.execute("""
            IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name='PackageItems')
                CREATE TABLE PackageItems (
                    ItemID      INT IDENTITY(1,1) PRIMARY KEY,
                    PackageID   INT NOT NULL REFERENCES Packages(PackageID),
                    ProductID   INT NOT NULL,
                    ProductName NVARCHAR(100),
                    Quantity    INT NOT NULL
                )
        """)
        # One-time 1996 init: null every ShippedDate so the full catalogue is available.
        # Guarded by a sentinel table so it only fires on the very first Start ever.
        setup.execute("""
            IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'FulfillDemoInit')
            BEGIN
                CREATE TABLE FulfillDemoInit (InitAt DATETIME NOT NULL DEFAULT GETDATE())
                INSERT INTO FulfillDemoInit DEFAULT VALUES
                DELETE FROM PackageItems
                DELETE FROM Packages
                UPDATE Orders SET ShippedDate = NULL
            END
        """)
        # Wrap-around: if no unstarted orders remain, reset for the next cycle.
        setup.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM Orders
                WHERE ShippedDate IS NULL
                  AND NOT EXISTS (SELECT 1 FROM Packages WHERE OrderID = Orders.OrderID)
            )
            BEGIN
                DELETE FROM PackageItems
                DELETE FROM Packages
                UPDATE Orders SET ShippedDate = NULL
            END
        """)
        cur = setup.cursor()
        cur.execute("""
            SELECT TOP 5 OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate,
                         ShipVia, Freight, ShipName, ShipAddress, ShipCity,
                         ShipRegion, ShipPostalCode, ShipCountry
            FROM Orders
            WHERE ShippedDate IS NULL
              AND NOT EXISTS (
                  SELECT 1 FROM Packages WHERE OrderID = Orders.OrderID
              )
            ORDER BY OrderID
        """)
        orders = [
            {col: _fulfill_fix_val(r[i]) for i, col in enumerate(_FULFILL_ORDER_COLS)}
            for r in cur.fetchall()
        ]
        setup.close()

        # Open a dedicated autocommit connection for SQL logging
        global _FULFILL_LOG_CONN
        try:
            if _FULFILL_LOG_CONN:
                try: _FULFILL_LOG_CONN.close()
                except Exception: pass
            _FULFILL_LOG_CONN = pyodbc.connect(conn_str, autocommit=True, timeout=10)
        except Exception:
            _FULFILL_LOG_CONN = None

    except Exception as e:
        with _FULFILL_LOCK:
            _FULFILL_STATE['phase'] = 'error'
            _FULFILL_STATE['error'] = str(e)
        return

    # Seed P&L initial capital from CompanySettings
    try:
        _ic_conn = pyodbc.connect(conn_str, autocommit=True, timeout=5)
        _ic_cur  = _ic_conn.cursor()
        _ic_cur.execute("SELECT SettingValue FROM CompanySettings WHERE SettingKey='InitialCapital'")
        _ic_row = _ic_cur.fetchone()
        _ic = float(_ic_row[0]) if _ic_row else 500000.0

        # Seed salary ledger rows for this run
        _ic_cur.execute("SELECT EmployeeID, FirstName, LastName, MonthlySalary FROM Employees WHERE MonthlySalary IS NOT NULL")
        _sal_rows = _ic_cur.fetchall()

        # Seed overhead
        _ic_cur.execute("SELECT SettingValue FROM CompanySettings WHERE SettingKey='MonthlyOverhead'")
        _oh_row = _ic_cur.fetchone()
        _oh = float(_oh_row[0]) if _oh_row else 5000.0
        _ic_conn.close()
    except Exception:
        _ic = 500000.0; _sal_rows = []; _oh = 5000.0

    with _FULFILL_LOCK:
        _FULFILL_STATE['orders']           = orders
        _FULFILL_STATE['orders_total']     = len(orders)
        _FULFILL_STATE['order_cols']       = _FULFILL_ORDER_COLS
        _FULFILL_STATE['pnl']['initial_capital'] = _ic

    # Insert salary + overhead ledger rows (fire-and-forget, non-blocking)
    def _seed_ledger():
        for eid, fname, lname, sal in _sal_rows:
            _ledger_insert(conn_str, 'salary', -float(sal),
                           f'Monthly salary: {fname} {lname}', employee_id=eid)
        _ledger_insert(conn_str, 'overhead', -_oh, 'Monthly overhead (rent/utilities)')

    threading.Thread(target=_seed_ledger, daemon=True).start()
    threading.Thread(target=_fulfill_worker, daemon=True).start()


def fulfill_reset():
    global _FULFILL_ABORTED, _FULFILL_LOG_CONN
    _FULFILL_ABORTED = True
    _FULFILL_STEP_EVENT.set()   # unblock any waiting step

    if _FULFILL_LOG_CONN:
        try: _FULFILL_LOG_CONN.close()
        except Exception: pass
        _FULFILL_LOG_CONN = None

    with _FULFILL_LOCK:
        ch       = copy.deepcopy(_FULFILL_STATE['changes'])
        conn_str = _FULFILL_STATE['conn_str']

    # Always ensure schema exists — recovers from manual DROP TABLE
    if conn_str:
        try:
            _fulfill_ensure_tables(conn_str)
        except Exception:
            pass

    if conn_str:
        try:
            conn = pyodbc.connect(conn_str, autocommit=False, timeout=15)
            cur  = conn.cursor()
            try:
                if ch['shipped_order_ids']:
                    ph = ','.join('?' * len(ch['shipped_order_ids']))
                    cur.execute(
                        f"UPDATE Orders SET ShippedDate=NULL WHERE OrderID IN ({ph})",
                        ch['shipped_order_ids'],
                    )
                for d in ch['deleted_details']:
                    cur.execute(
                        "INSERT INTO [Order Details]"
                        "(OrderID,ProductID,UnitPrice,Quantity,Discount)"
                        " VALUES (?,?,?,?,?)",
                        [d['OrderID'], d['ProductID'], d['UnitPrice'],
                         d['Quantity'], d['Discount']],
                    )
                for pid, delta in ch['stock_decremented']:
                    cur.execute(
                        "UPDATE Products SET UnitsInStock=UnitsInStock+? WHERE ProductID=?",
                        [delta, pid],
                    )
                for pid, delta in ch['stock_incremented']:
                    cur.execute(
                        "UPDATE Products SET UnitsInStock=UnitsInStock-? WHERE ProductID=?",
                        [delta, pid],
                    )
                if ch['package_ids']:
                    ph = ','.join('?' * len(ch['package_ids']))
                    cur.execute(f"DELETE FROM PackageItems WHERE PackageID IN ({ph})",
                                ch['package_ids'])
                    cur.execute(f"DELETE FROM Packages WHERE PackageID IN ({ph})",
                                ch['package_ids'])
                # Clear refill orders and ledger from this run
                if ch.get('shipped_order_ids') or ch.get('deleted_details'):
                    cur.execute("DELETE FROM RefillOrders WHERE Status IN ('sent','arrived')")
                cur.execute("DELETE FROM CompanyLedger")
                conn.commit()
            except Exception:
                conn.rollback()
            finally:
                conn.close()
        except Exception:
            pass

    _fulfill_reset_state()


# ── Partial-order completion helper ──────────────────────────────────────────

def _check_deliveries(conn_str: str) -> bool:
    """Decrement delivery ticks; arrive orders whose tick reaches 0; restock Products.
    Returns True if aborted."""
    with _FULFILL_LOCK:
        # Decrement ticks for all in-transit refills
        for q in _FULFILL_STATE['order_queue']:
            if q.get('type') == 'refill' and q.get('status') == 'refill':
                q['ticks_remaining'] = max(0, q.get('ticks_remaining', 3) - 1)
        # Decrement in DB too (best-effort, fire-and-forget)
        _conn_str_snap = _FULFILL_STATE.get('conn_str', conn_str)

    try:
        _tc = pyodbc.connect(_conn_str_snap, autocommit=True, timeout=5)
        _tc.execute(
            "UPDATE RefillOrders SET TicksUntilDelivery = CASE WHEN TicksUntilDelivery > 0"
            " THEN TicksUntilDelivery - 1 ELSE 0 END WHERE Status='sent'"
        )
        _tc.close()
    except Exception:
        pass

    with _FULFILL_LOCK:
        pending = [q for q in _FULFILL_STATE['order_queue']
                   if q.get('type') == 'refill' and q.get('status') == 'refill'
                   and q.get('ticks_remaining', 3) <= 0]

    if not pending:
        return False

    if _step(phase='delivery_check',
             phase_label='Checking for incoming deliveries…'):
        return True

    for entry in pending:
        if _FULFILL_ABORTED:
            return True

        pid         = entry.get('product_id')
        restock_qty = entry.get('restock_qty', 100)
        product     = entry.get('product', f'Product #{pid}')

        # Mark arrived in queue
        with _FULFILL_LOCK:
            for q in _FULFILL_STATE['order_queue']:
                if (q.get('type') == 'refill' and q.get('product_id') == pid
                        and q.get('status') == 'refill'):
                    q['status'] = 'arrived'
                    break

        # Restock in DB + mark RefillOrders row as arrived
        try:
            conn_rs = pyodbc.connect(conn_str, autocommit=True, timeout=10)
            conn_rs.execute(
                'UPDATE Products SET UnitsInStock=UnitsInStock+? WHERE ProductID=?',
                [restock_qty, pid],
            )
            try:
                conn_rs.execute(
                    "UPDATE RefillOrders SET Status='arrived' WHERE ProductID=? AND Status='sent'",
                    [pid],
                )
            except Exception:
                pass
            conn_rs.close()
            _fulfill_sql_log(
                f'UPDATE Products +{restock_qty}'
                f' WHERE ProductID={pid}  ← delivery arrived ✓'
            )
            _fulfill_sql_log(
                f"UPDATE RefillOrders SET Status='arrived' WHERE ProductID={pid}"
            )
            with _FULFILL_LOCK:
                _FULFILL_STATE['changes']['stock_incremented'].append((pid, restock_qty))

            # P&L: restock cost = RestockQty × UnitCost
            try:
                conn_uc = pyodbc.connect(conn_str, autocommit=True, timeout=5)
                cur_uc  = conn_uc.cursor()
                cur_uc.execute('SELECT UnitCost, ProductName FROM Products WHERE ProductID=?', [pid])
                uc_row = cur_uc.fetchone()
                conn_uc.close()
                unit_cost    = float(uc_row[0]) if uc_row and uc_row[0] else 0.0
                product_name = uc_row[1] if uc_row else product
            except Exception:
                unit_cost = 0.0; product_name = product
            restock_cost = round(unit_cost * restock_qty, 2)
            if restock_cost:
                _ledger_insert(conn_str, 'restock', -restock_cost,
                               f'Restock: {product_name} ×{restock_qty} from supplier',
                               product_id=pid)
        except Exception as e:
            with _FULFILL_LOCK:
                _FULFILL_STATE['phase'] = 'error'
                _FULFILL_STATE['error'] = str(e)
            return True

        if _step(phase='delivery_arrived',
                 phase_label=f'✓ Delivery arrived: {product} ×{restock_qty}'):
            return True

    return False


def _can_fulfill_partial(pp: dict, conn_str: str) -> bool:
    """Return True if all short items in pp have sufficient stock now."""
    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=10)
        cur  = conn.cursor()
        for item in pp['short_items']:
            cur.execute(
                'SELECT UnitsInStock FROM Products WHERE ProductID=?',
                [item['ProductID']],
            )
            row = cur.fetchone()
            if not row or row[0] < item['Quantity']:
                conn.close()
                return False
        conn.close()
        return True
    except Exception:
        return False


def _complete_and_ship_partial(p: dict, conn_str: str) -> bool:
    """Pack already-restocked items and ship the partial order.
    Delivery restock is assumed done by _check_deliveries.
    Returns True if aborted."""
    order_id = p['order_id']
    pkg_id   = p['pkg_id']

    _queue_set(order_id, 'active')

    if _step(phase='returning_to_partial',
             phase_label=f'Returning to partial order {order_id}…'):
        return True

    # Restore the partial order's display state
    with _FULFILL_LOCK:
        _FULFILL_STATE['order_idx']     = p['order_idx']
        _FULFILL_STATE['items']         = [dict(it) for it in p['raw_items']]
        _FULFILL_STATE['package_id']    = pkg_id
        _FULFILL_STATE['package_items'] = [dict(pi) for pi in p['pkg_items_snapshot']]
        _FULFILL_STATE['package_meta']  = dict(p['package_meta'])

    # Pack each restocked short item
    for short_item in p['short_items']:
        if _FULFILL_ABORTED:
            return True

        with _FULFILL_LOCK:
            for pkg in _FULFILL_STATE['package_items']:
                if pkg['ProductID'] == short_item['ProductID']:
                    pkg['status'] = 'completing'
                    break

        _fulfill_sql_log(
            f'BEGIN TRAN  -- completing partial: {short_item["ProductName"]}'
        )
        try:
            conn_c = pyodbc.connect(conn_str, autocommit=False, timeout=15)
            conn_c.execute(
                'UPDATE Products SET UnitsInStock=UnitsInStock-? WHERE ProductID=?',
                [short_item['Quantity'], short_item['ProductID']],
            )
            _fulfill_sql_log(
                f'UPDATE Products -{short_item["Quantity"]}'
                f' WHERE ProductID={short_item["ProductID"]} ✓'
            )
            conn_c.execute(
                "UPDATE PackageItems SET Status='packed'"
                " WHERE PackageID=? AND ProductID=? AND Status='awaiting_restock'",
                [p['pkg_id'], short_item['ProductID']],
            )
            _fulfill_sql_log(
                f"UPDATE PackageItems SET Status='packed'"
                f" WHERE PackageID={p['pkg_id']} AND ProductID={short_item['ProductID']}"
            )
            conn_c.commit()
            conn_c.close()
        except Exception as e:
            try: conn_c.rollback(); conn_c.close()
            except Exception: pass
            with _FULFILL_LOCK:
                _FULFILL_STATE['phase'] = 'error'
                _FULFILL_STATE['error'] = str(e)
            return True

        with _FULFILL_LOCK:
            for pkg in _FULFILL_STATE['package_items']:
                if pkg['ProductID'] == short_item['ProductID']:
                    pkg['status'] = 'packed'
                    break
            _FULFILL_STATE['changes']['stock_decremented'].append(
                (short_item['ProductID'], short_item['Quantity'])
            )

        if _step(phase='completing_partial',
                 phase_label=f'✓ Packed: {short_item["ProductName"]} ×{short_item["Quantity"]}'):
            return True

    # Ship
    _fulfill_sql_log(f'BEGIN TRAN  -- shipping partial order {order_id}')
    try:
        conn_s = pyodbc.connect(conn_str, autocommit=False, timeout=15)
        cur_s  = conn_s.cursor()
    except Exception as e:
        with _FULFILL_LOCK:
            _FULFILL_STATE['phase'] = 'error'
            _FULFILL_STATE['error'] = str(e)
        return True

    if _step(phase='removing_details',
             phase_label=f'Removing Order Details for order {order_id}…'):
        conn_s.rollback(); conn_s.close(); return True

    for item in p['raw_items']:
        if _FULFILL_ABORTED:
            conn_s.rollback(); conn_s.close(); return True
        try:
            cur_s.execute(
                'DELETE FROM [Order Details] WHERE OrderID=? AND ProductID=?',
                [order_id, item['ProductID']],
            )
        except Exception as e:
            conn_s.rollback(); conn_s.close()
            with _FULFILL_LOCK:
                _FULFILL_STATE['phase'] = 'error'
                _FULFILL_STATE['error'] = str(e)
            return True
        _fulfill_sql_log(
            f"DELETE [Order Details] OrderID={order_id} ProductID={item['ProductID']}"
        )
        with _FULFILL_LOCK:
            _FULFILL_STATE['changes']['deleted_details'].append({
                'OrderID':   order_id,
                'ProductID': item['ProductID'],
                'UnitPrice': item['UnitPrice'],
                'Quantity':  item['Quantity'],
                'Discount':  item['Discount'],
            })
        if _step(phase='removing_details',
                 phase_label=f'Deleted {item["ProductName"]} from Order Details'):
            conn_s.rollback(); conn_s.close(); return True

    try:
        cur_s.execute(
            'UPDATE Orders SET ShippedDate=GETDATE() WHERE OrderID=?', [order_id]
        )
        cur_s.execute(
            "UPDATE Packages SET Status='shipped' WHERE PackageID=?", [pkg_id]
        )
        _fulfill_sql_log(
            f'UPDATE Orders ShippedDate=GETDATE() WHERE OrderID={order_id}'
        )
        _fulfill_sql_log('COMMIT')
        conn_s.commit()
    except Exception as e:
        conn_s.rollback(); conn_s.close()
        with _FULFILL_LOCK:
            _FULFILL_STATE['phase'] = 'error'
            _FULFILL_STATE['error'] = str(e)
        return True
    conn_s.close()

    with _FULFILL_LOCK:
        _FULFILL_STATE['changes']['shipped_order_ids'].append(order_id)

    # P&L: revenue + COGS per line item, freight per order
    for item in p['raw_items']:
        rev = round(item['UnitPrice'] * item['Quantity'] * (1 - item['Discount']), 2)
        try:
            _cc = pyodbc.connect(conn_str, autocommit=True, timeout=5)
            _cr = _cc.cursor()
            _cr.execute('SELECT UnitCost FROM Products WHERE ProductID=?', [item['ProductID']])
            _uc_row = _cr.fetchone()
            _cc.close()
            unit_cost = float(_uc_row[0]) if _uc_row and _uc_row[0] else item['UnitPrice'] * 0.6
        except Exception:
            unit_cost = item['UnitPrice'] * 0.6
        cogs = round(unit_cost * item['Quantity'], 2)
        _ledger_insert(conn_str, 'revenue', rev,
                       f"Revenue: {item['ProductName']} ×{item['Quantity']}",
                       order_id=order_id, product_id=item['ProductID'])
        _ledger_insert(conn_str, 'cogs', -cogs,
                       f"COGS: {item['ProductName']} ×{item['Quantity']}",
                       order_id=order_id, product_id=item['ProductID'])
    freight = float(p['package_meta'].get('Freight') or 0)
    if freight:
        ship_to = ', '.join(filter(None, [
            p['package_meta'].get('ShipName'), p['package_meta'].get('ShipCity'),
        ]))
        _ledger_insert(conn_str, 'freight', -freight,
                       f'Freight: {ship_to}', order_id=order_id)

    _queue_set(order_id, 'shipped')
    with _FULFILL_LOCK:
        # Attach final details to the queue entry
        pkg_items_now = list(_FULFILL_STATE['package_items'])
        meta_now      = dict(_FULFILL_STATE['package_meta'])
        for q in _FULFILL_STATE['order_queue']:
            if q['order_id'] == order_id and q.get('type') != 'refill':
                q['details'] = {
                    'ship_to': ', '.join(filter(None, [
                        meta_now.get('ShipName'), meta_now.get('ShipCity'),
                        meta_now.get('ShipCountry'),
                    ])),
                    'items': [{'name': pi['ProductName'], 'qty': pi['Quantity'],
                               'status': pi['status']} for pi in pkg_items_now],
                }
                break
        # Remove refill delivery entries for this order — delivery is consumed
        _FULFILL_STATE['order_queue'] = [
            q for q in _FULFILL_STATE['order_queue']
            if not (q.get('type') == 'refill' and q.get('order_id') == order_id)
        ]
    return _step(phase='shipped',
                 phase_label=f'✓ Partial order {order_id} fully shipped!')


# ── Dynamic order loader ──────────────────────────────────────────────────────

def _load_next_order(conn_str: str):
    """Fetch the next unprocessed order and append it to the live orders list."""
    with _FULFILL_LOCK:
        loaded_ids = [o['OrderID'] for o in _FULFILL_STATE['orders']]

    if not loaded_ids:
        return

    placeholders = ','.join('?' * len(loaded_ids))
    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=10)
        cur  = conn.cursor()
        cur.execute(f"""
            SELECT TOP 1 OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate,
                         ShipVia, Freight, ShipName, ShipAddress, ShipCity,
                         ShipRegion, ShipPostalCode, ShipCountry
            FROM Orders
            WHERE ShippedDate IS NULL
              AND NOT EXISTS (SELECT 1 FROM Packages WHERE OrderID = Orders.OrderID)
              AND OrderID NOT IN ({placeholders})
            ORDER BY OrderID
        """, loaded_ids)
        row = cur.fetchone()
        conn.close()
        if row:
            order = {col: _fulfill_fix_val(row[i])
                     for i, col in enumerate(_FULFILL_ORDER_COLS)}
            with _FULFILL_LOCK:
                _FULFILL_STATE['orders'].append(order)
                _FULFILL_STATE['orders_total'] = len(_FULFILL_STATE['orders'])
    except Exception:
        pass


# ── Worker ────────────────────────────────────────────────────────────────────

def _fulfill_worker():
    with _FULFILL_LOCK:
        conn_str = _FULFILL_STATE['conn_str']

    pending_partials = []   # partial orders waiting for delivery
    idx = 0

    while True:
        if _FULFILL_ABORTED:
            return
        with _FULFILL_LOCK:
            if idx >= len(_FULFILL_STATE['orders']):
                break
            order = dict(_FULFILL_STATE['orders'][idx])

        order_id = order['OrderID']

        # Reset all per-order display state
        _queue_set(order_id, 'active')
        with _FULFILL_LOCK:
            _FULFILL_STATE.update({
                'order_idx':     idx,
                'phase':         'reading_order',
                'phase_label':   f'Order {order_id}',
                'order_col_idx': -1,
                'sub_table':     None,
                'items':         [],
                'item_idx':      -1,
                'package_id':    None,
                'package_items': [],
                'package_meta':  {},
                'customer_card': {},
                'employee_card': {},
                'shipper_card':  {},
                'supplier_card': {},
                'product_card':  {},
                'refill_order':  None,
            })

        if _step(phase='reading_order',
                 phase_label=f'Order {order_id} — click Next to begin reading'):
            return

        # ── Read each column of the Orders row, follow FK columns ──
        _fulfill_sql_log(
            f"SELECT OrderID,CustomerID,EmployeeID,OrderDate,\n"
            f"  RequiredDate,ShipVia,Freight,ShipName,...\n"
            f"FROM Orders WHERE OrderID={order_id}"
        )
        for col_idx, col in enumerate(_FULFILL_ORDER_COLS):
            _fulfill_sql_log(f"  ↳ [{col}] = {repr(order.get(col, ''))}")

            # Accumulate package metadata from Orders fields as they are read
            with _FULFILL_LOCK:
                if col in _FULFILL_META_FIELDS:
                    _FULFILL_STATE['package_meta'][col] = order.get(col)
                new_meta = dict(_FULFILL_STATE['package_meta'])

            if _step(phase='reading_field',
                     phase_label=f'Orders.{col} = {order.get(col, "")}',
                     order_col_idx=col_idx,
                     sub_table=None,
                     package_meta=new_meta):
                return

            if col in _FULFILL_FK_MAP:
                tbl, id_col, scan_cols, card_key = _FULFILL_FK_MAP[col]
                if not _scan_subtable(conn_str, tbl, id_col, order[col],
                                      scan_cols, card_key):
                    return
                # After FK scan: pull the "name" field into package metadata
                with _FULFILL_LOCK:
                    card_data = _FULFILL_STATE.get(card_key, {})
                    if card_key == 'customer_card':
                        _FULFILL_STATE['package_meta']['Customer'] = card_data.get('CompanyName')
                        # Also update queue entry so collapsed header can show customer name
                        cname = card_data.get('CompanyName', '')
                        for q in _FULFILL_STATE['order_queue']:
                            if q['order_id'] == order_id:
                                q['customer'] = cname
                                break
                    elif card_key == 'employee_card':
                        fname = card_data.get('FirstName', '') or ''
                        lname = card_data.get('LastName', '') or ''
                        _FULFILL_STATE['package_meta']['Employee'] = f'{fname} {lname}'.strip()
                    elif card_key == 'shipper_card':
                        _FULFILL_STATE['package_meta']['Shipper'] = card_data.get('CompanyName')
                    # Snapshot updated meta so the package card rerenders on next poll
                    _FULFILL_STATE['package_meta'] = dict(_FULFILL_STATE['package_meta'])

        # ── Load Order Details rows ──
        _fulfill_sql_log(
            f"SELECT od.ProductID, p.ProductName, od.Quantity,\n"
            f"  od.UnitPrice, od.Discount, p.UnitsInStock\n"
            f"FROM [Order Details] od\n"
            f"  JOIN Products p ON p.ProductID = od.ProductID\n"
            f"WHERE od.OrderID = {order_id}"
        )
        try:
            conn_items = pyodbc.connect(conn_str, autocommit=True, timeout=10)
            cur_items  = conn_items.cursor()
            cur_items.execute("""
                SELECT od.ProductID, p.ProductName, od.Quantity, od.UnitPrice,
                       od.Discount, p.UnitsInStock
                FROM [Order Details] od
                JOIN Products p ON p.ProductID = od.ProductID
                WHERE od.OrderID = ?
            """, [order_id])
            raw_items = [
                {
                    'ProductID':    r[0],
                    'ProductName':  _fulfill_fix_val(r[1]),
                    'Quantity':     r[2],
                    'UnitPrice':    float(r[3]) if r[3] is not None else 0.0,
                    'Discount':     float(r[4]) if r[4] is not None else 0.0,
                    'UnitsInStock': r[5],
                    'status':       'pending',
                }
                for r in cur_items.fetchall()
            ]
            conn_items.close()
        except Exception as e:
            with _FULFILL_LOCK:
                _FULFILL_STATE['phase'] = 'error'
                _FULFILL_STATE['error'] = str(e)
            return

        with _FULFILL_LOCK:
            _FULFILL_STATE['items'] = raw_items

        # ── Scan each item row, follow ProductID → Products sub-table ──
        for i, item in enumerate(raw_items):
            if _step(phase='reading_items',
                     phase_label=f'Item {i + 1}/{len(raw_items)}: {item["ProductName"]}',
                     item_idx=i,
                     sub_table=None,
                     product_card={}):
                return

            if not _scan_subtable(conn_str, 'Products', 'ProductID',
                                  item['ProductID'], _FULFILL_PRODUCT_COLS,
                                  'product_card'):
                return

            ok = item['UnitsInStock'] >= item['Quantity']
            with _FULFILL_LOCK:
                _FULFILL_STATE['items'][i]['status'] = 'ok' if ok else 'short'
                if ok:
                    # Immediately reflect the reservation: decrement displayed stock
                    # and queue item in the package card
                    _FULFILL_STATE['items'][i]['UnitsInStock'] -= item['Quantity']
                    _FULFILL_STATE['package_items'].append({
                        'ProductID':   item['ProductID'],
                        'ProductName': item['ProductName'],
                        'Quantity':    item['Quantity'],
                        'status':      'queued',
                    })

            if _step(
                phase='stock_checked',
                phase_label=(
                    f'{"✓ OK" if ok else "✗ SHORT"}: {item["ProductName"]} — '
                    f'{item["UnitsInStock"]} in stock, need {item["Quantity"]}'
                ),
            ): return

        # ── Pack & Ship ───────────────────────────────────────────
        if _step(phase='checking_stock',
                 phase_label='Stock check complete — ready to begin transaction?'):
            return

        _fulfill_sql_log('BEGIN TRAN')
        try:
            conn_tx = pyodbc.connect(conn_str, autocommit=False, timeout=15)
        except Exception as e:
            with _FULFILL_LOCK:
                _FULFILL_STATE['phase'] = 'error'
                _FULFILL_STATE['error'] = str(e)
            return
        cur_tx = conn_tx.cursor()

        if _step(phase='begin_tran', phase_label='BEGIN TRANSACTION'):
            conn_tx.rollback(); conn_tx.close(); return

        # INSERT Packages
        try:
            cur_tx.execute(
                "INSERT INTO Packages(OrderID, Status)"
                " OUTPUT INSERTED.PackageID VALUES (?, 'packing')",
                [order_id],
            )
            row_pkg = cur_tx.fetchone()
            pkg_id  = int(row_pkg[0]) if row_pkg and row_pkg[0] is not None else None
        except Exception as e:
            conn_tx.rollback(); conn_tx.close()
            with _FULFILL_LOCK:
                _FULFILL_STATE['phase'] = 'error'
                _FULFILL_STATE['error'] = str(e)
            return

        _fulfill_sql_log(f'INSERT INTO Packages(OrderID={order_id}) → PackageID={pkg_id}')
        with _FULFILL_LOCK:
            _FULFILL_STATE['package_id'] = pkg_id
            # package_items already populated with 'queued' entries from stock-check — keep them

        if _step(phase='creating_package', phase_label=f'Package #{pkg_id} created'):
            conn_tx.rollback(); conn_tx.close(); return
        if _step(phase='packing', phase_label='Packing items…'):
            conn_tx.rollback(); conn_tx.close(); return

        # Pack each item: OK → deduct stock now; SHORT → mark awaiting_restock, defer
        short_items   = []
        short_pid_set = set()
        for i, item in enumerate(raw_items):
            if _FULFILL_ABORTED:
                conn_tx.rollback(); conn_tx.close(); return

            item_ok = (_FULFILL_STATE['items'][i].get('status') == 'ok')
            item_status = 'packed' if item_ok else 'awaiting_restock'

            try:
                cur_tx.execute(
                    'INSERT INTO PackageItems(PackageID,ProductID,ProductName,Quantity,Status)'
                    ' VALUES (?,?,?,?,?)',
                    [pkg_id, item['ProductID'], item['ProductName'],
                     item['Quantity'], item_status],
                )
            except Exception as e:
                conn_tx.rollback(); conn_tx.close()
                with _FULFILL_LOCK:
                    _FULFILL_STATE['phase'] = 'error'
                    _FULFILL_STATE['error'] = str(e)
                return

            _fulfill_sql_log(
                f"INSERT PackageItems: {item['ProductName']} ×{item['Quantity']}"
                f" [Status={item_status}]"
            )

            if item_ok:
                # Trigger trg_PackageItems_DecrStock fires automatically on INSERT
                # and decrements Products.UnitsInStock. CK_UnitsInStock enforces >= 0.
                _fulfill_sql_log(
                    f"  → TRIGGER trg_PackageItems_DecrStock: "
                    f"UnitsInStock -= {item['Quantity']} (ProductID={item['ProductID']})"
                )
                with _FULFILL_LOCK:
                    for pkg in _FULFILL_STATE['package_items']:
                        if pkg['ProductID'] == item['ProductID'] and pkg['status'] == 'queued':
                            pkg['status'] = 'packed'
                            break
                    _FULFILL_STATE['changes']['stock_decremented'].append(
                        (item['ProductID'], item['Quantity'])
                    )
                if _step(phase='packing',
                         phase_label=f'✓ Packed: {item["ProductName"]} ×{item["Quantity"]}'):
                    conn_tx.rollback(); conn_tx.close(); return
            else:
                short_items.append(item)
                short_pid_set.add(item['ProductID'])
                with _FULFILL_LOCK:
                    for pkg in _FULFILL_STATE['package_items']:
                        if pkg['ProductID'] == item['ProductID'] and pkg['status'] == 'queued':
                            pkg['status'] = 'awaiting_restock'
                            break
                _fulfill_sql_log(
                    f"  ↳ SHORT: {item['ProductName']} — Status=awaiting_restock, trigger skipped"
                )
                if _step(phase='packing',
                         phase_label=f'⚠ {item["ProductName"]}: short stock — deferred'):
                    conn_tx.rollback(); conn_tx.close(); return

        # Commit partial or full pack
        is_partial = len(short_items) > 0
        try:
            cur_tx.execute(
                "UPDATE Packages SET Status=? WHERE PackageID=?",
                ['partial' if is_partial else 'packing', pkg_id],
            )
            _fulfill_sql_log(
                f"COMMIT  -- Package #{pkg_id} "
                f"[{'partial' if is_partial else 'full'}]"
            )
            conn_tx.commit()
        except Exception as e:
            conn_tx.rollback(); conn_tx.close()
            with _FULFILL_LOCK:
                _FULFILL_STATE['phase'] = 'error'
                _FULFILL_STATE['error'] = str(e)
            return
        conn_tx.close()

        with _FULFILL_LOCK:
            _FULFILL_STATE['changes']['package_ids'].append(pkg_id)
            # stock_decremented already populated per-item in the packing loop above

        if is_partial:
            # Contact supplier(s) for each short item — no delivery yet
            for short_item in short_items:
                if _FULFILL_ABORTED: return

                # Open a fresh refill_order card for this short item
                with _FULFILL_LOCK:
                    _FULFILL_STATE['refill_order'] = {
                        'status':    'open',
                        'order_id':  order_id,
                        'OrderNeed': short_item['Quantity'],
                        'RestockQty': 100,
                    }

                if not _scan_subtable(conn_str, 'Products', 'ProductID',
                                      short_item['ProductID'], _FULFILL_PRODUCT_COLS,
                                      'product_card', refill_key='refill_order'):
                    return
                with _FULFILL_LOCK:
                    raw_sup = _FULFILL_STATE.get('product_card', {}).get('SupplierID')
                sup_id = int(raw_sup) if raw_sup is not None else None
                if sup_id is not None:
                    if not _scan_subtable(conn_str, 'Suppliers', 'SupplierID',
                                          sup_id, _FULFILL_SUPPLIER_COLS, 'supplier_card',
                                          refill_key='refill_order'):
                        return
                if _step(phase='contacting_supplier',
                         phase_label=f'Supplier contacted for "{short_item["ProductName"]}" — delivery pending'):
                    return

                # Collapse refill card into the order queue
                with _FULFILL_LOCK:
                    ro = _FULFILL_STATE.get('refill_order') or {}
                    ro['status'] = 'sent'
                    _FULFILL_STATE['refill_order'] = None
                    _FULFILL_STATE['order_queue'].append({
                        'order_id':       order_id,
                        'status':         'refill',
                        'type':           'refill',
                        'product_id':     short_item['ProductID'],
                        'product':        short_item['ProductName'],
                        'qty':            short_item['Quantity'],
                        'restock_qty':    ro.get('RestockQty', 100),
                        'supplier':       ro.get('CompanyName', ''),
                        'ticks_remaining': 3,
                    })

                # Persist refill order to DB
                _restock_qty = ro.get('RestockQty', 100)
                _supplier_id = sup_id
                _supplier    = ro.get('CompanyName', '')
                _fulfill_sql_log(
                    f"INSERT INTO RefillOrders(OrderID,ProductID,ProductName,"
                    f"NeededQty,RestockQty,SupplierID,Supplier) VALUES "
                    f"({order_id},{short_item['ProductID']},'{short_item['ProductName']}',"
                    f"{short_item['Quantity']},{_restock_qty},{_supplier_id},'{_supplier}')"
                )
                try:
                    conn_rf = pyodbc.connect(conn_str, autocommit=True, timeout=10)
                    conn_rf.execute(
                        "INSERT INTO RefillOrders"
                        "(OrderID,ProductID,ProductName,NeededQty,RestockQty,SupplierID,Supplier)"
                        " VALUES (?,?,?,?,?,?,?)",
                        [order_id, short_item['ProductID'], short_item['ProductName'],
                         short_item['Quantity'], _restock_qty, _supplier_id, _supplier],
                    )
                    conn_rf.close()
                except Exception:
                    pass

            # Snapshot package state and move on to next order
            with _FULFILL_LOCK:
                pkg_snap  = [dict(pi) for pi in _FULFILL_STATE['package_items']]
                meta_snap = dict(_FULFILL_STATE['package_meta'])

            pending_partials.append({
                'order_id':           order_id,
                'order_idx':          idx,
                'pkg_id':             pkg_id,
                'raw_items':          raw_items,
                'short_items':        short_items,
                'pkg_items_snapshot': pkg_snap,
                'package_meta':       meta_snap,
            })

            _queue_set(order_id, 'partial')
            with _FULFILL_LOCK:
                for q in _FULFILL_STATE['order_queue']:
                    if q['order_id'] == order_id and q.get('type') != 'refill':
                        q['details'] = {
                            'ship_to': ', '.join(filter(None, [
                                meta_snap.get('ShipName'), meta_snap.get('ShipCity'),
                                meta_snap.get('ShipCountry'),
                            ])),
                            'items': [{'name': pi['ProductName'], 'qty': pi['Quantity'],
                                       'status': pi['status']} for pi in pkg_snap],
                        }
                        break
            if _step(phase='partial_order',
                     phase_label=f'Partial order {order_id} saved — processing next order…'):
                return

        else:
            # Full pack — ship immediately
            _fulfill_sql_log(f'BEGIN TRAN  -- shipping order {order_id}')
            try:
                conn_s = pyodbc.connect(conn_str, autocommit=False, timeout=15)
                cur_s  = conn_s.cursor()
            except Exception as e:
                with _FULFILL_LOCK:
                    _FULFILL_STATE['phase'] = 'error'
                    _FULFILL_STATE['error'] = str(e)
                return

            if _step(phase='removing_details', phase_label='Removing from Order Details…'):
                conn_s.rollback(); conn_s.close(); return

            for item in raw_items:
                if _FULFILL_ABORTED:
                    conn_s.rollback(); conn_s.close(); return
                try:
                    cur_s.execute(
                        'DELETE FROM [Order Details] WHERE OrderID=? AND ProductID=?',
                        [order_id, item['ProductID']],
                    )
                except Exception as e:
                    conn_s.rollback(); conn_s.close()
                    with _FULFILL_LOCK:
                        _FULFILL_STATE['phase'] = 'error'
                        _FULFILL_STATE['error'] = str(e)
                    return
                _fulfill_sql_log(
                    f"DELETE [Order Details] OrderID={order_id} ProductID={item['ProductID']}"
                )
                with _FULFILL_LOCK:
                    _FULFILL_STATE['changes']['deleted_details'].append({
                        'OrderID': order_id, 'ProductID': item['ProductID'],
                        'UnitPrice': item['UnitPrice'], 'Quantity': item['Quantity'],
                        'Discount': item['Discount'],
                    })
                if _step(phase='removing_details',
                         phase_label=f'Deleted {item["ProductName"]} from Order Details'):
                    conn_s.rollback(); conn_s.close(); return

            try:
                cur_s.execute(
                    'UPDATE Orders SET ShippedDate=GETDATE() WHERE OrderID=?', [order_id]
                )
                cur_s.execute(
                    "UPDATE Packages SET Status='shipped' WHERE PackageID=?", [pkg_id]
                )
                _fulfill_sql_log(
                    f'UPDATE Orders ShippedDate=GETDATE() WHERE OrderID={order_id}'
                )
                _fulfill_sql_log('COMMIT')
                conn_s.commit()
            except Exception as e:
                conn_s.rollback(); conn_s.close()
                with _FULFILL_LOCK:
                    _FULFILL_STATE['phase'] = 'error'
                    _FULFILL_STATE['error'] = str(e)
                return
            conn_s.close()

            with _FULFILL_LOCK:
                _FULFILL_STATE['changes']['shipped_order_ids'].append(order_id)

            # P&L: revenue + COGS per line item, freight per order
            for item in raw_items:
                rev = round(item['UnitPrice'] * item['Quantity'] * (1 - item['Discount']), 2)
                # Fetch UnitCost from Products (may be None for legacy rows)
                try:
                    _cc = pyodbc.connect(conn_str, autocommit=True, timeout=5)
                    _cr = _cc.cursor()
                    _cr.execute('SELECT UnitCost FROM Products WHERE ProductID=?', [item['ProductID']])
                    _uc_row = _cr.fetchone()
                    _cc.close()
                    unit_cost = float(_uc_row[0]) if _uc_row and _uc_row[0] else item['UnitPrice'] * 0.6
                except Exception:
                    unit_cost = item['UnitPrice'] * 0.6
                cogs = round(unit_cost * item['Quantity'], 2)
                _ledger_insert(conn_str, 'revenue', rev,
                               f"Revenue: {item['ProductName']} ×{item['Quantity']}",
                               order_id=order_id, product_id=item['ProductID'])
                _ledger_insert(conn_str, 'cogs', -cogs,
                               f"COGS: {item['ProductName']} ×{item['Quantity']}",
                               order_id=order_id, product_id=item['ProductID'])
            freight = float(order.get('Freight') or 0)
            if freight:
                ship_to = ', '.join(filter(None, [order.get('ShipName'), order.get('ShipCity')]))
                _ledger_insert(conn_str, 'freight', -freight,
                               f'Freight: {ship_to}', order_id=order_id)

            _queue_set(order_id, 'shipped')
            with _FULFILL_LOCK:
                pkg_items_now = list(_FULFILL_STATE['package_items'])
                meta_now      = dict(_FULFILL_STATE['package_meta'])
                for q in _FULFILL_STATE['order_queue']:
                    if q['order_id'] == order_id and q.get('type') != 'refill':
                        q['details'] = {
                            'ship_to': ', '.join(filter(None, [
                                meta_now.get('ShipName'), meta_now.get('ShipCity'),
                                meta_now.get('ShipCountry'),
                            ])),
                            'items': [{'name': pi['ProductName'], 'qty': pi['Quantity'],
                                       'status': pi['status']} for pi in pkg_items_now],
                        }
                        break
            if _step(phase='shipped', phase_label=f'✓ Order {order_id} shipped!'):
                return

        # After every order: load the next one into the queue
        _load_next_order(conn_str)
        idx += 1

        # Delivery check runs after every order (tick-based: each order = 1 tick).
        # Refills queued this iteration start at ticks_remaining=3, so they won't
        # arrive until 3 orders later — the transit delay is enforced by the counter.
        if _check_deliveries(conn_str):
            return
        still_pending = []
        for pp in pending_partials:
            if _can_fulfill_partial(pp, conn_str):
                if _complete_and_ship_partial(pp, conn_str):
                    return
            else:
                still_pending.append(pp)
        pending_partials = still_pending

    # End of orders loop: one final delivery check + complete any remaining partials
    if _check_deliveries(conn_str):
        return
    for pp in pending_partials:
        if _complete_and_ship_partial(pp, conn_str):
            return

    with _FULFILL_LOCK:
        _FULFILL_STATE['phase']       = 'done'
        _FULFILL_STATE['phase_label'] = 'All orders processed'
