"""
One-time script: GeoNames cities1000.txt → data/europe_graph.xml
Run from the repo root: python scripts/generate_city_data.py

Coverage: Afro-Eurasia "World Island" + major island nations
  - Continental: Europe, Asia (no JP/TW/ID/PH/LK), Africa (no MG/CV/KM)
  - Islands: GB, IE, IS, JP, ID, PH, LK, TW, CY, MT
  - Island bridges use a 3× ferry-penalty weight so A* prefers land routes

Edge strategy:
  1. KNN-3 mandatory connections per city (guarantees local mesh)
  2. Radius fill (≤ MAX_KM for radius edges)
  3. Kruskal MST bridging (connects remaining components; tagged as ferry)

Hyperparams from Optuna: pop_threshold=130,000  max_dist_km=180

GeoNames columns (no header, tab-separated):
  0=geonameid  1=name  2=asciiname  4=lat  5=lng  8=countryCode  14=population
"""
import heapq
import math
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

INPUT  = '/tmp/cities1000.txt'
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'northwind-control-center', 'data', 'europe_graph.xml')

MIN_POP       = 130_000
MAX_KM        = 180
K_NEAREST     = 3
FERRY_PENALTY = 3.0   # Kruskal bridge weight multiplier (proxy for ferry/tunnel)

CONTINENTAL_CC = {
    # Europe (no CY, MT — handled in ISLAND_CC)
    'AL','AT','BY','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR',
    'HU','IT','LV','LT','LU','MD','NL','MK','NO','PL','PT','RO','RS',
    'SK','SI','ES','SE','CH','UA','ME','AD','LI','MC','SM','VA','XK',
    # Caucasus / Central Asia
    'GE','AM','AZ','KZ','UZ','TM','TJ','KG',
    # Middle East
    'TR','IR','IQ','SY','JO','IL','LB','PS','SA','AE','KW','BH','QA','OM','YE',
    # South Asia (continental)
    'IN','PK','AF','NP','BT','BD',
    # East / SE Asia (continental only)
    'CN','MN','KP','KR','MM','TH','VN','LA','KH','MY',
    # Russia
    'RU',
    # Africa — continental (no MG, CV, KM, SC, MU, RE, SH)
    'DZ','EG','LY','MA','SD','TN',               # North Africa
    'ET','ER','DJ','KE','TZ','UG','RW','BI','SO', # East Africa
    'BJ','BF','CI','GH','GN','GM','GW','LR',      # West Africa
    'ML','MR','NE','NG','SN','SL','TG',           # West Africa cont.
    'CM','CF','TD','CG','CD','GQ','GA',           # Central Africa
    'AO','BW','LS','MW','MZ','NA','ZA','ZM','ZW', # Southern Africa
    'SS',                                          # South Sudan
}

ISLAND_CC = {
    'GB','IE','IS',        # British Isles + Iceland
    'JP','TW',             # East Asian islands
    'ID','PH','LK',        # SE Asian / South Asian islands
    'CY','MT',             # Mediterranean islands
}

ALL_CC = CONTINENTAL_CC | ISLAND_CC


def haversine_km(lat1, lng1, lat2, lng2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ── 1. Parse cities ────────────────────────────────────────────────────────────
print('1. Parsing GeoNames …')
cities = []
seen_names = set()
with open(INPUT, encoding='utf-8') as f:
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 15:
            continue
        cc  = parts[8]
        pop = parts[14]
        if cc not in ALL_CC:
            continue
        try:
            if int(pop) < MIN_POP:
                continue
        except ValueError:
            continue
        name = (parts[2] or parts[1]).strip()
        if not name or name in seen_names:
            continue
        seen_names.add(name)
        try:
            lat = float(parts[4])
            lng = float(parts[5])
        except ValueError:
            continue
        is_island = cc in ISLAND_CC
        cities.append({
            'id':       str(len(cities) + 1),
            'name':     name,
            'country':  cc,
            'lat':      str(round(lat, 6)),
            'lng':      str(round(lng, 6)),
            'pop':      pop,
            'island':   is_island,   # internal flag, not written to XML
        })

n = len(cities)
island_count = sum(1 for c in cities if c['island'])
print(f'   → {n} cities  ({n - island_count} continental + {island_count} island)')

# ── 2. Distance matrix ────────────────────────────────────────────────────────
print(f'2. Building distance matrix ({n}×{n}) …')
dm = [[0.0] * n for _ in range(n)]
for i in range(n):
    if i % 200 == 0:
        print(f'   {i}/{n}…')
    la1, lo1 = float(cities[i]['lat']), float(cities[i]['lng'])
    for j in range(i + 1, n):
        d = haversine_km(la1, lo1, float(cities[j]['lat']), float(cities[j]['lng']))
        dm[i][j] = dm[j][i] = d

# ── 3. KNN-3 + radius edges ───────────────────────────────────────────────────
print(f'3. KNN-{K_NEAREST} mandatory + radius fill (≤{MAX_KM} km) …')
added = set()      # (lo_idx, hi_idx)
edges = []         # {'from','to','distance','ferry'}

def add_edge(i, j, dist, ferry=False):
    key = (min(i, j), max(i, j))
    if key in added:
        return
    added.add(key)
    lo, hi = key
    # Ferry weight: actual distance stored; weight used by A* = dist * FERRY_PENALTY (done in service)
    edges.append({
        'from':     cities[lo]['id'],
        'to':       cities[hi]['id'],
        'distance': str(round(dist, 1)),
        'ferry':    '1' if ferry else '0',
    })

for i in range(n):
    order = sorted(range(n), key=lambda j, _i=i: dm[_i][j] if j != _i else 1e9)
    # Mandatory KNN-3
    for j in order[:K_NEAREST]:
        add_edge(i, j, dm[i][j])
    # Radius fill
    for j in order[K_NEAREST:]:
        if dm[i][j] > MAX_KM:
            break
        add_edge(i, j, dm[i][j])

print(f'   → {len(edges):,} edges after KNN + radius')

# ── 4. Kruskal bridge: connect remaining components ───────────────────────────
print('4. Kruskal bridging …')
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
    union(int(e['from']) - 1, int(e['to']) - 1)

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
            add_edge(i, j, d, ferry=True)
            bridge_count += 1
            n_comp -= 1
            print(f'   ⚠ Ferry bridge: {cities[i]["name"]} ({cities[i]["country"]}) ↔ '
                  f'{cities[j]["name"]} ({cities[j]["country"]})  {d:.1f} km')

ferry_total = sum(1 for e in edges if e['ferry'] == '1')
print(f'   → {len(edges):,} total edges  ({len(edges)*2:,} directed)  '
      f'[{bridge_count} ferry bridges, {ferry_total} ferry edges total]')

# ── 5. Write XML ──────────────────────────────────────────────────────────────
print('5. Writing XML …')
root      = ET.Element('GraphData')
cities_el = ET.SubElement(root, 'Cities')
for c in cities:
    ET.SubElement(cities_el, 'City', {
        'id':      c['id'],
        'name':    c['name'],
        'country': c['country'],
        'lat':     c['lat'],
        'lng':     c['lng'],
        'pop':     c['pop'],
    })

roads_el = ET.SubElement(root, 'Roads')
for e in edges:
    ET.SubElement(roads_el, 'Road', e)

xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
out_path = os.path.abspath(OUTPUT)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(xml_str)

print(f'   → Saved to {out_path}')
print('Done.')
