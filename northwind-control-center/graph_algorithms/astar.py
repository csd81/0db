"""
A* — heuristic-guided shortest path.
Uses Haversine distance to the destination as a greedy guide (ε = 1.1).
Visits far fewer nodes than Dijkstra for long-range routes.

Visual signature: a "flashlight beam" aimed at the destination — directional
search with occasional side-expansions to guarantee near-optimality.
"""
from __future__ import annotations
import heapq

import networkx as nx

from graph_algorithms.common import StepEvent, haversine_km

ASTAR_EPSILON = 1.1   # heuristic inflation — matches graph_routing_service.py


def run(G: nx.Graph, src: str, dst: str, weight: str = 'weight', **_):
    """Yield StepEvents in A* traversal order."""
    dst_lat = G.nodes[dst]['lat']
    dst_lng = G.nodes[dst]['lng']

    def h(u: str) -> float:
        n = G.nodes[u]
        return haversine_km(n['lat'], n['lng'], dst_lat, dst_lng) * ASTAR_EPSILON

    dist:    dict[str, float]      = {src: 0.0}
    prev:    dict[str, str | None] = {src: None}
    settled: set[str]              = set()
    pq                             = [(h(src), 0.0, src)]

    while pq:
        _, d, u = heapq.heappop(pq)
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
                heapq.heappush(pq, (nd + h(v), nd, v))

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
