"""
One-time script: GeoNames cities1000.txt → data/europe_graph.xml
Run from the repo root: python scripts/generate_city_data.py

Coverage: Europe + Asia continental (no islands: GB, IE, IS, JP, ID, PH, LK, TW, CY, MT)
Hyperparams tuned via Optuna (scripts/tune_graph_hyperparams.py):
  pop_threshold = 80,000  (min city population)
  max_dist_km   = 120     (max edge length for radius fill)
  k_nearest     = 3       (mandatory KNN connections per city)

Edge strategy: KNN-3 mandatory + radius fill + Kruskal MST bridging
→ guarantees full connectivity even across continental divides

GeoNames tab-separated columns (no header):
  0=geonameid  1=name  2=asciiname  3=alternatenames  4=lat  5=lng
  6=featureClass  7=featureCode  8=countryCode  ...  14=population
"""
import heapq
import math
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

INPUT  = '/tmp/cities1000.txt'
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'northwind-control-center', 'data', 'europe_graph.xml')

MIN_POP   = 130_000  # Optuna best_params['pop_threshold']
MAX_KM    = 180      # Optuna best_params['max_dist_km']
K_NEAREST = 3        # mandatory KNN per city

# Europe + Asia continental; islands excluded (GB, IE, IS, CY, MT, JP, TW, ID, PH, LK)
EURASIA_CC = {
    # Europe
    'AL','AT','BY','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR',
    'HU','IT','LV','LT','LU','MD','NL','MK','NO','PL','PT','RO','RS',
    'SK','SI','ES','SE','CH','UA','ME','AD','LI','MC','SM','VA','XK',
    # Caucasus / Central Asia
    'GE','AM','AZ','KZ','UZ','TM','TJ','KG',
    # Middle East
    'TR','IR','IQ','SY','JO','IL','LB','PS','SA','AE','KW','BH','QA','OM','YE',
    # South Asia
    'IN','PK','AF','NP','BT','BD',
    # East / SE Asia (continental only)
    'CN','MN','KP','KR','MM','TH','VN','LA','KH','MY',
    # Russia (spans both continents)
    'RU',
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
        if cc not in EURASIA_CC:
            continue
        try:
            if int(pop) < MIN_POP:
                continue
        except ValueError:
            continue
        name = parts[2] or parts[1]
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

n = len(cities)
print(f'   → {n} cities kept (pop ≥ {MIN_POP:,}, Eurasia CC)')

print(f'2. Computing distances and building KNN-{K_NEAREST} + radius (≤{MAX_KM} km) edges …')

# Precompute full distance matrix
dm = [[0.0] * n for _ in range(n)]
for i in range(n):
    if i % 100 == 0:
        print(f'   distance matrix: {i}/{n}…')
    la1, lo1 = float(cities[i]['lat']), float(cities[i]['lng'])
    for j in range(i + 1, n):
        d = haversine_km(la1, lo1, float(cities[j]['lat']), float(cities[j]['lng']))
        dm[i][j] = dm[j][i] = d

added = set()   # (lo_id, hi_id) string pairs to deduplicate
edges = []      # list of {'from','to','distance'}

for i in range(n):
    order = sorted(range(n), key=lambda j, _i=i: dm[_i][j] if j != _i else 1e9)
    # Mandatory KNN-3
    for j in order[:K_NEAREST]:
        key = (min(i, j), max(i, j))
        if key not in added:
            edges.append({
                'from':     cities[key[0]]['id'],
                'to':       cities[key[1]]['id'],
                'distance': str(round(dm[key[0]][key[1]], 1)),
            })
            added.add(key)
    # Radius fill
    for j in order[K_NEAREST:]:
        if dm[i][j] > MAX_KM:
            break
        key = (min(i, j), max(i, j))
        if key not in added:
            edges.append({
                'from':     cities[key[0]]['id'],
                'to':       cities[key[1]]['id'],
                'distance': str(round(dm[key[0]][key[1]], 1)),
            })
            added.add(key)

print(f'   → {len(edges):,} edges after KNN + radius')

print('3. Kruskal bridging: connecting remaining components …')
parent = list(range(n))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(x, y):
    px, py = find(x), find(y)
    if px == py:
        return False
    parent[px] = py
    return True

for e in edges:
    i = int(e['from']) - 1
    j = int(e['to']) - 1
    union(i, j)

n_comp = len(set(find(i) for i in range(n)))
bridge_count = 0

if n_comp > 1:
    print(f'   → {n_comp} components; building bridge heap …')
    heap = []
    for i in range(n):
        for j in range(i + 1, n):
            if find(i) != find(j):
                heapq.heappush(heap, (dm[i][j], i, j))

    while heap and n_comp > 1:
        d, i, j = heapq.heappop(heap)
        if union(i, j):
            key = (min(i, j), max(i, j))
            edges.append({
                'from':     cities[key[0]]['id'],
                'to':       cities[key[1]]['id'],
                'distance': str(round(d, 1)),
            })
            added.add(key)
            bridge_count += 1
            n_comp -= 1
            ci_name = cities[i]['name']
            cj_name = cities[j]['name']
            print(f'   ⚠ Bridge: {ci_name} ↔ {cj_name} ({d:.1f} km)')

print(f'   → {len(edges):,} total edges  ({len(edges)*2:,} directed)  [{bridge_count} bridges added]')

print('4. Writing XML …')
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
