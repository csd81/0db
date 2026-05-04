"""
GPU-accelerated HPO — Valence-Cap Graph Tuner  (sm_61 / Quadro P2000 compatible)

Tunes:  min_knn, max_valence, local_km
Obj:    avg_stretch + valence_penalty + hop_density_penalty

GPU phase (CuPy, JIT-compiled for sm_61): batched N×K_MAX haversine KNN matrix
CPU phase: NetworkX Dijkstra + BFS hop counting, Optuna TPE search

cuDF / cuGraph are NOT used — they require sm_70+ and will crash on P2000.

Run: python scripts/tune_graph_hyperparams_gpu.py
"""
import math
import random
import time

import cupy as cp
import networkx as nx
import numpy as np
import optuna

INPUT_FILE  = '/tmp/cities1000.txt'
MIN_POP     = 40_000       # same as generator — fixed city set
R           = 6371.0
K_MAX       = 17           # max_valence_max(12) + 5 candidates per city
BATCH_SIZE  = 1_000        # rows per GPU batch (keeps VRAM < 200 MB)

TARGET_VALENCE         = 7.5
TARGET_HOPS_PER_1000KM = 11.0
VALENCE_PENALTY_WEIGHT = 2.0
HOP_PENALTY_WEIGHT     = 0.5

N_ANCHORS  = 10   # Dijkstra sources per trial
N_TARGETS  = 50   # candidate pairs sampled per anchor

CONTINENTAL_CC = {
    'AL','AT','BY','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR',
    'HU','IT','LV','LT','LU','MD','NL','MK','NO','PL','PT','RO','RS',
    'SK','SI','ES','SE','CH','UA','ME','AD','LI','MC','SM','VA','XK',
    'GE','AM','AZ','KZ','UZ','TM','TJ','KG',
    'TR','IR','IQ','SY','JO','IL','LB','PS','SA','AE','KW','BH','QA','OM','YE',
    'IN','PK','AF','NP','BT','BD',
    'CN','MN','KP','KR','MM','TH','VN','LA','KH','MY','RU',
    'DZ','EG','LY','MA','SD','TN',
    'ET','ER','DJ','KE','TZ','UG','RW','BI','SO',
    'BJ','BF','CI','GH','GN','GM','GW','LR','ML','MR','NE','NG','SN','SL','TG',
    'CM','CF','TD','CG','CD','GQ','GA','AO','BW','LS','MW','MZ','NA','ZA','ZM','ZW','SS',
}
ISLAND_CC = {'GB','IE','IS','JP','TW','ID','PH','LK','CY','MT'}
ALL_CC    = CONTINENTAL_CC | ISLAND_CC


# ── 1. Load cities (fixed set, same threshold as generator) ───────────────────
print('Loading cities …')
_cities: list = []
_seen: set = set()
with open(INPUT_FILE, encoding='utf-8') as f:
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) < 15 or p[8] not in ALL_CC:
            continue
        try:
            if int(p[14]) < MIN_POP:
                continue
            lat = float(p[4])
            lng = float(p[5])
        except ValueError:
            continue
        name = (p[2] or p[1]).strip()
        if not name or name in _seen:
            continue
        _seen.add(name)
        _cities.append({'name': name, 'lat': lat, 'lng': lng})

n = len(_cities)
lats_np = np.array([c['lat'] for c in _cities], dtype=np.float32)
lngs_np = np.array([c['lng'] for c in _cities], dtype=np.float32)
print(f'   → {n} cities (MIN_POP={MIN_POP:,})')


# ── 2. GPU: batched N×K_MAX KNN distance matrix ───────────────────────────────
def _precompute_knn_gpu() -> tuple[np.ndarray, np.ndarray]:
    print(f'Pre-computing {n}×{K_MAX} KNN on GPU (batches of {BATCH_SIZE}) …')
    t0 = time.perf_counter()

    phi_all = cp.asarray(np.radians(lats_np), dtype=cp.float32).reshape(1, -1)
    lam_all = cp.asarray(np.radians(lngs_np), dtype=cp.float32).reshape(1, -1)

    indices  = np.empty((n, K_MAX), dtype=np.int32)
    dists_km = np.empty((n, K_MAX), dtype=np.float32)

    for start in range(0, n, BATCH_SIZE):
        end = min(start + BATCH_SIZE, n)
        bs  = end - start

        phi_b = cp.asarray(np.radians(lats_np[start:end]), dtype=cp.float32).reshape(-1, 1)
        lam_b = cp.asarray(np.radians(lngs_np[start:end]), dtype=cp.float32).reshape(-1, 1)

        a = (cp.sin((phi_b - phi_all) / 2.0) ** 2
             + cp.cos(phi_b) * cp.cos(phi_all) * cp.sin((lam_b - lam_all) / 2.0) ** 2)
        D = R * 2.0 * cp.arctan2(cp.sqrt(a), cp.sqrt(1.0 - a))   # (bs, N) float32 km
        del a, phi_b, lam_b

        # Exclude self by setting diagonal to large value
        D[cp.arange(bs, dtype=cp.int32), cp.arange(start, end, dtype=cp.int32)] = 1e9

        # K_MAX nearest per row (unsorted partition, then sort K_MAX slice)
        part_idx = cp.argpartition(D, K_MAX, axis=1)[:, :K_MAX]   # (bs, K_MAX)
        part_d   = D[cp.arange(bs)[:, None], part_idx]
        del D

        sort_ord   = cp.argsort(part_d, axis=1)
        sorted_idx = part_idx[cp.arange(bs)[:, None], sort_ord]
        sorted_d   = part_d[cp.arange(bs)[:, None], sort_ord]
        del part_idx, part_d, sort_ord

        indices[start:end]  = cp.asnumpy(sorted_idx).astype(np.int32)
        dists_km[start:end] = cp.asnumpy(sorted_d).astype(np.float32)
        del sorted_idx, sorted_d
        cp.get_default_memory_pool().free_all_blocks()

    del phi_all, lam_all
    cp.get_default_memory_pool().free_all_blocks()
    print(f'   → done in {time.perf_counter() - t0:.1f}s')
    return indices, dists_km


