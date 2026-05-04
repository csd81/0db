"""
Floyd-Warshall — all-pairs shortest paths in a single O(V³) pass.

Unlike single-source algorithms, FW computes the shortest path between
every pair of nodes simultaneously by iterating over each city k as an
intermediate vertex and checking whether routing through k shortens the
i→j path for any pair (i, j).

Restricted to the reduced 200-city graph (needs_reduced: True) because
V³ = 8 million ops on 200 nodes is fast; on 18k nodes it would be
5.8 × 10¹² ops — impossible.

Animation: one 'pivot_node' event per k city (200 total), plus up to
MAX_RELAX_PER_PIVOT relax_edge events per pass so the viewer can see
edges tightening without flooding the step list.

After the full matrix is computed, the src→dst path is reconstructed
from the predecessor matrix and returned as 'found_path'.
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent

MAX_RELAX_PER_PIVOT = 3   # relax_edge events emitted per k-pass


def run(G: nx.Graph, src: str, dst: str, weight: str = 'weight', **_):
    """
    Yield StepEvents for Floyd-Warshall traversal.

    Events:
      pivot_node  — current intermediate vertex k being processed
      relax_edge  — dist[i][j] improved via k (up to MAX_RELAX_PER_PIVOT per pass)
      found_path  — path successfully reconstructed from predecessor matrix
      no_path     — destination unreachable (disconnected component)
    """
    nodes = list(G.nodes())
    n     = len(nodes)
    idx   = {name: i for i, name in enumerate(nodes)}
    rev   = list(nodes)          # rev[i] → city name
    INF   = float('inf')

    # ── Initialise distance and predecessor matrices ──────────────────────────
    dist = [[INF] * n for _ in range(n)]
    pred = [[None] * n for _ in range(n)]

    for i, u in enumerate(nodes):
        dist[i][i] = 0.0
        for v in G.neighbors(u):
            j       = idx[v]
            w       = G[u][v].get(weight, G[u][v].get('weight', 1.0))
            if w < dist[i][j]:
                dist[i][j] = w
                pred[i][j] = i

    # ── Main triple loop ──────────────────────────────────────────────────────
    for k in range(n):
        yield StepEvent(type='pivot_node', node=rev[k])

        relaxed = 0
        for i in range(n):
            d_ik = dist[i][k]
            if d_ik == INF:
                continue
            for j in range(n):
                if dist[k][j] == INF:
                    continue
                nd = d_ik + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
                    pred[i][j] = pred[k][j]
                    if relaxed < MAX_RELAX_PER_PIVOT:
                        yield StepEvent(
                            type   = 'relax_edge',
                            source = rev[i],
                            target = rev[j],
                            cost   = round(nd, 1),
                        )
                        relaxed += 1

    # ── Extract src → dst path ────────────────────────────────────────────────
    si = idx.get(src)
    di = idx.get(dst)

    if si is None or di is None or dist[si][di] == INF:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    path: list[str] = []
    j = di
    visited: set[int] = set()
    while j != si:
        if j is None or j in visited:
            yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
            return
        visited.add(j)
        path.append(rev[j])
        j = pred[si][j]
    path.append(rev[si])
    path.reverse()

    yield StepEvent(type='found_path', flags={'path': path})
