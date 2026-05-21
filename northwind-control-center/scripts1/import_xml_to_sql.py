"""
One-time import: northwind-control-center/data/europe_graph.xml → EuropeGraph DB
Run from repo root: python scripts/import_xml_to_sql.py

Reads SQL connection from .env (SQL_SA_USERNAME / SQL_SA_PASSWORD for sa account,
falls back to SQL_USERNAME / SQL_PASSWORD).
"""
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pyodbc
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / 'northwind-control-center' / '.env')
load_dotenv(Path(__file__).parent.parent / '.env', override=False)

server   = os.environ['SQL_SERVER']
driver   = os.environ.get('SQL_DRIVER', 'ODBC Driver 18 for SQL Server')
encrypt  = os.environ.get('SQL_ENCRYPT', 'yes')
trust    = os.environ.get('SQL_TRUST_SERVER_CERT', 'yes')
user     = os.environ.get('SQL_SA_USERNAME') or os.environ.get('SQL_USERNAME')
password = os.environ.get('SQL_SA_PASSWORD') or os.environ.get('SQL_PASSWORD')

if not password:
    print("ERROR: SQL_SA_PASSWORD (or SQL_PASSWORD) not set in .env", file=sys.stderr)
    sys.exit(1)

conn_str = (
    f"DRIVER={{{driver}}};SERVER={server};DATABASE=EuropeGraph;"
    f"UID={user};PWD={password};"
    f"Encrypt={encrypt};TrustServerCertificate={trust};"
)

XML_PATH = Path(__file__).parent.parent / 'northwind-control-center' / 'data' / 'europe_graph.xml'

print('Parsing XML …')
tree  = ET.parse(XML_PATH)
root  = tree.getroot()
cities = root.find('Cities').findall('City')
roads  = root.find('Roads').findall('Road')
print(f'  {len(cities):,} cities, {len(roads):,} roads')

print('Connecting to SQL Server …')
conn = pyodbc.connect(conn_str)
conn.autocommit = False
cur  = conn.cursor()
cur.fast_executemany = True   # array binding: 10–50× faster than row-by-row

print('Migrating schema — adding extended columns if absent …')
_EXT_COLS = [
    ('CostAdjustment',  'FLOAT', '0.0'),
    ('ReliabilityScore','FLOAT', '0.95'),
    ('Capacity',        'INT',   '100'),
]
for _col, _dtype, _default in _EXT_COLS:
    cur.execute(
        f"IF NOT EXISTS ("
        f"  SELECT 1 FROM sys.columns"
        f"  WHERE object_id = OBJECT_ID('EuropeGraph.dbo.EuropeRoad') AND name = '{_col}'"
        f") ALTER TABLE EuropeGraph.dbo.EuropeRoad"
        f"  ADD {_col} {_dtype} NULL DEFAULT {_default}"
    )
conn.commit()
print('  Extended columns ready.')

print('Clearing old data …')
cur.execute("DELETE FROM EuropeGraph.dbo.EuropeRoad")
cur.execute("DELETE FROM EuropeGraph.dbo.EuropeCity")
conn.commit()

print('Seeding EuropeCity …')
BATCH = 2000
city_rows = [
    (int(c.get('id')), c.get('name'), c.get('country'),
     float(c.get('lat')), float(c.get('lng')), int(c.get('pop', 0)))
    for c in cities
]
for i in range(0, len(city_rows), BATCH):
    cur.executemany(
        "INSERT INTO EuropeGraph.dbo.EuropeCity (CityID, Name, Country, Lat, Lng, Population)"
        " VALUES (?,?,?,?,?,?)",
        city_rows[i:i + BATCH],
    )
conn.commit()
print(f'  {len(city_rows):,} cities inserted')

print('Seeding EuropeRoad …')
road_rows = [
    (int(r.get('from')), int(r.get('to')),
     float(r.get('distance')),
     int(r.get('ferry', 0)),
     2 if r.get('ocean') == '1' else (1 if r.get('ferry') == '1' else 0),
     float(r.get('cost_adj',    '0.0')),
     float(r.get('reliability', '0.95')),
     int(r.get('capacity',      '100')))
    for r in roads
]
for i in range(0, len(road_rows), BATCH):
    cur.executemany(
        "INSERT INTO EuropeGraph.dbo.EuropeRoad"
        " (FromCityID, ToCityID, DistanceKM, IsFerry, CrossingType,"
        "  CostAdjustment, ReliabilityScore, Capacity)"
        " VALUES (?,?,?,?,?,?,?,?)",
        road_rows[i:i + BATCH],
    )
conn.commit()
print(f'  {len(road_rows):,} roads inserted')

cur.close()
conn.close()
print('Import complete.')
