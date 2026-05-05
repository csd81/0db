"""
Planarity Check — Boyer-Myrvold planarity testing via NetworkX.

Determines whether the graph can be drawn in a plane without edge crossings.
A graph is planar iff it contains no subgraph homeomorphic to K₅ or K₃,₃
(Kuratowski's theorem / Wagner's theorem).

Logistical applications (from the lecture notes):
  • Network design: planar networks can route cables/roads without crossings.
  • Circuit board layout: non-planar circuits require multiple wiring layers.
  • 4-Color theorem: every planar map is 4-colorable (χ ≤ 4).
  • Euler's formula: planar graph satisfies V − E + F = 2, so E ≤ 3V − 6.

Complexity: O(V + E).
Graph: reduced 200-city subgraph (needs_reduced: True).
No destination needed (needs_dst: False).
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src=None, dst=None, **_):
    """
    Yield StepEvents for planarity checking.

    Events:
      visit_node   — cities visited during DFS traversal simulation
      enqueue      — neighbours queued for visiting
      found_analysis — terminal; flags carry verdict/detail/is_planar
    """
    # Simulate the DFS traversal that underlies most planarity algorithms.
    visited: set[str] = set()
    start   = src if src and src in G.nodes else next(iter(G.nodes()), None)
    stack   = [start] if start else []

    steps_shown = 0
    while stack and steps_shown < 100:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        steps_shown += 1
        yield StepEvent(type='visit_node', node=u)

        for v in G.neighbors(u):
            if v not in visited:
                stack.append(v)
                yield StepEvent(type='enqueue', node=v, source=u)

    # ── Actual planarity test ────────────────────────────────────────────
    is_planar, _ = nx.check_planarity(G)

    n = G.number_of_nodes()
    m = G.number_of_edges()
    euler_bound = 3 * n - 6

    if m <= euler_bound:
        euler_note = f"Euler's formula: m={m} ≤ 3V−6={euler_bound} ✓. "
    else:
        euler_note = f"Euler's formula violated: m={m} > 3V−6={euler_bound}. "

    if is_planar:
        verdict = 'Planar graph ✓'
        detail  = (
            f'{n} cities, {m} connections. '
            f'{euler_note}'
            f'No subgraph homeomorphic to K₅ or K₃,₃ found (Kuratowski\'s theorem). '
            f'Can be drawn on a plane without edge crossings. '
            f'4-Color theorem guarantees χ(G) ≤ 4 for any planar map.'
        )
    else:
        verdict = 'Non-planar graph ✗'
        detail  = (
            f'{n} cities, {m} connections. '
            f'{euler_note}'
            f'Contains a subgraph homeomorphic to K₅ or K₃,₃ (Kuratowski\'s theorem). '
            f'Cannot be drawn on a plane without crossings. '
            f'Requires ≥ 2 routing layers for conflict-free cable layout.'
        )

    yield StepEvent(
        type  = 'found_analysis',
        flags = {
            'verdict':   verdict,
            'detail':    detail,
            'is_planar': is_planar,
        },
    )
