"""
VM Lifecycle Demo — Cold / Warm / Hot state machine.

Simulates Google Compute Engine VM provisioning transitions:
  stopped → cold → warm → hot  (and reverse: hot → warm → cold → stopped)

State definitions (from lecture "Bpart_05: Cold/Warm/Hot"):
  stopped  — VM deallocated; disk persists, IP released; cost: $0/hr
  cold     — VM allocated, OS booting; not accepting traffic; ~60 s spin-up
  warm     — VM running, app loaded but idle; accepting traffic; full IaaS rate
  hot      — VM under load, pre-scaled, minimum latency; same rate as warm

Educational goals:
  • IaaS billing: you pay for warm/hot even with 0 requests
  • FaaS contrast: Cloud Functions never have an always-on cost
  • State machine: transitions are not instant (boot, shutdown have latency)
  • Cost model displayed as $/hour at each state
"""
import threading
import time
from datetime import datetime

_lock = threading.Lock()

# Transition durations (simulated seconds → displayed with countdown)
TRANSITIONS = {
    ('stopped', 'cold'):  {'label': 'Allocating + Booting OS', 'duration_s': 8},
    ('cold',    'warm'):  {'label': 'Loading application',      'duration_s': 4},
    ('warm',    'hot'):   {'label': 'Scaling to hot standby',   'duration_s': 3},
    ('hot',     'warm'):  {'label': 'Scaling down',             'duration_s': 2},
    ('warm',    'cold'):  {'label': 'Suspending application',   'duration_s': 3},
    ('cold',    'stopped'): {'label': 'Deallocating VM',        'duration_s': 4},
}

COSTS = {
    'stopped': {'rate': 0.00,   'label': '$0.00/hr — deallocated'},
    'cold':    {'rate': 0.048,  'label': '$0.048/hr — booting'},
    'warm':    {'rate': 0.096,  'label': '$0.096/hr — idle but allocated'},
    'hot':     {'label': '$0.096/hr — under load (same rate as warm)',
                'rate': 0.096},
}

_STATE = {
    'current':    'stopped',
    'target':     None,
    'transition': None,   # {'label', 'duration_s', 'elapsed_s', 'pct'}
    'history':    [],     # [{from, to, ts, duration_ms}]
    'cost_accrued': 0.0,  # running total in $
    'uptime_s':   0,      # seconds since last start
    'started_at': None,
}

_cost_thread  = None
_trans_thread = None


def _fmt_ts() -> str:
    return datetime.now().strftime('%H:%M:%S')


def _accrue_cost():
    while True:
        time.sleep(1)
        with _lock:
            state = _STATE['current']
            rate  = COSTS.get(state, {}).get('rate', 0.0)
            _STATE['cost_accrued'] += rate / 3600   # per second
            if state != 'stopped':
                _STATE['uptime_s'] += 1


def _do_transition(from_state: str, to_state: str):
    key  = (from_state, to_state)
    meta = TRANSITIONS.get(key)
    if meta is None:
        return

    total = meta['duration_s']
    with _lock:
        _STATE['transition'] = {
            'from':       from_state,
            'to':         to_state,
            'label':      meta['label'],
            'duration_s': total,
            'elapsed_s':  0,
            'pct':        0,
        }

    t0 = time.time()
    while True:
        elapsed = time.time() - t0
        if elapsed >= total:
            break
        with _lock:
            _STATE['transition']['elapsed_s'] = round(elapsed, 1)
            _STATE['transition']['pct']       = min(99, int(100 * elapsed / total))
        time.sleep(0.25)

    with _lock:
        _STATE['current']    = to_state
        _STATE['target']     = None
        _STATE['transition'] = None
        _STATE['history'].append({
            'from':        from_state,
            'to':          to_state,
            'ts':          _fmt_ts(),
            'duration_ms': round((time.time() - t0) * 1000),
        })
        _STATE['history'] = _STATE['history'][-12:]


# ── Public API ────────────────────────────────────────────────────────────────

def vm_start_cost_ticker():
    global _cost_thread
    if _cost_thread is None or not _cost_thread.is_alive():
        _cost_thread = threading.Thread(target=_accrue_cost, daemon=True)
        _cost_thread.start()


def vm_transition(target: str) -> dict:
    """Request a state transition. Returns error if invalid or already in progress."""
    with _lock:
        current = _STATE['current']
        if _STATE['transition'] is not None:
            return {'error': 'Transition already in progress'}
        if current == target:
            return {'error': f'Already in state: {target}'}

    # Build valid transition path
    ORDER = ['stopped', 'cold', 'warm', 'hot']
    if target not in ORDER or current not in ORDER:
        return {'error': f'Invalid target state: {target}'}

    ci = ORDER.index(current)
    ti = ORDER.index(target)
    # Step one level at a time
    next_state = ORDER[ci + (1 if ti > ci else -1)]

    with _lock:
        _STATE['target'] = target

    global _trans_thread
    _trans_thread = threading.Thread(
        target=_do_transition, args=(current, next_state), daemon=True)
    _trans_thread.start()
    return {'ok': True, 'from': current, 'next': next_state}


def vm_get_state() -> dict:
    with _lock:
        s    = dict(_STATE)
        cost = COSTS.get(s['current'], {})
        s['cost_label']    = cost.get('label', '')
        s['cost_per_hour'] = cost.get('rate', 0.0)
        s['cost_accrued']  = round(s['cost_accrued'], 6)
        return s


def vm_reset():
    with _lock:
        _STATE['current']      = 'stopped'
        _STATE['target']       = None
        _STATE['transition']   = None
        _STATE['history']      = []
        _STATE['cost_accrued'] = 0.0
        _STATE['uptime_s']     = 0
        _STATE['started_at']   = None
