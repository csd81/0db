"""
Monte Carlo π — Embarrassingly Parallel Estimation.

N worker threads (mappers) each throw random darts at a unit square.
Points inside the inscribed quarter-circle (x²+y²≤1) count as hits.
π ≈ 4 × (hits / total).  As N→∞ the estimate converges.

Educational goals:
  • Embarrassingly parallel: zero inter-worker communication required
  • Why Hadoop/Spark: partition input space, map locally, reduce globally
  • Law of Large Numbers: convergence ∝ 1/√N (needs more darts, not smarter ones)
  • Each worker = one Spark executor / Hadoop mapper

Workers publish individual sub-estimates that are visible in real time —
showing how the global average stabilises while local estimates still vary.
"""
import math
import random
import threading
import time
from datetime import datetime

_lock   = threading.Lock()
_stop   = threading.Event()
_thread = None
PI      = math.pi


def _fresh():
    return {
        'phase':        'idle',   # idle|running|stopped
        'total_points': 0,
        'hits':         0,
        'pi_estimate':  0.0,
        'pi_error':     None,
        'n_workers':    4,
        'workers':      [],       # [{id, points, hits, pi_local}]
        'samples':      [],       # [{x, y, inside}] last 800 for canvas
        'convergence':  [],       # [{n, pi}] for line chart
        'log':          [],
        'started_at':   None,
    }


_state = _fresh()


def _log(msg: str):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    _state['log'].append({'ts': ts, 'msg': msg})
    if len(_state['log']) > 60:
        _state['log'] = _state['log'][-60:]


def _worker(worker_id: int):
    local_pts  = 0
    local_hits = 0

    while not _stop.is_set():
        batch = []
        for _ in range(20):
            x      = random.uniform(-1.0, 1.0)
            y      = random.uniform(-1.0, 1.0)
            inside = (x * x + y * y) <= 1.0
            batch.append({'x': round(x, 4), 'y': round(y, 4), 'inside': inside})
            local_pts += 1
            if inside:
                local_hits += 1

        with _lock:
            _state['total_points'] += len(batch)
            _state['hits']         += sum(1 for b in batch if b['inside'])
            _state['samples']       = (_state['samples'] + batch)[-800:]

            w = _state['workers'][worker_id]
            w['points']   = local_pts
            w['hits']     = local_hits
            w['pi_local'] = round(4.0 * local_hits / local_pts, 6) if local_pts else 0.0

            n = _state['total_points']
            h = _state['hits']
            if n > 0:
                pi_est              = 4.0 * h / n
                _state['pi_estimate'] = round(pi_est, 8)
                _state['pi_error']    = round(abs(pi_est - PI), 8)
                if n % 500 < 20:
                    _state['convergence'].append({'n': n, 'pi': round(pi_est, 6)})
                    _state['convergence'] = _state['convergence'][-300:]

        time.sleep(0.012)


def _run(n_workers: int):
    threads = []
    with _lock:
        _state['workers'] = [
            {'id': i, 'points': 0, 'hits': 0, 'pi_local': 0.0}
            for i in range(n_workers)
        ]

    for i in range(n_workers):
        t = threading.Thread(target=_worker, args=(i,), daemon=True)
        t.start()
        threads.append(t)

    with _lock:
        _state['phase'] = 'running'
        _log(f'Launched {n_workers} mapper thread{"s" if n_workers > 1 else ""} — darts incoming…')

    for t in threads:
        t.join()

    with _lock:
        n = _state['total_points']
        h = _state['hits']
        _state['phase'] = 'stopped'
        if n > 0:
            _log(f'Stopped — {n:,} darts, π ≈ {4.0*h/n:.8f}, error {abs(4.0*h/n - PI):.2e}')


# ── Public API ────────────────────────────────────────────────────────────────

def mc_start(n_workers: int = 4):
    global _thread, _state
    with _lock:
        if _state['phase'] == 'running':
            return
        _state               = _fresh()
        _state['n_workers']  = n_workers
        _state['started_at'] = time.time()
    _stop.clear()
    _thread = threading.Thread(target=_run, args=(n_workers,), daemon=True)
    _thread.start()


def mc_stop():
    _stop.set()


def mc_get_state() -> dict:
    with _lock:
        return dict(_state)


def mc_reset():
    global _state
    _stop.set()
    with _lock:
        _state = _fresh()
