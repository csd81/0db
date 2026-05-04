"""
Prim's Minimum Spanning Tree — greedy node expansion from a seed city.

Maintains a priority queue of candidate edges leaving the current tree.
At each step the cheapest edge that connects a new city is accepted.

Logistical interpretation: same MST result as Kruskal but the growth
pattern is a blob expanding from the seed city — useful for showing how
an MST is constructed incrementally from a depot.

Visual signature: similar to Dijkstra's expanding ring but builds a tree
rather than a path.  Cities are coloured as they join the tree.

Complexity: O((V + E) log V) with a binary heap.
Restricted to the reduced 200-city graph (needs_reduced: True).
"""
from __future__ import annotations

import heapq

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst=None, weight: str = 'weight', **_):
    """
    Yield StepEvents for Prim's MST starting from src.

    Events:
      visit_node — city admitted to the spanning tree
      mst_edge   — edge accepted into the spanning tree
      found_tree — final tree edge list
    """
    in_tree:    set[str]                    = {src}
    tree_edges: list[tuple[str, str]]       = []
    pq:         list[tuple[float, str, str]] = []

    yield StepEvent(type='visit_node', node=src)

    for nbr in G.neighbors(src):
        heapq.heappush(pq, (G[src][nbr].get(weight, 1.0), src, nbr))

    while pq:
        w, u, v = heapq.heappop(pq)
        if v in in_tree:
            continue
        in_tree.add(v)
        tree_edges.append((u, v))

        yield StepEvent(type='mst_edge', source=u, target=v, cost=round(w, 1))
        yield StepEvent(type='visit_node', node=v)

        for nbr in G.neighbors(v):
            if nbr not in in_tree:
                heapq.heappush(pq, (G[v][nbr].get(weight, 1.0), v, nbr))

    yield StepEvent(type='found_tree', flags={'tree_edges': tree_edges})
