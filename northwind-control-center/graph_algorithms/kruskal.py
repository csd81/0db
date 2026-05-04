"""
Kruskal's Minimum Spanning Tree — greedy edge selection with Union-Find.

Sorts all edges by weight, then greedily adds each edge to the tree if it
does not create a cycle (checked via Union-Find in near-O(1)).  The result
is the cheapest set of V-1 edges that keeps the graph connected.

Logistical interpretation: the MST is the backbone road network that
connects all cities with the minimum total cost — equivalent to designing
a new rail or pipeline system from scratch.

Visual signature: edges "pop in" across the whole map from cheapest to most
expensive, with no geographic bias — very different from the node-by-node
blob of Prim's.

Complexity: O(E log E) dominated by the initial sort.
Restricted to the reduced 200-city graph (needs_reduced: True).
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


class _UnionFind:
    """Path-halving union-find for cycle detection."""

    __slots__ = ('_p', '_r')

    def __init__(self, nodes):
        self._p = {n: n for n in nodes}
        self._r = {n: 0  for n in nodes}

    def find(self, x: str) -> str:
        while self._p[x] != x:
            self._p[x] = self._p[self._p[x]]   # path halving
            x = self._p[x]
        return x

    def union(self, x: str, y: str) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self._r[rx] < self._r[ry]:
            rx, ry = ry, rx
        self._p[ry] = rx
        if self._r[rx] == self._r[ry]:
            self._r[rx] += 1
        return True


def run(G: nx.Graph, src=None, dst=None, weight: str = 'weight', **_):
    """
    Yield StepEvents for Kruskal's MST.

    Events:
      mst_edge   — edge accepted into the spanning tree
      found_tree — final tree edge list (path reconstruction analogue)
    """
    nodes        = list(G.nodes())
    uf           = _UnionFind(nodes)
    tree_edges:  list[tuple[str, str]] = []
    target_edges = len(nodes) - 1

    for u, v, data in sorted(G.edges(data=True),
                              key=lambda e: e[2].get(weight, 1.0)):
        if uf.union(u, v):
            tree_edges.append((u, v))
            yield StepEvent(
                type   = 'mst_edge',
                source = u,
                target = v,
                cost   = round(data.get(weight, 1.0), 1),
            )
            if len(tree_edges) == target_edges:
                break   # spanning tree complete — no need to scan remaining edges

    yield StepEvent(type='found_tree', flags={'tree_edges': tree_edges})
