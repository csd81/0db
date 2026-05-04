"""
Shared fixtures for routing tests.
The graph is loaded from SQL once per pytest session (~1-2 s) and reused
across all test modules — 52k edges, 14k nodes, zero repeated SQL round-trips.
"""
import math
import os

import networkx as nx
import pyodbc
import pytest
from dotenv import load_dotenv
from pathlib import Path

_REPO = Path(__file__).parent.parent
load_dotenv(_REPO / 'northwind-control-center' / '.env')
load_dotenv(_REPO / '.env', override=False)

FERRY_PENALTY = 1.5
OCEAN_PENALTY = 5.0
ASTAR_EPSILON = 1.1
R             = 6371.0
MEGACITY_POP  = 5_000_000


def _conn_str() -> str:
    return (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={os.environ['SQL_SERVER']};DATABASE=EuropeGraph;"
        f"UID={os.environ.get('SQL_SA_USERNAME') or os.environ.get('SQL_USERNAME')};"
        f"PWD={os.environ.get('SQL_SA_PASSWORD') or os.environ.get('SQL_PASSWORD')};"
        f"Encrypt={os.environ.get('SQL_ENCRYPT', 'yes')};"
        f"TrustServerCertificate={os.environ.get('SQL_TRUST_SERVER_CERT', 'yes')};"
    )


def hav_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlng / 2) ** 2)
    return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


@pytest.fixture(scope='session')
def G() -> nx.Graph:
    """Load full EuropeGraph into NetworkX once per test session."""
    conn = pyodbc.connect(_conn_str())
    cur  = conn.cursor()
    graph = nx.Graph()

    cur.execute('SELECT Name, Lat, Lng FROM EuropeGraph.dbo.EuropeCity')
    for r in cur.fetchall():
        graph.add_node(r[0], lat=float(r[1]), lng=float(r[2]))

    cur.execute(
        'SELECT c1.Name, c2.Name, r.DistanceKM, r.CrossingType '
        'FROM EuropeGraph.dbo.EuropeRoad r '
        'JOIN EuropeGraph.dbo.EuropeCity c1 ON c1.CityID = r.FromCityID '
        'JOIN EuropeGraph.dbo.EuropeCity c2 ON c2.CityID = r.ToCityID'
    )
    for r in cur.fetchall():
        d = float(r[2]); c = int(r[3])
        w = d * OCEAN_PENALTY if c == 2 else d * FERRY_PENALTY if c == 1 else d
        graph.add_edge(r[0], r[1], weight=w, dist_km=d, crossing=c)

    conn.close()
    print(f'\n[conftest] Graph loaded: {graph.number_of_nodes():,} nodes, '
          f'{graph.number_of_edges():,} edges')
    return graph


@pytest.fixture(scope='session')
def megacities(G: nx.Graph) -> list[str]:
    """Cities with population >= 5M (city-proper, GeoNames) that are in the graph."""
    conn = pyodbc.connect(_conn_str()); cur = conn.cursor()
    cur.execute(
        f'SELECT Name FROM EuropeGraph.dbo.EuropeCity WHERE Population >= {MEGACITY_POP}'
    )
    cities = [r[0] for r in cur.fetchall() if r[0] in G.nodes]
    conn.close()
    return cities
