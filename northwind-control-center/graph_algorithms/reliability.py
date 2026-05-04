"""
Reliability Routing — find the most probable path through the network.

Each edge carries a ReliabilityScore p ∈ (0, 1].  The probability of a
multi-hop route is the product of its edge scores:

    P(route) = ∏ p(edge)

Maximising P is equivalent to minimising ∑ −log p, so we run Dijkstra
on the pre-computed 'log_weight' attribute (= −log(ReliabilityScore)).

The result is the Viterbi-optimal path — the one least likely to experience
a delay, breakdown, or failed crossing.  Ocean crossings hurt most because
their base reliability is 0.85 per hop; high-frequency land corridors stay
close to 0.97.

Complexity: O((V + E) log V) — identical to standard Dijkstra.
Visual signature: similar expanding ring, but nudged away from ocean hops
toward denser land/ferry corridors.
"""
from __future__ import annotations

import heapq
import math

import networkx as nx

from graph_algorithms.common import StepEvent


def run(G: nx.Graph, src: str, dst: str, weight: str = 'log_weight', **_):
    """
    Yield StepEvents for Reliability Routing traversal.

    Events:
      visit_node  — node settled; flags carry 'reliability' (cumulative path prob)
      relax_edge  — cost improved; flags carry 'reliability' of new partial path
      found_path  — path successfully reconstructed
      no_path     — destination unreachable
    """
    INF  = float('inf')
    dist: dict[str, float]      = {src: 0.0}
    prev: dict[str, str | None] = {src: None}
    settled: set[str]           = set()
    pq: list[tuple[float, str]] = [(0.0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if u in settled:
            continue
        settled.add(u)
        yield StepEvent(
            type  = 'visit_node',
            node  = u,
            cost  = round(d, 4),
            flags = {'reliability': round(math.exp(-d), 4)},
        )
        if u == dst:
            break
        for v in G.neighbors(u):
            w  = G[u][v].get(weight, G[u][v].get('weight', 0.0))
            nd = d + w
            if nd < dist.get(v, INF):
                dist[v] = nd
                prev[v] = u
                yield StepEvent(
                    type   = 'relax_edge',
                    source = u,
                    target = v,
                    cost   = round(nd, 4),
                    flags  = {'reliability': round(math.exp(-nd), 4)},
                )
                heapq.heappush(pq, (nd, v))

    if dist.get(dst, INF) == INF:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    # ── Path reconstruction ───────────────────────────────────────────────────
    path: list[str] = []
    node: str | None = dst
    seen: set[str]   = set()
    while node is not None:
        if node in seen:
            yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
            return
        seen.add(node)
        path.append(node)
        node = prev.get(node)

    if not path or path[-1] != src:
        yield StepEvent(type='no_path', flags={'src': src, 'dst': dst})
        return

    path.reverse()
    yield StepEvent(type='found_path', flags={'path': path})
