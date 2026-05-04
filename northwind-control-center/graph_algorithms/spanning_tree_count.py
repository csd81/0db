"""
Spanning Tree Count — Kirchhoff's Matrix-Tree Theorem (Fa-Mátrix Tétel).

The number of distinct spanning trees of a connected graph equals the
determinant of any cofactor of its Laplacian matrix L = D − A, where D
is the diagonal degree matrix.

Logistical interpretation: counts how many different "backbone" networks
could connect all cities using exactly V−1 roads.  A higher count means
greater structural redundancy — more alternative skeletons exist.

For a dense 200-node graph the count can exceed 10^300, so we use
numpy.linalg.slogdet() to return (sign, log|det|) and display the result
as "~10^X" when the exact integer would overflow float64.

Algorithm:
  1. Compute L = nx.laplacian_matrix(G) as a dense numpy array.
  2. Delete row 0 and column 0 (any cofactor gives the same answer).
  3. slogdet(L_reduced) → (sign, logdet).
  4. Exact count if 10^logdet10 < 15; scientific notation otherwise.

Complexity: O(V^3) for the determinant.
Graph: reduced 200-city subgraph (needs_reduced: True).
No destination needed (needs_dst: False).
"""
from __future__ import annotations

import math

import networkx as nx
import numpy as np

from graph_algorithms.common import StepEvent

_TOP_K_HIGHLIGHT = 8   # number of high-degree nodes to flash before result


def run(G: nx.Graph, src=None, dst=None, **_):
    """
    Yield StepEvents for the spanning tree count.

    Events:
      check_node    — top-degree cities (most influential in the Laplacian)
      found_analysis — scalar result + Kirchhoff explanation
    """
    n = G.number_of_nodes()
    e = G.number_of_edges()

    # Flash the highest-degree cities (they dominate the Laplacian diagonal)
    top_nodes = sorted(G.nodes(), key=lambda v: -G.degree(v))[:_TOP_K_HIGHLIGHT]
    for node in top_nodes:
        yield StepEvent(type='check_node', node=node,
                        flags={'degree': G.degree(node)})

    # Laplacian  L = D − A
    L = nx.laplacian_matrix(G).toarray().astype(np.float64)

    # Cofactor: delete row 0, col 0 (Kirchhoff's theorem — any cofactor works)
    L_reduced = L[1:, 1:]

    sign, logdet = np.linalg.slogdet(L_reduced)

    if sign <= 0:
        count_str    = '0 (graph is disconnected)'
        log10_count  = None
        euler_check  = None
    else:
        log10_count = logdet / math.log(10)
        if log10_count < 15:
            count_str   = f'{int(round(math.exp(logdet))):,}'
        else:
            count_str   = f'~10^{log10_count:.1f}'
        euler_check = f'V({n}) − E({e}) + F = 2  →  F = {e - n + 2}'

    yield StepEvent(
        type  = 'found_analysis',
        flags = {
            'verdict':      f'{count_str} spanning trees',
            'detail':       (
                f'Kirchhoff\'s Matrix-Tree Theorem: det(cofactor of L) = {count_str}. '
                f'L = D − A for the {n}-city graph. '
                f'Each spanning tree uses exactly {n - 1} roads and keeps all cities '
                f'connected. The {count_str} count measures the network\'s structural '
                f'redundancy — how many alternative "backbone" topologies exist.'
                + (f'  Euler polyhedron check: {euler_check}.' if euler_check else '')
            ),
            'spanning_tree_count': count_str,
            'log10_count':  round(log10_count, 2) if log10_count else None,
            'n_nodes':      n,
            'n_edges':      e,
            'laplacian_size': f'{n}×{n}',
        },
    )
