"""
Cloud Pub/Sub Demo — Northwind Order Events.

Simulates Google Cloud Pub/Sub on real Northwind data:
  Publisher  → reads Orders from SQL Server, emits to topic "northwind-orders"
  Topic      → in-memory FIFO queue with per-subscription delivery
  Subscribers → 3 independent consumers at different processing speeds:
                • Inventory Service  — fast  (2 acks / tick)
                • Shipping Service   — medium (1 ack / tick)
                • Analytics Service  — slow   (1 ack / 3 ticks) → visible lag

Educational goals:
  • Decoupled architecture: publisher is unaware of subscribers
  • Fan-out: one publish → independent delivery to all 3 subscriptions
  • Async delivery: publisher does not block on subscriber acknowledgment
  • Backlog / lag: slow subscriber accumulates unacked messages
  • At-least-once: messages stay in delivery queue until acked
"""
import threading
import time
from datetime import datetime

import pyodbc

_lock   = threading.Lock()
_thread = None


def _fresh():
    return {
        'phase':    'idle',   # idle|connecting|publishing|delivering|done|error
        'progress': 0,
        'topic': {
            'name':      'northwind-orders',
            'published': 0,   # cumulative messages pushed to topic
            'backlog':   0,   # max unacked across all subscriptions
        },
        'publisher': {
            'published': 0,
            'recent':    [],   # [{id, customer, amount, country}] last 5
        },
        'subscribers': {
            'inventory': {
                'label': 'Inventory Service',
                'speed': 'fast',
                'color': '#2a9d8f',
                'acked': 0,
                'lag':   0,
                'recent': [],   # [{id, customer}] last 5
            },
            'shipping': {
                'label': 'Shipping Service',
                'speed': 'medium',
                'color': '#e9c46a',
                'acked': 0,
                'lag':   0,
                'recent': [],
            },
            'analytics': {
                'label': 'Analytics Service',
                'speed': 'slow',
                'color': '#e63946',
                'acked': 0,
                'lag':   0,
                'recent': [],
            },
        },
        'messages':   [],   # [{id, customer, amount, country, acked_by:[]}] last 25
        'total_orders': 0,
        'log':        [],
        'error':      None,
        'started_at': None,
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
    with _lock:
        _state['phase']    = 'connecting'
        _state['progress'] = 5
        _log('Connecting to Northwind — fetching orders...')

    conn = _connect(conn_str)
    cur  = conn.cursor()

    cur.execute("""
        SELECT o.OrderID,
               c.CompanyName,
               ROUND(SUM(od.UnitPrice * od.Quantity * (1.0 - od.Discount)), 2) AS OrderValue,
               o.ShipCountry
        FROM   Orders o
        JOIN   Customers c         ON o.CustomerID = c.CustomerID
        JOIN   [Order Details] od  ON o.OrderID   = od.OrderID
        GROUP  BY o.OrderID, c.CompanyName, o.ShipCountry
        ORDER  BY o.OrderID
    """)
    orders = [
        {'id': r[0], 'customer': r[1],
         'amount': round(float(r[2]), 2), 'country': r[3]}
        for r in cur.fetchall()
    ]
    conn.close()

    total = len(orders)
    with _lock:
        _state['total_orders'] = total
        _state['phase']        = 'publishing'
        _state['progress']     = 10
        _log(f'Fetched {total:,} orders — starting Pub/Sub fan-out...')

    # Per-subscription delivery queues (simulating independent push subscriptions)
    inv_q  = []
    ship_q = []
    ana_q  = []

    TICK        = 0.11    # seconds per simulation tick
    PUB_PER_TICK = 2      # messages published each tick
    ana_counter  = 0      # throttle counter for slow subscriber

    pub_idx = 0

    while pub_idx < total or inv_q or ship_q or ana_q:
        published_this_tick = []

        # ── PUBLISH: push PUB_PER_TICK new messages to all queues ───────────
        for _ in range(PUB_PER_TICK):
            if pub_idx >= total:
                break
            msg = orders[pub_idx]
            pub_idx += 1
            inv_q.append(msg)
            ship_q.append(msg)
            ana_q.append(msg)
            published_this_tick.append(msg)

        # ── DELIVER: each subscriber acks at its own speed ───────────────────
        inv_acked  = [inv_q.pop(0)  for _ in range(min(2, len(inv_q)))]
        ship_acked = [ship_q.pop(0) for _ in range(min(1, len(ship_q)))]

        ana_counter += 1
        if ana_counter >= 3 and ana_q:
            ana_acked    = [ana_q.pop(0)]
            ana_counter  = 0
        else:
            ana_acked = []

        # ── UPDATE STATE (under lock) ────────────────────────────────────────
        with _lock:
            _state['publisher']['published']  = pub_idx
            _state['topic']['published']      = pub_idx
            _state['topic']['backlog']        = max(len(inv_q), len(ship_q), len(ana_q))

            # Append new published messages to the feed
            for msg in published_this_tick:
                _state['messages'].append({
                    'id':       msg['id'],
                    'customer': msg['customer'],
                    'amount':   msg['amount'],
                    'country':  msg['country'],
                    'acked_by': [],
                })
            _state['messages'] = _state['messages'][-25:]
            _state['publisher']['recent'] = [
                {'id': m['id'], 'customer': m['customer'],
                 'amount': m['amount'], 'country': m['country']}
                for m in _state['messages'][-5:]
            ]

            def _apply_acks(acked_list, key):
                sub = _state['subscribers'][key]
                for msg in acked_list:
                    sub['acked'] += 1
                    sub['recent'].append({'id': msg['id'], 'customer': msg['customer']})
                    sub['recent'] = sub['recent'][-5:]
                    for m in _state['messages']:
                        if m['id'] == msg['id'] and key not in m['acked_by']:
                            m['acked_by'].append(key)

            _apply_acks(inv_acked,  'inventory')
            _apply_acks(ship_acked, 'shipping')
            _apply_acks(ana_acked,  'analytics')

            _state['subscribers']['inventory']['lag'] = len(inv_q)
            _state['subscribers']['shipping']['lag']  = len(ship_q)
            _state['subscribers']['analytics']['lag'] = len(ana_q)

            if total > 0:
                _state['progress'] = min(95, int(10 + 85 * pub_idx / total))

            if pub_idx == total and _state['phase'] == 'publishing':
                _state['phase'] = 'delivering'
                _log(f'All {total:,} messages published — draining subscriber backlogs...')

        time.sleep(TICK)

    elapsed = (time.time() - _state['started_at']) * 1000
    with _lock:
        _state['phase']    = 'done'
        _state['progress'] = 100
        _log(
            f'Done — {total:,} orders delivered to all 3 subscribers. '
            f'Wall time: {elapsed:.0f} ms'
        )


# ── Public API ────────────────────────────────────────────────────────────────

def ps_start(conn_str: str):
    global _thread, _state
    with _lock:
        if _state['phase'] not in ('idle', 'done', 'error'):
            return
        _state               = _fresh()
        _state['started_at'] = time.time()
    _thread = threading.Thread(target=_run, args=(conn_str,), daemon=True)
    _thread.start()


def ps_get_state() -> dict:
    with _lock:
        return dict(_state)


def ps_reset():
    global _state
    with _lock:
        _state = _fresh()
