"""
Graph Algorithm Laboratory — coordinator and algorithm registry.

Phase 0  — infrastructure: StepEvent schema, dual graph cache, /solve endpoint.
           All algorithms served by A* backbone; step lists are empty.
Phase 1  — BFS / DFS / Dijkstra / A* with full step-by-step animation.
Phase 2  — Bellman-Ford with negative-edge highlight (reduced graph).
Phase 3  — Reliability routing: max-probability path via -log(p) weights.
Phase 4  — Floyd-Warshall / flow algorithms on reduced graph.
"""
from __future__ import annotations

import networkx as nx

from graph_algorithms.common import (
    StepEvent,
    get_full_graph, get_reduced_graph,
    haversine_km, REDUCED_N,
)

_ASTAR_EPSILON = 1.1   # heuristic inflation — matches graph_routing_service.py


# ── Algorithm registry ────────────────────────────────────────────────────────
# Each entry describes a single algorithm: which problem category it solves,
# whether it needs the reduced graph, which edge-weight attribute to use,
# and which Phase adds step-by-step animation.

ALGORITHM_REGISTRY: dict[str, dict] = {
    'astar': {
        'label':         'A*',
        'problem':       'nav',
        'needs_reduced': False,
        'weight_attr':   'weight',
        'description':   (
            'Uses Haversine distance to the goal as a heuristic to "aim" the search. '
            'Fastest for long-range point-to-point routing.'
        ),
        'phase': 1,
    },
    'dijkstra': {
        'label':         'Dijkstra',
        'problem':       'nav',
        'needs_reduced': False,
        'weight_attr':   'weight',
        'description':   (
            'Expands nodes in all directions by accumulated road cost. '
            'Guaranteed optimal on non-negative weights; no geographic bias.'
        ),
        'phase': 1,
    },
    'bfs': {
        'label':         'BFS',
        'problem':       'nav',
        'needs_reduced': False,
        'weight_attr':   None,
        'description':   (
            'Breadth-First Search ignores distance — finds the route '
            'with the fewest city-to-city transfers (minimum hops).'
        ),
        'phase': 1,
    },
    'dfs': {
        'label':         'DFS',
        'problem':       'reach',
        'needs_reduced': False,
        'weight_attr':   None,
        'description':   (
            'Depth-First Search plunges down one branch before backtracking. '
            'Shows network reachability rather than optimal routing.'
        ),
        'phase': 1,
    },
    'bellman_ford': {
        'label':         'Bellman-Ford',
        'problem':       'nav',
        'needs_reduced': True,
        'weight_attr':   'bellman_weight',
        'description':   (
            'Handles negative edge costs (wind assistance, subsidies). '
            f'Detects negative cycles. Runs on the reduced {REDUCED_N}-city graph.'
        ),
        'phase': 2,
    },
    'reliability': {
        'label':         'Reliability Routing',
        'problem':       'stoch',
        'needs_reduced': False,
        'weight_attr':   'log_weight',
        'description':   (
            'Finds the most probable route by minimising −log(ReliabilityScore). '
            'Equivalent to maximising ∏ p(edge) — a Viterbi-style objective.'
        ),
        'phase': 3,
    },
    'floyd_warshall': {
        'label':         'Floyd-Warshall',
        'problem':       'global',
        'needs_reduced': True,
        'weight_attr':   'weight',
        'description':   (
            'All-pairs shortest paths in one O(V³) pass. '
            f'Restricted to the top-{REDUCED_N} cities; pre-computes the full distance matrix.'
        ),
        'phase': 4,
    },
}

# ── Problem registry ──────────────────────────────────────────────────────────
# Groups algorithms by the class of problem they solve; drives the frontend
# dual-dropdown (problem → available algorithms).

PROBLEM_REGISTRY: dict[str, dict] = {
    'nav': {
        'label':      'Point-to-Point Navigation',
        'algorithms': ['astar', 'dijkstra', 'bfs', 'bellman_ford'],
    },
    'reach': {
        'label':      'Network Reachability',
        'algorithms': ['bfs', 'dfs'],
    },
    'stoch': {
        'label':      'Reliability Routing',
        'algorithms': ['reliability'],
    },
    'global': {
        'label':      'Global Hub Analysis',
        'algorithms': ['floyd_warshall'],
    },
}


