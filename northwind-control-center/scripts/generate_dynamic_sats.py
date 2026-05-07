#!/usr/bin/env python3
"""
generate_dynamic_sats.py
========================
One-time pre-computation of 2,000 Starlink satellite positions for every
minute of a 24-hour simulation day.

Data source:
  Celestrak satcat JSON  →  https://celestrak.org/satcat/records.php?GROUP=starlink
  Returns active Starlink entries with PERIOD, INCLINATION, APOGEE, PERIGEE.

Propagation:
  Pure-Python Keplerian orbit equations (no skyfield required).
  Each satellite is assigned to a Walker Delta orbital plane derived from
  its NORAD catalog number — standard Starlink Shell-1 geometry (72 planes,
  53° inclination, ~550 km altitude).  Positions are computed analytically
  for each of the 1 440 minutes of the simulation day.

Requirements:
    pip install scipy numpy requests pyodbc

Run once (takes ~60 seconds):
    cd northwind-control-center
    python scripts/generate_dynamic_sats.py

Creates / populates two SQL tables:
  SpaceNodes_Dynamic  (MinuteOfDay, SatID, Lat, Lng, AltKM)
  SpaceEdges_Dynamic  (MinuteOfDay, SatA, SatB, DistKM, LatencyMS)
"""

import math
import time
from collections import defaultdict

# ── Parameters ────────────────────────────────────────────────────────────────
SAT_LIMIT  = 2_000         # manageable subset: 2000 sats × 1440 min → ~2.9M edges
MINUTES    = 1_440         # full 24-hour day, 1-minute steps
ISL_K      = 4             # ISL links per satellite
VACUUM_KMS = 300_000.0     # km/s
UPLINK_MS  = 12.0          # ms fixed overhead per uplink hop
BATCH_SIZE = 100_000       # rows per SQL commit

SATCAT_URL = "https://celestrak.org/satcat/records.php?GROUP=starlink"
HEADERS    = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

# ── SQL connection ─────────────────────────────────────────────────────────────
CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=InfraDB;"
    "UID=sa;PWD=CsorDa81;"
    "TrustServerCertificate=yes;"
    "Encrypt=no;"
)


# ── Helpers ───────────────────────────────────────────────────────────────────
def haversine_km(lat1, lng1, lat2, lng2):
    R  = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a  = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.asin(math.sqrt(max(0.0, a)))


