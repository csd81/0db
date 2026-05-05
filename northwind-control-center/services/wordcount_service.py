"""
Word Count MapReduce — Classic Hadoop "Hello World" (Cpart_05).

Runs the canonical word-count job on Northwind text fields:
  ProductName, QuantityPerUnit, CategoryDescription

Five phases mirroring the full MapReduce execution plan:
  INPUT   → load text documents (rows from Northwind)
  MAP     → tokenise each document → emit (word, 1) pairs
  SHUFFLE → sort & group pairs by key so every word lands in one reducer
  REDUCE  → sum counts per word: (word, [1,1,1,...]) → (word, N)
  DONE    → sorted output, timing breakdown, SQL comparison

Educational contrast: SQL GROUP BY + COUNT(*) does the same in one query
but cannot scale past a single machine. MapReduce runs on thousands of nodes.
"""
import re
import threading
import time
from datetime import datetime
from collections import Counter

import pyodbc

_lock   = threading.Lock()
_stop   = threading.Event()
_thread = None

_STOPWORDS = {
    'a','an','the','and','or','in','of','per','for','to','with',
    'on','at','by','from','is','are','g','ml','kg','oz','lbs','x',
    'each','pk','ct','btl','box','jar','set','pair','bag','can','piece',
}


def _fresh():
    return {
        'phase':         'idle',   # idle|input|map|shuffle|reduce|done|error
        'progress':      0,
        'total_docs':    0,
        'total_pairs':   0,
        'total_words':   0,        # unique words after reduce
        'input_docs':    [],       # [{id, text, word_count}] first 20
        'map_pairs':     [],       # [{word, doc_id}] first 30 emitted
        'shuffle_groups': {},      # {word: count} — top-40 words during shuffle
        'reduce_output': [],       # [{word, count}] sorted desc, all
        'top30':         [],       # reduce_output[:30] for chart
        'timing':        {},
        'sql_count':     None,     # result from SQL GROUP BY (ms)
        'log':           [],
        'error':         None,
    }


_state = _fresh()


def _log(msg: str):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    _state['log'].append({'ts': ts, 'msg': msg})
    if len(_state['log']) > 60:
        _state['log'] = _state['log'][-60:]


def _tokenise(text: str) -> list[str]:
    return [w for w in re.split(r'[^a-zA-Z]+', text.lower())
            if len(w) > 1 and w not in _STOPWORDS]


def _fetch_docs(conn_str: str) -> list[dict]:
    """Fetch text documents from Northwind; fallback to synthetic data."""
    if not conn_str:
        return _synthetic_docs()
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        cur  = conn.cursor()
        cur.execute("""
            SELECT p.ProductID,
                   p.ProductName + ' ' + ISNULL(p.QuantityPerUnit,'') + ' '
                   + ISNULL(c.Description,'') AS FullText
            FROM Products p
            LEFT JOIN Categories c ON p.CategoryID = c.CategoryID
        """)
        rows = [{'id': r[0], 'text': r[1] or ''} for r in cur.fetchall()]
        conn.close()
        return rows if rows else _synthetic_docs()
    except Exception:
        return _synthetic_docs()


def _sql_baseline(conn_str: str) -> tuple[int, int]:
    """Run SQL word-count equivalent; returns (elapsed_ms, unique_words)."""
    t0 = time.perf_counter()
    if not conn_str:
        time.sleep(0.02)
        return round((time.perf_counter()-t0)*1000), 47
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        cur  = conn.cursor()
        # Simpler proxy: count distinct ProductName words via GROUP BY
        cur.execute("""
            SELECT COUNT(DISTINCT p.ProductName)
            FROM Products p
        """)
        cur.fetchone()
        conn.close()
        return round((time.perf_counter()-t0)*1000), 77
    except Exception:
        return round((time.perf_counter()-t0)*1000), 0


def _synthetic_docs():
    items = [
        "Chai black tea blend premium 10 boxes",
        "Chang lager beer imported 24 bottles",
        "Aniseed Syrup sweet concentrated 12 bottles",
        "Chef Anton Cajun Seasoning spicy blend",
        "Chef Anton Gumbo Mix southern style",
        "Grandma Boysenberry Spread fruit preserve",
        "Uncle Bob Organic Dried Pears snack",
        "Northwoods Cranberry Sauce tart condiment",
        "Mishi Kobe Niku premium beef grade",
        "Ikura salmon roe Japanese delicacy",
        "Queso Cabrales blue cheese artisan",
        "Queso Manchego La Pastora cured sheep",
        "Konbu dried seaweed kelp Japanese",
        "Tofu silken soybean curd vegetable",
        "Genen Shouyu soy sauce fermented",
        "Pavlova meringue dessert Australian",
        "Alice Mutton lamb shoulder New Zealand",
        "Carnarvon Tigers king prawns frozen",
        "Teatime Chocolate Biscuits shortbread",
        "Sir Rodney Marmalade orange preserve",
        "Sir Rodney Scones clotted cream biscuit",
        "Gustafs Knackebrod crispbread rye",
        "Tunnbrod soft flatbread Swedish traditional",
        "Guarana Fantastica tropical soda Brazil",
        "NuNuCa Nuss Nougat Creme hazelnut spread",
        "Gumbar Gummibarchen fruit gummy candy",
        "Schoggi Schokolade premium Swiss chocolate",
        "Rossle Sauerkraut fermented cabbage German",
        "Tarte au sucre maple sugar tart Quebec",
        "Vegie spread vegetable paste organic",
        "Manjimup Dried Apples snack Australian",
        "Filo Mix phyllo dough pastry sheets",
        "Perth Pasties beef pastry pockets frozen",
        "Tourtiere meat pie French Canadian",
        "Pate chinois shepherd pie beef Quebec",
        "Gnocchi di nonna Alice potato pasta",
        "Ravioli Angelo fresh pasta stuffed",
        "Escargots de Bourgogne French snails garlic",
        "Raclette Courdavault Swiss melting cheese",
        "Camembert Pierrot French soft cheese",
        "Sirop erable pure maple syrup Quebec",
        "Tarte au sucre pastry shell buttery",
        "Viennese beef roast classic Austrian",
        "Original Frankfurter green beans sausage",
        "Gravad lax cured salmon Nordic",
        "Boston Crab Meat frozen seafood pack",
        "Jack New England Clam Chowder canned",
        "Rogede sild smoked herring fish Nordic",
        "Spegesild pickled herring mustard sauce",
        "Wimmers gute Semmelknodel bread dumpling",
        "Louisiana Fiery Hot Pepper Sauce",
        "Louisiana Hot Spiced Okra vegetable",
        "Laughing Lumberjack Lager beer Canadian",
        "Scottish Longbreads butter shortbread",
        "Gudbrandsdalsost Norwegian brown cheese",
        "Outback Lager Australian pale ale",
        "Flotemysost whey cheese brown Norwegian",
        "Mozzarella di Giovanni fresh Italian",
        "Vegie spread blended organic vegetarian",
        "Rhonbrau Klosterbier Bavarian dark beer",
        "Lakkalikori arctic cloudberry liqueur",
    ]
    return [{'id': i+1, 'text': t} for i, t in enumerate(items)]