def get_registry() -> dict:
    """Return problem + algorithm maps — consumed by the frontend dropdown builder."""
    return {
        'problems':   PROBLEM_REGISTRY,
        'algorithms': {k: {kk: vv for kk, vv in v.items() if kk != 'phase'}
                       for k, v in ALGORITHM_REGISTRY.items()},
        'reduced_n':  REDUCED_N,
    }


# ── Path geometry helper ──────────────────────────────────────────────────────

def _path_to_geo(G: nx.Graph, path: list[str], city_by_name: dict) -> list[dict]:
    """Convert a name-list path into the hop-annotated GeoJSON list the frontend expects."""
    result    = []
    actual_km = 0.0
    for i, name in enumerate(path):
        ferry_hop = ocean_hop = False
        if i > 0:
            edge       = G[path[i - 1]][name]
            actual_km += edge.get('dist_km', 0.0)
            ferry_hop  = edge.get('ferry', False)
            ocean_hop  = edge.get('ocean', False)
        nd   = G.nodes[name]
        meta = city_by_name.get(name, {})
        result.append({
            'name':            name,
            'country':         meta.get('country', ''),
            'lat':             nd['lat'],
            'lng':             nd['lng'],
            'dist_from_start': round(actual_km, 1),
            'ferry':           ferry_hop,
            'ocean':           ocean_hop,
        })
    return result


# ── Phase 0 solver ────────────────────────────────────────────────────────────

def solve(conn_str: str, problem: str, algorithm: str,
          src: str, dst: str) -> dict:
    """
    Route a solve request to the appropriate algorithm.

    Phase 0: Every algorithm uses A* internally (correct weight_attr, no heuristic
    inflation for BFS/DFS — those use hop count). The 'steps' list is always empty;
    step-by-step animation generators are added per-algorithm in Phases 1–4.
    """
    if algorithm not in ALGORITHM_REGISTRY:
        return {'error': f'Unknown algorithm: {algorithm!r}'}
    meta = ALGORITHM_REGISTRY[algorithm]

    cache        = (get_reduced_graph(conn_str)
                    if meta['needs_reduced']
                    else get_full_graph(conn_str))
    G            = cache['graph']
    city_by_name = cache['city_by_name']

    if src not in G.nodes:
        return {'error': f'City not found: {src!r}'}
    if dst not in G.nodes:
        return {'error': f'City not found: {dst!r}'}

    weight_attr = meta['weight_attr'] or 'weight'

    # A* heuristic — for BFS/DFS (no weight) we still use geographic aim in the stub
    def _h(u: str, v: str) -> float:
        nu, nv = G.nodes[u], G.nodes[v]
        return haversine_km(nu['lat'], nu['lng'], nv['lat'], nv['lng']) * _ASTAR_EPSILON

    try:
        path = nx.astar_path(G, src, dst, heuristic=_h, weight=weight_attr)
    except nx.NetworkXNoPath:
        return {'error': f'No route found: {src!r} → {dst!r}'}

    path_geo   = _path_to_geo(G, path, city_by_name)
    total_km   = sum(
        G[path[i]][path[i + 1]].get('dist_km', 0.0)
        for i in range(len(path) - 1)
    )
    total_cost = sum(
        G[path[i]][path[i + 1]].get(weight_attr, 0.0)
        for i in range(len(path) - 1)
    )

    return {
        'algorithm':    algorithm,
        'algo_label':   meta['label'],
        'problem':      problem,
        'src':          src,
        'dst':          dst,
        'path':         path_geo,
        'total_km':     round(total_km, 1),
        'total_cost':   round(total_cost, 3),
        'hop_count':    len(path) - 1,
        'confidence':   None,
        'graph_mode':   'reduced' if meta['needs_reduced'] else 'full',
        'n_nodes':      G.number_of_nodes(),
        'n_edges':      G.number_of_edges(),
        'steps':        [],
        'warnings':     [],
        'has_extended': cache.get('has_extended', False),
    }
