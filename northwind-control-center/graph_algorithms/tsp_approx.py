"""
TSP 2-Approximation — Minimum Spanning Tree + DFS preorder.

The Traveling Salesman Problem is NP-complete (O(2^V) exact).
This algorithm finds a Hamilton cycle guaranteed to be ≤ 2× the optimal:

  1. Build a Minimum Spanning Tree T (O(E log E)).
  2. Perform DFS preorder on T from the seed city — this visits every
     city exactly once following tree edges.
  3. Close the tour by returning to the seed city.

Correctness: MST weight ≤ OPT (removing any edge from the optimal tour
gives a spanning tree).  The DFS preorder tour visits each MST edge at
most twice → tour weight ≤ 2 × MST weight ≤ 2 × OPT.

The geographic distance function satisfies the triangle inequality
(w(x,z) ≤ w(x,y) + w(y,z)) so the shortcut is always valid.

Complexity: O(E log E) for the MST + O(V) for DFS.
Graph: reduced 200-city subgraph (needs_reduced: True).
From city = tour starting point; no destination needed (needs_dst: False).
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst=None, weight: str = 'weight', **_):
    """
    Yield StepEvents for the MST-based TSP approximation.

    Events:
      visit_node — city added to the tour in DFS preorder
      found_path — complete Hamilton cycle (path[0] == path[-1] == src)
    """
    # Step 1: Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(G, weight=weight)

    # Step 2: DFS preorder from src — visits every city exactly once
    preorder: list[str] = list(nx.dfs_preorder_nodes(mst, source=src))

    # Animate tour construction city by city
    for city in preorder:
        yield StepEvent(type='visit_node', node=city)

    # Step 3: Close the tour
    tour = preorder + [preorder[0]]

    yield StepEvent(type='found_path', flags={'path': tour})
