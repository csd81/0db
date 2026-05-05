"""
Kafka Consumer Groups — Persistent Log vs Ephemeral Queue (Cpart_07).

Simulates Apache Kafka's append-only log model:
  Topic        → ordered, immutable log of messages (never deleted on ack)
  Partition    → single partition for simplicity
  Consumer group → independent cursor (offset) into the log
                   Each group reads from its own position
  Offset        → position of the next message to read

Contrast with Pub/Sub (C3 demo):
  Pub/Sub  → message deleted after all subscribers ack (ephemeral)
  Kafka    → message retained on disk; any new consumer can replay from offset 0
             (log compaction / retention by time or size — not ack)

Three consumer groups at different speeds show independent lag without
affecting each other — the core operational advantage of the log model.
"""
import random
import threading
import time
from datetime import datetime

import pyodbc

_lock   = threading.Lock()
_stop   = threading.Event()
_thread = None

# The Kafka topic log (append-only list of messages)
_log: list = []

CONSUMER_GROUPS = {
    'analytics': {'label': 'Analytics Job',   'speed': 'fast',   'lag_every': 1},
    'search':    {'label': 'Search Indexer',  'speed': 'medium', 'lag_every': 2},
    'archive':   {'label': 'Cold Archiver',   'speed': 'slow',   'lag_every': 4},
}

_offsets: dict = {k: 0 for k in CONSUMER_GROUPS}
_consumed: dict = {k: 0 for k in CONSUMER_GROUPS}


def _fresh_state():
    return {
        'phase':         'idle',
        'log_size':      0,
        'log_preview':   [],  # last 20 messages
        'offsets':       {k: 0 for k in CONSUMER_GROUPS},
        'consumed':      {k: 0 for k in CONSUMER_GROUPS},
        'lag':           {k: 0 for k in CONSUMER_GROUPS},
        'groups':        CONSUMER_GROUPS,
        'total_produced':0,
        'ops_log':       [],
        'started_at':    None,
    }


_state = _fresh_state()


def _ops_log(msg: str):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    _state['ops_log'].append({'ts': ts, 'msg': msg})
    if len(_state['ops_log']) > 60:
        _state['ops_log'] = _state['ops_log'][-60:]


def _fetch_orders(conn_str: str) -> list:
    if not conn_str:
        # Fallback: generate synthetic messages
        return [
            {'order_id': 10248 + i,
             'customer': f'Customer_{i}',
             'country': random.choice(['Germany','France','UK','Spain']),
             'amount': round(random.uniform(50, 2000), 2)}
            for i in range(60)
        ]
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        cur  = conn.cursor()
        cur.execute("""
            SELECT TOP 60 o.OrderID, c.CompanyName, o.ShipCountry,
                   ROUND(SUM(od.UnitPrice*od.Quantity*(1-od.Discount)),2) AS Total
            FROM Orders o
            JOIN Customers c ON o.CustomerID=c.CustomerID
            JOIN [Order Details] od ON o.OrderID=od.OrderID
            GROUP BY o.OrderID, c.CompanyName, o.ShipCountry
            ORDER BY o.OrderID
        """)
        rows = [{'order_id': r[0], 'customer': r[1],
                 'country': r[2], 'amount': round(float(r[3]),2)}
                for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception:
        return []


def _run(conn_str: str):
    global _log, _offsets, _consumed

    with _lock:
        _state['phase'] = 'producing'
        _ops_log('Fetching Northwind orders to produce as Kafka messages…')

    orders = _fetch_orders(conn_str)
    if not orders:
        with _lock:
            _state['phase'] = 'error'
        return

    # Reset log and offsets
    with _lock:
        _log     = []
        _offsets = {k: 0 for k in CONSUMER_GROUPS}
        _consumed = {k: 0 for k in CONSUMER_GROUPS}

    PRODUCE_DELAY = 0.18  # seconds between produces

    for i, order in enumerate(orders):
        if _stop.is_set():
            break

        # ── PRODUCE: append to log ────────────────────────────────────────
        msg = {
            'offset':    i,
            'key':       str(order['order_id']),
            'value':     order,
            'ts':        datetime.now().strftime('%H:%M:%S.%f')[:-3],
        }
        with _lock:
            _log.append(msg)
            _state['log_size']      = len(_log)
            _state['total_produced'] = len(_log)
            _state['log_preview']   = _log[-20:]

        # ── CONSUME: each group advances its offset at its own speed ──────
        with _lock:
            for gid, meta in CONSUMER_GROUPS.items():
                lag_every = meta['lag_every']
                if i % lag_every == 0 and _offsets[gid] < len(_log):
                    _offsets[gid]  += 1
                    _consumed[gid] += 1

                _state['offsets'][gid]  = _offsets[gid]
                _state['consumed'][gid] = _consumed[gid]
                _state['lag'][gid]      = len(_log) - _offsets[gid]

            if i == 0:
                _ops_log('First message at offset 0. Consumer groups start reading.')
            if i % 10 == 9:
                _ops_log(f'Log at offset {i+1}. '
                         f'Lags: analytics={_state["lag"]["analytics"]} '
                         f'search={_state["lag"]["search"]} '
                         f'archive={_state["lag"]["archive"]}')

        time.sleep(PRODUCE_DELAY)

    # Drain remaining — let slow consumers catch up
    for _ in range(30):
        if _stop.is_set():
            break
        with _lock:
            all_caught = all(_offsets[g] >= len(_log) for g in CONSUMER_GROUPS)
            if all_caught:
                break
            for gid in CONSUMER_GROUPS:
                if _offsets[gid] < len(_log):
                    _offsets[gid]  += 1
                    _consumed[gid] += 1
                _state['offsets'][gid]  = _offsets[gid]
                _state['consumed'][gid] = _consumed[gid]
                _state['lag'][gid]      = max(0, len(_log) - _offsets[gid])
        time.sleep(0.25)

    with _lock:
        _state['phase'] = 'done'
        _ops_log(f'All {len(_log)} messages produced. Log persists — replay any group from offset 0.')


# ── Public API ────────────────────────────────────────────────────────────────

def kafka_start(conn_str: str = ''):
    global _thread, _state
    with _lock:
        if _state['phase'] in ('producing', 'done'):
            return
        _state               = _fresh_state()
        _state['started_at'] = time.time()
    _stop.clear()
    _thread = threading.Thread(target=_run, args=(conn_str,), daemon=True)
    _thread.start()


def kafka_get_state() -> dict:
    with _lock:
        return dict(_state)


def kafka_reset():
    global _state, _log, _offsets, _consumed
    _stop.set()
    with _lock:
        _log      = []
        _offsets  = {k: 0 for k in CONSUMER_GROUPS}
        _consumed = {k: 0 for k in CONSUMER_GROUPS}
        _state    = _fresh_state()
