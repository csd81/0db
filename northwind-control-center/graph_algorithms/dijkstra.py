"""
Dijkstra — optimal shortest-path on non-negative weighted graphs.
Explores in all directions by accumulated road cost (no geographic bias).
Guarantees the minimum-cost path when all edge weights ≥ 0.

Visual signature: a weighted circular expansion — denser along cheap roads.
"""
from __future__ import annotations
import heapq

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst: str, weight: str = 'weight', **_):
    """Yield StepEvents in Dijkstra traversal order."""
    dist:    dict[str, float]      = {src: 0.0}
    prev:    dict[str, str | None] = {src: None}
    settled: set[str]              = set()
    pq                             = [(0.0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if u in settled:
            continue
        settled.add(u)
        yield StepEvent(type='visit_node', node=u, cost=round(d, 1))
        if u == dst:
            break
        for v in G.neighbors(u):
            nd = d + G[u][v].get(weight, 1.0)
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                prev[v] = u
                yield StepEvent(type='relax_edge', source=u, target=v, cost=round(nd, 1))
                heapq.heappush(pq, (nd, v))

    if dst not in settled:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    path: list[str] = []
    node: str | None = dst
    while node is not None:
        path.append(node)
        node = prev.get(node)
    path.reverse()
    yield StepEvent(type='found_path', flags={'path': path})
