"""
Euler Circuit / Path check — degree parity analysis.

Euler's theorem (1736):
  • Euler Circuit exists  ⟺  every vertex has even degree
  • Euler Path exists     ⟺  exactly 0 or 2 vertices have odd degree

The animation highlights each odd-degree city in red so the viewer can
see which nodes "break" the one-stroke traversal.  The terminal event
carries the verdict and enough data for the result panel.

Complexity: O(V + E) — one degree scan.
Graph: reduced 200-city subgraph (needs_reduced: True).
No destination needed (needs_dst: False).
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src=None, dst=None, **_):
    """
    Yield StepEvents for the Euler check.

    Events:
      check_node    — an odd-degree city (red flash); flags carry 'degree'
      found_analysis — terminal; flags carry verdict, detail, counts
    """
    # Sort odd-degree nodes by degree descending so the most-connected
    # problem cities appear first in the animation.
    odd_nodes = sorted(
        [n for n in G.nodes() if G.degree(n) % 2 != 0],
        key=lambda n: -G.degree(n),
    )

    for node in odd_nodes:
        yield StepEvent(
            type  = 'check_node',
            node  = node,
            flags = {'degree': G.degree(node)},
        )

    n_odd = len(odd_nodes)
    n     = G.number_of_nodes()
    e     = G.number_of_edges()

    if n_odd == 0:
        verdict = 'Euler Circuit exists'
        detail  = (
            f'All {n} cities have even degree — the {n}-city network can be '
            'traversed in one stroke, returning to the starting point, without '
            'repeating any road. (Königsberg problem: solved!)'
        )
        has_circuit = True
        has_path    = True
    elif n_odd == 2:
        a, b    = odd_nodes[0], odd_nodes[1]
        verdict = 'Euler Path exists'
        detail  = (
            f'Exactly 2 odd-degree cities: {a} (deg {G.degree(a)}) and '
            f'{b} (deg {G.degree(b)}). Start at one, finish at the other — '
            'every road covered exactly once. No circuit back to start.'
        )
        has_circuit = False
        has_path    = True
    else:
        verdict = f'No Euler Path — {n_odd} odd-degree cities'
        detail  = (
            f'{n_odd} cities have odd degree (highlighted red). '
            f'Euler\'s theorem requires exactly 0 or 2 odd-degree vertices. '
            f'To fix: add or remove {n_odd // 2} edges to pair up the odd nodes.'
        )
        has_circuit = False
        has_path    = False

    yield StepEvent(
        type  = 'found_analysis',
        flags = {
            'verdict':     verdict,
            'detail':      detail,
            'has_circuit': has_circuit,
            'has_path':    has_path,
            'n_odd':       n_odd,
            'odd_nodes':   [f'{n} (deg {G.degree(n)})' for n in odd_nodes[:8]],
            'n_nodes':     n,
            'n_edges':     e,
        },
    )
