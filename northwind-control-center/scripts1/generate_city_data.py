"""
One-time script: GeoNames cities1000.txt → data/europe_graph.xml
Run from the repo root: python scripts/generate_city_data.py

Coverage: Global — Afro-Eurasia, Americas, Oceania + island nations
  Step 4b: island-to-mainland ferry bridges (≤500 km)
  Step 4c: Bering Strait bridge (Nome↔Anadyr, ferry penalty) +
           4 ocean corridors (Atlantic/Pacific, 5× penalty)

Speed: scipy.cKDTree replaces O(N²) Python loops → sub-second distance lookups.

Hyperparams (Optuna-tuned):
  MIN_KNN     = 5
  MAX_VALENCE = 7
  LOCAL_KM    = 81

GeoNames tab-separated (no header):
  0=geonameid  1=name  2=asciiname  4=lat  5=lng  8=CC  14=population
"""
import heapq
import math
import random
import xml.etree.ElementTree as ET
import os

import numpy as np
from scipy.spatial import cKDTree

INPUT  = '/tmp/cities1000.txt'
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'northwind-control-center', 'data', 'europe_graph.xml')

MIN_POP_MAIN     = 40_000   # Afro-Eurasia + islands: horse-cart topology, dense nodes
MIN_POP_AMERICAS = 15_000   # Americas + Oceania: automobile/railroad sprawl
MIN_KNN          = 5        # Optuna best: guaranteed connections per city
MAX_VALENCE      = 7        # Optuna best: hard degree ceiling (ferry bridges excluded)
LOCAL_KM         = 81       # Optuna best: always-add radius for EU urban clusters
LOCAL_KM_SPREAD  = 120      # Americas/Oceania: railroad-era ~100-mile town spacing
EXTRA_BRIDGES = 5         # redundant short bridges between large components
FERRY_PENALTY = 1.5       # weight multiplier for short ferry / island bridges
OCEAN_PENALTY = 5.0       # weight multiplier for intercontinental ocean corridors

R = 6371.0

CONTINENTAL_CC = {
    'AL','AT','BY','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR',
    'HU','IT','LV','LT','LU','MD','NL','MK','NO','PL','PT','RO','RS',
    'SK','SI','ES','SE','CH','UA','ME','AD','LI','MC','SM','VA','XK',
    'GE','AM','AZ','KZ','UZ','TM','TJ','KG',
    'TR','IR','IQ','SY','JO','IL','LB','PS','SA','AE','KW','BH','QA','OM','YE',
    'IN','PK','AF','NP','BT','BD',
    'CN','MN','KP','KR','MM','TH','VN','LA','KH','MY','RU','SG',
    'DZ','EG','LY','MA','SD','TN',
    'ET','ER','DJ','KE','TZ','UG','RW','BI','SO',
    'BJ','BF','CI','GH','GN','GM','GW','LR','ML','MR','NE','NG','SN','SL','TG',
    'CM','CF','TD','CG','CD','GQ','GA','AO','BW','LS','MW','MZ','NA','ZA','ZM','ZW','SS',
}
ISLAND_CC   = {'GB','IE','IS','JP','TW','ID','PH','LK','CY','MT'}
AMERICAS_CC = {
    'US','CA','MX','GT','BZ','HN','SV','NI','CR','PA',
    'CU','DO','HT','JM','PR','TT','BB','LC','VC','AG','KN','DM','GD',
    'BR','AR','CO','CL','PE','VE','EC','BO','PY','UY','GY','SR',
}
OCEANIA_CC  = {'AU','NZ','PG','FJ','SB','VU','WS','TO'}
ALL_CC      = CONTINENTAL_CC | ISLAND_CC | AMERICAS_CC | OCEANIA_CC

# Force-include below-threshold cities needed as geographic stepping stones
STRATEGIC_INCLUSIONS = {'Nome': 'US', 'Anadyr': 'RU'}

# Countries that use the lower population threshold (automobile/railroad settlement pattern)
_SPREAD_CC = AMERICAS_CC | OCEANIA_CC


def _chord(km: float) -> float:
    return 2.0 * math.sin(km / (2.0 * R))

def _hav(la1, lo1, la2, lo2):
    dlat = math.radians(la2 - la1)
    dlng = math.radians(lo2 - lo1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(la1)) * math.cos(math.radians(la2))
         * math.sin(dlng / 2) ** 2)
    return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


