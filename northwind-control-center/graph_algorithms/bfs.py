"""
BFS — Breadth-First Search.
Finds the minimum-hop path between two cities; ignores edge weights entirely.
Explores like an expanding ring: all cities 1 hop away, then 2, then 3, …

Visual signature: a uniform circular wave spreading from the source.
"""
from __future__ import annotations
from collections import deque

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst: str, **_):
    """Yield StepEvents in BFS traversal order; final event is found_path or no_path."""
    queue   = deque([src])
    visited = {src}
    prev:   dict[str, str | None] = {src: None}

    while queue:
        u = queue.popleft()
        yield StepEvent(type='visit_node', node=u)
        if u == dst:
            break
        for v in G.neighbors(u):
            if v not in visited:
                visited.add(v)
                prev[v] = u
                yield StepEvent(type='enqueue', node=v, source=u)
                queue.append(v)

    if dst not in prev:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    path: list[str] = []
    node: str | None = dst
    while node is not None:
        path.append(node)
        node = prev.get(node)
    path.reverse()
    yield StepEvent(type='found_path', flags={'path': path})
