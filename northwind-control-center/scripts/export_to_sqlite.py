"""
Export MS SQL databases to SQLite fallback files.

Run once (or nightly) while SQL Server is reachable:
    cd northwind-control-center
    python scripts/export_to_sqlite.py

Writes:
    instance/fallback/northwind.db   — all Northwind user tables
    instance/fallback/europe.db      — EuropeCity + EuropeRoad
    instance/fallback/infra.db       — InfraNodes + InfraEdges
"""
import os
import sys
import sqlite3
import pyodbc

# ── Locate project root (one level above scripts/) ───────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Load connection string from Flask config without starting the app
from config import Config  # type: ignore
cfg = Config()

DRIVER   = cfg.SQL_DRIVER
SERVER   = cfg.SQL_SERVER
UID      = cfg.SQL_USERNAME
PWD      = cfg.SQL_PASSWORD
ENCRYPT  = cfg.SQL_ENCRYPT
TRUST    = cfg.SQL_TRUST_SERVER_CERT

OUT_DIR = os.path.join(ROOT, 'instance', 'fallback')
os.makedirs(OUT_DIR, exist_ok=True)


def _conn(database: str = 'master') -> pyodbc.Connection:
    cs = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={database};"
        f"UID={UID};"
        f"PWD={PWD};"
        f"Encrypt={ENCRYPT};"
        f"TrustServerCertificate={TRUST};"
    )
    return pyodbc.connect(cs, timeout=30)


def _sqlite(name: str) -> sqlite3.Connection:
    path = os.path.join(OUT_DIR, name)
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=WAL")
    return db


# ── EuropeGraph → europe.db ───────────────────────────────────────────────────
def export_europe():
    print("Exporting EuropeGraph …")
    src = _conn('EuropeGraph')
    dst = _sqlite('europe.db')
    cur = src.cursor()

    dst.execute("DROP TABLE IF EXISTS EuropeCity")
    dst.execute("""
        CREATE TABLE EuropeCity (
            CityID     INTEGER PRIMARY KEY,
            Name       TEXT,
            Country    TEXT,
            Lat        REAL,
            Lng        REAL,
            Population INTEGER
        )
    """)

    cur.execute("SELECT CityID,Name,Country,Lat,Lng,Population FROM EuropeCity")
    rows = cur.fetchall()
    dst.executemany("INSERT INTO EuropeCity VALUES (?,?,?,?,?,?)", rows)
    print(f"  EuropeCity: {len(rows)} rows")

    dst.execute("DROP TABLE IF EXISTS EuropeRoad")
    dst.execute("""
        CREATE TABLE EuropeRoad (
            FromCityID      INTEGER,
            ToCityID        INTEGER,
            DistanceKM      REAL,
            IsFerry         INTEGER,
            CrossingType    INTEGER,
            CostAdjustment  REAL,
            ReliabilityScore REAL,
            Capacity        INTEGER
        )
    """)

    # Try extended schema first, fall back to legacy
    try:
        cur.execute(
            "SELECT FromCityID,ToCityID,DistanceKM,IsFerry,CrossingType,"
            "       CostAdjustment,ReliabilityScore,Capacity FROM EuropeRoad"
        )
        road_rows = cur.fetchall()
    except pyodbc.Error:
        cur.execute(
            "SELECT FromCityID,ToCityID,DistanceKM,IsFerry,CrossingType FROM EuropeRoad"
        )
        raw = cur.fetchall()
        road_rows = [r + (0.0, 0.95, 100) for r in raw]

    dst.executemany("INSERT INTO EuropeRoad VALUES (?,?,?,?,?,?,?,?)", road_rows)
    print(f"  EuropeRoad: {len(road_rows)} rows")

    dst.commit()
    dst.close()
    src.close()
    print("  → europe.db done")


# ── InfraDB → infra.db ────────────────────────────────────────────────────────
def export_infra():
    print("Exporting InfraDB …")
    # InfraNodes/InfraEdges live in the InfraDB database (not Northwind)
    src = _conn('InfraDB')
    dst = _sqlite('infra.db')
    cur = src.cursor()

    # Always create the InfraNodes/InfraEdges schema (may be empty if not in SQL yet)
    dst.execute("DROP TABLE IF EXISTS InfraNodes")
    dst.execute("""
        CREATE TABLE InfraNodes (
            NodeKey   TEXT PRIMARY KEY,
            Label     TEXT,
            Provider  TEXT,
            Type      TEXT,
            Latitude  REAL,
            Longitude REAL
        )
    """)
    cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='InfraNodes'")
    if cur.fetchone()[0] > 0:
        cur.execute("SELECT NodeKey,Label,Provider,Type,Latitude,Longitude FROM InfraNodes")
        node_rows = cur.fetchall()
    else:
        node_rows = []
    dst.executemany("INSERT INTO InfraNodes VALUES (?,?,?,?,?,?)", node_rows)
    print(f"  InfraNodes: {len(node_rows)} rows")

    dst.execute("DROP TABLE IF EXISTS InfraEdges")
    dst.execute("""
        CREATE TABLE InfraEdges (
            SourceKey  TEXT,
            TargetKey  TEXT,
            EdgeType   TEXT,
            DistanceKM REAL
        )
    """)
    cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='InfraEdges'")
    if cur.fetchone()[0] > 0:
        cur.execute("SELECT SourceKey,TargetKey,EdgeType,DistanceKM FROM InfraEdges")
        edge_rows = cur.fetchall()
    else:
        edge_rows = []
    dst.executemany("INSERT INTO InfraEdges VALUES (?,?,?,?)", edge_rows)
    print(f"  InfraEdges: {len(edge_rows)} rows")

    # Optional: SpaceNodes_Dynamic / SpaceEdges_Dynamic
    for tbl, create_sql, select_sql, insert_sql in [
        (
            'SpaceNodes_Dynamic',
            """CREATE TABLE IF NOT EXISTS SpaceNodes_Dynamic (
                MinuteOfDay INTEGER, SatID INTEGER, Lat REAL, Lng REAL, AltKM REAL
            )""",
            "SELECT MinuteOfDay,SatID,Lat,Lng,AltKM FROM SpaceNodes_Dynamic",
            "INSERT INTO SpaceNodes_Dynamic VALUES (?,?,?,?,?)",
        ),
        (
            'SpaceEdges_Dynamic',
            """CREATE TABLE IF NOT EXISTS SpaceEdges_Dynamic (
                MinuteOfDay INTEGER, SatA INTEGER, SatB INTEGER, DistKM REAL, LatencyMS REAL
            )""",
            "SELECT MinuteOfDay,SatA,SatB,DistKM,LatencyMS FROM SpaceEdges_Dynamic",
            "INSERT INTO SpaceEdges_Dynamic VALUES (?,?,?,?,?)",
        ),
    ]:
        try:
            cur.execute(
                f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{tbl}'"
            )
            if cur.fetchone()[0] == 0:
                continue
            dst.execute(f"DROP TABLE IF EXISTS {tbl}")
            dst.execute(create_sql)
            cur.execute(select_sql)
            rows = cur.fetchall()
            dst.executemany(insert_sql, rows)
            print(f"  {tbl}: {len(rows)} rows")
        except Exception as ex:
            print(f"  {tbl}: skipped ({ex})")

    dst.commit()
    dst.close()
    src.close()
    print("  → infra.db done")