# ── 3. Haversine helper ───────────────────────────────────────────────────────
def _hav(la1, lo1, la2, lo2):
    dlat = math.radians(la2 - la1)
    dlng = math.radians(lo2 - lo1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(la1)) * math.cos(math.radians(la2))
         * math.sin(dlng / 2) ** 2)
    return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


# ── 4. Optuna objective ───────────────────────────────────────────────────────
def make_objective(knn_indices: np.ndarray, knn_dists: np.ndarray):
    def objective(trial: optuna.Trial) -> float:
        min_knn     = trial.suggest_int('min_knn',     3,  5)
        max_valence = trial.suggest_int('max_valence',  7, 12)
        local_km    = trial.suggest_int('local_km',    35, 85)

        # Build graph with valence-cap logic
        G = nx.Graph()
        city_degree = np.zeros(n, dtype=np.int32)

        for i in range(n):
            for k in range(K_MAX):
                j    = int(knn_indices[i, k])
                d    = float(knn_dists[i, k])
                rank = k + 1   # 1-indexed

                is_mandatory = rank <= min_knn
                at_cap       = city_degree[i] >= max_valence

                if is_mandatory:
                    if not G.has_edge(i, j):
                        G.add_edge(i, j, weight=d)
                        city_degree[i] += 1
                        city_degree[j] += 1
                elif at_cap:
                    break   # past mandatory zone + at cap → no point looking further
                elif d <= local_km:
                    if not G.has_edge(i, j):
                        G.add_edge(i, j, weight=d)
                        city_degree[i] += 1
                        city_degree[j] += 1

        avg_valence = float(city_degree.mean())

        # Sample anchors — fixed per trial number for reproducibility
        random.seed(trial.number)
        anchors = random.sample(range(n), min(N_ANCHORS, n))

        stretch_scores: list = []
        hop_scores:     list = []

        for anchor in anchors:
            try:
                lengths  = nx.single_source_dijkstra_path_length(G, anchor, weight='weight')
                bfs_hops = nx.single_source_shortest_path_length(G, anchor)
            except Exception:
                return 1e6

            # Candidate long-haul targets
            candidates = [(tgt, km) for tgt, km in lengths.items()
                          if tgt != anchor and 500 <= km <= 8_000]
            random.shuffle(candidates)

            for tgt, km in candidates[:N_TARGETS]:
                direct = _hav(_cities[anchor]['lat'], _cities[anchor]['lng'],
                              _cities[tgt]['lat'],    _cities[tgt]['lng'])
                if direct < 200:
                    continue
                stretch_scores.append(km / direct)
                if km <= 3_000 and tgt in bfs_hops:
                    hop_scores.append(bfs_hops[tgt] / km * 1_000)

        if not stretch_scores:
            return 1e6

        avg_stretch = float(np.mean(stretch_scores))
        avg_hops    = float(np.mean(hop_scores)) if hop_scores else 0.0

        valence_penalty = max(0.0, avg_valence - TARGET_VALENCE) * VALENCE_PENALTY_WEIGHT
        hop_penalty     = max(0.0, TARGET_HOPS_PER_1000KM - avg_hops) * HOP_PENALTY_WEIGHT
        score = avg_stretch + valence_penalty + hop_penalty

        trial.report(score, step=0)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

        print(f'  T{trial.number:02d}: min_knn={min_knn} max_val={max_valence} '
              f'local={local_km:2d}km  '
              f'stretch={avg_stretch:.3f} valence={avg_valence:.1f} '
              f'hops/1k={avg_hops:.1f}  score={score:.3f}')
        return score

    return objective


# ── 5. Entry point ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    dev = cp.cuda.Device()
    print(f'GPU: CuPy device {dev.id}  ({dev.mem_info[1] / 1e9:.2f} GB VRAM)')
    print(f'Note: cuDF/cuGraph skipped — P2000 is sm_61; RAPIDS 26 requires sm_70+')
    print()

    knn_indices, knn_dists_km = _precompute_knn_gpu()

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=0),
    )

    print(f'\nRunning 50 trials …')
    t0 = time.perf_counter()
    study.optimize(make_objective(knn_indices, knn_dists_km),
                   n_trials=50, n_jobs=1, show_progress_bar=False)
    elapsed = time.perf_counter() - t0

    pruned    = sum(1 for t in study.trials if t.state == optuna.trial.TrialState.PRUNED)
    completed = sum(1 for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE)

    bp = study.best_params
    print(f'\n{"=" * 52}')
    print(f'Best params:  {bp}')
    print(f'Best score:   {study.best_value:.4f}')
    print(f'Wall time:    {elapsed:.1f}s  ({elapsed / 50:.1f}s/trial avg)')
    print(f'Completed: {completed}   Pruned: {pruned}')
    print(f'\nCopy these into generate_city_data.py:')
    print(f'  MIN_KNN     = {bp["min_knn"]}')
    print(f'  MAX_VALENCE = {bp["max_valence"]}')
    print(f'  LOCAL_KM    = {bp["local_km"]}')
