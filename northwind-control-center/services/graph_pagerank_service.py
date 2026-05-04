"""
Betweenness Centrality — global city importance via road network chokepoints.

Loads cities and penalty-weighted roads from EuropeGraph.dbo.*, builds a
NetworkX graph, and runs nx.betweenness_centrality(k=250, weight='weight').

Betweenness counts how many weighted shortest paths pass through each node.
Cities that sit on unavoidable corridors (Panama City, Istanbul, Cairo) rank
highest — not just dense local hubs. Ferry/ocean penalties push routes onto
real geographic chokepoints rather than open-water shortcuts.

Result is cached in-process; restart Flask to refresh after a re-import.
"""
import networkx as nx
import pyodbc

_FERRY_PENALTY = 1.5
_OCEAN_PENALTY = 5.0

_CACHE: dict | None = None


def _compute(conn_str: str) -> dict:
    conn = pyodbc.connect(conn_str)
    cur  = conn.cursor()

    cur.execute(
        "SELECT CityID, Name, Country, Lat, Lng, Population "
        "FROM EuropeGraph.dbo.EuropeCity ORDER BY CityID"
    )
    cities = [
        {'id': r[0], 'name': r[1], 'country': r[2],
         'lat': float(r[3]), 'lng': float(r[4]), 'population': int(r[5])}
        for r in cur.fetchall()
    ]

    G = nx.Graph()
    for c in cities:
        G.add_node(c['name'])

    cur.execute(
        "SELECT c1.Name, c2.Name, r.DistanceKM, r.CrossingType "
        "FROM EuropeGraph.dbo.EuropeRoad r "
        "JOIN EuropeGraph.dbo.EuropeCity c1 ON c1.CityID = r.FromCityID "
        "JOIN EuropeGraph.dbo.EuropeCity c2 ON c2.CityID = r.ToCityID"
    )
    for row in cur.fetchall():
        dist_km  = float(row[2])
        crossing = int(row[3])
        if crossing == 2:   weight = dist_km * _OCEAN_PENALTY
        elif crossing == 1: weight = dist_km * _FERRY_PENALTY
        else:               weight = dist_km
        G.add_edge(row[0], row[1], weight=weight)

    cur.close()
    conn.close()

    bc        = nx.betweenness_centrality(G, k=250, weight='weight')
    max_score = max(bc.values()) if bc else 1.0
    ranked    = sorted(bc.items(), key=lambda kv: kv[1], reverse=True)
    rank_map  = {name: i + 1 for i, (name, _) in enumerate(ranked)}
    n         = len(cities)

    result_cities = []
    for c in cities:
        score = bc.get(c['name'], 0.0)
        rank  = rank_map.get(c['name'], n)
        result_cities.append({
            **c,
            'pr_score': round(score, 9),
            'pr_norm':  round(score / max_score, 5),
            'pr_rank':  rank,
            'pr_pct':   round(rank / n, 5),   # 0 = top, 1 = bottom
        })

    top25 = sorted(result_cities, key=lambda x: x['pr_rank'])[:25]

    return {
        'cities':   result_cities,
        'top25':    top25,
        'n_cities': n,
        'n_edges':  G.number_of_edges(),
    }


def get_pagerank_data(conn_str: str) -> dict:
    global _CACHE
    if _CACHE is None:
        _CACHE = _compute(conn_str)
    return _CACHE


def invalidate_cache() -> None:
    global _CACHE
    _CACHE = None
