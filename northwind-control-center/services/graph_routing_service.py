"""
SQL Server Graph DB demo — Afro-Eurasia + Islands City Routing
State machine + A* shortest-path visualiser

Data source: EuropeGraph.dbo.EuropeCity / EuropeGraph.dbo.EuropeRoad
(pre-populated relational tables on the same SQL Server instance)

Ferry bridges (IsFerry=1) use a 1.5× weight penalty so A* prefers land routes.
Actual km is stored separately for display.
"""
FERRY_PENALTY  = 1.5   # matches generator; lower = ferries treated as near-normal roads
OCEAN_PENALTY  = 5.0   # intercontinental shipping lane corridors (CrossingType=2)
ASTAR_EPSILON  = 1.1   # weighted A*: h × ε — 1.1 keeps near-optimality, avoids Arctic greed
import heapq
import math
import threading

import networkx as nx
import pyodbc

# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------
_GR_LOCK        = threading.Lock()
_GR_STEP_EVENT  = threading.Event()
_GR_ABORTED     = False

_STATE_DEFAULTS: dict = {
    'phase':            'idle',
    'phase_label':      '',
    'waiting_for_step': False,
    'start_city':       None,
    'end_city':         None,

    # populated after seeding; sent to JS for Leaflet markers
    'cities': [],        # [{id, name, country, lat, lng, population}]

    # A* animation
    'visited':      [],  # settled city names (list, ordered)
    'current_city': None,
    'frontier':     [],  # [(name, dist_km)] max 8, sorted asc
    'distances':    {},  # {name: dist_km} — only discovered nodes

    # SQL Server SHORTEST_PATH result (educational, unweighted)
    'sqlserver_route': [],
    'sqlserver_hops':  0,

    # final result
    'path':           [],   # [{name, country, lat, lng, dist_from_start}]
    'total_distance': None,
    'hop_count':      0,

    # SQL ticker
    'sql_log':     [],
    'current_sql': '',

    'error':    None,
    'conn_str': '',
}

_GR_STATE: dict = {k: v for k, v in _STATE_DEFAULTS.items()}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _gr_log(sql: str) -> None:
    with _GR_LOCK:
        _GR_STATE['sql_log'].append(sql)
        _GR_STATE['current_sql'] = sql


def _gr_step(**updates) -> bool:
    """Update state, pause until JS fires /step, return True if aborted."""
    with _GR_LOCK:
        _GR_STATE.update(updates)
        _GR_STATE['waiting_for_step'] = True
    _GR_STEP_EVENT.wait()
    _GR_STEP_EVENT.clear()
    with _GR_LOCK:
        _GR_STATE['waiting_for_step'] = False
    return _GR_ABORTED


def _load_from_db(cur) -> tuple[list, dict]:
    """
    Pull cities and edge count from EuropeGraph.dbo.*.
    Returns (cities_list, city_by_name_dict).
    """
    cur.execute(
        "SELECT CityID, Name, Country, Lat, Lng, Population "
        "FROM EuropeGraph.dbo.EuropeCity ORDER BY CityID"
    )
    cities = [
        {'id': r[0], 'name': r[1], 'country': r[2],
         'lat': float(r[3]), 'lng': float(r[4]), 'population': int(r[5])}
        for r in cur.fetchall()
    ]
    city_by_name = {c['name']: c for c in cities}
    return cities, city_by_name


