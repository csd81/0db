"""
Graph Algorithm Laboratory — coordinator and algorithm registry.

Phase 0  — infrastructure skeleton (StepEvent, dual graph cache, /solve endpoint).
Phase 1  — BFS / DFS / Dijkstra / A* with step-by-step animation.
Phase 2  — Bellman-Ford with negative-edge highlight (reduced graph).
Phase 3  — Reliability routing: max-probability path via -log(p) weights.
Phase 4  — Floyd-Warshall all-pairs shortest paths (reduced graph).
Phase 5  — Minimum Spanning Tree: Kruskal + Prim (reduced graph).
Phase 6  — Connectivity Analysis: Euler check + TSP 2-approximation.
Phase 7  — Matrix Analysis: Walk Counting (A^k) + Spanning Tree Count.
"""
from __future__ import annotations

import math

import networkx as nx

from graph_algorithms.common import (
    StepEvent,
    get_full_graph, get_reduced_graph,
    haversine_km, REDUCED_N,
)
from graph_algorithms import (
    bfs, dfs, dijkstra, astar,
    bellman_ford, reliability, floyd_warshall,
    kruskal, prim,
    euler_check, tsp_approx,
    walk_count, spanning_tree_count,
    graph_coloring, planarity_check,
    articulation,
    max_flow,
)

_ASTAR_EPSILON = 1.1

# Terminal event types — split from traversal steps in solve().
_TERMINAL = frozenset({
    'found_path', 'no_path', 'found_tree', 'found_analysis',
    'found_coloring', 'error',
})

_ALGO_RUNNERS: dict = {
    'bfs':            bfs.run,
    'dfs':            dfs.run,
    'dijkstra':       dijkstra.run,
    'astar':          astar.run,
    'bellman_ford':   bellman_ford.run,
    'reliability':    reliability.run,
    'floyd_warshall': floyd_warshall.run,
    'kruskal':        kruskal.run,
    'prim':           prim.run,
    'euler_check':          euler_check.run,
    'tsp_approx':           tsp_approx.run,
    'walk_count':           walk_count.run,
    'spanning_tree_count':  spanning_tree_count.run,
    'graph_coloring':       graph_coloring.run,
    'planarity_check':      planarity_check.run,
    'articulation':         articulation.run,
    'max_flow':             max_flow.run,
}

MAX_ANIM_STEPS = 300


# ── Algorithm registry ────────────────────────────────────────────────────────

