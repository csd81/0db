"""
Cut-Vertex & Bridge Detection — Tarjan's DFS (via NetworkX).

A cut-vertex (articulation point) is a node whose removal disconnects the graph.
A bridge is an edge whose removal disconnects the graph.
Both are identified in a single O(V + E) DFS pass.

Logistical applications (from the lecture notes):
  • Vulnerability analysis: cut-vertices are single points of global failure.
  • Disaster planning: removing one hub city can isolate entire sub-networks.
  • Bridges are the most critical road segments — no alternative route exists.
  • Connectivity (1.36. Definíció): k-connected graph can lose k−1 vertices
    without disconnecting — cut-vertices mark k=1 weak points.

Complexity: O(V + E).
Graph: reduced 200-city subgraph (needs_reduced: True).
No destination needed (needs_dst: False).
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src=None, dst=None, **_):
    """
    Yield StepEvents for cut-vertex and bridge detection.

    Events:
      visit_node   — city processed during DFS traversal
      check_node   — city identified as a cut-vertex (role='cut_vertex')
      bridge_edge  — edge identified as a bridge (source/target = endpoints)
      found_analysis — terminal; flags carry cut_vertices, bridges, verdict, detail
    """
    # ── DFS traversal (visual) ───────────────────────────────────────────
    start   = src if src and src in G.nodes else next(iter(G.nodes()), None)
    visited: set[str] = set()
    stack   = [start] if start else []

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        yield StepEvent(type='visit_node', node=u)
        for v in G.neighbors(u):
            if v not in visited:
                stack.append(v)

    # ── Tarjan-based detection (via NetworkX) ────────────────────────────
    cut_vertices = list(nx.articulation_points(G))
    bridges      = list(nx.bridges(G))

    for node in cut_vertices:
        yield StepEvent(
            type  = 'check_node',
            node  = node,
            flags = {'role': 'cut_vertex', 'degree': G.degree(node)},
        )

    for u, v in bridges:
        yield StepEvent(type='bridge_edge', source=u, target=v)

    # ── Terminal event ───────────────────────────────────────────────────
    n         = G.number_of_nodes()
    m         = G.number_of_edges()
    n_cut     = len(cut_vertices)
    n_bridges = len(bridges)

    if n_cut == 0 and n_bridges == 0:
        resilience = '2-connected (no single point of failure).'
    else:
        resilience = (
            f'{n_cut} chokepoint{"s" if n_cut != 1 else ""} and '
            f'{n_bridges} critical link{"s" if n_bridges != 1 else ""} found.'
        )

    yield StepEvent(
        type  = 'found_analysis',
        flags = {
            'cut_vertices': cut_vertices,
            'bridges':      [(u, v) for u, v in bridges],
            'n_cut':        n_cut,
            'n_bridges':    n_bridges,
            'verdict':      f'{n_cut} cut-vertices · {n_bridges} bridges',
            'detail':       (
                f'Tarjan DFS on {n} cities, {m} connections. '
                f'{resilience} '
                f'Cut-vertices (red markers): removing any one isolates sub-networks. '
                f'Bridges (red links): sole road between two regions. '
                f'Connectivity (1.36 Def.): this graph is '
                f'{"2-connected" if n_cut == 0 else "1-connected"} — '
                f'{"no single node failure can disconnect it" if n_cut == 0 else "one node removal can partition the network"}.'
            ),
        },
    )
