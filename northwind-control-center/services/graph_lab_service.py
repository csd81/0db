"""
Graph Algorithm Laboratory — coordinator and algorithm registry.

Phase 0  — infrastructure skeleton (StepEvent, dual graph cache, /solve endpoint).
Phase 1  — BFS / DFS / Dijkstra / A* with step-by-step animation.
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
from graph_algorithms import bfs, dfs, dijkstra, astar

_ASTAR_EPSILON = 1.1

# ── Algorithm runners (Phase 1) ───────────────────────────────────────────────
# Maps algorithm key → generator function.  Each generator yields StepEvent
# objects; the final event is always 'found_path' or 'no_path'.

_ALGO_RUNNERS: dict = {
    'bfs':      bfs.run,
    'dfs':      dfs.run,
    'dijkstra': dijkstra.run,
    'astar':    astar.run,
}

# Maximum animation frames returned to the frontend.
# Steps are subsampled so the animation never takes more than ~30 s at 1×.
MAX_ANIM_STEPS = 300


# ── Algorithm registry ────────────────────────────────────────────────────────

ALGORITHM_REGISTRY: dict[str, dict] = {
    'astar': {
        'label':         'A*',
        'problem':       'nav',
        'needs_reduced': False,
        'weight_attr':   'weight',
        'description':   (
            'Uses Haversine distance to the goal as a heuristic to "aim" the search. '
            'Visits far fewer cities than Dijkstra — a "flashlight beam" effect.'
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
            'Breadth-First Search ignores distance — finds the route with the fewest '
            'city-to-city transfers. Explores like a uniform expanding ring.'
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
            'Shows network reachability — the "drunk explorer" effect.'
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


# ── Step throttling ───────────────────────────────────────────────────────────

def _throttle(steps: list[StepEvent], n: int) -> list[StepEvent]:
    """
    Subsample a step list to at most n frames.
    Always preserves the first 5 and last 5; samples the middle uniformly.
    This retains the algorithm's search signature without grinding through
    thousands of identical visit_node events.
    """
    if len(steps) <= n:
        return steps
    head   = steps[:5]
    tail   = steps[-5:]
    mid    = steps[5:-5]
    stride = max(1, len(mid) // max(n - 10, 1))
    return head + mid[::stride] + tail


# ── Path helpers ──────────────────────────────────────────────────────────────

def _path_to_geo(G: nx.Graph, path: list[str], city_by_name: dict) -> list[dict]:
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


def _city_coords_for_steps(G: nx.Graph, steps: list[StepEvent],
                            path_names: list[str],
                            city_by_name: dict) -> dict:
    """
    Build a {name: {lat, lng, country}} lookup for every city referenced in
    the step list + final path.  The frontend uses this to place markers
    without needing the full 18k-city list.
    """
    mentioned: set[str] = set(path_names)
    for s in steps:
        if s.node:   mentioned.add(s.node)
        if s.source: mentioned.add(s.source)
        if s.target: mentioned.add(s.target)
    result = {}
    for name in mentioned:
        if name and name in G.nodes:
            nd   = G.nodes[name]
            meta = city_by_name.get(name, {})
            result[name] = {
                'lat':     nd['lat'],
                'lng':     nd['lng'],
                'country': meta.get('country', ''),
            }
    return result


# ── Solver ────────────────────────────────────────────────────────────────────

def solve(conn_str: str, problem: str, algorithm: str,
          src: str, dst: str) -> dict:
    """
    Route a solve request to the appropriate algorithm generator.

    Phase 1 algorithms (bfs/dfs/dijkstra/astar) run their full generators,
    throttle the step list to MAX_ANIM_STEPS, and return city_coords for the
    frontend to place markers without fetching all 18k cities.

    Unimplemented algorithms (phase > 1) fall back to the A* backbone and
    return an empty steps list.
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
    runner      = _ALGO_RUNNERS.get(algorithm)

    # ── Phase 1+ algorithms: real generators ─────────────────────────────
    if runner:
        raw = list(runner(G, src, dst, weight=weight_attr))

        # Split terminal event from traversal steps
        terminal     = next((s for s in reversed(raw)
                             if s.type in ('found_path', 'no_path')), None)
        visit_steps  = [s for s in raw if s.type not in ('found_path', 'no_path')]

        if terminal is None or terminal.type == 'no_path':
            return {'error': f'No route found: {src!r} → {dst!r}'}

        path_names = terminal.flags.get('path', [])
        if not path_names:
            return {'error': f'No route found: {src!r} → {dst!r}'}

        throttled = _throttle(visit_steps, MAX_ANIM_STEPS)
        throttled.append(terminal)

        path_geo   = _path_to_geo(G, path_names, city_by_name)
        total_km   = sum(G[path_names[i]][path_names[i + 1]].get('dist_km', 0.0)
                         for i in range(len(path_names) - 1))
        total_cost = sum(G[path_names[i]][path_names[i + 1]].get(weight_attr, 0.0)
                         for i in range(len(path_names) - 1))
        n_visited  = sum(1 for s in visit_steps if s.type == 'visit_node')

        return {
            'algorithm':    algorithm,
            'algo_label':   meta['label'],
            'problem':      problem,
            'src':          src,
            'dst':          dst,
            'path':         path_geo,
            'total_km':     round(total_km, 1),
            'total_cost':   round(total_cost, 3),
            'hop_count':    len(path_names) - 1,
            'n_visited':    n_visited,
            'confidence':   None,
            'graph_mode':   'reduced' if meta['needs_reduced'] else 'full',
            'n_nodes':      G.number_of_nodes(),
            'n_edges':      G.number_of_edges(),
            'city_coords':  _city_coords_for_steps(G, throttled, path_names, city_by_name),
            'steps':        [s.to_dict() for s in throttled],
            'warnings':     [],
            'has_extended': cache.get('has_extended', False),
        }

    # ── Phase 0 fallback: A* backbone, empty steps ───────────────────────
    def _h(u: str, v: str) -> float:
        nu, nv = G.nodes[u], G.nodes[v]
        return haversine_km(nu['lat'], nu['lng'], nv['lat'], nv['lng']) * _ASTAR_EPSILON

    try:
        path_names = list(nx.astar_path(G, src, dst, heuristic=_h, weight=weight_attr))
    except nx.NetworkXNoPath:
        return {'error': f'No route found: {src!r} → {dst!r}'}

    path_geo   = _path_to_geo(G, path_names, city_by_name)
    total_km   = sum(G[path_names[i]][path_names[i + 1]].get('dist_km', 0.0)
                     for i in range(len(path_names) - 1))
    total_cost = sum(G[path_names[i]][path_names[i + 1]].get(weight_attr, 0.0)
                     for i in range(len(path_names) - 1))

    return {
        'algorithm':    algorithm,
        'algo_label':   meta['label'],
        'problem':      problem,
        'src':          src,
        'dst':          dst,
        'path':         path_geo,
        'total_km':     round(total_km, 1),
        'total_cost':   round(total_cost, 3),
        'hop_count':    len(path_names) - 1,
        'n_visited':    0,
        'confidence':   None,
        'graph_mode':   'reduced' if meta['needs_reduced'] else 'full',
        'n_nodes':      G.number_of_nodes(),
        'n_edges':      G.number_of_edges(),
        'city_coords':  _city_coords_for_steps(G, [], path_names, city_by_name),
        'steps':        [],
        'warnings':     [f'Step animation arrives in Phase {meta["phase"]}.'],
        'has_extended': cache.get('has_extended', False),
    }
