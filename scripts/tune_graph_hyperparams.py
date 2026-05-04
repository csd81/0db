"""
Offline HPO: find (pop_threshold, max_dist_km) that minimises edge count
while keeping the European city graph fully connected and avg_degree >= 2.5.

Run from repo root:
    pip install optuna
    python scripts/tune_graph_hyperparams.py
"""
import math
import optuna
import networkx as nx

INPUT = '/tmp/cities1000.txt'

EUROPEAN_CC = {
    'AL','AT','BY','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR',
    'HU','IE','IT','LV','LT','LU','MD','NL','MK','NO','PL','PT','RO','RS',
    'SK','SI','ES','SE','CH','UA','GB','ME','IS','MT','CY','AD','LI','MC',
    'SM','VA','XK',
}

# Load European cities once (name, lat, lng, pop) — reused across all trials
_ALL_CITIES = []
seen_names = set()
with open(INPUT, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) <= 14:
            continue
        if parts[8] not in EUROPEAN_CC:
            continue
        try:
            pop = int(parts[14])
            lat = float(parts[4])
            lng = float(parts[5])
        except ValueError:
            continue
        name = (parts[2] or parts[1]).strip()
        if not name or name in seen_names:
            continue
        seen_names.add(name)
        _ALL_CITIES.append((name, lat, lng, pop))

print(f"Loaded {len(_ALL_CITIES)} European cities from GeoNames.")


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def objective(trial):
    pop_thr  = trial.suggest_int('pop_threshold', 25_000, 80_000, step=5_000)
    max_dist = trial.suggest_int('max_dist_km',   40,     120,    step=5)

    cities = [c for c in _ALL_CITIES if c[3] >= pop_thr]
    n = len(cities)
    if n < 100:
        return 1_000_000

    G = nx.Graph()
    for i in range(n):
        G.add_node(i)

    for i in range(n):
        closest_dist = float('inf')
        closest_node = -1
        found_neighbor = False
        for j in range(i + 1, n):
            d = haversine(cities[i][1], cities[i][2], cities[j][1], cities[j][2])
            if d < closest_dist:
                closest_dist = d
                closest_node = j
            if d <= max_dist:
                G.add_edge(i, j)
                found_neighbor = True
        # Island fix: connect isolated cities to nearest
        if not found_neighbor and closest_node != -1:
            G.add_edge(i, closest_node)

    num_edges  = G.number_of_edges()
    avg_degree = (2 * num_edges) / n

    if not nx.is_connected(G):
        components = nx.number_connected_components(G)
        return 500_000 + components * 2_000 + num_edges

    if avg_degree < 2.5:
        return 400_000 + num_edges

    return num_edges


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=80, show_progress_bar=True)

print(f"\nBest Hyperparams: {study.best_params}")
print(f"Minimum Edges:    {study.best_value:,.0f} undirected")
print(f"Directed edges in GraphRoad: {int(study.best_value)*2:,}")