ALGORITHM_REGISTRY: dict[str, dict] = {
    'astar': {
        'label':         'A*',
        'problem':       'nav',
        'needs_reduced': False,
        'needs_dst':     True,
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
        'needs_dst':     True,
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
        'needs_dst':     True,
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
        'needs_dst':     True,
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
        'needs_dst':     True,
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
        'needs_dst':     True,
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
        'needs_dst':     True,
        'weight_attr':   'weight',
        'description':   (
            'All-pairs shortest paths in one O(V³) pass. '
            f'Restricted to the top-{REDUCED_N} cities; pre-computes the full distance matrix.'
        ),
        'phase': 4,
    },
    'kruskal': {
        'label':         'Kruskal (MST)',
        'problem':       'mst',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   'weight',
        'description':   (
            'Builds the cheapest spanning tree by greedily adding the lowest-weight edge '
            'that does not create a cycle (Union-Find). '
            f'Visual: edges pop in across the {REDUCED_N}-city map, cheapest first.'
        ),
        'phase': 5,
    },
    'prim': {
        'label':         'Prim (MST)',
        'problem':       'mst',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   'weight',
        'description':   (
            'Grows the spanning tree node-by-node from the seed city using a priority queue. '
            'Same MST result as Kruskal but expands as a geographic blob. '
            f'Restricted to the top-{REDUCED_N} cities.'
        ),
        'phase': 5,
    },
    'euler_check': {
        'label':         'Euler Check',
        'problem':       'connectivity',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   None,
        'description':   (
            'Counts odd-degree cities. '
            '0 odd → Euler Circuit (every road once, back to start). '
            '2 odd → Euler Path (every road once, start ≠ end). '
            'Otherwise: neither — the Königsberg bridge problem.'
        ),
        'phase': 6,
    },
    'tsp_approx': {
        'label':         'TSP 2-Approx',
        'problem':       'connectivity',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   'weight',
        'description':   (
            'MST-based 2-approximation for the Traveling Salesman Problem (NP-complete). '
            'Builds MST, traverses via DFS preorder — visits all cities once. '
            f'Guaranteed ≤ 2× the optimal Hamilton cycle. '
            f'Runs on the {REDUCED_N}-city graph.'
        ),
        'phase': 6,
    },
    'articulation': {
        'label':         'Cut-Vertices & Bridges',
        'problem':       'connectivity',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   None,
        'description':   (
            'Tarjan DFS identifies cut-vertices (single-node failures that split the '
            'network) and bridges (single-edge failures). '
            'Cut-vertices shown in red; bridges drawn as red links. '
            'Based on 1.36. Definíció (k-connectivity).'
        ),
        'phase': 9,
    },
    'walk_count': {
        'label':         'Walk Count (A^k)',
        'problem':       'matrix',
        'needs_reduced': True,
        'needs_dst':     True,
        'weight_attr':   None,
        'extra_params':  [
            {'id': 'k', 'label': 'Walk length k', 'type': 'int',
             'default': 2, 'min': 1, 'max': 6},
        ],
        'description':   (
            'Counts walks of exactly length k using the 4.8. Theorem: '
            'A^k[src, dst] = number of k-hop routes (may revisit cities). '
            f'Computes on the {REDUCED_N}-city adjacency matrix.'
        ),
        'phase': 7,
    },
    'spanning_tree_count': {
        'label':         'Spanning Tree Count',
        'problem':       'matrix',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   None,
        'description':   (
            'Kirchhoff\'s Matrix-Tree Theorem: det(cofactor of L) counts all '
            f'distinct spanning trees. L = D − A. Runs on the {REDUCED_N}-city graph. '
            'Uses slogdet to handle counts that reach 10^300+.'
        ),
        'phase': 7,
    },
    'graph_coloring': {
        'label':         'Graph Coloring χ(G)',
        'problem':       'structural',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   None,
        'description':   (
            'Greedy largest-first assigns each city the smallest colour '
            'unused by its neighbours. Computes χ(G) (chromatic number). '
            f'Runs on the {REDUCED_N}-city graph. '
            "Brooks' theorem: χ ≤ Δ for most graphs. "
            '4-Color theorem: any planar map needs ≤ 4 colours.'
        ),
        'phase': 8,
    },
    'planarity_check': {
        'label':         'Planarity Check',
        'problem':       'structural',
        'needs_reduced': True,
        'needs_dst':     False,
        'weight_attr':   None,
        'description':   (
            'Tests if the graph can be drawn without edge crossings. '
            'Boyer-Myrvold LR-planarity algorithm O(V+E). '
            'Kuratowski: planar ⟺ no K₅/K₃,₃ minor. '
            '4-Color theorem applies to all planar graphs.'
        ),
        'phase': 8,
    },
    'max_flow': {
        'label':         'Max-Flow / Min-Cut',
        'problem':       'flow',
        'needs_reduced': True,
        'needs_dst':     True,
        'weight_attr':   'capacity',
        'description':   (
            'Edmonds-Karp (BFS Ford-Fulkerson): finds maximum concurrent '
            'logistics throughput from source to sink. '
            'Min-Cut Theorem: max-flow = capacity of the bottleneck cut. '
            f'Road=1000, Ferry=200, Ocean=100 units. {REDUCED_N}-city graph.'
        ),
        'phase': 10,
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
    'mst': {
        'label':      'Spanning Tree Design',
        'algorithms': ['kruskal', 'prim'],
    },
    'connectivity': {
        'label':      'Connectivity Analysis',
        'algorithms': ['euler_check', 'tsp_approx', 'articulation'],
    },
    'matrix': {
        'label':      'Matrix Analysis',
        'algorithms': ['walk_count', 'spanning_tree_count'],
    },
    'structural': {
        'label':      'Structural Analysis',
        'algorithms': ['graph_coloring', 'planarity_check'],
    },
    'flow': {
        'label':      'Network Flow',
        'algorithms': ['max_flow'],
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
    """
    if len(steps) <= n:
        return steps
    head   = steps[:5]
    tail   = steps[-5:]
    mid    = steps[5:-5]
    stride = max(1, len(mid) // max(n - 10, 1))
    return head + mid[::stride] + tail


# ── Geo helpers ───────────────────────────────────────────────────────────────

def _path_to_geo(G: nx.Graph, path: list[str], city_by_name: dict) -> list[dict]:
    result    = []
    actual_km = 0.0
    for i, name in enumerate(path):
        ferry_hop = ocean_hop = False
        nd   = G.nodes[name]
        meta = city_by_name.get(name, {})
        if i > 0:
            prev = path[i - 1]
            if G.has_edge(prev, name):
                edge       = G[prev][name]
                actual_km += edge.get('dist_km', 0.0)
                ferry_hop  = edge.get('ferry', False)
                ocean_hop  = edge.get('ocean', False)
            else:
                # TSP shortcut: no direct road — use haversine as km estimate
                pnd        = G.nodes[prev]
                actual_km += haversine_km(pnd['lat'], pnd['lng'],
                                          nd['lat'],  nd['lng'])
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


def _tree_edges_to_geo(G: nx.Graph,
                       tree_edges: list[tuple[str, str]],
                       city_by_name: dict) -> list[dict]:
    """Convert MST edge pairs to lat/lng dicts for the frontend renderer."""
    result = []
    for u, v in tree_edges:
        nu   = G.nodes[u]
        nv   = G.nodes[v]
        edata = G[u][v]
        result.append({
            'u':       u,
            'v':       v,
            'lat1':    nu['lat'],
            'lng1':    nu['lng'],
            'lat2':    nv['lat'],
            'lng2':    nv['lng'],
            'dist_km': round(edata.get('dist_km', 0.0), 1),
            'weight':  round(edata.get('weight', 0.0), 1),
            'ferry':   edata.get('ferry', False),
            'ocean':   edata.get('ocean', False),
        })
    return result


def _city_coords_for_steps(G: nx.Graph,
                            steps: list[StepEvent],
                            mentioned_names: list[str],
                            city_by_name: dict) -> dict:
    """
    Build {name: {lat, lng, country}} for every city referenced in steps
    and the explicitly provided name list (path nodes or tree nodes).
    """
    mentioned: set[str] = set(mentioned_names)
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


# ── Extra-param coercion ──────────────────────────────────────────────────────

def _coerce(param_spec: dict, raw_value) -> int | float | str:
    """Cast a raw extra-param value to the type declared in the registry."""
    t = param_spec.get('type', 'int')
    try:
        if t == 'int':
            v = int(raw_value)
            return max(param_spec.get('min', v), min(param_spec.get('max', v), v))
        if t == 'float':
            return float(raw_value)
    except (TypeError, ValueError):
        pass
    return param_spec.get('default', raw_value)


# ── Solver ────────────────────────────────────────────────────────────────────

def solve(conn_str: str, problem: str, algorithm: str,
          src: str, dst: str, params: dict | None = None) -> dict:
    """
    Route a solve request to the appropriate algorithm generator.

    Algorithms with needs_dst=False (MST, global checks) skip the dst
    validation and receive dst=None.  The response includes result_type
    ('path' or 'tree') so the frontend can choose the correct renderer.
    """
    if algorithm not in ALGORITHM_REGISTRY:
        return {'error': f'Unknown algorithm: {algorithm!r}'}
    meta = ALGORITHM_REGISTRY[algorithm]

    cache        = (get_reduced_graph(conn_str)
                    if meta['needs_reduced']
                    else get_full_graph(conn_str))
    G            = cache['graph']
    city_by_name = cache['city_by_name']

    needs_dst = meta.get('needs_dst', True)

    if src not in G.nodes:
        return {'error': f'City not found: {src!r}'}
    if needs_dst and dst not in G.nodes:
        return {'error': f'City not found: {dst!r}'}

    weight_attr   = meta['weight_attr'] or 'weight'
    effective_dst = dst if needs_dst else None
    extra_params  = {p['id']: _coerce(p, (params or {}).get(p['id'], p['default']))
                     for p in meta.get('extra_params', [])}
    runner        = _ALGO_RUNNERS.get(algorithm)

    # ── Algorithms with real generators ──────────────────────────────────
    if runner:
        raw = list(runner(G, src, effective_dst, weight=weight_attr, **extra_params))

        terminal    = next((s for s in reversed(raw) if s.type in _TERMINAL), None)
        visit_steps = [s for s in raw if s.type not in _TERMINAL]

        if terminal is None:
            return {'error': 'Algorithm produced no terminal event'}
        if terminal.type == 'error':
            return {'error': terminal.flags.get('message', 'Algorithm error')}
        if terminal.type == 'no_path':
            return {'error': f'No route found: {src!r} → {dst!r}'}

        throttled = _throttle(visit_steps, MAX_ANIM_STEPS)
        throttled.append(terminal)

        n_visited = sum(1 for s in visit_steps
                        if s.type in ('visit_node', 'pivot_node', 'color_node'))

        base = {
            'algorithm':    algorithm,
            'algo_label':   meta['label'],
            'problem':      problem,
            'src':          src,
            'dst':          dst,
            'graph_mode':   'reduced' if meta['needs_reduced'] else 'full',
            'n_nodes':      G.number_of_nodes(),
            'n_edges':      G.number_of_edges(),
            'n_visited':    n_visited,
            'steps':        [s.to_dict() for s in throttled],
            'warnings':     [],
            'has_extended': cache.get('has_extended', False),
        }

        # ── Tree result (MST algorithms) ──────────────────────────────
        if terminal.type == 'found_tree':
            tree_edges_raw = terminal.flags.get('tree_edges', [])
            tree_geo       = _tree_edges_to_geo(G, tree_edges_raw, city_by_name)
            all_cities     = [c for e in tree_edges_raw for c in e]
            total_km       = sum(G[u][v].get('dist_km', 0.0) for u, v in tree_edges_raw)
            total_cost     = sum(G[u][v].get(weight_attr, 0.0) for u, v in tree_edges_raw)
            return {
                **base,
                'result_type': 'tree',
                'path':        [],
                'tree_edges':  tree_geo,
                'total_km':    round(total_km, 1),
                'total_cost':  round(total_cost, 3),
                'hop_count':   len(tree_edges_raw),
                'confidence':  None,
                'city_coords': _city_coords_for_steps(G, throttled, all_cities, city_by_name),
            }

        # ── Analysis result (Euler check, planarity, matrix, articulation) ──
        if terminal.type == 'found_analysis':
            analysis    = terminal.flags
            all_cities  = [s.node for s in visit_steps if s.node]
            # Convert bridge pairs to geo so the frontend can draw them
            raw_bridges = analysis.get('bridges', [])
            bridge_geo  = (_tree_edges_to_geo(G, raw_bridges, city_by_name)
                           if raw_bridges else [])
            return {
                **base,
                'result_type': 'analysis',
                'path':        [],
                'tree_edges':  bridge_geo,
                'total_km':    0,
                'total_cost':  0,
                'hop_count':   0,
                'confidence':  None,
                'analysis':    analysis,
                'city_coords': _city_coords_for_steps(G, throttled, all_cities, city_by_name),
            }

        # ── Coloring result (graph_coloring) ─────────────────────────
        if terminal.type == 'found_coloring':
            flags    = terminal.flags
            coloring = flags.get('coloring', {})
            return {
                **base,
                'result_type':      'coloring',
                'path':             [],
                'tree_edges':       [],
                'total_km':         0,
                'total_cost':       0,
                'hop_count':        0,
                'confidence':       None,
                'coloring':         coloring,
                'chromatic_number': flags.get('chromatic_number', 0),
                'verdict':          flags.get('verdict', ''),
                'detail':           flags.get('detail', ''),
                'city_coords': _city_coords_for_steps(
                    G, throttled, list(coloring.keys()), city_by_name),
            }

        # ── Path result (navigation / traversal algorithms) ───────────
        path_names = terminal.flags.get('path', [])
        if not path_names:
            return {'error': f'No route found: {src!r} → {dst!r}'}

        def _edge_val(u: str, v: str, attr: str, fallback: float = 0.0) -> float:
            if G.has_edge(u, v):
                return G[u][v].get(attr, fallback)
            if attr == 'dist_km':
                nu, nv = G.nodes[u], G.nodes[v]
                return haversine_km(nu['lat'], nu['lng'], nv['lat'], nv['lng'])
            return fallback

        path_geo   = _path_to_geo(G, path_names, city_by_name)
        total_km   = sum(_edge_val(path_names[i], path_names[i + 1], 'dist_km')
                         for i in range(len(path_names) - 1))
        total_cost = sum(_edge_val(path_names[i], path_names[i + 1], weight_attr)
                         for i in range(len(path_names) - 1))
        confidence = (round(math.exp(-total_cost), 4)
                      if algorithm == 'reliability' else None)

        return {
            **base,
            'result_type': 'path',
            'path':        path_geo,
            'tree_edges':  [],
            'total_km':    round(total_km, 1),
            'total_cost':  round(total_cost, 3),
            'hop_count':   len(path_names) - 1,
            'confidence':  confidence,
            'city_coords': _city_coords_for_steps(G, throttled, path_names, city_by_name),
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
        'result_type':  'path',
        'algorithm':    algorithm,
        'algo_label':   meta['label'],
        'problem':      problem,
        'src':          src,
        'dst':          dst,
        'path':         path_geo,
        'tree_edges':   [],
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
