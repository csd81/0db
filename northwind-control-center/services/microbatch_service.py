"""
Micro-batch vs True Stream — Side-by-Side Comparison (Cpart_08).

Two pipelines fed by the same GPS ping source:

  TRUE STREAM  → each event is processed the instant it arrives
                 Latency ≈ 0 ms  |  Throughput = event-rate limited

  MICRO-BATCH  → events are buffered for W seconds, then flushed as a batch
                 Latency ≈ W/2 ms on average  |  Higher throughput per flush

This models Apache Spark Streaming (micro-batch) vs Apache Flink (true stream).
The tradeoff: micro-batch reuses batch infrastructure but adds inherent latency.
"""
import random
import threading
import time
from datetime import datetime
from collections import deque

_lock   = threading.Lock()
_stop   = threading.Event()
_thread = None

PING_HZ          = 3.0   # events per second (shared source)
WINDOW_SIZES_S   = (1, 5, 10)

_CITIES = [
    ('Paris', 'France'), ('London', 'UK'), ('Berlin', 'Germany'),
    ('Madrid', 'Spain'), ('Rome', 'Italy'), ('Vienna', 'Austria'),
    ('Warsaw', 'Poland'), ('Amsterdam', 'Netherlands'), ('Prague', 'Czech Rep.'),
    ('Budapest', 'Hungary'), ('Stockholm', 'Sweden'), ('Oslo', 'Norway'),
]


def _fresh():
    return {
        'phase':            'idle',   # idle|running|stopped
        'ping_count':       0,
        'stream_events':    [],   # last 20 — processed immediately
        'stream_latencies': [],   # [{n, latency_ms}] last 60
        'stream_avg_lat':   0.0,
        'batches':          [],   # completed micro-batches (last 10)
        'batch_buffer':     0,    # events currently buffered
        'batch_window_s':   1,    # current window size
        'batch_avg_lat':    0.0,
        'batch_latencies':  [],   # [{n, latency_ms}] last 60
        'log':              [],
        'started_at':       None,
    }


_state = _fresh()


def _log(msg: str):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    _state['log'].append({'ts': ts, 'msg': msg})
    if len(_state['log']) > 60:
        _state['log'] = _state['log'][-60:]


def _make_ping():
    city, country = random.choice(_CITIES)
    speed = max(10.0, min(160.0, random.gauss(88, 22)))
    return {
        'city':    city,
        'country': country,
        'speed':   round(speed, 1),
        'ts':      datetime.now().strftime('%H:%M:%S.%f')[:-3],
        'emit_t':  time.perf_counter(),
    }


def _run(window_s: int):
    window_buf   = []
    window_start = time.time()
    ping_idx     = 0

    with _lock:
        _state['phase']          = 'running'
        _state['batch_window_s'] = window_s
        _log(f'Stream started — true-stream + {window_s}s micro-batch windows')

    while not _stop.is_set():
        t0   = time.perf_counter()
        ping = _make_ping()
        ping_idx += 1
        now  = time.time()

        # ── TRUE STREAM: process immediately ──────────────────────────────
        proc_latency_ms = round((time.perf_counter() - ping['emit_t']) * 1000, 3)
        stream_event = {
            'n':          ping_idx,
            'city':       ping['city'],
            'country':    ping['country'],
            'speed':      ping['speed'],
            'ts':         ping['ts'],
            'latency_ms': proc_latency_ms,
        }

        # ── MICRO-BATCH: buffer until window expires ──────────────────────
        window_buf.append(ping)

        with _lock:
            _state['ping_count'] += 1
            _state['batch_buffer'] = len(window_buf)

            # Stream events
            _state['stream_events'].append(stream_event)
            _state['stream_events'] = _state['stream_events'][-20:]
            _state['stream_latencies'].append({'n': ping_idx, 'latency_ms': proc_latency_ms})
            _state['stream_latencies'] = _state['stream_latencies'][-60:]
            if _state['stream_latencies']:
                _state['stream_avg_lat'] = round(
                    sum(p['latency_ms'] for p in _state['stream_latencies'])
                    / len(_state['stream_latencies']), 3)

            # Flush micro-batch when window expires
            if now - window_start >= window_s and window_buf:
                flush_t   = time.perf_counter()
                n_events  = len(window_buf)
                # Batch latency = time from first event in window until flush
                oldest_emit = min(p['emit_t'] for p in window_buf)
                batch_lat   = round((flush_t - oldest_emit) * 1000, 1)

                avg_speed = round(sum(p['speed'] for p in window_buf) / n_events, 1)
                top_city  = max(
                    {p['city']: 0 for p in window_buf},
                    key=lambda c: sum(1 for p in window_buf if p['city'] == c)
                )
                batch_rec = {
                    'window_start': datetime.fromtimestamp(window_start).strftime('%H:%M:%S'),
                    'window_end':   datetime.fromtimestamp(now).strftime('%H:%M:%S'),
                    'events':       n_events,
                    'avg_speed':    avg_speed,
                    'top_city':     top_city,
                    'latency_ms':   batch_lat,
                }
                _state['batches'].append(batch_rec)
                _state['batches'] = _state['batches'][-10:]
                _state['batch_latencies'].append({'n': ping_idx, 'latency_ms': batch_lat})
                _state['batch_latencies'] = _state['batch_latencies'][-60:]
                if _state['batch_latencies']:
                    _state['batch_avg_lat'] = round(
                        sum(p['latency_ms'] for p in _state['batch_latencies'])
                        / len(_state['batch_latencies']), 1)

                _log(f'Batch flushed — {n_events} events, avg {avg_speed} km/h, lat {batch_lat} ms')
                window_buf   = []
                window_start = now

        elapsed = time.perf_counter() - t0
        time.sleep(max(0, 1.0 / PING_HZ - elapsed))

    with _lock:
        _state['phase'] = 'stopped'
        _log(f'Stopped — {ping_idx} pings, stream avg lat {_state["stream_avg_lat"]:.3f} ms')


# ── Public API ────────────────────────────────────────────────────────────────

def mb_start(window_s: int = 1):
    global _thread, _state
    with _lock:
        if _state['phase'] == 'running':
            return
        _state               = _fresh()
        _state['started_at'] = time.time()
    _stop.clear()
    _thread = threading.Thread(target=_run, args=(window_s,), daemon=True)
    _thread.start()


def mb_stop():
    _stop.set()


def mb_get_state() -> dict:
    with _lock:
        return dict(_state)


def mb_reset():
    global _state
    _stop.set()
    with _lock:
        _state = _fresh()
