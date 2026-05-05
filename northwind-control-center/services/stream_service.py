"""
Data Stream Processing Demo — Live Logistics GPS Stream.

Simulates a Dataflow/Kafka stream of GPS pings from 200-city European logistics network:
  Source    → background thread emits ~2 Hz GPS pings (city, speed, timestamp)
  Buffer    → in-process ring buffer (bounded deque, 200 elements)
  Welford   → one-pass running mean/variance without storing all records
  Window    → 30-second tumbling windows → avg speed per country/region

Educational goals:
  • Unbounded vs bounded data (stream has no end, batch has fixed input)
  • Welford's algorithm: online mean/σ in O(1) space vs O(n) array
  • Tumbling window: aggregate over fixed time intervals without full replay
  • Low-latency streaming vs MapReduce batch throughput tradeoff
"""
import math
import random
import threading
import time
from collections import deque
from datetime import datetime

_lock   = threading.Lock()
_thread = None
_stop   = threading.Event()

# Representative 40-city European pool (lat/lng/country)
_CITIES = [
    ('Paris',        'France',      48.8566,  2.3522),
    ('Lyon',         'France',      45.7640,  4.8357),
    ('Marseille',    'France',      43.2965,  5.3698),
    ('London',       'UK',          51.5074, -0.1278),
    ('Manchester',   'UK',          53.4808, -2.2426),
    ('Birmingham',   'UK',          52.4862, -1.8904),
    ('Berlin',       'Germany',     52.5200, 13.4050),
    ('Munich',       'Germany',     48.1351, 11.5820),
    ('Hamburg',      'Germany',     53.5753,  9.9936),
    ('Frankfurt',    'Germany',     50.1109,  8.6821),
    ('Madrid',       'Spain',       40.4168, -3.7038),
    ('Barcelona',    'Spain',       41.3851,  2.1734),
    ('Valencia',     'Spain',       39.4699, -0.3763),
    ('Rome',         'Italy',       41.9028, 12.4964),
    ('Milan',        'Italy',       45.4654,  9.1859),
    ('Naples',       'Italy',       40.8518, 14.2681),
    ('Amsterdam',    'Netherlands', 52.3676,  4.9041),
    ('Rotterdam',    'Netherlands', 51.9244,  4.4777),
    ('Brussels',     'Belgium',     50.8503,  4.3517),
    ('Antwerp',      'Belgium',     51.2213,  4.4051),
    ('Vienna',       'Austria',     48.2082, 16.3738),
    ('Graz',         'Austria',     47.0707, 15.4395),
    ('Warsaw',       'Poland',      52.2297, 21.0122),
    ('Krakow',       'Poland',      50.0647, 19.9450),
    ('Prague',       'Czech Rep.',  50.0755, 14.4378),
    ('Brno',         'Czech Rep.',  49.1951, 16.6068),
    ('Budapest',     'Hungary',     47.4979, 19.0402),
    ('Bucharest',    'Romania',     44.4268, 26.1025),
    ('Sofia',        'Bulgaria',    42.6977, 23.3219),
    ('Athens',       'Greece',      37.9838, 23.7275),
    ('Stockholm',    'Sweden',      59.3293, 18.0686),
    ('Gothenburg',   'Sweden',      57.7089, 11.9746),
    ('Copenhagen',   'Denmark',     55.6761, 12.5683),
    ('Oslo',         'Norway',      59.9139, 10.7522),
    ('Helsinki',     'Finland',     60.1699, 24.9384),
    ('Zurich',       'Switzerland', 47.3769,  8.5417),
    ('Geneva',       'Switzerland', 46.2044,  6.1432),
    ('Lisbon',       'Portugal',    38.7223, -9.1393),
    ('Porto',        'Portugal',    41.1579, -8.6291),
    ('Dublin',       'Ireland',     53.3498, -6.2603),
]


WINDOW_SECONDS = 30   # tumbling window duration
RING_SIZE      = 200  # ring buffer capacity
PING_HZ        = 2.0  # target pings per second
SPEED_MEAN     = 88.0 # km/h base
SPEED_STD      = 22.0 # km/h standard deviation


def _fresh():
    return {
        'phase':       'idle',   # idle|streaming|stopped
        'ping_count':  0,
        'ring_buffer': [],       # [{city,country,lat,lng,speed,ts}] last 30 for UI
        'welford': {
            'n':        0,
            'mean':     0.0,
            'variance': 0.0,
            'std_dev':  0.0,
        },
        'speed_series': [],      # [{n, mean, std_dev}] last 120 points for chart
        'current_window': {
            'start_ts':     None,
            'end_ts':       None,
            'count':        0,
            'country_stats': {},  # country -> {count, sum_speed, avg_speed}
        },
        'completed_windows': [], # [{start_ts, end_ts, count, avg_speed, top_country}]
        'log':  [],
        'started_at': None,
    }


_state = _fresh()
_ring  = deque(maxlen=RING_SIZE)   # internal ring buffer, not exposed directly


def _log(msg: str):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    _state['log'].append({'ts': ts, 'msg': msg})
    if len(_state['log']) > 80:
        _state['log'] = _state['log'][-80:]