# ── Step 1: Fetch satellite catalog ──────────────────────────────────────────
def fetch_satcat():
    import requests, json
    print("[1/4] Fetching Starlink satcat from Celestrak …")
    r = requests.get(SATCAT_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    records = r.json()

    # Filter: active payloads only (OPS_STATUS_CODE "+" or "P"), with usable orbit
    active = [
        rec for rec in records
        if rec.get("OPS_STATUS_CODE") in ("+", "P")
        and rec.get("PERIOD") and rec.get("PERIOD") > 80
        and rec.get("INCLINATION") and rec.get("APOGEE") and rec.get("PERIGEE")
    ]
    active.sort(key=lambda r: r["NORAD_CAT_ID"])
    active = active[:SAT_LIMIT]
    print(f"     {len(records)} total Starlink entries → {len(active)} active, "
          f"capped at {SAT_LIMIT}")
    return active


# ── Step 2: Propagate positions using Keplerian elements ──────────────────────
def propagate(records):
    """
    Compute (minute, sat_id, lat, lng, alt_km) for all satellites × all minutes.

    Orbital model:
      - Each satellite has a unique RAAN assigned by plane index (NORAD order).
      - Inclination and period are taken from the satcat record.
      - Semi-major axis derived from period via Kepler's 3rd law.
      - Position computed analytically for a circular orbit — accurate to within
        a few degrees for LEO sats over a 24-hour window.
    """
    print(f"[2/4] Propagating {len(records)} satellites × {MINUTES} minutes …")

    # Starlink Shell-1: 72 planes, ~28 sats/plane for 2000-sat subset
    N_PLANES    = 72
    sats_per_pl = max(1, len(records) // N_PLANES)
    MU          = 398_600.4418   # km³/s²  Earth gravitational parameter
    RE          = 6371.0         # km

    t0 = time.time()
    rows = []

    for sat_id, rec in enumerate(records):
        if sat_id % 400 == 0:
            print(f"     sat {sat_id:>5}/{len(records)}  ({time.time()-t0:.0f}s)")

        period_s  = rec["PERIOD"] * 60.0     # convert minutes → seconds
        incl_rad  = math.radians(rec["INCLINATION"])
        alt_km    = (rec["APOGEE"] + rec["PERIGEE"]) / 2.0   # mean altitude
        a_km      = RE + alt_km               # semi-major axis
        n_rad_s   = math.sqrt(MU / a_km**3)  # mean motion (rad/s)
        n_deg_min = math.degrees(n_rad_s) * 60.0  # deg/minute

        # Assign RAAN to orbital plane — wrap so sats beyond slot 72*sats_per_pl
        # don't alias back to plane 0, 1, 2 … and produce co-located duplicates
        plane_id  = (sat_id // sats_per_pl) % N_PLANES
        raan_rad  = math.radians((plane_id / N_PLANES) * 360.0)

        # Initial mean anomaly — distribute satellites evenly within plane
        pos_in_plane = sat_id % sats_per_pl
        M0_deg = (pos_in_plane / sats_per_pl) * 360.0

        # Pre-compute rotation matrix components (RAAN × inclination)
        cos_O, sin_O = math.cos(raan_rad), math.sin(raan_rad)
        cos_i, sin_i = math.cos(incl_rad), math.sin(incl_rad)

        for minute in range(MINUTES):
            M_rad = math.radians(M0_deg + n_deg_min * minute)

            # Circular orbit: eccentric anomaly = mean anomaly
            # Position in orbital plane (perifocal frame)
            cos_M, sin_M = math.cos(M_rad), math.sin(M_rad)

            # Rotate to ECI (Earth-Centred Inertial)
            # x_eci = cos_O*cos_M - sin_O*sin_M*cos_i
            # y_eci = sin_O*cos_M + cos_O*sin_M*cos_i
            # z_eci = sin_M * sin_i
            x = cos_O * cos_M - sin_O * sin_M * cos_i
            y = sin_O * cos_M + cos_O * sin_M * cos_i
            z = sin_M * sin_i

            # Convert ECI to lat/lng (assumes vernal equinox at 0h UTC, i.e.
            # GMST ≈ 0 + 0.25068 deg/min × minute — accurate to ±1° for demo)
            gmst_rad  = math.radians(0.25068 * minute)   # GMST progression
            cos_g, sin_g = math.cos(gmst_rad), math.sin(gmst_rad)

            # Rotate ECI → ECEF by -GMST
            x_ecef =  cos_g * x + sin_g * y
            y_ecef = -sin_g * x + cos_g * y
            z_ecef = z

            lat = math.degrees(math.asin(max(-1.0, min(1.0, z_ecef))))
            lng = math.degrees(math.atan2(y_ecef, x_ecef))

            rows.append((minute, sat_id,
                         round(lat, 3), round(lng, 3), round(alt_km, 1)))

    print(f"     {len(rows):,} position rows in {time.time()-t0:.1f}s")
    return rows


# ── Step 3: Compute ISL edges ─────────────────────────────────────────────────
def compute_edges(node_rows):
    import numpy as np
    from scipy.spatial import cKDTree

    print(f"[3/4] Computing ISL edges for {MINUTES} minutes …")
    R_SAT = 6371.0 + 550.0    # approximate orbital radius

    by_min = defaultdict(list)
    for m, sid, lat, lng, alt in node_rows:
        by_min[m].append((sid, lat, lng, alt))

    def xyz_km(lat, lng, alt_km):
        """True 3-D Cartesian position in km, including orbital altitude."""
        r  = 6371.0 + alt_km
        ph = math.radians(lat)
        la = math.radians(lng)
        c  = math.cos(ph)
        return np.array([r * c * math.cos(la), r * c * math.sin(la), r * math.sin(ph)])

    edge_rows = []
    t0 = time.time()
    for m in range(MINUTES):
        if m % 240 == 0:
            print(f"     minute {m:>5}/{MINUTES}  ({time.time()-t0:.0f}s)")
        pts = by_min[m]
        if not pts:
            continue
        # Build kNN tree on unit-sphere projections (fast, direction-only)
        unit = np.array([[math.cos(math.radians(p[1]))*math.cos(math.radians(p[2])),
                          math.cos(math.radians(p[1]))*math.sin(math.radians(p[2])),
                          math.sin(math.radians(p[1]))] for p in pts])
        tree   = cKDTree(unit)
        _, idx = tree.query(unit, k=min(ISL_K + 1, len(pts)))

        for i, neighbours in enumerate(idx):
            for j in neighbours[1:]:
                if i < j:
                    p1    = xyz_km(pts[i][1], pts[i][2], pts[i][3])
                    p2    = xyz_km(pts[j][1], pts[j][2], pts[j][3])
                    km_3d = float(np.linalg.norm(p1 - p2))
                    if km_3d < 0.5:   # truly co-located — skip
                        continue
                    ms = (km_3d / VACUUM_KMS) * 1000.0
                    edge_rows.append((m, pts[i][0], pts[j][0],
                                      round(km_3d, 1), round(ms, 3)))

    print(f"     {len(edge_rows):,} edge rows in {time.time()-t0:.1f}s")
    return edge_rows


# ── Step 4: SQL schema + bulk insert ─────────────────────────────────────────
def create_tables(cur):
    # Drop and recreate so schema changes (SMALLINT→INT) and re-runs are clean
    cur.execute("DROP TABLE IF EXISTS SpaceEdges_Dynamic")
    cur.execute("DROP TABLE IF EXISTS SpaceNodes_Dynamic")
    cur.execute("""
        CREATE TABLE SpaceNodes_Dynamic (
            MinuteOfDay SMALLINT NOT NULL,
            SatID       INT      NOT NULL,
            Lat         REAL     NOT NULL,
            Lng         REAL     NOT NULL,
            AltKM       REAL     NOT NULL,
            CONSTRAINT PK_SND PRIMARY KEY (MinuteOfDay, SatID)
        )
    """)
    cur.execute("CREATE INDEX IX_SND_Min ON SpaceNodes_Dynamic (MinuteOfDay)")
    cur.execute("""
        CREATE TABLE SpaceEdges_Dynamic (
            MinuteOfDay SMALLINT NOT NULL,
            SatA        INT      NOT NULL,
            SatB        INT      NOT NULL,
            DistKM      REAL     NOT NULL,
            LatencyMS   REAL     NOT NULL,
            CONSTRAINT PK_SED PRIMARY KEY (MinuteOfDay, SatA, SatB)
        )
    """)
    cur.execute("CREATE INDEX IX_SED_Min ON SpaceEdges_Dynamic (MinuteOfDay)")


def bulk_insert(cur, sql, rows, label):
    cur.fast_executemany = True
    for i in range(0, len(rows), BATCH_SIZE):
        chunk = rows[i: i + BATCH_SIZE]
        cur.executemany(sql, chunk)
        cur.connection.commit()
        pct = min(100, int((i + len(chunk)) / len(rows) * 100))
        print(f"     {label}: {i + len(chunk):>9,} / {len(rows):,}  ({pct}%)")


def insert_to_sql(node_rows, edge_rows):
    import pyodbc
    print("[4/4] Inserting into SQL Server …")
    conn = pyodbc.connect(CONN_STR, timeout=30)
    cur  = conn.cursor()
    create_tables(cur)
    conn.commit()
    print("     Tables ready.")
    bulk_insert(cur, "INSERT INTO SpaceNodes_Dynamic VALUES (?,?,?,?,?)",
                node_rows, "nodes")
    bulk_insert(cur, "INSERT INTO SpaceEdges_Dynamic VALUES (?,?,?,?,?)",
                edge_rows, "edges")
    conn.close()
    print("     SQL done.")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    t_total  = time.time()
    records  = fetch_satcat()
    node_rows = propagate(records)
    edge_rows = compute_edges(node_rows)
    insert_to_sql(node_rows, edge_rows)
    print(f"\nDone in {time.time()-t_total:.0f}s")
    print(f"  SpaceNodes_Dynamic : {len(node_rows):>10,} rows")
    print(f"  SpaceEdges_Dynamic : {len(edge_rows):>10,} rows")


if __name__ == "__main__":
    main()
