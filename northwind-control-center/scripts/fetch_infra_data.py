"""
Global Infrastructure Digital Twin — Data Ingestion Script
===========================================================
Run once (or to refresh) to populate InfraNodes + InfraEdges in SQL Server.

Sources:
  1. TeleGeography Submarine Cable Map API (GitHub, free, public)
     → cable landing station coordinates + submarine cable edges
  2. PeeringDB REST API (free, no auth for basic queries)
     → IXP facility coordinates for major ASNs (Google, AWS, Azure, Meta)
  3. Hardcoded fallback catalogue (from global_infra_service.py)
     → cloud DCs, OpenAI Stargate, Starlink gateways, chokepoints

Usage:
  cd northwind-control-center
  python scripts/fetch_infra_data.py [--dry-run] [--drop]

Flags:
  --dry-run   Fetch & print stats, skip SQL writes
  --drop      DROP and recreate tables before import (full refresh)
"""
import sys, os, math, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import pyodbc
from dotenv import load_dotenv

load_dotenv()

# ── Connection ─────────────────────────────────────────────────────────────────
def _conn_str():
    driver   = os.environ.get('SQL_DRIVER', 'ODBC Driver 18 for SQL Server')
    server   = os.environ.get('SQL_SERVER', 'localhost')
    database = os.environ.get('SQL_DATABASE', 'Northwind')
    user     = os.environ.get('SQL_SA_USERNAME') or os.environ.get('SQL_USERNAME', '')
    pwd      = os.environ.get('SQL_SA_PASSWORD') or os.environ.get('SQL_PASSWORD', '')
    encrypt  = os.environ.get('SQL_ENCRYPT', 'yes')
    trust    = os.environ.get('SQL_TRUST_SERVER_CERT', 'yes')
    return (f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"UID={user};PWD={pwd};Encrypt={encrypt};TrustServerCertificate={trust};")

# ── SQL DDL ────────────────────────────────────────────────────────────────────
CREATE_NODES = """
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'InfraNodes'
)
CREATE TABLE InfraNodes (
    NodeID   INT IDENTITY(1,1) PRIMARY KEY,
    NodeKey  NVARCHAR(150) UNIQUE NOT NULL,
    Label    NVARCHAR(300),
    Provider NVARCHAR(100),
    Type     NVARCHAR(60),
    Latitude  DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    Source   NVARCHAR(50) DEFAULT 'hardcoded'
);
"""

CREATE_EDGES = """
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'InfraEdges'
)
CREATE TABLE InfraEdges (
    EdgeID     INT IDENTITY(1,1) PRIMARY KEY,
    SourceKey  NVARCHAR(150) NOT NULL,
    TargetKey  NVARCHAR(150) NOT NULL,
    EdgeType   NVARCHAR(50),
    DistanceKM FLOAT,
    LatencyMS  AS (CASE
        WHEN EdgeType = 'starlink_laser'  THEN DistanceKM / 300.0
        WHEN EdgeType = 'starlink_uplink' THEN 12.0
        ELSE                                   DistanceKM / 200.0
    END) PERSISTED,
    Source     NVARCHAR(50) DEFAULT 'auto'
);
"""

DROP_NODES = "IF OBJECT_ID('InfraNodes','U') IS NOT NULL DROP TABLE InfraNodes;"
DROP_EDGES = "IF OBJECT_ID('InfraEdges','U') IS NOT NULL DROP TABLE InfraEdges;"