def _welford_update(wf: dict, x: float):
    """Welford's one-pass online mean/variance update — O(1) space."""
    wf['n']    += 1
    delta       = x - wf['mean']
    wf['mean'] += delta / wf['n']
    delta2      = x - wf['mean']
    wf['_M2']   = wf.get('_M2', 0.0) + delta * delta2
    if wf['n'] > 1:
        wf['variance'] = wf['_M2'] / wf['n']
        wf['std_dev']  = math.sqrt(wf['variance'])


def _open_window(now: float):
    _state['current_window'] = {
        'start_ts':      datetime.fromtimestamp(now).strftime('%H:%M:%S'),
        'end_ts':        datetime.fromtimestamp(now + WINDOW_SECONDS).strftime('%H:%M:%S'),
        'count':         0,
        'country_stats': {},
    }


def _close_window(now: float):
    w    = _state['current_window']
    cs   = w['country_stats']
    if not cs:
        return
    for c in cs.values():
        c['avg_speed'] = round(c['sum_speed'] / c['count'], 1)
    top = max(cs, key=lambda k: cs[k]['count'])
    summary = {
        'start_ts':   w['start_ts'],
        'end_ts':     w['end_ts'],
        'count':      w['count'],
        'avg_speed':  round(
            sum(c['sum_speed'] for c in cs.values())
            / max(1, sum(c['count'] for c in cs.values())), 1),
        'top_country': top,
        'n_countries': len(cs),
    }
    _state['completed_windows'].append(summary)
    _state['completed_windows'] = _state['completed_windows'][-10:]
    _log(
        f'Window closed — {summary["count"]} pings, '
        f'avg {summary["avg_speed"]} km/h, '
        f'top region: {top} ({cs[top]["count"]} pings)'
    )


# ── Background worker ─────────────────────────────────────────────────────────

def _run(conn_str: str):
    global _ring
    _ring = deque(maxlen=RING_SIZE)

    with _lock:
        _state['phase'] = 'streaming'
        _log(f'Stream started — {PING_HZ} Hz, {WINDOW_SECONDS}s tumbling windows, Welford σ tracking')

    window_start = time.time()
    _open_window(window_start)

    while not _stop.is_set():
        t0 = time.time()

        # ── Emit one GPS ping ──────────────────────────────────────────────
        city_data = random.choice(_CITIES)
        name, country, lat, lng = city_data
        # Speed: normally distributed, clipped to [10, 160]
        speed = max(10.0, min(160.0, random.gauss(SPEED_MEAN, SPEED_STD)))
        speed = round(speed, 1)
        ts_str = datetime.now().strftime('%H:%M:%S.%f')[:-3]

        ping = {
            'city':    name,
            'country': country,
            'lat':     lat,
            'lng':     lng,
            'speed':   speed,
            'ts':      ts_str,
        }
        _ring.append(ping)

        # ── Update Welford ─────────────────────────────────────────────────
        with _lock:
            _welford_update(_state['welford'], speed)
            n = _state['ping_count'] + 1
            _state['ping_count'] = n

            # Update ring buffer display (last 30)
            _state['ring_buffer'] = list(_ring)[-30:]

            # Emit a chart point every ping
            _state['speed_series'].append({
                'n':       n,
                'mean':    round(_state['welford']['mean'], 2),
                'std_dev': round(_state['welford']['std_dev'], 2),
            })
            _state['speed_series'] = _state['speed_series'][-120:]

            # ── Tumbling window bookkeeping ────────────────────────────────
            w  = _state['current_window']
            cs = w['country_stats']
            w['count'] += 1
            if country not in cs:
                cs[country] = {'count': 0, 'sum_speed': 0.0, 'avg_speed': 0.0}
            cs[country]['count']     += 1
            cs[country]['sum_speed'] += speed
            cs[country]['avg_speed']  = round(cs[country]['sum_speed'] / cs[country]['count'], 1)

            # Check window boundary
            now = time.time()
            if now - window_start >= WINDOW_SECONDS:
                _close_window(now)
                window_start = now
                _open_window(now)

        # Sleep to hit target Hz (account for processing time)
        elapsed = time.time() - t0
        sleep_t = max(0, (1.0 / PING_HZ) - elapsed)
        time.sleep(sleep_t)

    with _lock:
        _state['phase'] = 'stopped'
        _log(f'Stream stopped — {_state["ping_count"]:,} total pings, '
             f'{len(_state["completed_windows"])} windows completed')


# ── Public API ────────────────────────────────────────────────────────────────

def st_start(conn_str: str = ''):
    global _thread, _state
    with _lock:
        if _state['phase'] == 'streaming':
            return
        if _state['phase'] in ('idle', 'stopped'):
            _state = _fresh()
            _state['started_at'] = time.time()
    _stop.clear()
    _thread = threading.Thread(target=_run, args=(conn_str,), daemon=True)
    _thread.start()


def st_stop():
    _stop.set()


def st_get_state() -> dict:
    with _lock:
        return dict(_state)


def st_reset():
    global _state
    _stop.set()
    with _lock:
        _state = _fresh()
