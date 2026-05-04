"""
Walk Counting via Adjacency Matrix Power (4.8. Theorem).

The (i, j)-th entry of A^k gives the number of walks of exactly length k
from city i to city j, counting every route that may revisit vertices.

This is distinct from "paths" (no repetition): walks answer questions
like "how many 3-hop sequences exist between Paris and Berlin?" which
measures route redundancy rather than shortest routes.

Algorithm:
  1. Build the binary adjacency matrix A (200×200 for the reduced graph).
  2. Compute A^k with numpy (O(n^2.37… or naively O(n^3 log k))).
  3. Return A^k[src_idx][dst_idx].

Complexity: O(V^3 log k) via fast matrix exponentiation.
Graph: reduced 200-city subgraph (needs_reduced: True).
Requires src AND dst (needs_dst: True).
Extra param: k ∈ {1 … 6} (walk length).
"""
from __future__ import annotations

import networkx as nx
import numpy as np

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst: str, weight=None, k: int = 2, **_):
    """
    Yield StepEvents for walk counting.

    Events:
      check_node    — highlight src (blue) and dst (orange) before computing
      found_analysis — scalar result with explanation
    """
    # Highlight the query nodes so the viewer knows which pair is being counted
    yield StepEvent(type='check_node', node=src, flags={'role': 'source'})
    yield StepEvent(type='check_node', node=dst, flags={'role': 'dest'})

    nodes = list(G.nodes())
    n     = len(nodes)
    idx   = {name: i for i, name in enumerate(nodes)}

    # Binary adjacency matrix
    A = np.zeros((n, n), dtype=np.float64)
    for u, v in G.edges():
        i, j       = idx[u], idx[v]
        A[i][j] = A[j][i] = 1.0

    Ak = np.linalg.matrix_power(A, int(k))

    si = idx.get(src, -1)
    di = idx.get(dst, -1)
    raw_count = float(Ak[si][di]) if si >= 0 and di >= 0 else 0.0

    if raw_count >= 1e15:
        count_str = f'~{raw_count:.3e}'
    else:
        count_str = f'{int(round(raw_count)):,}'

    yield StepEvent(
        type  = 'found_analysis',
        flags = {
            'verdict': f'{count_str} walks of length {k}',
            'detail':  (
                f'A^{k}[{src}, {dst}] = {count_str}. '
                f'The (i,j) entry of the adjacency matrix raised to the {k}th power '
                f'counts every walk of exactly {k} steps from {src} to {dst}, '
                f'including routes that revisit cities. '
                f'Increase k to measure deeper route redundancy.'
            ),
            'walks':       count_str,
            'k':           k,
            'n_nodes':     n,
            'n_edges':     G.number_of_edges(),
            'matrix_size': f'{n}×{n}',
        },
    )
