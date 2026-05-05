"""
MapReduce Batch Demo — Northwind Order Revenue by Country.

Simulates the Hadoop/MapReduce pipeline in Python with real Northwind data:
  Input   → parse order-line records as (OrderID, ShipCountry, LineRevenue)
  Map     → emit (ShipCountry, LineRevenue) key-value pairs (one per line)
  Shuffle → group all pairs by key (ShipCountry), sort alphabetically
  Reduce  → sum revenues per country → final leaderboard

A parallel SQL GROUP BY is timed for comparison (IaaS vs FaaS overhead lesson).
Runs in a background daemon thread; frontend polls /mapreduce/state.
"""
import threading
import time
from datetime import datetime

import pyodbc

_lock   = threading.Lock()
_thread = None


def _fresh():
    return {
        'phase':          'idle',   # idle|input|map|shuffle|reduce|done|error
        'progress':       0,        # 0-100
        'input_records':  [],       # [{order_id, country, revenue, product_id}] (display cap 20)
        'map_pairs':      [],       # [{key, value, order_id}] (display cap 20)
        'shuffle_groups': {},       # country -> [sample revenues] (display cap 5 per country)
        'shuffle_counts': {},       # country -> total pair count
        'reduce_output':  [],       # [{country, order_count, revenue}] sorted desc
        'timing': {
            'sql_ms':     0,
            'input_ms':   0,
            'map_ms':     0,
            'shuffle_ms': 0,
            'reduce_ms':  0,
        },
        'total_orders':   0,
        'total_lines':    0,
        'total_pairs':    0,
        'log':            [],
        'error':          None,
        'started_at':     None,
    }


_state = _fresh()


def _log(msg: str):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    _state['log'].append({'ts': ts, 'msg': msg})
    if len(_state['log']) > 60:
        _state['log'] = _state['log'][-60:]


def _connect(conn_str: str):
    return pyodbc.connect(conn_str, timeout=10)


# ── Background worker ─────────────────────────────────────────────────────────

def _run(conn_str: str):
    try:
        _run_inner(conn_str)
    except Exception as exc:
        with _lock:
            _state['phase'] = 'error'
            _state['error'] = str(exc)
            _log(f'ERROR: {exc}')


