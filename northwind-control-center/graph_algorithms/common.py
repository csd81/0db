"""
Shared types, graph cache, and utilities for the Graph Algorithm Laboratory.

Two graph modes:
  full    — all ~18k cities  (BFS / DFS / Dijkstra / A* / Reliability)
  reduced — top-N by pop     (Bellman-Ford / Floyd-Warshall — O(V²/V³) algorithms)

Edge weight attributes loaded per road:
  weight        — penalty-adjusted km  (A* / Dijkstra)
  bellman_weight — weight + CostAdjustment  (may be negative for BF demo)
  log_weight    — -log(reliability)    (Reliability / Viterbi-style routing)
  capacity      — int lanes            (flow algorithms)
"""
from __future__ import annotations
import math
import threading
from dataclasses import dataclass, field

import networkx as nx
import pyodbc

FERRY_PENALTY = 1.5
OCEAN_PENALTY = 5.0
REDUCED_N     = 200   # top cities by population for O(V²/V³) algorithms


# ── Step event ────────────────────────────────────────────────────────────────

@dataclass
class StepEvent:
    """
    One frame of algorithm animation.

    type values:
      visit_node      — node settled / popped from priority queue / stack
      enqueue         — node added to BFS queue
      push_stack      — node pushed to DFS stack
      relax_edge      — edge relaxed (Dijkstra / Bellman-Ford)
      negative_relax  — edge relaxed via a negative-cost hop (BF highlight)
      found_path      — final path reconstructed
      no_path         — source and destination are disconnected
      error           — fatal: negative cycle, missing city, etc.
    """
    type:   str
    node:   str | None = None
    source: str | None = None
    target: str | None = None
    cost:   float | None = None
    flags:  dict       = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'type':   self.type,
            'node':   self.node,
            'source': self.source,
            'target': self.target,
            'cost':   self.cost,
            'flags':  self.flags,
        }


# ── Graph cache ───────────────────────────────────────────────────────────────

_LOCK:            threading.Lock = threading.Lock()
_FULL_CACHE:     dict | None = None
_REDUCED_CACHE:  dict | None = None


def _build_graph(conn_str: str, top_n: int | None = None) -> dict:
    """
    Load cities and multi-weight edges from EuropeGraph.dbo.*.

    top_n  — if given, keep only the top_n cities by Population (reduced graph).

    Gracefully handles both the legacy schema (DistanceKM / IsFerry / CrossingType)
    and the extended schema (+ CostAdjustment / ReliabilityScore / Capacity).
    Falls back to sensible defaults when extended columns are absent.
    """
    conn = pyodbc.connect(conn_str, timeout=30)
    cur  = conn.cursor()

    cur.execute(
        "SELECT CityID, Name, Country, Lat, Lng, Population "
        "FROM EuropeGraph.dbo.EuropeCity ORDER BY Population DESC"
    )
    all_cities = [
        {'id': r[0], 'name': r[1], 'country': r[2],
         'lat': float(r[3]), 'lng': float(r[4]), 'population': int(r[5])}
        for r in cur.fetchall()
    ]
    cities       = all_cities[:top_n] if top_n else all_cities
    city_by_name = {c['name']: c for c in cities}
    allowed      = set(city_by_name)

    G = nx.Graph()
    for c in cities:
        G.add_node(c['name'], lat=c['lat'], lng=c['lng'])

    # Try extended schema first; fall back to legacy if new columns are absent.
    try:
        cur.execute(
            "SELECT c1.Name, c2.Name, r.DistanceKM, r.IsFerry, r.CrossingType,"
            "       r.CostAdjustment, r.ReliabilityScore, r.Capacity"
            " FROM EuropeGraph.dbo.EuropeRoad r"
            " JOIN EuropeGraph.dbo.EuropeCity c1 ON c1.CityID = r.FromCityID"
            " JOIN EuropeGraph.dbo.EuropeCity c2 ON c2.CityID = r.ToCityID"
        )
        road_rows    = cur.fetchall()
        has_extended = True
    except pyodbc.Error:
        cur.execute(
            "SELECT c1.Name, c2.Name, r.DistanceKM, r.IsFerry, r.CrossingType"
            " FROM EuropeGraph.dbo.EuropeRoad r"
            " JOIN EuropeGraph.dbo.EuropeCity c1 ON c1.CityID = r.FromCityID"
            " JOIN EuropeGraph.dbo.EuropeCity c2 ON c2.CityID = r.ToCityID"
        )
        road_rows    = cur.fetchall()
        has_extended = False

    for row in road_rows:
        u, v = row[0], row[1]
        if u not in allowed or v not in allowed:
            continue

        dist_km  = float(row[2])
        crossing = int(row[4])

        if has_extended:
            cost_adj    = float(row[5]) if row[5] is not None else 0.0
            reliability = float(row[6]) if row[6] is not None else 0.95
            capacity    = int(row[7])   if row[7] is not None else 100
        else:
            cost_adj    = 0.0
            reliability = 0.95
            capacity    = 100

        # Navigation weight — always non-negative (used by A* / Dijkstra)
        if crossing == 2:   nav_w = dist_km * OCEAN_PENALTY
        elif crossing == 1: nav_w = dist_km * FERRY_PENALTY
        else:               nav_w = dist_km

        # Bellman-Ford weight — CostAdjustment can make this negative
        bf_w = nav_w + cost_adj

        # Reliability weight: minimise −log(p) ≡ maximise ∏ p(edge)
        log_w = -math.log(max(reliability, 1e-9))

        G.add_edge(u, v,
            dist_km        = dist_km,
            weight         = nav_w,
            bellman_weight = bf_w,
            log_weight     = log_w,
            capacity       = capacity,
            reliability    = reliability,
            ferry          = bool(row[3]),
            ocean          = (crossing == 2),
        )

    conn.close()
    return {
        'graph':        G,
        'cities':       cities,
        'city_by_name': city_by_name,
        'has_extended': has_extended,
    }


def get_full_graph(conn_str: str) -> dict:
    """Return the full ~18k-node graph, building once and caching for the server lifetime."""
    global _FULL_CACHE
    if _FULL_CACHE is not None:
        return _FULL_CACHE
    with _LOCK:
        if _FULL_CACHE is None:
            _FULL_CACHE = _build_graph(conn_str)
    return _FULL_CACHE


def get_reduced_graph(conn_str: str) -> dict:
    """Return the top-REDUCED_N city graph for heavy O(V²/V³) algorithms."""
    global _REDUCED_CACHE
    if _REDUCED_CACHE is not None:
        return _REDUCED_CACHE
    with _LOCK:
        if _REDUCED_CACHE is None:
            _REDUCED_CACHE = _build_graph(conn_str, top_n=REDUCED_N)
    return _REDUCED_CACHE


def invalidate_caches() -> None:
    """Drop both caches — call after re-importing graph data into SQL Server."""
    global _FULL_CACHE, _REDUCED_CACHE
    with _LOCK:
        _FULL_CACHE    = None
        _REDUCED_CACHE = None


# ── Geometry ──────────────────────────────────────────────────────────────────

def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R    = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a    = (math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
            * math.sin(dlng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