# ---------------------------------------------------------------------------
# A* step generator
# ---------------------------------------------------------------------------
def _astar_steps(G: nx.Graph, start: str, end: str):
    """
    Yield (step_dict, is_done) for each A* node settlement.
    Final yield has is_done=True and step_dict['path'] is the reconstructed path.

    Uses weighted A* (ε = ASTAR_EPSILON) so the heuristic dominates on long
    routes — prevents the algorithm from expanding every village in France
    while searching for Tokyo.  ε=1.5 is suboptimal by at most 50 % but
    visits ~10× fewer nodes in practice.

    Frontier is maintained as a dict (discovered but not settled) so the
    O(N) scan over all 7k+ nodes is eliminated — O(|frontier|) per step instead.
    """
    def h(u: str) -> float:
        nu, nv = G.nodes[u], G.nodes[end]
        return _haversine_km(nu['lat'], nu['lng'], nv['lat'], nv['lng'])

    dist_g: dict[str, float] = {start: 0.0}
    prev:   dict[str, str | None] = {start: None}
    # discovered: name → g-score for nodes seen but not yet settled
    discovered: dict[str, float] = {start: 0.0}
    pq      = [(ASTAR_EPSILON * h(start), 0.0, start)]
    visited: set = set()

    while pq:
        _, d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        discovered.pop(u, None)   # settled — remove from open set

        is_done = (u == end)

        # Frontier: top-8 closest discovered (not yet settled) nodes by g-score
        frontier = sorted(discovered.items(), key=lambda kv: kv[1])[:8]
        frontier = [(name, round(g, 1)) for name, g in frontier]

        # distances_snap: only discovered nodes (compact; frontend colours them)
        distances_snap = {k: round(v, 1) for k, v in discovered.items()}
        distances_snap[u] = round(d, 1)   # include the just-settled node

        path_out: list = []
        if is_done:
            node: str | None = end
            while node is not None:
                path_out.append(node)
                node = prev.get(node)
            path_out.reverse()

        yield {
            'visited':      list(visited),
            'current_city': u,
            'frontier':     frontier,
            'distances':    distances_snap,
            'path':         path_out,
        }, is_done

        if is_done:
            break

        for v in G.neighbors(u):
            nd = d + G[u][v]['weight']
            if nd < dist_g.get(v, float('inf')):
                dist_g[v]     = nd
                prev[v]       = u
                discovered[v] = nd
                heapq.heappush(pq, (nd + ASTAR_EPSILON * h(v), nd, v))


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------
def _gr_worker(conn_str: str, start: str, end: str) -> None:
    global _GR_ABORTED
    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=30)
        cur  = conn.cursor()

        # ── 1. SEED NODES — from EuropeGraph.dbo.EuropeCity ─────────────────
        _gr_step(phase='seeding_nodes',
                 phase_label='Reading EuropeGraph.dbo.EuropeCity …')
        if _GR_ABORTED:
            return

        _gr_log(
            "-- Source: pre-populated relational table (not XML)\n"
            "SELECT CityID, Name, Country, Lat, Lng, Population\n"
            "FROM   EuropeGraph.dbo.EuropeCity\n"
            "ORDER  BY CityID;"
        )
        cities, city_by_name = _load_from_db(cur)

        ddl_node = (
            "IF OBJECT_ID('GraphRoad','U') IS NOT NULL DROP TABLE GraphRoad;\n"
            "IF OBJECT_ID('GraphCity','U') IS NOT NULL DROP TABLE GraphCity;\n"
            "CREATE TABLE [GraphCity] (\n"
            "    CityID     INT           NOT NULL,\n"
            "    Name       NVARCHAR(100) NOT NULL,\n"
            "    Country    NVARCHAR(10)  NULL,\n"
            "    Lat        FLOAT         NOT NULL,\n"
            "    Lng        FLOAT         NOT NULL,\n"
            "    Population INT           NULL\n"
            ") AS NODE;"
        )
        _gr_log(ddl_node)
        cur.execute("IF OBJECT_ID('GraphRoad','U') IS NOT NULL DROP TABLE GraphRoad")
        cur.execute("IF OBJECT_ID('GraphCity','U') IS NOT NULL DROP TABLE GraphCity")
        cur.execute(
            "CREATE TABLE [GraphCity]("
            "CityID INT NOT NULL, Name NVARCHAR(100) NOT NULL,"
            "Country NVARCHAR(10) NULL, Lat FLOAT NOT NULL,"
            "Lng FLOAT NOT NULL, Population INT NULL) AS NODE"
        )

        insert_cities_sql = (
            f"-- Cross-database INSERT: {len(cities)} cities\n"
            "INSERT INTO [GraphCity] (CityID, Name, Country, Lat, Lng, Population)\n"
            "SELECT CityID, Name, Country, Lat, Lng, Population\n"
            "FROM   EuropeGraph.dbo.EuropeCity;"
        )
        _gr_log(insert_cities_sql)
        cur.execute(
            "INSERT INTO [GraphCity](CityID,Name,Country,Lat,Lng,Population)"
            " SELECT CityID,Name,Country,Lat,Lng,Population"
            " FROM EuropeGraph.dbo.EuropeCity"
        )

        cities_for_state = cities  # already dicts with id/name/country/lat/lng/population
        if _gr_step(phase='seeding_nodes',
                    phase_label=f'GraphCity seeded — {len(cities)} cities',
                    cities=cities_for_state):
            return

        # ── 2. SEED EDGES — from EuropeGraph.dbo.EuropeRoad (bidirectional) ──
        ddl_edge = "CREATE TABLE [GraphRoad] (DistanceKM FLOAT NOT NULL) AS EDGE;"
        _gr_log(ddl_edge)
        cur.execute("CREATE TABLE [GraphRoad](DistanceKM FLOAT NOT NULL) AS EDGE")

        cur.execute("SELECT COUNT(*) FROM EuropeGraph.dbo.EuropeRoad")
        edge_count = cur.fetchone()[0]

        insert_edges_sql = (
            f"-- {edge_count:,} bidirectional rows from EuropeGraph.dbo.EuropeRoad\n"
            "-- $node_id resolved via JOIN on CityID (no Python loop needed)\n"
            "INSERT INTO [GraphRoad] ($from_id, $to_id, DistanceKM)\n"
            "SELECT c1.$node_id, c2.$node_id, r.DistanceKM\n"
            "FROM   EuropeGraph.dbo.EuropeRoad r\n"
            "JOIN   [GraphCity] c1 ON c1.CityID = r.FromCityID\n"
            "JOIN   [GraphCity] c2 ON c2.CityID = r.ToCityID;"
        )
        _gr_log(insert_edges_sql)
        cur.execute(
            "INSERT INTO [GraphRoad]($from_id,$to_id,DistanceKM)"
            " SELECT c1.$node_id,c2.$node_id,r.DistanceKM"
            " FROM EuropeGraph.dbo.EuropeRoad r"
            " JOIN [GraphCity] c1 ON c1.CityID=r.FromCityID"
            " JOIN [GraphCity] c2 ON c2.CityID=r.ToCityID"
        )

        if _gr_step(phase='seeding_edges',
                    phase_label=f'GraphRoad seeded — {edge_count:,} directed edges'):
            return

        # ── 3. SQL SERVER SHORTEST_PATH (educational) ────────────────────
        sp_sql = (
            "-- SQL Server Graph SHORTEST_PATH\n"
            "-- Finds min HOPS, NOT min km distance\n"
            "SELECT TOP 1\n"
            f"    c1.Name AS Origin,\n"
            f"    STRING_AGG(c2.Name,' → ') WITHIN GROUP (GRAPH PATH) AS Route,\n"
            f"    COUNT(c2.CityID)           WITHIN GROUP (GRAPH PATH) AS Hops\n"
            f"FROM GraphCity        AS c1,\n"
            f"     GraphRoad FOR PATH AS e,\n"
            f"     GraphCity FOR PATH AS c2\n"
            f"WHERE MATCH(SHORTEST_PATH(c1-(e)->c2+))\n"
            f"  AND c1.Name = '{start}'\n"
            f"  AND LAST_VALUE(c2.Name) WITHIN GROUP (GRAPH PATH) = '{end}'\n"
            f"ORDER BY Hops;\n"
            f"-- ⚠ Minimises hop count — NOT road distance.\n"
            f"-- ⚠ Use A* (below) for true km-shortest routing."
        )
        _gr_log(sp_sql)

        sp_route: list = []
        sp_hops         = 0
        try:
            cur.execute(
                "SELECT TOP 1 "
                "  STRING_AGG(c2.Name,' -> ') WITHIN GROUP (GRAPH PATH) AS Route,"
                "  COUNT(c2.CityID)           WITHIN GROUP (GRAPH PATH) AS Hops"
                " FROM [GraphCity] AS c1,"
                "      [GraphRoad] FOR PATH AS e,"
                "      [GraphCity] FOR PATH AS c2"
                " WHERE MATCH(SHORTEST_PATH(c1-(e)->c2+))"
                "   AND c1.Name = ? AND LAST_VALUE(c2.Name) WITHIN GROUP (GRAPH PATH) = ?"
                " ORDER BY Hops",
                (start, end)
            )
            row = cur.fetchone()
            if row and row[0]:
                sp_route = [s.strip() for s in row[0].split('->')]
                sp_hops  = int(row[1])
                _gr_log(
                    f"-- SHORTEST_PATH result: {' → '.join(sp_route)}\n"
                    f"-- Hops: {sp_hops}  (unweighted — may not be shortest km!)"
                )
        except pyodbc.Error as exc:
            _gr_log(f"-- SHORTEST_PATH not supported on this SQL Server version.\n-- {exc}")

        # Log educational XML shredding block
        xml_block = (
            "-- ─────────────────────────────────────────────────────────────\n"
            "-- Educational: SQL Server native XML shredding alternative\n"
            "-- (requires file accessible from server filesystem)\n"
            "-- ─────────────────────────────────────────────────────────────\n"
            "DECLARE @xml XML =\n"
            "  (SELECT CAST(BulkColumn AS XML)\n"
            "   FROM OPENROWSET(BULK 'C:\\data\\europe_graph.xml', SINGLE_BLOB) AS x);\n"
            "INSERT INTO GraphCity(CityID,Name,Country,Lat,Lng,Population)\n"
            "SELECT City.value('@id','INT'), City.value('@name','NVARCHAR(100)'),\n"
            "       City.value('@country','NVARCHAR(10)'), City.value('@lat','FLOAT'),\n"
            "       City.value('@lng','FLOAT'), City.value('@pop','INT')\n"
            "FROM @xml.nodes('/GraphData/Cities/City') AS Data(City);\n"
            "-- Demo uses Python ElementTree for portability (no file-path config needed)"
        )
        _gr_log(xml_block)

        if _gr_step(phase='querying_graph',
                    phase_label='SQL Server SHORTEST_PATH executed',
                    sqlserver_route=sp_route,
                    sqlserver_hops=sp_hops):
            return

        # ── 4. BUILD NETWORKX GRAPH — from EuropeGraph relational tables ───
        nx_sql = (
            "-- NetworkX weighted graph from EuropeGraph.dbo.EuropeRoad\n"
            f"-- Ferry (CrossingType=1): {FERRY_PENALTY}× penalty; "
            f"Ocean (CrossingType=2): {OCEAN_PENALTY}× penalty\n"
            "SELECT c1.Name AS src, c2.Name AS dst, r.DistanceKM, r.IsFerry, r.CrossingType\n"
            "FROM   EuropeGraph.dbo.EuropeRoad  r\n"
            "JOIN   EuropeGraph.dbo.EuropeCity  c1 ON c1.CityID = r.FromCityID\n"
            "JOIN   EuropeGraph.dbo.EuropeCity  c2 ON c2.CityID = r.ToCityID;"
        )
        _gr_log(nx_sql)

        G = nx.Graph()
        for c in cities:
            G.add_node(c['name'], lat=c['lat'], lng=c['lng'])

        cur.execute(
            "SELECT c1.Name, c2.Name, r.DistanceKM, r.IsFerry, r.CrossingType"
            " FROM EuropeGraph.dbo.EuropeRoad r"
            " JOIN EuropeGraph.dbo.EuropeCity c1 ON c1.CityID=r.FromCityID"
            " JOIN EuropeGraph.dbo.EuropeCity c2 ON c2.CityID=r.ToCityID"
        )
        for row in cur.fetchall():
            dist_km  = float(row[2])
            ferry    = bool(row[3])
            crossing = int(row[4])
            if crossing == 2:
                weight = dist_km * OCEAN_PENALTY
            elif crossing == 1:
                weight = dist_km * FERRY_PENALTY
            else:
                weight = dist_km
            G.add_edge(row[0], row[1], weight=weight, dist_km=dist_km, ferry=ferry,
                       ocean=(crossing == 2))

        _gr_log(
            f"-- NetworkX Graph ready: {G.number_of_nodes()} nodes,"
            f" {G.number_of_edges()} undirected edges"
        )

        if start not in G.nodes or end not in G.nodes:
            missing = start if start not in G.nodes else end
            _gr_step(phase='error',
                     phase_label=f'City not found in graph: {missing}',
                     error=f'City "{missing}" not found in the graph.')
            return

        if _gr_step(phase='building_networkx',
                    phase_label=(
                        f'NetworkX graph: {G.number_of_nodes()} nodes,'
                        f' {G.number_of_edges()} edges')):
            return

        # ── 5. A* STEP-BY-STEP ───────────────────────────────────────────
        last_step = None
        for step, is_done in _astar_steps(G, start, end):
            label = (
                f"A* settling: {step['current_city']}"
                f" ({step['distances'].get(step['current_city'], 0):.0f} km)"
            )
            frontier_log = '  |  '.join(
                f"{n}: {d} km" for n, d in step['frontier']
            )
            _gr_log(
                f"-- A* step: visited {step['current_city']}"
                f" (g={step['distances'].get(step['current_city'],0):.0f} km)\n"
                f"-- Frontier: {frontier_log or '(empty)'}"
            )
            if _gr_step(
                phase='running_astar',
                phase_label=label,
                visited=step['visited'],
                current_city=step['current_city'],
                frontier=step['frontier'],
                distances=step['distances'],
            ):
                return
            last_step = step
            if is_done:
                break

        if _GR_ABORTED:
            return

        # ── 6. FOUND PATH ────────────────────────────────────────────────
        path_names = (last_step or {}).get('path', [])
        if not path_names:
            _gr_step(phase='error',
                     phase_label=f'No path found between {start} and {end}',
                     error=f'A* could not reach "{end}" from "{start}" — graph may be disconnected.')
            return

        # Compute actual (unpenalized) km and flag crossing type per hop
        path_with_geo = []
        actual_dist   = 0.0
        for i, name in enumerate(path_names):
            ferry_hop = False
            ocean_hop = False
            if i > 0:
                prev_name = path_names[i - 1]
                edge      = G[prev_name][name]
                actual_dist += edge['dist_km']
                ferry_hop    = edge.get('ferry', False)   # CrossingType=1
                ocean_hop    = edge.get('ocean', False)   # CrossingType=2
            nd        = G.nodes[name]
            city_meta = city_by_name.get(name, {})
            path_with_geo.append({
                'name':            name,
                'country':         city_meta.get('country', ''),
                'lat':             nd['lat'],
                'lng':             nd['lng'],
                'dist_from_start': round(actual_dist, 1),
                'ferry':           ferry_hop,
                'ocean':           ocean_hop,
            })
        total_dist = round(actual_dist, 1)

        _gr_log(
            f"-- A* path found: {' → '.join(path_names)}\n"
            f"-- Total distance: {total_dist:.1f} km  |  Hops: {len(path_names)-1}"
        )

        if _gr_step(
            phase='found_path',
            phase_label=(
                f'Route found: {len(path_names)-1} hops,'
                f' {total_dist:.0f} km'
            ),
            path=path_with_geo,
            total_distance=round(total_dist, 1),
            hop_count=len(path_names) - 1,
        ):
            return

        _gr_step(phase='done', phase_label='Route complete')

    except Exception as exc:
        with _GR_LOCK:
            _GR_STATE['phase']       = 'error'
            _GR_STATE['phase_label'] = str(exc)
            _GR_STATE['error']       = str(exc)
    finally:
        try:
            conn.close()  # type: ignore[name-defined]
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def graph_routing_start(conn_str: str, start: str, end: str) -> None:
    global _GR_ABORTED, _GR_STATE
    # Abort any running worker
    _GR_ABORTED = True
    _GR_STEP_EVENT.set()

    import time
    time.sleep(0.1)

    with _GR_LOCK:
        _GR_ABORTED = False
        _GR_STATE   = {k: v for k, v in _STATE_DEFAULTS.items()}
        _GR_STATE['conn_str']   = conn_str
        _GR_STATE['start_city'] = start
        _GR_STATE['end_city']   = end
    _GR_STEP_EVENT.clear()

    t = threading.Thread(target=_gr_worker, args=(conn_str, start, end), daemon=True)
    t.start()


