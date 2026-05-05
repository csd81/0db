"""
Cloud Functions Demo — HTTP + Background FaaS Simulation.

Simulates Google Cloud Functions invocation model:
  HTTP function    → synchronous request→response, billed per invocation
  Background func  → triggered by Pub/Sub message, runs asynchronously

Cold start / warm execution model:
  First call to a function instance: cold start delay (0.8–2.0 s simulated)
  Subsequent calls within 5 minutes: warm execution (<50 ms)
  Instance expires after 5 min idle → next call is cold again

Educational goals:
  • Stateless constraint: each invocation shares no memory with others
  • Cold start penalty: container spin-up cost on first invocation
  • IaaS vs PaaS vs FaaS: management overhead comparison
  • Billing model: pay-per-invocation vs pay-per-hour (IaaS)
"""
import random
import time
from datetime import datetime

# ── Function registry ─────────────────────────────────────────────────────────
# Each entry: label, description, execution_ms (warm), trigger_type
_FUNCTIONS = {
    'get_order': {
        'label':       'getOrder (HTTP)',
        'trigger':     'http',
        'warm_ms':     18,
        'description': 'Returns a Northwind order summary by ID. Read-only, idempotent.',
    },
    'calc_discount': {
        'label':       'calcDiscount (HTTP)',
        'trigger':     'http',
        'warm_ms':     12,
        'description': 'Computes loyalty discount tier for a customer. Stateless calculation.',
    },
    'update_inventory': {
        'label':       'updateInventory (Background)',
        'trigger':     'pubsub',
        'warm_ms':     35,
        'description': 'Triggered by order-placed Pub/Sub event. Decrements stock count.',
    },
    'send_notification': {
        'label':       'sendNotification (Background)',
        'trigger':     'pubsub',
        'warm_ms':     22,
        'description': 'Triggered by order-placed Pub/Sub event. Queues email via SendGrid.',
    },
    'generate_report': {
        'label':       'generateReport (HTTP)',
        'trigger':     'http',
        'warm_ms':     280,
        'description': 'Aggregates last 30 days of orders into a CSV report. CPU-bound.',
    },
}

COLD_START_MIN_MS = 800
COLD_START_MAX_MS = 2100
WARM_TTL_S        = 300   # 5 minutes warm window

# Instance state: tracks last invocation time per function to simulate warm/cold
_instances: dict[str, float] = {}   # fn_key → last_invoked unix timestamp

# Invocation log (last 50)
_invocations: list[dict] = []

MAX_LOG = 50


def _is_warm(fn_key: str) -> bool:
    last = _instances.get(fn_key)
    return last is not None and (time.time() - last) < WARM_TTL_S


def _touch(fn_key: str):
    _instances[fn_key] = time.time()


def _fmt_ts() -> str:
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


# ── Public API ────────────────────────────────────────────────────────────────

def cf_invoke(fn_key: str, payload: dict) -> dict:
    """Invoke a named function and return the invocation record."""
    fn = _FUNCTIONS.get(fn_key)
    if fn is None:
        return {'error': f'Unknown function: {fn_key}'}

    warm = _is_warm(fn_key)
    if warm:
        latency_ms = fn['warm_ms'] + random.randint(-5, 5)
        start_type = 'warm'
    else:
        cold_ms    = random.randint(COLD_START_MIN_MS, COLD_START_MAX_MS)
        latency_ms = cold_ms + fn['warm_ms']
        start_type = 'cold'

    # Simulate the latency (capped at 2.5 s so UI stays snappy)
    sleep_s = min(2.5, latency_ms / 1000)
    time.sleep(sleep_s)

    _touch(fn_key)

    # Generate a realistic-looking response based on function type
    if fn_key == 'get_order':
        order_id = payload.get('order_id', random.randint(10248, 11077))
        result   = {'order_id': order_id, 'status': 'shipped',
                    'total': round(random.uniform(50, 4000), 2)}
    elif fn_key == 'calc_discount':
        tier   = random.choice(['bronze', 'silver', 'gold', 'platinum'])
        result = {'tier': tier, 'discount_pct': {'bronze': 2, 'silver': 5,
                                                  'gold': 10, 'platinum': 15}[tier]}
    elif fn_key == 'update_inventory':
        product_id  = payload.get('product_id', random.randint(1, 77))
        units_delta = -payload.get('quantity', random.randint(1, 10))
        result = {'product_id': product_id, 'units_delta': units_delta,
                  'new_stock': max(0, random.randint(0, 200) + units_delta)}
    elif fn_key == 'send_notification':
        result = {'recipient': payload.get('email', 'customer@example.com'),
                  'message_id': f'msg_{random.randint(100000,999999)}',
                  'queued': True}
    elif fn_key == 'generate_report':
        rows = random.randint(820, 830)
        result = {'rows': rows, 'size_kb': round(rows * 0.18, 1),
                  'format': 'CSV', 'download_url': '/reports/latest.csv'}
    else:
        result = {'ok': True}

    record = {
        'id':         len(_invocations) + 1,
        'fn_key':     fn_key,
        'label':      fn['label'],
        'trigger':    fn['trigger'],
        'start_type': start_type,
        'latency_ms': round(latency_ms),
        'warm_ms':    fn['warm_ms'],
        'payload':    payload,
        'result':     result,
        'ts':         _fmt_ts(),
        'error':      None,
    }
    _invocations.append(record)
    if len(_invocations) > MAX_LOG:
        _invocations.pop(0)

    return record


def cf_get_state() -> dict:
    instances_info = {}
    now = time.time()
    for fn_key, fn in _FUNCTIONS.items():
        last = _instances.get(fn_key)
        if last is None:
            warm_pct = 0
            status   = 'cold (never invoked)'
        else:
            age_s    = now - last
            warm_pct = max(0, round(100 * (1 - age_s / WARM_TTL_S)))
            status   = f'warm ({int(age_s)}s ago)' if age_s < WARM_TTL_S else 'cold (expired)'
        instances_info[fn_key] = {
            'label':      fn['label'],
            'trigger':    fn['trigger'],
            'warm_ms':    fn['warm_ms'],
            'warm_pct':   warm_pct,
            'status':     status,
            'description': fn['description'],
        }
    return {
        'functions':   instances_info,
        'invocations': list(_invocations),
    }


def cf_reset():
    global _invocations
    _instances.clear()
    _invocations = []


def cf_get_functions() -> dict:
    return {k: v.copy() for k, v in _FUNCTIONS.items()}