# ── 1. Parse ──────────────────────────────────────────────────────────────────
print('1. Parsing GeoNames …')
cities: list = []
seen_names: set = set()
with open(INPUT, encoding='utf-8') as f:
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 15:
            continue
        cc = parts[8]
        if cc not in ALL_CC:
            continue
        try:
            pop_int = int(parts[14])
            lat     = float(parts[4])
            lng     = float(parts[5])
        except ValueError:
            continue
        name = (parts[2] or parts[1]).strip()
        if not name or name in seen_names:
            continue
        is_strategic = STRATEGIC_INCLUSIONS.get(name) == cc
        threshold    = MIN_POP_AMERICAS if cc in _SPREAD_CC else MIN_POP_MAIN
        if pop_int < threshold and not is_strategic:
            continue
        seen_names.add(name)
        cities.append({
            'id':      str(len(cities) + 1),
            'name':    name,
            'country': cc,
            'lat':     str(round(lat, 6)),
            'lng':     str(round(lng, 6)),
            'pop':     str(pop_int),
            '_island': cc in ISLAND_CC,
        })

n = len(cities)
island_n = sum(1 for c in cities if c['_island'])
print(f'   → {n} cities  ({n - island_n} continental + {island_n} island) '
      f'[main ≥ {MIN_POP_MAIN:,}  Americas/Oceania ≥ {MIN_POP_AMERICAS:,}]')
city_degree = [0] * n

# ── 2. Build KDTree ───────────────────────────────────────────────────────────
print('2. Building 3D KDTree …')
lats_r = np.radians(np.array([float(c['lat']) for c in cities]))
lngs_r = np.radians(np.array([float(c['lng']) for c in cities]))
pts    = np.column_stack([
    np.cos(lats_r) * np.cos(lngs_r),
    np.cos(lats_r) * np.sin(lngs_r),
    np.sin(lats_r),
])
tree = cKDTree(pts)
print(f'   → tree built for {n} cities')

# ── 3. Valence-capped edge generation ─────────────────────────────────────────
print(f'3. Valence-capped generation '
      f'(KNN-{MIN_KNN} mandatory + {LOCAL_KM} km local, cap {MAX_VALENCE}) …')

added:       set  = set()   # (lo_idx, hi_idx)
edges:       list = []      # {'from','to','distance','ferry','ocean'}
edge_index:  dict = {}      # key → index into edges (for flag upgrades)

def _road_reliability(ferry: bool, ocean: bool, dist_km: float) -> float:
    """Deterministic reliability score: wetter and longer roads are less reliable."""
    base  = 0.85 if ocean else 0.91 if ferry else 0.97
    decay = min(dist_km / 100_000.0, 0.05)   # −0.01 per 1000 km, cap −0.05
    return round(max(base - decay, 0.70), 4)


def add_edge(i: int, j: int, dist_km: float,
             ferry: bool = False, ocean: bool = False) -> None:
    key = (min(i, j), max(i, j))
    if key in added:
        if ferry or ocean:
            idx = edge_index[key]
            if ferry: edges[idx]['ferry'] = '1'
            if ocean: edges[idx]['ocean'] = '1'
        return
    added.add(key)
    lo, hi = key
    edge_index[key] = len(edges)
    edges.append({
        'from':        cities[lo]['id'],
        'to':          cities[hi]['id'],
        'distance':    str(round(dist_km, 1)),
        'ferry':       '1' if ferry else '0',
        'ocean':       '1' if ocean else '0',
        'cost_adj':    '0.0',
        'reliability': str(_road_reliability(ferry, ocean, dist_km)),
        'capacity':    '100',
    })
    city_degree[lo] += 1
    city_degree[hi] += 1

K_SEARCH = min(MAX_VALENCE * 3 + 10, n)  # extra headroom for cross-continental skips
_, knn = tree.query(pts, k=K_SEARCH)

def _cross_continental(i: int, j: int) -> bool:
    """True if this edge crosses the Americas ↔ rest-of-world boundary."""
    return (cities[i]['country'] in AMERICAS_CC) != (cities[j]['country'] in AMERICAS_CC)

def _water_penalty(i: int, j: int, d: float) -> tuple[bool, bool]:
    """
    Return (ferry, ocean) flags for a mandatory KNN edge.

    Water penalty applies only when cities are in DIFFERENT countries AND at least
    one is ISLAND_CC.  Same-country edges (e.g. Tokyo→Osaka within JP) and
    continental-to-continental edges (e.g. Moscow→Novosibirsk within RU) stay land
    regardless of distance.
    """
    ci, cj = cities[i]['country'], cities[j]['country']
    if ci == cj:
        return False, False
    if ci in ISLAND_CC or cj in ISLAND_CC:
        if d > 800:
            return False, True    # ocean 5×  (e.g. Reykjavik → Ireland ~1800 km)
        if d > 150:
            return True,  False   # ferry 1.5× (e.g. Dublin → Liverpool ~230 km)
    return False, False           # both continental — long road, land penalty