# ── Northwind → northwind.db ──────────────────────────────────────────────────
_MSSQL_TYPE_MAP = {
    # text-like
    'nvarchar': 'TEXT', 'varchar': 'TEXT', 'char': 'TEXT', 'nchar': 'TEXT',
    'text': 'TEXT', 'ntext': 'TEXT', 'uniqueidentifier': 'TEXT',
    'xml': 'TEXT',
    # integers
    'int': 'INTEGER', 'bigint': 'INTEGER', 'smallint': 'INTEGER',
    'tinyint': 'INTEGER', 'bit': 'INTEGER',
    # reals
    'decimal': 'REAL', 'numeric': 'REAL', 'float': 'REAL', 'real': 'REAL',
    'money': 'REAL', 'smallmoney': 'REAL',
    # dates
    'date': 'TEXT', 'datetime': 'TEXT', 'datetime2': 'TEXT',
    'smalldatetime': 'TEXT', 'time': 'TEXT', 'datetimeoffset': 'TEXT',
    # binary → blob
    'binary': 'BLOB', 'varbinary': 'BLOB', 'image': 'BLOB',
}


import decimal as _decimal

# SQL Server graph tables have hidden internal columns and cannot be exported via SELECT.
_SKIP_TABLES = frozenset({
    'city', 'person', 'restaurant', 'friendof', 'likes', 'livesin', 'locatedin',
    'GraphCity', 'GraphRoad',
})


def _clean_cell(v):
    """Coerce pyodbc-returned values to types sqlite3 accepts."""
    if isinstance(v, (bytes, bytearray)):
        return None
    if isinstance(v, _decimal.Decimal):
        return float(v)
    return v


def export_northwind():
    print("Exporting Northwind …")
    src = _conn(cfg.SQL_DATABASE)
    dst = _sqlite('northwind.db')
    cur = src.cursor()

    # Get all user tables, skipping SQL Server graph tables
    cur.execute(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME"
    )
    tables = [r[0] for r in cur.fetchall() if r[0] not in _SKIP_TABLES]
    print(f"  Tables found: {len(tables)} (graph tables excluded)")

    for tbl in tables:
        # Get column info, excluding internal graph columns
        cur.execute(
            "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE "
            "FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_NAME=? AND COLUMN_NAME NOT LIKE '$%' "
            "ORDER BY ORDINAL_POSITION",
            (tbl,)
        )
        cols = cur.fetchall()
        if not cols:
            continue

        col_defs = ', '.join(
            f'"{c[0]}" {_MSSQL_TYPE_MAP.get(c[1].lower(), "TEXT")}'
            for c in cols
        )
        col_names = ', '.join(f'"{c[0]}"' for c in cols)
        placeholders = ', '.join('?' for _ in cols)

        dst.execute(f'DROP TABLE IF EXISTS "{tbl}"')
        dst.execute(f'CREATE TABLE "{tbl}" ({col_defs})')

        try:
            cur.execute(f'SELECT {col_names} FROM [{tbl}]')
            rows = cur.fetchall()
            cleaned = [tuple(_clean_cell(v) for v in row) for row in rows]
            dst.executemany(f'INSERT INTO "{tbl}" VALUES ({placeholders})', cleaned)
            print(f"  {tbl}: {len(cleaned)} rows")
        except Exception as ex:
            print(f"  {tbl}: ERROR — {ex}")

    dst.commit()
    dst.close()
    src.close()
    print("  → northwind.db done")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Export MS SQL DBs to SQLite fallback files")
    parser.add_argument('--only', choices=['northwind', 'europe', 'infra'],
                        help="Export only one database")
    args = parser.parse_args()

    if args.only == 'europe':
        export_europe()
    elif args.only == 'infra':
        export_infra()
    elif args.only == 'northwind':
        export_northwind()
    else:
        export_europe()
        export_infra()
        export_northwind()

    print("\nAll done. Files in:", OUT_DIR)
    for f in os.listdir(OUT_DIR):
        path = os.path.join(OUT_DIR, f)
        if f.endswith('.db'):
            print(f"  {f}: {os.path.getsize(path):,} bytes")
