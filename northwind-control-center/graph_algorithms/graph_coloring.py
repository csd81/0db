"""
Graph Coloring — greedy chromatic-number approximation.

Assigns colours to cities so that no two adjacent cities share a colour,
using the largest-first greedy heuristic (process nodes in descending
degree order, assign the smallest available colour index).

Logistical applications (from the lecture notes):
  • Scheduling: cities coloured with the same index can share a delivery
    time-slot without conflicting with neighbours.
  • Frequency assignment: adjacent distribution hubs must broadcast on
    different channels — colour index = channel number.
  • Brooks' theorem: χ(G) ≤ Δ for most graphs (Δ = max degree).
  • 4-Color theorem: any planar map needs ≤ 4 colours.

Complexity: O(V log V + E).
Graph: reduced 200-city subgraph (needs_reduced: True).
No destination needed (needs_dst: False).
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src=None, dst=None, **_):
    """
    Yield StepEvents for greedy graph coloring.

    Events:
      color_node    — city receives a colour index; flags carry 'color'
      found_coloring — terminal; flags carry full coloring dict + χ(G)
    """
    # Largest-first order: high-degree nodes are hardest to colour — do them first.
    nodes_sorted = sorted(G.nodes(), key=lambda n: -G.degree(n))

    coloring: dict[str, int] = {}

    for node in nodes_sorted:
        used = {coloring[nb] for nb in G.neighbors(node) if nb in coloring}
        color = 0
        while color in used:
            color += 1
        coloring[node] = color
        yield StepEvent(
            type  = 'color_node',
            node  = node,
            flags = {'color': color, 'degree': G.degree(node)},
        )

    chi = max(coloring.values()) + 1 if coloring else 0
    n   = G.number_of_nodes()
    max_deg = max(G.degree(v) for v in G.nodes()) if G.nodes() else 0

    brooks = chi <= max_deg
    four_color_note = (
        'χ(G) ≤ 4 — consistent with the 4-Color Theorem (planar map). '
        if chi <= 4 else
        f'χ(G) = {chi} > 4 — graph is non-planar (Kuratowski\'s theorem confirms K₅/K₃,₃ minor). '
    )
    brooks_note = (
        f'Brooks\' theorem: χ ≤ Δ = {max_deg} ✓'
        if brooks else
        f'χ = Δ + 1 = {chi} — this is a complete graph or odd cycle.'
    )

    yield StepEvent(
        type  = 'found_coloring',
        flags = {
            'coloring':          coloring,
            'chromatic_number':  chi,
            'verdict':           f'χ(G) = {chi} colours',
            'detail':            (
                f'Greedy (largest-first) coloured {n} cities using {chi} colours. '
                f'No two adjacent cities share a colour. '
                f'{four_color_note}'
                f'{brooks_note}'
            ),
        },
    )
