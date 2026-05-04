"""
SQL Server Graph DB demo — European City Routing
State machine + A* shortest-path visualiser
"""
import heapq
import math
import os
import threading
import xml.etree.ElementTree as ET

import networkx as nx
import pyodbc

# ---------------------------------------------------------------------------
# XML path
# ---------------------------------------------------------------------------
_XML_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'europe_graph.xml')

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


def _load_xml():
    """Return (cities_list, edges_list) from europe_graph.xml."""
    tree = ET.parse(_XML_PATH)
    root = tree.getroot()
    cities = []
    for c in root.find('Cities'):
        cities.append({
            'id':         int(c.attrib['id']),
            'name':       c.attrib['name'],
            'country':    c.attrib['country'],
            'lat':        float(c.attrib['lat']),
            'lng':        float(c.attrib['lng']),
            'population': int(c.attrib['pop']),
        })
    edges = []
    for r in root.find('Roads'):
        edges.append({
            'from_id':  int(r.attrib['from']),
            'to_id':    int(r.attrib['to']),
            'distance': float(r.attrib['distance']),
        })
    return cities, edges


# ---------------------------------------------------------------------------
# A* step generator
# ---------------------------------------------------------------------------
def _astar_steps(G: nx.Graph, start: str, end: str):
    """
    Yield (step_dict, is_done) for each A* node settlement.
    Final yield has is_done=True and step_dict['path'] is the reconstructed path.
    """
    def heuristic(u: str, v: str) -> float:
        nu, nv = G.nodes[u], G.nodes[v]
        return _haversine_km(nu['lat'], nu['lng'], nv['lat'], nv['lng'])

    dist_g = {n: float('inf') for n in G.nodes}
    prev   = {n: None        for n in G.nodes}
    dist_g[start] = 0.0
    pq      = [(heuristic(start, end), 0.0, start)]
    visited: set = set()

    while pq:
        _, d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        is_done = (u == end)

        frontier = sorted(
            [(n, round(dist_g[n], 1))
             for n in G.nodes
             if n not in visited and dist_g[n] < float('inf')],
            key=lambda x: x[1])[:8]

        distances_snap = {
            k: round(v, 1)
            for k, v in dist_g.items()
            if v < float('inf')
        }

        # Reconstruct path only for final step
        path_out: list = []
        if is_done:
            node = end
            while node is not None:
                path_out.append(node)
                node = prev[node]
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
            if nd < dist_g[v]:
                dist_g[v] = nd
                prev[v]   = u
                heapq.heappush(pq, (nd + heuristic(v, end), nd, v))


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------
def _gr_worker(conn_str: str, start: str, end: str) -> None:
    global _GR_ABORTED
    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=30)
        cur  = conn.cursor()

        # ── 1. SEED NODES ────────────────────────────────────────────────
        _gr_step(phase='seeding_nodes', phase_label='Parsing europe_graph.xml …')
        if _GR_ABORTED:
            return

        cities, edges = _load_xml()
        city_by_id   = {c['id']: c for c in cities}

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

        city_rows = [
            (c['id'], c['name'], c['country'], c['lat'], c['lng'], c['population'])
            for c in cities
        ]
        insert_cities_sql = (
            f"-- Inserting {len(cities)} cities (executemany)\n"
            f"INSERT INTO [GraphCity] (CityID, Name, Country, Lat, Lng, Population)\n"
            f"VALUES (?, ?, ?, ?, ?, ?)"
        )
        _gr_log(insert_cities_sql)
        cur.executemany(
            "INSERT INTO [GraphCity](CityID,Name,Country,Lat,Lng,Population)"
            " VALUES(?,?,?,?,?,?)",
            city_rows
        )

        cities_for_state = [
            {'id': c['id'], 'name': c['name'], 'country': c['country'],
             'lat': c['lat'], 'lng': c['lng'], 'population': c['population']}
            for c in cities
        ]
        if _gr_step(phase='seeding_nodes',
                    phase_label=f'GraphCity seeded — {len(cities)} cities',
                    cities=cities_for_state):
            return

        # ── 2. SEED EDGES ────────────────────────────────────────────────
        ddl_edge = (
            "CREATE TABLE [GraphRoad] (DistanceKM FLOAT NOT NULL) AS EDGE;"
        )
        _gr_log(ddl_edge)
        cur.execute(
            "CREATE TABLE [GraphRoad](DistanceKM FLOAT NOT NULL) AS EDGE"
        )

        # Staging table + INSERT-SELECT with JOIN for fast graph edge load
        staging_sql = (
            "-- Fast bulk-load via staging table\n"
            "CREATE TABLE #EdgeStaging (FromID INT, ToID INT, Dist FLOAT);\n"
            f"-- Inserting {len(edges)*2:,} directed edges via executemany …\n"
            "INSERT INTO [GraphRoad] ($from_id, $to_id, DistanceKM)\n"
            "SELECT c1.$node_id, c2.$node_id, s.Dist\n"
            "FROM   #EdgeStaging s\n"
            "JOIN   [GraphCity] c1 ON c1.CityID = s.FromID\n"
            "JOIN   [GraphCity] c2 ON c2.CityID = s.ToID;"
        )
        _gr_log(staging_sql)

        cur.execute(
            "CREATE TABLE #EdgeStaging (FromID INT NOT NULL, ToID INT NOT NULL, Dist FLOAT NOT NULL)"
        )

        # Build bidirectional rows
        staging_rows: list = []
        for e in edges:
            fid, tid, d = e['from_id'], e['to_id'], e['distance']
            staging_rows.append((fid, tid, d))
            staging_rows.append((tid, fid, d))

        total = len(staging_rows)
        BATCH = 2000
        for i in range(0, total, BATCH):
            batch = staging_rows[i:i + BATCH]
            cur.executemany(
                "INSERT INTO #EdgeStaging(FromID,ToID,Dist) VALUES(?,?,?)",
                batch
            )
            if _GR_ABORTED:
                return
            pct = min(i + BATCH, total)
            with _GR_LOCK:
                _GR_STATE['phase_label'] = (
                    f'Staging edges: {pct:,} / {total:,} …'
                )

        _gr_log(
            f"-- Staged {total:,} rows → running INSERT-SELECT …\n"
            "INSERT INTO [GraphRoad] ($from_id, $to_id, DistanceKM)\n"
            "SELECT c1.$node_id, c2.$node_id, s.Dist\n"
            "FROM   #EdgeStaging s\n"
            "JOIN   [GraphCity] c1 ON c1.CityID = s.FromID\n"
            "JOIN   [GraphCity] c2 ON c2.CityID = s.ToID"
        )
        cur.execute(
            "INSERT INTO [GraphRoad]($from_id,$to_id,DistanceKM)"
            " SELECT c1.$node_id,c2.$node_id,s.Dist"
            " FROM #EdgeStaging s"
            " JOIN [GraphCity] c1 ON c1.CityID=s.FromID"
            " JOIN [GraphCity] c2 ON c2.CityID=s.ToID"
        )
        cur.execute("DROP TABLE #EdgeStaging")

        if _gr_step(phase='seeding_edges',
                    phase_label=f'GraphRoad seeded — {total:,} directed edges'):
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

        # ── 4. BUILD NETWORKX GRAPH ──────────────────────────────────────
        match_sql = (
            "-- Building NetworkX graph from SQL Server graph tables\n"
            "SELECT Name, Lat, Lng FROM [GraphCity];\n"
            "SELECT c1.Name AS src, c2.Name AS dst, e.DistanceKM\n"
            "FROM   [GraphCity] c1, [GraphRoad] e, [GraphCity] c2\n"
            "WHERE  MATCH(c1-(e)->c2);"
        )
        _gr_log(match_sql)

        cur.execute("SELECT Name, Lat, Lng FROM [GraphCity]")
        G = nx.Graph()
        for row in cur.fetchall():
            G.add_node(row[0], lat=float(row[1]), lng=float(row[2]))

        cur.execute(
            "SELECT c1.Name, c2.Name, e.DistanceKM"
            " FROM [GraphCity] c1, [GraphRoad] e, [GraphCity] c2"
            " WHERE MATCH(c1-(e)->c2)"
        )
        for row in cur.fetchall():
            G.add_edge(row[0], row[1], weight=float(row[2]))

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
        path_names    = (last_step or {}).get('path', [])
        total_dist    = 0.0
        path_with_geo = []
        for i, name in enumerate(path_names):
            d = 0.0
            if i > 0:
                prev_name = path_names[i - 1]
                d = G[prev_name][name]['weight']
            if path_with_geo:
                d = path_with_geo[-1]['dist_from_start'] + d
            else:
                d = 0.0
            nd = G.nodes[name]
            city_meta = next((c for c in cities if c['name'] == name), {})
            path_with_geo.append({
                'name':            name,
                'country':         city_meta.get('country', ''),
                'lat':             nd['lat'],
                'lng':             nd['lng'],
                'dist_from_start': round(
                    last_step['distances'].get(name, 0) if last_step else 0, 1
                ),
            })
        total_dist = last_step['distances'].get(end, 0.0) if last_step else 0.0

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
