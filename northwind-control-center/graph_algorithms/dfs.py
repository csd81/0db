"""
DFS — Depth-First Search.
Plunges down one branch before backtracking. Finds *a* path, not the shortest.
Useful for demonstrating network reachability and why naive search fails for routing.

Visual signature: an erratic, depth-first line — the "drunk explorer" effect.
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst: str, **_):
    """Yield StepEvents in iterative DFS traversal order."""
    stack   = [src]
    visited: set[str] = set()
    prev:   dict[str, str | None] = {src: None}

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        yield StepEvent(type='visit_node', node=u)
        if u == dst:
            break
        for v in G.neighbors(u):
            if v not in visited:
                if v not in prev:
                    prev[v] = u
                yield StepEvent(type='push_stack', node=v, source=u)
                stack.append(v)

    if dst not in visited:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    path: list[str] = []
    node: str | None = dst
    while node is not None:
        path.append(node)
        node = prev.get(node)
    path.reverse()
    yield StepEvent(type='found_path', flags={'path': path})
