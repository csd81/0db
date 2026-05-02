"""
rqlite_service.py — HTTP client for a rqlite Raft-consensus SQLite cluster.

rqlite speaks plain JSON over HTTP — no driver needed.
Reads:  GET  /db/query?q=<SQL>&level=weak
Writes: POST /db/execute  body: ["SQL", ...]
Status: GET  /status
Nodes:  GET  /nodes
"""

import time
import requests
import meta_db


class RqliteClient:
    def __init__(self, url: str, timeout: int = 10):
        self.url = url.rstrip('/')
        self.timeout = timeout

    # ── Internals ──────────────────────────────────────────────────────────────

    def _query(self, sql: str, level: str = 'weak') -> dict:
        r = requests.get(
            f'{self.url}/db/query',
            params={'q': sql, 'level': level},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def _execute(self, statements: list[str]) -> dict:
        r = requests.post(
            f'{self.url}/db/execute',
            json=statements,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    # ── Public API ─────────────────────────────────────────────────────────────

    def query(self, sql: str) -> tuple[list, list, float | None, str | None]:
        """Execute a SELECT. Returns (columns, rows, time_s, error)."""
        try:
            data = self._query(sql)
            results = data.get('results', [{}])
            first = results[0] if results else {}
            if 'error' in first:
                return [], [], None, first['error']
            columns = first.get('columns', [])
            values  = first.get('values', []) or []
            rows    = [list(v) for v in values]
            return columns, rows, data.get('time'), None
        except Exception as e:
            return [], [], None, str(e)

    def execute(self, sql: str) -> tuple[int, int | None, float | None, str | None]:
        """Execute a write statement. Returns (rows_affected, last_insert_id, time_s, error)."""
        try:
            data = self._execute([sql])
            results = data.get('results', [{}])
            first = results[0] if results else {}
            if 'error' in first:
                return 0, None, None, first['error']
            return (
                first.get('rows_affected', 0),
                first.get('last_insert_id'),
                data.get('time'),
                None,
            )
        except Exception as e:
            return 0, None, None, str(e)

    def status(self) -> tuple[dict, str | None]:
        try:
            r = requests.get(f'{self.url}/status', timeout=self.timeout)
            r.raise_for_status()
            return r.json(), None
        except Exception as e:
            return {}, str(e)

    def nodes(self) -> tuple[list, str | None]:
        try:
            r = requests.get(f'{self.url}/nodes', timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            # v8 returns a dict keyed by node-id
            if isinstance(data, dict):
                node_list = [
                    {'id': k, **v} for k, v in data.items()
                ]
            else:
                node_list = data
            return node_list, None
        except Exception as e:
            return [], str(e)

    def tables(self) -> tuple[list, str | None]:
        cols, rows, _, err = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        if err:
            return [], err
        return [r[0] for r in rows], None


# ── Connection-aware helpers ──────────────────────────────────────────────────

def _client(conn_id: int) -> RqliteClient:
    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found")
    url = rec['conn_params'].get('url', 'http://127.0.0.1:4001')
    return RqliteClient(url)


def get_cluster_info(conn_id: int) -> dict:
    client = _client(conn_id)
    status, s_err = client.status()
    nodes, n_err  = client.nodes()
    tables, t_err = client.tables()

    store  = status.get('store', {})
    raft   = store.get('raft', {})
    leader = raft.get('leader', {})

    return {
        'node_id':     store.get('node_id', '?'),
        'leader_id':   leader.get('node_id', '?') if isinstance(leader, dict) else str(leader),
        'leader_addr': leader.get('addr', '?')    if isinstance(leader, dict) else '?',
        'state':       raft.get('state', '?'),
        'commit_index': raft.get('commit_index', '?'),
        'applied_index': raft.get('applied_index', '?'),
        'nodes':       nodes,
        'tables':      tables,
        'status_error': s_err,
        'nodes_error':  n_err,
        'tables_error': t_err,
    }


def run_query(conn_id: int, sql: str) -> tuple[list, list, int, str | None]:
    """Thin wrapper for Query Studio: returns (columns, rows, elapsed_ms, error)."""
    client = _client(conn_id)
    sql = sql.strip()
    start = time.perf_counter()

    first_word = sql.split()[0].upper() if sql.split() else ''
    if first_word in ('SELECT', 'WITH', 'PRAGMA'):
        cols, rows, _, err = client.query(sql)
    else:
        ra, _, _, err = client.execute(sql)
        cols  = ['rows_affected']
        rows  = [[ra]] if not err else []

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    return cols, rows, elapsed_ms, err