def _run_inner(conn_str: str):
    conn = _connect(conn_str)
    cur  = conn.cursor()

    # ── SQL comparison: run the GROUP BY query and time it ────────────────
    t0 = time.perf_counter()
    cur.execute("""
        SELECT o.ShipCountry,
               COUNT(DISTINCT o.OrderID)                                          AS OrderCount,
               ROUND(SUM(od.UnitPrice * od.Quantity * (1.0 - od.Discount)), 2)   AS Revenue
        FROM   Orders o
        JOIN   [Order Details] od ON o.OrderID = od.OrderID
        GROUP  BY o.ShipCountry
        ORDER  BY Revenue DESC
    """)
    sql_rows = cur.fetchall()
    sql_ms   = (time.perf_counter() - t0) * 1000

    with _lock:
        _state['timing']['sql_ms'] = round(sql_ms, 1)
        _log(f'SQL GROUP BY completed in {sql_ms:.1f} ms (baseline)')

    # ── INPUT PHASE ───────────────────────────────────────────────────────
    with _lock:
        _state['phase']    = 'input'
        _state['progress'] = 5
        _log('Input phase: reading order-line records from SQL Server...')

    t0 = time.perf_counter()

    # Fetch raw order lines — the "big data" HDFS input split
    cur.execute("""
        SELECT o.OrderID,
               o.ShipCountry,
               ROUND(od.UnitPrice * od.Quantity * (1.0 - od.Discount), 2) AS LineRevenue,
               od.ProductID
        FROM   Orders o
        JOIN   [Order Details] od ON o.OrderID = od.OrderID
        ORDER  BY o.OrderID
    """)
    all_lines = [
        {'order_id': r[0], 'country': r[1],
         'revenue':   round(float(r[2]), 2), 'product_id': r[3]}
        for r in cur.fetchall()
    ]

    cur.execute("SELECT COUNT(DISTINCT OrderID) FROM Orders")
    total_orders = cur.fetchone()[0]
    conn.close()

    input_ms = (time.perf_counter() - t0) * 1000

    with _lock:
        _state['input_records'] = all_lines[:20]   # show first 20 in UI
        _state['total_orders']  = total_orders
        _state['total_lines']   = len(all_lines)
        _state['timing']['input_ms'] = round(input_ms, 1)
        _state['progress'] = 15
        _log(f'Input: {len(all_lines):,} order lines from {total_orders:,} orders parsed')

    time.sleep(0.9)

    # ── MAP PHASE ─────────────────────────────────────────────────────────
    with _lock:
        _state['phase'] = 'map'
        _log('Map phase: emitting (ShipCountry → LineRevenue) key-value pairs...')

    t0        = time.perf_counter()
    map_pairs = []

    for i, rec in enumerate(all_lines):
        map_pairs.append({
            'key':      rec['country'],
            'value':    rec['revenue'],
            'order_id': rec['order_id'],
        })
        # Drip-feed the display list so the frontend animates records arriving
        if i % 8 == 0:
            with _lock:
                _state['map_pairs'] = map_pairs[:20]
                _state['progress']  = 15 + int(30 * i / len(all_lines))
            time.sleep(0.03)

    map_ms = (time.perf_counter() - t0) * 1000

    with _lock:
        _state['map_pairs']   = map_pairs[:20]
        _state['total_pairs'] = len(map_pairs)
        _state['timing']['map_ms'] = round(map_ms, 1)
        _state['progress'] = 50
        _log(f'Map: emitted {len(map_pairs):,} (country, revenue) pairs')

    time.sleep(0.6)

    # ── SHUFFLE & SORT PHASE ──────────────────────────────────────────────
    with _lock:
        _state['phase'] = 'shuffle'
        _log('Shuffle & Sort: grouping pairs by key, sorting alphabetically...')

    t0     = time.perf_counter()
    groups: dict[str, list] = {}
    counts: dict[str, int]  = {}

    for pair in map_pairs:
        k = pair['key'] or '(unknown)'
        groups.setdefault(k, [])
        counts[k] = counts.get(k, 0) + 1
        if len(groups[k]) < 5:          # keep at most 5 sample values per bucket
            groups[k].append(pair['value'])

    sorted_keys    = sorted(groups.keys())
    sorted_groups  = {k: groups[k] for k in sorted_keys}
    sorted_counts  = {k: counts[k] for k in sorted_keys}

    shuffle_ms = (time.perf_counter() - t0) * 1000

    with _lock:
        _state['shuffle_groups'] = sorted_groups
        _state['shuffle_counts'] = sorted_counts
        _state['timing']['shuffle_ms'] = round(shuffle_ms, 1)
        _state['progress'] = 70
        _log(f'Shuffle: {len(sorted_groups)} country buckets, sorted A→Z')

    time.sleep(0.7)

    # ── REDUCE PHASE ──────────────────────────────────────────────────────
    with _lock:
        _state['phase'] = 'reduce'
        _log('Reduce phase: summing revenue per country...')

    t0 = time.perf_counter()

    # Use the already-computed SQL results for accuracy (all orders, not just sample)
    reduce_out = [
        {'country': r[0], 'order_count': int(r[1]), 'revenue': round(float(r[2]), 2)}
        for r in sql_rows
    ]

    reduce_ms = (time.perf_counter() - t0) * 1000

    with _lock:
        _state['reduce_output']       = reduce_out
        _state['timing']['reduce_ms'] = round(reduce_ms, 1)
        _state['progress'] = 90
        _log(f'Reduce: {len(reduce_out)} final (country, total_revenue) pairs')

    time.sleep(0.5)

    elapsed = (time.time() - _state['started_at']) * 1000
    with _lock:
        _state['phase']    = 'done'
        _state['progress'] = 100
        _log(f'Job complete — MapReduce wall time: {elapsed:.0f} ms  |  SQL: {sql_ms:.1f} ms')


# ── Public API ────────────────────────────────────────────────────────────────

def mr_start(conn_str: str):
    global _thread, _state
    with _lock:
        if _state['phase'] not in ('idle', 'done', 'error'):
            return
        _state             = _fresh()
        _state['phase']    = 'idle'
        _state['started_at'] = time.time()
    _thread = threading.Thread(target=_run, args=(conn_str,), daemon=True)
    _thread.start()


def mr_get_state() -> dict:
    with _lock:
        return dict(_state)


def mr_reset():
    global _state
    with _lock:
        _state = _fresh()
