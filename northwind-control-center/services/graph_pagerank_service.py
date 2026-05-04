"""
PageRank city importance — Afro-Eurasia + Islands road network.

Loads cities and roads from EuropeGraph.dbo.*, builds an unweighted
undirected NetworkX graph, and runs nx.pagerank().  Unweighted PR
measures pure structural centrality: cities that bridge continents
(Istanbul, Cairo, Moscow) outrank dense-but-local clusters.

Result is cached in-process; restart Flask to refresh after a re-import.
"""
import networkx as nx
import pyodbc

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
        "SELECT c1.Name, c2.Name "
        "FROM EuropeGraph.dbo.EuropeRoad r "
        "JOIN EuropeGraph.dbo.EuropeCity c1 ON c1.CityID = r.FromCityID "
        "JOIN EuropeGraph.dbo.EuropeCity c2 ON c2.CityID = r.ToCityID"
    )
    for row in cur.fetchall():
        G.add_edge(row[0], row[1])

    cur.close()
    conn.close()

    pr       = nx.pagerank(G, max_iter=300)
    max_score = max(pr.values()) if pr else 1.0
    ranked   = sorted(pr.items(), key=lambda kv: kv[1], reverse=True)
    rank_map = {name: i + 1 for i, (name, _) in enumerate(ranked)}
    n        = len(cities)

    result_cities = []
    for c in cities:
        score = pr.get(c['name'], 0.0)
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