# ── Haversine ──────────────────────────────────────────────────────────────────
def haversine(lat1, lng1, lat2, lng2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a  = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ── Source 1: TeleGeography submarine cable map ────────────────────────────────
TELEGEOGRAPHY_URL = (
    "https://raw.githubusercontent.com/telegeography/"
    "www.submarinecablemap.com/master/web/public/api/v3/cable/all.json"
)

def fetch_telegeography():
    """
    Returns (landing_nodes, cable_edges) from TeleGeography public API.

    landing_nodes: list of dicts with key/label/lat/lng/type
    cable_edges:   list of dicts with src/dst/type (deduped landing point pairs per cable)
    """
    print("Fetching TeleGeography submarine cable data …", end=" ", flush=True)
    try:
        resp = requests.get(TELEGEOGRAPHY_URL, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        print(f"OK ({len(data.get('cables', []))} cables)")
    except Exception as e:
        print(f"FAILED: {e}")
        return [], []

    # Index landing points by id
    lp_index = {}
    for lp in data.get("landing_points", []):
        lid   = lp.get("id", "")
        name  = lp.get("name", "") or lp.get("id", "")
        cntry = lp.get("country", "")
        lat   = lp.get("latitude")
        lng   = lp.get("longitude")
        if lat is None or lng is None:
            continue
        try:
            lat = float(lat)
            lng = float(lng)
        except (TypeError, ValueError):
            continue
        key = f"cls-tg-{lid.lower().replace(' ','-').replace(',','').replace('.','')[:40]}"
        lp_index[lid] = {
            "key":      key,
            "label":    f"{name}, {cntry}" if cntry else name,
            "provider": "Cable",
            "type":     "cable_landing",
            "lat":      lat,
            "lng":      lng,
            "source":   "telegeography",
        }

    # Collect landing point pairs per cable as edges
    edge_set = set()
    edges    = []
    for cable in data.get("cables", []):
        c_lps = cable.get("landing_points", [])
        # Connect consecutive pairs along the cable route
        for i in range(len(c_lps) - 1):
            a_id = c_lps[i] if isinstance(c_lps[i], str) else c_lps[i].get("id","")
            b_id = c_lps[i+1] if isinstance(c_lps[i+1], str) else c_lps[i+1].get("id","")
            if a_id not in lp_index or b_id not in lp_index:
                continue
            pair = tuple(sorted([a_id, b_id]))
            if pair in edge_set:
                continue
            edge_set.add(pair)
            na, nb = lp_index[a_id], lp_index[b_id]
            km = haversine(na["lat"], na["lng"], nb["lat"], nb["lng"])
            if km < 10:     # skip same-site duplicates
                continue
            edges.append({
                "src":   na["key"],
                "dst":   nb["key"],
                "type":  "submarine",
                "km":    round(km, 1),
                "source": "telegeography",
            })

    nodes = list(lp_index.values())
    print(f"  → {len(nodes)} landing stations, {len(edges)} cable edges")
    return nodes, edges


# ── Source 2: PeeringDB IXP facilities ────────────────────────────────────────
PEERINGDB_FAC_URL = "https://www.peeringdb.com/api/fac"
PEERINGDB_NET_URL = "https://www.peeringdb.com/api/net"

# ASNs of major cloud / network providers
TARGET_ASNS = {
    15169: ("GCP",       "cloud_dc"),
    16509: ("AWS",       "cloud_dc"),
    8075:  ("Azure",     "cloud_dc"),
    32934: ("Meta",      "cloud_dc"),
    2906:  ("Netflix",   "cloud_dc"),
    13335: ("Cloudflare","ixp"),
    714:   ("Apple",     "cloud_dc"),
}

def fetch_peeringdb_asn_facilities(asn, provider, node_type, existing_keys):
    """Fetch facilities for a single ASN from PeeringDB."""
    try:
        r = requests.get(f"{PEERINGDB_NET_URL}?asn={asn}", timeout=20,
                         headers={"User-Agent": "GlobalInfraDemo/1.0 (university research)"})
        r.raise_for_status()
        nets = r.json().get("data", [])
        if not nets:
            return []

        net = nets[0]
        fac_ids = [f["id"] for f in net.get("fac_set", [])]
        nodes   = []

        for fid in fac_ids:
            rf = requests.get(f"https://www.peeringdb.com/api/fac/{fid}", timeout=15,
                              headers={"User-Agent": "GlobalInfraDemo/1.0"})
            rf.raise_for_status()
            fac_data = rf.json().get("data", [{}])[0]
            lat = fac_data.get("latitude")
            lng = fac_data.get("longitude")
            if lat is None or lng is None:
                continue
            name    = fac_data.get("name", f"Facility {fid}")
            city    = fac_data.get("city", "")
            country = fac_data.get("country", "")
            label   = f"{provider} @ {name} ({city}, {country})" if city else f"{provider} @ {name}"
            key     = f"pdb-{asn}-{fid}"
            if key in existing_keys:
                continue
            nodes.append({
                "key": key, "label": label[:300],
                "provider": provider, "type": node_type,
                "lat": float(lat), "lng": float(lng),
                "source": "peeringdb",
            })
            time.sleep(0.3)   # rate-limit: be polite

        return nodes
    except Exception as e:
        print(f"    PeeringDB ASN {asn} failed: {e}")
        return []


def fetch_peeringdb_ixps():
    """Fetch major IXP facility locations from PeeringDB /api/ix."""
    print("Fetching PeeringDB IXP list …", end=" ", flush=True)
    try:
        r = requests.get("https://www.peeringdb.com/api/ix?limit=100",
                         timeout=30,
                         headers={"User-Agent": "GlobalInfraDemo/1.0"})
        r.raise_for_status()
        ixs = r.json().get("data", [])
        print(f"OK ({len(ixs)} IXPs)")
    except Exception as e:
        print(f"FAILED: {e}")
        return []

    nodes = []
    for ix in ixs[:80]:   # top 80 by peeringdb ordering (usually by member count)
        fac_set = ix.get("fac_set", [])
        for fac in fac_set[:1]:    # one facility per IXP is enough for our map
            lat = fac.get("latitude")
            lng = fac.get("longitude")
            if lat is None or lng is None:
                continue
            name    = ix.get("name", "IXP")
            city    = fac.get("city", "")
            country = fac.get("country", "")
            key     = f"pdb-ix-{ix['id']}"
            label   = f"{name} ({city}, {country})" if city else name
            nodes.append({
                "key": key, "label": label[:300],
                "provider": name, "type": "ixp",
                "lat": float(lat), "lng": float(lng),
                "source": "peeringdb",
            })
    print(f"  → {len(nodes)} IXP nodes from PeeringDB")
    return nodes


# ── Merge with hardcoded catalogue ─────────────────────────────────────────────
def merge_with_catalogue(fetched_nodes, fetched_edges):
    """
    Merge TeleGeography + PeeringDB data with the hardcoded service catalogue.
    Hardcoded nodes take priority (they have richer metadata).
    Fetched nodes fill in what's missing.
    Returns (all_nodes, all_edges).
    """
    # Import hardcoded data from the service
    from services.global_infra_service import NODES as CATALOGUE_NODES, BACKBONE_EDGES, CHOKEPOINT_LINKS

    cat_keys = {n["key"] for n in CATALOGUE_NODES}

    # De-duplicate fetched nodes by proximity to existing nodes (within 30km = same facility)
    def is_nearby_existing(lat, lng, existing):
        for en in existing:
            if haversine(lat, lng, en["lat"], en["lng"]) < 30:
                return True
        return False

    all_nodes = list(CATALOGUE_NODES)   # start with hardcoded
    for n in fetched_nodes:
        if n["key"] in cat_keys:
            continue
        if is_nearby_existing(n["lat"], n["lng"], all_nodes):
            continue    # skip near-duplicate
        all_nodes.append(n)

    # Build edge list: backbone edges from catalogue + fetched cable edges
    node_map = {n["key"]: n for n in all_nodes}
    all_edges = []

    for src, dst, etype in (BACKBONE_EDGES + CHOKEPOINT_LINKS):
        if src in node_map and dst in node_map:
            km = haversine(node_map[src]["lat"], node_map[src]["lng"],
                           node_map[dst]["lat"], node_map[dst]["lng"])
            all_edges.append({"src": src, "dst": dst, "type": etype, "km": round(km,1), "source": "catalogue"})

    for e in fetched_edges:
        if e["src"] in node_map and e["dst"] in node_map:
            all_edges.append(e)

    # Deduplicate edges
    seen = set()
    deduped = []
    for e in all_edges:
        key = tuple(sorted([e["src"], e["dst"]]))
        if key not in seen:
            seen.add(key)
            deduped.append(e)

    print(f"\nMerge result: {len(all_nodes)} nodes ({len(CATALOGUE_NODES)} hardcoded + {len(all_nodes)-len(CATALOGUE_NODES)} from APIs)")
    print(f"              {len(deduped)} edges")
    return all_nodes, deduped


# ── SQL import ─────────────────────────────────────────────────────────────────
def sql_import(nodes, edges, drop=False, dry_run=False):
    if dry_run:
        print("\n[dry-run] Would import to SQL Server:")
        print(f"  {len(nodes)} nodes → InfraNodes")
        print(f"  {len(edges)} edges → InfraEdges")
        return

    print("\nConnecting to SQL Server …", end=" ", flush=True)
    try:
        conn = pyodbc.connect(_conn_str(), timeout=15)
        cursor = conn.cursor()
        print("OK")
    except Exception as e:
        print(f"FAILED: {e}")
        print("Skipping SQL import. The service will use hardcoded data.")
        return

    cursor.fast_executemany = True

    if drop:
        print("Dropping existing tables …")
        cursor.execute(DROP_EDGES)
        cursor.execute(DROP_NODES)
        conn.commit()

    print("Creating tables (if not exist) …")
    cursor.execute(CREATE_NODES)
    conn.commit()
    cursor.execute(CREATE_EDGES)
    conn.commit()

    # Import nodes
    print(f"Importing {len(nodes)} nodes …", end=" ", flush=True)
    node_rows = [
        (n["key"], n["label"][:300], n["provider"][:100], n["type"][:60],
         n["lat"], n["lng"], n.get("source","hardcoded"))
        for n in nodes
    ]
    cursor.executemany(
        "IF NOT EXISTS (SELECT 1 FROM InfraNodes WHERE NodeKey=?) "
        "INSERT INTO InfraNodes (NodeKey,Label,Provider,Type,Latitude,Longitude,Source) "
        "VALUES (?,?,?,?,?,?,?)",
        [(r[0], *r) for r in node_rows]
    )
    conn.commit()
    print("OK")

    # Import edges
    print(f"Importing {len(edges)} edges …", end=" ", flush=True)
    edge_rows = [
        (e["src"][:150], e["dst"][:150], e["type"][:50], e["km"], e.get("source","auto"))
        for e in edges
    ]
    cursor.executemany(
        "IF NOT EXISTS (SELECT 1 FROM InfraEdges WHERE SourceKey=? AND TargetKey=?) "
        "INSERT INTO InfraEdges (SourceKey,TargetKey,EdgeType,DistanceKM,Source) "
        "VALUES (?,?,?,?,?)",
        [(r[0], r[1], *r) for r in edge_rows]
    )
    conn.commit()
    print("OK")

    conn.close()
    print(f"\nSQL import complete. InfraNodes and InfraEdges are ready.")
    print("The global_infra_service will load from SQL on next Flask startup.")


# ── Verify by querying back ────────────────────────────────────────────────────
def verify_sql():
    try:
        conn   = pyodbc.connect(_conn_str(), timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT Type, COUNT(*) FROM InfraNodes GROUP BY Type ORDER BY COUNT(*) DESC")
        print("\nSQL verification — InfraNodes by type:")
        for row in cursor.fetchall():
            print(f"  {row[0]:20s}  {row[1]:5d}")
        cursor.execute("SELECT EdgeType, COUNT(*), AVG(DistanceKM) FROM InfraEdges GROUP BY EdgeType")
        print("InfraEdges by type:")
        for row in cursor.fetchall():
            print(f"  {row[0]:20s}  {row[1]:5d}  avg {int(row[2])} km")
        conn.close()
    except Exception as e:
        print(f"Verify failed: {e}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Fetch global infrastructure data and import to SQL Server")
    parser.add_argument("--dry-run",  action="store_true", help="Fetch only, skip SQL writes")
    parser.add_argument("--drop",     action="store_true", help="DROP and recreate tables before import")
    parser.add_argument("--no-pdb",   action="store_true", help="Skip PeeringDB (faster, uses TeleGeography only)")
    parser.add_argument("--no-tg",    action="store_true", help="Skip TeleGeography (hardcoded catalogue only)")
    args = parser.parse_args()

    print("=" * 60)
    print("Global Infrastructure Digital Twin — Data Ingestion")
    print("=" * 60)

    fetched_nodes, fetched_edges = [], []

    # 1. TeleGeography
    if not args.no_tg:
        tg_nodes, tg_edges = fetch_telegeography()
        fetched_nodes.extend(tg_nodes)
        fetched_edges.extend(tg_edges)

    # 2. PeeringDB IXPs
    if not args.no_pdb:
        pdb_ixps = fetch_peeringdb_ixps()
        fetched_nodes.extend(pdb_ixps)

    # 3. Merge with hardcoded catalogue
    all_nodes, all_edges = merge_with_catalogue(fetched_nodes, fetched_edges)

    # 4. SQL import
    sql_import(all_nodes, all_edges, drop=args.drop, dry_run=args.dry_run)

    # 5. Verify
    if not args.dry_run:
        verify_sql()

    print("\nDone.")


if __name__ == "__main__":
    main()