for i in range(n):
    mandatory_found = 0   # same-continent mandatory edges added for city i
    for j_raw in knn[i]:
        j = int(j_raw)
        if j == i:
            continue
        if _cross_continental(i, j):
            continue   # explicit bridges (Step 4c) handle cross-continental links

        d = _hav(float(cities[i]['lat']), float(cities[i]['lng']),
                 float(cities[j]['lat']), float(cities[j]['lng']))

        is_mandatory = mandatory_found < MIN_KNN
        at_cap       = city_degree[i] >= MAX_VALENCE

        if is_mandatory:
            is_ferry, is_ocean = _water_penalty(i, j, d)
            add_edge(i, j, d, ferry=is_ferry, ocean=is_ocean)
            mandatory_found += 1
        elif at_cap:
            break   # past mandatory zone and at degree cap → done with this city
        elif d <= (LOCAL_KM_SPREAD if cities[i]['country'] in _SPREAD_CC else LOCAL_KM):
            add_edge(i, j, d)

print(f'   → {len(edges):,} edges after valence-capped generation')

# ── 4. Kruskal bridging ───────────────────────────────────────────────────────
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
    print(f'   → {n_comp} components; scanning for bridges …')
    sample_size = max(n_comp * 4, n // 10)
    scouts      = random.sample(range(n), min(sample_size, n))
    _, scan     = tree.query(pts[scouts], k=min(200, n))

    heap: list  = []
    seen_pairs: set = set()
    for si, neighbors in enumerate(scan):
        i  = scouts[si]
        ri = find(i)
        for j in neighbors:
            j = int(j)
            if find(j) != ri:
                key = (min(i, j), max(i, j))
                if key not in seen_pairs:
                    seen_pairs.add(key)
                    d = _hav(float(cities[i]['lat']), float(cities[i]['lng']),
                             float(cities[j]['lat']), float(cities[j]['lng']))
                    heapq.heappush(heap, (d, i, j))

    extra = EXTRA_BRIDGES
    while heap and (n_comp > 1 or extra > 0):
        d, i, j = heapq.heappop(heap)
        cross = _cross_continental(i, j)
        if union(i, j):
            # Any Kruskal bridge > 1500 km is a trans-oceanic crossing regardless of
            # continental group (handles Hawaii→US-mainland, Fiji→NZ, NZ→AU, etc.)
            is_ocean = cross or d > 1500
            add_edge(i, j, d, ferry=not is_ocean, ocean=is_ocean)
            bridge_count += 1
            n_comp -= 1
            label = 'Ocean bridge' if is_ocean else 'Ferry bridge'
            print(f'   ⚠ {label}: {cities[i]["name"]} ({cities[i]["country"]}) ↔ '
                  f'{cities[j]["name"]} ({cities[j]["country"]})  {d:.1f} km')
        elif n_comp == 1 and extra > 0:
            add_edge(i, j, d, ferry=not cross, ocean=cross)
            extra -= 1

# ── 4b. Island-to-mainland scan ───────────────────────────────────────────────
# Kruskal only bridges disconnected *components*.  If an island cluster (e.g.
# Japan) is already reachable via a long back-road (Sakhalin→Hokkaido), the
# direct short crossing (Busan→Fukuoka) is never added.  This pass explicitly
# finds the shortest edge from every ISLAND_CC city to a non-island neighbour,
# regardless of component membership, and adds it as a ferry bridge when no
# short cross-strait land edge already exists.
MAX_ISLAND_BRIDGE_KM = 500   # cap: only add realistic ferry distances
island_idx = [i for i, c in enumerate(cities) if c['_island']]
if island_idx:
    print(f'4b. Island-to-mainland scan ({len(island_idx)} island cities) …')
    mainland_idx = [i for i, c in enumerate(cities) if not c['_island']]
    # Build a KDTree of mainland points only
    ml_pts = pts[mainland_idx]
    ml_tree = cKDTree(ml_pts)
    island_bridges = 0
    for ii in island_idx:
        # find closest mainland city
        dist_chord, nn_pos = ml_tree.query(pts[ii], k=1)
        nn_idx = mainland_idx[nn_pos]
        d_km = _hav(float(cities[ii]['lat']), float(cities[ii]['lng']),
                    float(cities[nn_idx]['lat']), float(cities[nn_idx]['lng']))
        if d_km <= MAX_ISLAND_BRIDGE_KM:
            key = (min(ii, nn_idx), max(ii, nn_idx))
            if key not in added:   # don't duplicate existing land edge
                add_edge(ii, nn_idx, d_km, ferry=True)
                island_bridges += 1
    print(f'   → {island_bridges} island-to-mainland bridges added (≤{MAX_ISLAND_BRIDGE_KM} km)')

# ── 4c. Global ocean corridors ────────────────────────────────────────────────
# Bering Strait (ferry penalty, CrossingType=1): Nome↔Anadyr ~82 km
# Atlantic/Pacific (ocean penalty, CrossingType=2): 4 strategic shipping lanes
BERING_BRIDGES = [
    ('Nome', 'US', 'Anadyr', 'RU'),
]
EXPLICIT_FERRY_ROUTES = [
    ('Dublin', 'IE', 'Glasgow', 'GB'),  # Irish Sea — Dublin↔Glasgow ~300 km; Liverpool AU stole 'Liverpool'
]
OCEAN_CORRIDORS = [
    ('Natal',         'BR', 'Dakar',   'SN'),   # narrowest Atlantic, ~3150 km
    ('New York City', 'US', 'Leeds',   'GB'),   # North Atlantic, ~5380 km; Leeds is unique (Liverpool AU collision)
    ('Seattle',       'US', 'Tokyo',   'JP'),   # North Pacific, ~7700 km
    ('Sydney',        'AU', 'Singapore','SG'),  # South Pacific gateway, ~6300 km
]

print('4c. Global bridges …')
name_cc_idx = {(c['name'], c['country']): int(c['id']) - 1 for c in cities}

for n1, cc1, n2, cc2 in BERING_BRIDGES:
    i = name_cc_idx.get((n1, cc1))
    j = name_cc_idx.get((n2, cc2))
    if i is None or j is None:
        print(f'   ⚠  Bering skipped: {n1}({cc1}) or {n2}({cc2}) not in city set')
        continue
    d_km = _hav(float(cities[i]['lat']), float(cities[i]['lng']),
                float(cities[j]['lat']), float(cities[j]['lng']))
    add_edge(i, j, d_km, ferry=True)
    print(f'   ⚓ Bering:  {n1}({cc1}) ↔ {n2}({cc2})  {d_km:.0f} km  (ferry 1.5×)')

for n1, cc1, n2, cc2 in EXPLICIT_FERRY_ROUTES:
    i = name_cc_idx.get((n1, cc1))
    j = name_cc_idx.get((n2, cc2))
    if i is None or j is None:
        print(f'   ⚠  Ferry skipped: {n1}({cc1}) or {n2}({cc2}) not in city set')
        continue
    d_km = _hav(float(cities[i]['lat']), float(cities[i]['lng']),
                float(cities[j]['lat']), float(cities[j]['lng']))
    add_edge(i, j, d_km, ferry=True)
    print(f'   ⛴ Ferry:   {n1}({cc1}) ↔ {n2}({cc2})  {d_km:.0f} km  (ferry 1.5×)')

ocean_added = 0
for n1, cc1, n2, cc2 in OCEAN_CORRIDORS:
    i = name_cc_idx.get((n1, cc1))
    j = name_cc_idx.get((n2, cc2))
    if i is None or j is None:
        print(f'   ⚠  Ocean skipped: {n1}({cc1}) or {n2}({cc2}) not in city set')
        continue
    d_km = _hav(float(cities[i]['lat']), float(cities[i]['lng']),
                float(cities[j]['lat']), float(cities[j]['lng']))
    add_edge(i, j, d_km, ocean=True)
    ocean_added += 1
    print(f'   🌊 Ocean:  {n1}({cc1}) ↔ {n2}({cc2})  {d_km:.0f} km  (ocean 5×)')
print(f'   → {ocean_added} ocean corridors added')

ferry_total = sum(1 for e in edges if e['ferry'] == '1')
ocean_total = sum(1 for e in edges if e['ocean'] == '1')
print(f'   → {len(edges):,} total edges  ({len(edges)*2:,} directed)  '
      f'[{bridge_count} Kruskal bridges  {ferry_total} ferry  {ocean_total} ocean]')

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

# ET.indent() (Python ≥ 3.9) pretty-prints in-place — zero extra memory vs minidom
ET.indent(root, space='  ')
out_path = os.path.abspath(OUTPUT)
ET.ElementTree(root).write(out_path, encoding='unicode', xml_declaration=True)

print(f'   → Saved to {out_path}')
print('Done.')
