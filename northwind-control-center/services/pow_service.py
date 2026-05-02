"""
pow_service.py — Proof-of-Work consensus simulator.

Launches N threads ("nodes"), each racing to find SHA-256(payload+nonce)
starting with `difficulty` zero bits. The first winner's data is applied.

NOTE: module-level state (_consensus_state, _stores) is NOT shared across
Gunicorn workers. Run with a single process: python app.py or gunicorn --workers=1.
"""

import hashlib
import json
import threading
from datetime import datetime

_lock = threading.Lock()
_consensus_state: dict = {
    'active': False,
    'difficulty': 4,
    'payload': None,
    'nodes': {},
    'winner': None,
    'started_at': None,
    'finished_at': None,
}


def start_consensus_round(payload: dict, difficulty: int = 4, n_nodes: int = 3) -> dict:
    """Launch n_nodes mining threads and return initial state."""
    with _lock:
        _consensus_state.update({
            'active': True,
            'difficulty': difficulty,
            'payload': payload,
            'nodes': {i: {'status': 'mining', 'nonce': 0, 'hash': '', 'elapsed_ms': 0, 'winner': False}
                      for i in range(1, n_nodes + 1)},
            'winner': None,
            'started_at': datetime.utcnow().isoformat(),
            'finished_at': None,
        })

    payload_str = json.dumps(payload, sort_keys=True)
    prefix = '0' * difficulty

    for node_id in range(1, n_nodes + 1):
        t = threading.Thread(
            target=_mine_worker,
            args=(node_id, payload_str, prefix),
            daemon=True,
        )
        t.start()

    return get_consensus_state()


def _mine_worker(node_id: int, payload_str: str, prefix: str) -> None:
    nonce = 0
    started = datetime.utcnow()
    while True:
        with _lock:
            if _consensus_state['winner'] is not None:
                _consensus_state['nodes'][node_id]['status'] = 'lost'
                return

        candidate = payload_str + str(nonce)
        h = hashlib.sha256(candidate.encode()).hexdigest()
        elapsed = int((datetime.utcnow() - started).total_seconds() * 1000)

        with _lock:
            _consensus_state['nodes'][node_id]['nonce'] = nonce
            _consensus_state['nodes'][node_id]['hash'] = h[:16] + '…'
            _consensus_state['nodes'][node_id]['elapsed_ms'] = elapsed

        if h.startswith(prefix):
            with _lock:
                if _consensus_state['winner'] is None:
                    _consensus_state['winner'] = node_id
                    _consensus_state['active'] = False
                    _consensus_state['finished_at'] = datetime.utcnow().isoformat()
                    _consensus_state['nodes'][node_id]['status'] = 'won'
                    _consensus_state['nodes'][node_id]['hash'] = h
                    _consensus_state['nodes'][node_id]['winner'] = True
            return

        nonce += 1


def get_consensus_state() -> dict:
    with _lock:
        return json.loads(json.dumps(_consensus_state))


def reset_consensus() -> None:
    with _lock:
        _consensus_state.update({
            'active': False, 'difficulty': 4, 'payload': None,
            'nodes': {}, 'winner': None, 'started_at': None, 'finished_at': None,
        })


def validate_proof(payload_str: str, nonce: int, difficulty: int) -> bool:
    h = hashlib.sha256((payload_str + str(nonce)).hexdigest()).hexdigest()
    return h.startswith('0' * difficulty)
