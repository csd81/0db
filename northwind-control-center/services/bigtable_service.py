"""
Bigtable Wide-Column Store — In-Memory Simulation.

Implements the Bigtable data model (Epart_01–05):
  Row key       → unique identifier, often composite (city:timestamp_ms)
  Column family → logical grouping, defined at table creation
  Column        → cf:qualifier — cells within a family
  Cell version  → each cell stores up to MAX_VERSIONS timestamped values

Sparse storage: only cells that actually have values are stored.
A SQL table with 10 columns and 1 row stores 10 cells.
A Bigtable row with 100 possible columns but 3 populated stores 3 cells.

Operations exposed:
  insert_ping  → write a GPS ping as a new row (sensor:lat/lng/speed + meta:city/country)
  read_row     → fetch latest cell version for every populated column in a row
  get_versions → return all versions (timestamps) for one specific cell
  range_scan   → prefix scan on row key (e.g., all 'paris:*' rows)
  reset        → drop all rows
"""
import time
import threading
from datetime import datetime

_lock       = threading.Lock()
MAX_VERSIONS = 5
_table: dict = {}   # {row_key: {cf: {col: [{ts, value}]}}}
_ops_log: list = []


CF_SENSOR = 'sensor'
CF_META   = 'meta'
ALL_CFS   = (CF_SENSOR, CF_META)


def _ts_ms() -> int:
    return int(time.time() * 1000)


def _log(op: str, row_key: str, detail: str = ''):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    _ops_log.append({'ts': ts, 'op': op, 'row_key': row_key, 'detail': detail})
    if len(_ops_log) > 80:
        _ops_log.pop(0)


def _insert_cell(row_key: str, cf: str, col: str, value):
    """Low-level cell write — appends a versioned value."""
    if row_key not in _table:
        _table[row_key] = {}
    if cf not in _table[row_key]:
        _table[row_key][cf] = {}
    if col not in _table[row_key][cf]:
        _table[row_key][cf][col] = []

    _table[row_key][cf][col].append({'ts': _ts_ms(), 'value': value})
    _table[row_key][cf][col] = _table[row_key][cf][col][-MAX_VERSIONS:]


# ── Public API ────────────────────────────────────────────────────────────────

def bt_insert_ping(ping: dict) -> str:
    """Write one GPS ping as a new Bigtable row. Returns the generated row key."""
    city    = ping.get('city', 'unknown')
    ts_ms   = _ts_ms()
    row_key = f"{city.lower().replace(' ', '_')}:{ts_ms}"

    with _lock:
        _insert_cell(row_key, CF_SENSOR, 'lat',     round(float(ping.get('lat',   0)), 4))
        _insert_cell(row_key, CF_SENSOR, 'lng',     round(float(ping.get('lng',   0)), 4))
        _insert_cell(row_key, CF_SENSOR, 'speed',   round(float(ping.get('speed', 0)), 1))
        _insert_cell(row_key, CF_META,   'city',    ping.get('city',    ''))
        _insert_cell(row_key, CF_META,   'country', ping.get('country', ''))
        _log('INSERT', row_key, f"speed={ping.get('speed',0):.1f} km/h")

    return row_key


def bt_read_row(row_key: str) -> dict | None:
    """Return latest-version cells for all columns in a row."""
    with _lock:
        if row_key not in _table:
            _log('READ_ROW', row_key, 'NOT FOUND')
            return None
        row = _table[row_key]
        result = {}
        for cf, cols in row.items():
            for col, versions in cols.items():
                result[f'{cf}:{col}'] = {
                    'value':    versions[-1]['value'],
                    'ts':       versions[-1]['ts'],
                    'versions': len(versions),
                }
        _log('READ_ROW', row_key, f'{len(result)} cells')
        return {'row_key': row_key, 'cells': result}


def bt_get_versions(row_key: str, cf: str, col: str) -> list:
    """Return all stored versions for one cell."""
    with _lock:
        try:
            versions = _table[row_key][cf][col]
            _log('GET_VERSIONS', row_key, f'{cf}:{col} → {len(versions)} versions')
            return versions
        except KeyError:
            return []


def bt_range_scan(prefix: str) -> list:
    """
    Prefix scan: return all rows whose key starts with prefix.
    E.g. prefix='paris' → all rows for Paris (ordered by timestamp).
    """
    with _lock:
        rows = []
        for rk in sorted(k for k in _table if k.startswith(prefix)):
            cells = {}
            for cf, cols in _table[rk].items():
                for col, versions in cols.items():
                    cells[f'{cf}:{col}'] = versions[-1]['value']
            rows.append({'row_key': rk, 'cells': cells})
        _log('RANGE_SCAN', prefix + '*', f'{len(rows)} rows returned')
        return rows


def bt_get_state() -> dict:
    with _lock:
        rows_display = []
        for rk in sorted(list(_table.keys()))[-40:]:
            cells = {}
            for cf in ALL_CFS:
                if cf in _table[rk]:
                    for col, versions in _table[rk][cf].items():
                        cells[f'{cf}:{col}'] = {
                            'value':    versions[-1]['value'],
                            'n_ver':    len(versions),
                        }
            rows_display.append({'row_key': rk, 'cells': cells})

        total_cells = sum(
            len(cols)
            for row in _table.values()
            for cf, cols in row.items()
        )
        # Sparse saving: every row has 5 possible columns (sensor:lat/lng/speed, meta:city/country)
        max_possible = len(_table) * 5
        saved = max_possible - total_cells if max_possible > 0 else 0

        return {
            'rows':          rows_display,
            'total_rows':    len(_table),
            'total_cells':   total_cells,
            'sparse_saving': max(0, saved),
            'ops_log':       list(_ops_log[-30:]),
        }


def bt_reset():
    with _lock:
        _table.clear()
        _ops_log.clear()
