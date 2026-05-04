"""
Offline HPO: find (pop_threshold, max_dist_km) that minimises Route Stretch Factor
while keeping the Eurasia city graph fully connected (after auto-bridging components).

Coverage: Europe + Asia continental — islands (GB, IE, IS, JP, ID, PH, LK, TW, CY, MT) excluded.

Objective: avg_stretch + edges/50000 + bridge_count*0.05
  - avg_stretch measured over 50 random city pairs
  - bridge_count = Kruskal MST edges needed to merge disconnected components
  - No trial returns 1e6 — all graphs are force-connected then evaluated

Run:
    pip install optuna networkx
    python scripts/tune_graph_hyperparams.py
"""
import heapq
import math
import optuna
import networkx as nx
import random

INPUT_FILE = '/tmp/cities1000.txt'
K_NEAREST  = 3

# Europe + Asia continental; islands and city-states excluded
EURASIA_CC = {
    # Europe (no GB, IE, IS, CY, MT)
    'AL','AT','BY','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR',
    'HU','IT','LV','LT','LU','MD','NL','MK','NO','PL','PT','RO','RS',
    'SK','SI','ES','SE','CH','UA','ME','AD','LI','MC','SM','VA','XK',
    # Caucasus / Central Asia
    'GE','AM','AZ','KZ','UZ','TM','TJ','KG',
    # Middle East
    'TR','IR','IQ','SY','JO','IL','LB','PS','SA','AE','KW','BH','QA','OM','YE',
    # South Asia
    'IN','PK','AF','NP','BT','BD',
    # East / SE Asia (continental only — no JP, TW, ID, PH, LK)
    'CN','MN','KP','KR','MM','TH','VN','LA','KH','MY',
    # Russia spans both
    'RU',
}


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon  = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# Load once
_ALL_CITIES = []
seen = set()
with open(INPUT_FILE, encoding='utf-8') as f:
    for line in f:
        p = line.strip().split('\t')
        if len(p) <= 14 or p[8] not in EURASIA_CC:
            continue
        try:
            pop = int(p[14])
            lat = float(p[4])
            lng = float(p[5])
        except ValueError:
            continue
        name = (p[2] or p[1]).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        _ALL_CITIES.append({'name': name, 'lat': lat, 'lng': lng, 'pop': pop})

print(f"Loaded {len(_ALL_CITIES)} Eurasia cities (no islands).")


def build_and_connect(cities, max_dist):
    """Build KNN-3 + radius graph, then Kruskal-bridge disconnected components."""
    n = len(cities)

    # Precompute full distance matrix
    dm = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine(cities[i]['lat'], cities[i]['lng'],
                          cities[j]['lat'], cities[j]['lng'])
            dm[i][j] = dm[j][i] = d

    G = nx.Graph()

    for i in range(n):
        order = sorted(range(n), key=lambda j, _i=i: dm[_i][j] if j != _i else 1e9)
        # Mandatory KNN
        for idx in order[:K_NEAREST]:
            G.add_edge(i, idx, weight=dm[i][idx])
        # Radius fill (list is sorted so break early)
        for idx in order[K_NEAREST:]:
            if dm[i][idx] <= max_dist:
                G.add_edge(i, idx, weight=dm[i][idx])
            else:
                break

    # Kruskal component bridging
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

    for u, v in G.edges():
        union(u, v)

    n_comp = len(set(find(i) for i in range(n)))
    bridge_count = 0

    if n_comp > 1:
        # Push ALL inter-component pairs into a min-heap
        heap = []
        for i in range(n):
            for j in range(i + 1, n):
                if find(i) != find(j):
                    heapq.heappush(heap, (dm[i][j], i, j))

        while heap and n_comp > 1:
            d, i, j = heapq.heappop(heap)
            if union(i, j):
                G.add_edge(i, j, weight=d)
                bridge_count += 1
                n_comp -= 1

    return G, dm, bridge_count


def objective(trial):
    pop_thr  = trial.suggest_int('pop_threshold', 50_000, 150_000, step=10_000)
    max_dist = trial.suggest_int('max_dist_km',   80,     200,     step=10)

    cities = [c for c in _ALL_CITIES if c['pop'] >= pop_thr]
    n = len(cities)
    if n < 50:
        return 1e6

    G, dm, bridges = build_and_connect(cities, max_dist)

    # Stretch factor over 50 random pairs
    random.seed(42)
    pairs = [(random.randint(0, n - 1), random.randint(0, n - 1)) for _ in range(50)]
    stretches = []
    for u, v in pairs:
        if u == v:
            continue
        try:
            gd = nx.astar_path_length(G, u, v, weight='weight')
            sd = dm[u][v]
            if sd > 0:
                stretches.append(gd / sd)
        except nx.NetworkXNoPath:
            pass  # shouldn't happen after bridging

    if not stretches:
        return 1e6

    avg_stretch = sum(stretches) / len(stretches)
    return avg_stretch + G.number_of_edges() / 50_000.0 + bridges * 0.05


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=40, show_progress_bar=True)

print(f"\nBest Params:   {study.best_params}")
print(f"Best Value:    {study.best_value:.4f}")
bp = study.best_params
cities_best = [c for c in _ALL_CITIES if c['pop'] >= bp['pop_threshold']]
print(f"Cities at best pop threshold: {len(cities_best)}")
