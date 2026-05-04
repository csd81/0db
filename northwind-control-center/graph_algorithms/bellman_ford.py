"""
Bellman-Ford — optimal shortest path on graphs that may contain negative-weight edges.

Unlike Dijkstra, does not greedily "settle" nodes. Instead, sweeps ALL edges
V−1 times so that a cheaper path discovered via a later relaxation (e.g., a
subsidised "green energy corridor" with CostAdjustment < 0) is never missed.

After the V−1 passes a final sweep checks for negative cycles — edges that
reduce total cost no matter how many times they are traversed.  If found, no
shortest path exists and the error event is emitted so the UI shows a banner.

Complexity: O(V·E).  Restricted to the reduced 200-city graph.
Visual signature: repeated sweeps through all edges — very different from
Dijkstra's expanding circle.  Negative-weight relaxations emit 'negative_relax'
so the frontend flashes them red.
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst: str, weight: str = 'bellman_weight', **_):
    """
    Yield StepEvents for Bellman-Ford traversal.

    Events:
      relax_edge      — cost improved via a positive-weight hop
      negative_relax  — cost improved via a negative-weight hop (red flash)
      found_path      — path successfully reconstructed
      no_path         — destination unreachable
      error           — negative cycle detected; no solution possible
    """
    nodes = list(G.nodes())
    edges = list(G.edges(data=True))
    INF   = float('inf')

    dist: dict[str, float]      = {n: INF for n in nodes}
    prev: dict[str, str | None] = {}
    dist[src] = 0.0

    for _ in range(len(nodes) - 1):
        changed = False

        for u, v, data in edges:
            w = data.get(weight, data.get('weight', 1.0))

            # Relax u → v
            if dist[u] < INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                changed  = True
                yield StepEvent(
                    type   = 'negative_relax' if w < 0 else 'relax_edge',
                    source = u, target = v,
                    cost   = round(dist[v], 1),
                    flags  = {'negative': w < 0},
                )

            # Relax v → u (undirected graph — same weight both ways)
            if dist[v] < INF and dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                prev[u] = v
                changed  = True
                yield StepEvent(
                    type   = 'negative_relax' if w < 0 else 'relax_edge',
                    source = v, target = u,
                    cost   = round(dist[u], 1),
                    flags  = {'negative': w < 0},
                )

        if not changed:
            break   # early exit: no relaxation in this pass

    # ── Negative-cycle detection — V-th pass ─────────────────────────────────
    for u, v, data in edges:
        w = data.get(weight, data.get('weight', 1.0))
        if (dist[u] < INF and dist[u] + w < dist[v]) or \
           (dist[v] < INF and dist[v] + w < dist[u]):
            yield StepEvent(
                type  = 'error',
                flags = {
                    'message': (
                        'Negative Cycle Detected — this graph contains a loop '
                        'where total cost decreases on every traversal. '
                        'No finite shortest path exists; Dijkstra would loop forever.'
                    ),
                },
            )
            return

    # ── Unreachable ───────────────────────────────────────────────────────────
    if dist.get(dst, INF) == INF:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    # ── Path reconstruction ───────────────────────────────────────────────────
    path: list[str] = []
    node: str | None = dst
    seen:  set[str]  = set()
    while node is not None:
        if node in seen:            # guard against malformed prev chain
            yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
            return
        seen.add(node)
        path.append(node)
        node = prev.get(node)

    if not path or path[-1] != src:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    path.reverse()
    yield StepEvent(type='found_path', flags={'path': path})