def graph_routing_get_state() -> dict:
    with _GR_LOCK:
        return dict(_GR_STATE)


def graph_routing_step() -> None:
    _GR_STEP_EVENT.set()


def graph_routing_cities(conn_str: str) -> list:
    """Return all cities sorted by population desc, for datalist pre-population."""
    conn = pyodbc.connect(conn_str, timeout=10)
    cur  = conn.cursor()
    cur.execute(
        "SELECT CityID, Name, Country, Population "
        "FROM EuropeGraph.dbo.EuropeCity "
        "ORDER BY Population DESC"
    )
    result = [
        {'id': int(r[0]), 'name': r[1], 'country': r[2], 'pop': int(r[3])}
        for r in cur.fetchall()
    ]
    conn.close()
    return result


def graph_routing_reset(conn_str: str) -> None:
    global _GR_ABORTED, _GR_STATE
    _GR_ABORTED = True
    _GR_STEP_EVENT.set()

    import time
    time.sleep(0.1)

    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=10)
        cur  = conn.cursor()
        for tbl in ('GraphRoad', 'GraphCity'):
            try:
                cur.execute(f"IF OBJECT_ID('{tbl}','U') IS NOT NULL DROP TABLE [{tbl}]")
            except Exception:
                pass
        conn.close()
    except Exception:
        pass

    with _GR_LOCK:
        _GR_ABORTED = False
        _GR_STATE   = {k: v for k, v in _STATE_DEFAULTS.items()}
    _GR_STEP_EVENT.clear()
