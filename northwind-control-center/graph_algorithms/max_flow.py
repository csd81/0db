"""
Max-Flow / Min-Cut — Edmonds-Karp algorithm.

Finds the maximum flow from source to sink using BFS-based augmenting paths
(Edmonds-Karp is Ford-Fulkerson restricted to shortest augmenting paths).
The Min-Cut Theorem guarantees: max-flow = min-cut capacity.

Logistical applications (from the lecture notes — Chapter 14: Hálózati folyamok):
  • "How many virtual trucks can move from Paris to Warsaw simultaneously?"
  • Min-cut identifies the 'thinnest' part of the network — upgrading those
    road segments gives the greatest throughput improvement.
  • Saturated edges (flow = capacity) are the bottlenecks in red.
  • Capacity values: highways=1000, ferry=200, ocean=100 units.

Complexity: O(V · E²).
Graph: reduced 200-city subgraph (needs_reduced: True).
Destination required (needs_dst: True).
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst: str, weight: str = 'weight', **_):
    """
    Yield StepEvents for Edmonds-Karp max-flow.

    Events:
      visit_node   — city visited during BFS augmenting-path search
      relax_edge   — augmenting path edge being used for this iteration
      found_path   — terminal; flags carry flow_value, cut_edges, saturated_edges
    """
    if src == dst:
        yield StepEvent(type='error', flags={'message': 'Source and sink must be different cities.'})
        return

    # Build a DiGraph with capacity attributes (undirected → bidirectional)
    DG = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        cap = data.get('capacity', 100)
        DG.add_edge(u, v, capacity=cap)
        DG.add_edge(v, u, capacity=cap)

    # ── Edmonds-Karp (BFS augmenting paths) ─────────────────────────────
    flow_value = 0
    flow_dict: dict[str, dict[str, int]] = {n: {} for n in DG.nodes()}

    def _residual_cap(u, v):
        fwd = DG[u][v].get('capacity', 0) - flow_dict[u].get(v, 0)
        return fwd

    max_iters = 60   # cap animation iterations
    iteration = 0

    while iteration < max_iters:
        # BFS to find shortest augmenting path
        visited = {src}
        parent  = {src: None}
        queue   = [src]
        found   = False

        while queue and not found:
            curr = queue.pop(0)
            yield StepEvent(type='visit_node', node=curr)
            for nb in DG.successors(curr):
                if nb not in visited and _residual_cap(curr, nb) > 0:
                    visited.add(nb)
                    parent[nb] = curr
                    if nb == dst:
                        found = True
                        break
                    queue.append(nb)

        if not found:
            break

        # Find bottleneck along the path
        path, node = [], dst
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()

        bottleneck = min(_residual_cap(path[i], path[i + 1])
                         for i in range(len(path) - 1))

        # Emit path edges
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            yield StepEvent(type='relax_edge', source=u, target=v,
                            cost=round(bottleneck, 1))
            flow_dict[u][v] = flow_dict[u].get(v, 0) + bottleneck
            flow_dict[v][u] = flow_dict[v].get(u, 0) - bottleneck

        flow_value += bottleneck
        iteration  += 1

    # ── Identify min-cut edges ───────────────────────────────────────────
    # Reachable from src in residual graph = source side of cut
    reachable: set[str] = set()
    stack = [src]
    while stack:
        u = stack.pop()
        if u in reachable:
            continue
        reachable.add(u)
        for v in DG.successors(u):
            if v not in reachable and _residual_cap(u, v) > 0:
                stack.append(v)

    cut_edges        = []
    saturated_edges  = []
    for u in reachable:
        for v in DG.successors(u):
            if v not in reachable:
                cap  = DG[u][v].get('capacity', 0)
                flow = flow_dict[u].get(v, 0)
                cut_edges.append((u, v))
                if flow >= cap:
                    saturated_edges.append((u, v))

    n_cut = len(cut_edges)
    cut_cap = sum(DG[u][v].get('capacity', 0) for u, v in cut_edges)

    yield StepEvent(
        type  = 'found_path',
        flags = {
            'path':             [src, dst],
            'flow_value':       flow_value,
            'cut_edges':        [(u, v) for u, v in cut_edges],
            'saturated_edges':  [(u, v) for u, v in saturated_edges],
            'verdict':          f'Max flow = {int(flow_value):,} units',
            'detail':           (
                f'Edmonds-Karp from {src} → {dst}: '
                f'{int(flow_value):,} units/hour max throughput. '
                f'Min-cut: {n_cut} road segment{"s" if n_cut != 1 else ""} '
                f'with combined capacity {int(cut_cap):,}. '
                f'Max-Flow Min-Cut Theorem: these links are the binding constraint. '
                f'{len(saturated_edges)} segment{"s" if len(saturated_edges) != 1 else ""} '
                f'fully saturated — upgrade these first for maximum gain.'
            ),
        },
    )
