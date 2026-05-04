"""
One-time script: GeoNames cities1000.txt → data/europe_graph.xml
Run from the repo root: python scripts/generate_city_data.py

GeoNames tab-separated columns (no header):
  0=geonameid  1=name  2=asciiname  3=alternatenames  4=lat  5=lng
  6=featureClass  7=featureCode  8=countryCode  ...  14=population
"""
import math
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

INPUT = '/tmp/cities1000.txt'
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'northwind-control-center', 'data', 'europe_graph.xml')
MIN_POP = 100_000
MAX_KM  = 500

EUROPEAN_CC = {
    'AL','AT','BY','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR',
    'HU','IE','IT','LV','LT','LU','MD','NL','MK','NO','PL','PT','RO','RS',
    'SK','SI','ES','SE','CH','UA','GB','ME','IS','MT','CY','AD','LI','MC',
    'SM','VA','XK',
}

def haversine_km(lat1, lng1, lat2, lng2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


print('1. Parsing GeoNames cities1000.txt …')
cities = []
seen_names = set()
with open(INPUT, encoding='utf-8') as f:
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 15:
            continue
        cc  = parts[8]
        pop = parts[14]
        if cc not in EUROPEAN_CC:
            continue
        try:
            if int(pop) < MIN_POP:
                continue
        except ValueError:
            continue
        name = parts[2] or parts[1]   # prefer ASCII name
        name = name.strip()
        if not name or name in seen_names:
            continue
        seen_names.add(name)
        try:
            lat = float(parts[4])
            lng = float(parts[5])
        except ValueError:
            continue
        cities.append({
            'id':      str(len(cities) + 1),
            'name':    name,
            'country': cc,
            'lat':     str(round(lat, 6)),
            'lng':     str(round(lng, 6)),
            'pop':     pop,
        })

print(f'   → {len(cities)} cities kept (pop ≥ {MIN_POP:,}, European CC)')

print('2. Computing adjacency edges (≤ 500 km) …')
edges = []
for i, c1 in enumerate(cities):
    for j, c2 in enumerate(cities):
        if i >= j:
            continue
        d = haversine_km(float(c1['lat']), float(c1['lng']),
                         float(c2['lat']), float(c2['lng']))
        if d <= MAX_KM:
            edges.append({
                'from':     c1['id'],
                'to':       c2['id'],
                'distance': str(round(d, 1)),
            })

print(f'   → {len(edges):,} undirected edges (each stored bidirectionally → {len(edges)*2:,} in GraphRoad)')

print('3. Writing XML …')
root      = ET.Element('GraphData')
cities_el = ET.SubElement(root, 'Cities')
for c in cities:
    ET.SubElement(cities_el, 'City', c)

roads_el = ET.SubElement(root, 'Roads')
for e in edges:
    ET.SubElement(roads_el, 'Road', e)

xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
out_path = os.path.abspath(OUTPUT)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(xml_str)

print(f'   → Saved to {out_path}')
print('Done.')