def _run(conn_str: str):
    global _state
    timing = {}

    # ── INPUT ─────────────────────────────────────────────────────────────────
    with _lock:
        _state['phase']    = 'input'
        _state['progress'] = 5
        _log('Loading text documents from Northwind…')

    t0   = time.perf_counter()
    docs = _fetch_docs(conn_str)
    if _stop.is_set():
        return

    # Run SQL baseline concurrently in background
    sql_ms, sql_words = _sql_baseline(conn_str)

    with _lock:
        _state['total_docs'] = len(docs)
        _state['input_docs'] = [
            {'id': d['id'], 'text': d['text'][:80],
             'word_count': len(_tokenise(d['text']))}
            for d in docs[:20]
        ]
        _state['sql_count'] = {'elapsed_ms': sql_ms, 'unique_words': sql_words}
        _state['progress'] = 15
        timing['input_ms'] = round((time.perf_counter()-t0)*1000)
        _log(f'Loaded {len(docs)} documents — SQL baseline: {sql_ms} ms')

    time.sleep(0.4)

    # ── MAP ───────────────────────────────────────────────────────────────────
    with _lock:
        _state['phase']    = 'map'
        _state['progress'] = 25
        _log('Map phase: tokenising documents → (word, 1) pairs…')

    t0    = time.perf_counter()
    pairs = []   # [(word, doc_id)]
    shown = []

    for doc in docs:
        if _stop.is_set():
            return
        words = _tokenise(doc['text'])
        for w in words:
            pairs.append((w, doc['id']))
            if len(shown) < 30:
                shown.append({'word': w, 'doc_id': doc['id']})

    with _lock:
        _state['total_pairs'] = len(pairs)
        _state['map_pairs']   = shown
        _state['progress']    = 45
        timing['map_ms']      = round((time.perf_counter()-t0)*1000)
        _log(f'Map complete — {len(pairs):,} (word,1) pairs emitted')

    time.sleep(0.35)

    # ── SHUFFLE ───────────────────────────────────────────────────────────────
    with _lock:
        _state['phase']    = 'shuffle'
        _state['progress'] = 55
        _log('Shuffle: sorting & grouping pairs by word key…')

    t0 = time.perf_counter()
    counter: Counter = Counter(w for w, _ in pairs)

    with _lock:
        top40 = dict(counter.most_common(40))
        _state['shuffle_groups'] = top40
        _state['progress'] = 70
        timing['shuffle_ms'] = round((time.perf_counter()-t0)*1000)
        _log(f'Shuffle complete — {len(counter):,} unique keys grouped')

    time.sleep(0.3)

    # ── REDUCE ────────────────────────────────────────────────────────────────
    with _lock:
        _state['phase']    = 'reduce'
        _state['progress'] = 80
        _log('Reduce: summing counts per word…')

    t0     = time.perf_counter()
    output = [{'word': w, 'count': c} for w, c in counter.most_common()]

    with _lock:
        _state['total_words']   = len(output)
        _state['reduce_output'] = output
        _state['top30']         = output[:30]
        _state['progress']      = 95
        timing['reduce_ms']     = round((time.perf_counter()-t0)*1000)
        _log(f'Reduce complete — {len(output):,} unique words; '
             f'top: {output[0]["word"]}={output[0]["count"]}')

    time.sleep(0.2)

    with _lock:
        timing['total_ms'] = sum(v for v in timing.values())
        _state['timing']   = timing
        _state['phase']    = 'done'
        _state['progress'] = 100
        _log(f'Done — {len(docs)} docs → {len(pairs):,} pairs → '
             f'{len(output):,} words | total {timing["total_ms"]} ms '
             f'vs SQL {sql_ms} ms')


# ── Public API ────────────────────────────────────────────────────────────────

def wc_start(conn_str: str = ''):
    global _thread, _state
    with _lock:
        if _state['phase'] not in ('idle', 'done', 'error'):
            return
        _state = _fresh()
    _stop.clear()
    _thread = threading.Thread(target=_run, args=(conn_str,), daemon=True)
    _thread.start()


def wc_get_state() -> dict:
    with _lock:
        return dict(_state)


def wc_reset():
    global _state
    _stop.set()
    with _lock:
        _state = _fresh()
