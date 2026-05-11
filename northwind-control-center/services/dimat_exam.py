"""
dimat_exam.py — Loads the 39-topic exam-syllabus ("tételsor") markdown files
into structured records cached in memory.

Source-of-truth files at:
  northwind-control-center/content/tetelsor/01.md … 39.md

Each file has YAML frontmatter (n, title, glossary, path, related_*, formulas)
followed by Hungarian markdown body. The body is rendered to HTML at load time.

Public accessors:
  - get_topic(n)            → dict for one tétel, with prev/next computed within its path
  - list_topics_in_path(p)  → ordered list for path ∈ {'combo','graph','szamelm'}
  - all_topics()            → ordered list 1..39
  - reload()                → rebuild cache (dev convenience)

Path → tétel-number convention:
  combo   = 1..10
  graph   = 11..29
  szamelm = 30..39
"""

from __future__ import annotations

import re
import threading
from pathlib import Path

import yaml
import markdown as md_lib

_CONTENT_DIR = Path(__file__).resolve().parents[1] / 'content' / 'tetelsor'

_FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)$', re.DOTALL)

PATH_OF_N = {}
for n in range(1, 11):
    PATH_OF_N[n] = 'combo'
for n in range(11, 30):
    PATH_OF_N[n] = 'graph'
for n in range(30, 40):
    PATH_OF_N[n] = 'szamelm'

PATH_META = {
    'combo':   {'slug': 'combo',   'title': 'Kombinatorika',   'colour': '#f59e0b', 'range': (1, 10)},
    'graph':   {'slug': 'graph',   'title': 'Gráfelmélet',     'colour': '#38bdf8', 'range': (11, 29)},
    'szamelm': {'slug': 'szamelm', 'title': 'Számelmélet',     'colour': '#a78bfa', 'range': (30, 39)},
}

_CACHE: dict[int, dict] = {}
_LOCK = threading.Lock()


def _md_to_html(body: str) -> str:
    return md_lib.markdown(
        body,
        extensions=['extra', 'tables', 'sane_lists', 'fenced_code', 'toc'],
        output_format='html5',
    )


def _parse_file(p: Path) -> dict | None:
    try:
        raw = p.read_text(encoding='utf-8')
    except OSError:
        return None
    m = _FRONTMATTER_RE.match(raw)
    if not m:
        return None
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None
    body_md = m.group(2)
    n = int(meta.get('n', 0))
    if not (1 <= n <= 39):
        return None
    return {
        'n': n,
        'title': meta.get('title', f'Tétel {n}'),
        'glossary': meta.get('glossary', ''),
        'path': meta.get('path') or PATH_OF_N.get(n, 'combo'),
        'related_dimat': meta.get('related_dimat', []) or [],
        'related_ila': meta.get('related_ila', []) or [],
        'related_exercises': meta.get('related_exercises', []) or [],
        'formulas': meta.get('formulas', []) or [],
        'body_html': _md_to_html(body_md),
    }


def _load_all() -> None:
    cache: dict[int, dict] = {}
    if _CONTENT_DIR.exists():
        for p in sorted(_CONTENT_DIR.glob('*.md')):
            rec = _parse_file(p)
            if rec is not None:
                cache[rec['n']] = rec
    with _LOCK:
        _CACHE.clear()
        _CACHE.update(cache)


_load_all()


def reload() -> None:
    _load_all()


def _siblings(n: int) -> tuple[int | None, int | None]:
    """Prev/next tétel within the same path (None at path boundary)."""
    path = PATH_OF_N.get(n)
    if not path:
        return (None, None)
    lo, hi = PATH_META[path]['range']
    prev_n = n - 1 if n - 1 >= lo else None
    next_n = n + 1 if n + 1 <= hi else None
    return (prev_n, next_n)


def get_topic(n: int) -> dict | None:
    rec = _CACHE.get(n)
    if rec is None:
        return None
    prev_n, next_n = _siblings(n)
    return {
        **rec,
        'path_meta': PATH_META[rec['path']],
        'prev': prev_n,
        'next': next_n,
    }


def list_topics_in_path(path: str) -> list[dict]:
    if path not in PATH_META:
        return []
    lo, hi = PATH_META[path]['range']
    out = []
    for n in range(lo, hi + 1):
        rec = _CACHE.get(n)
        if rec is None:
            out.append({
                'n': n,
                'title': f'Tétel {n} (még nincs feltöltve)',
                'glossary': '',
                'path': path,
                'related_dimat': [],
                'related_ila': [],
                'related_exercises': [],
                'formulas': [],
                'body_html': '',
                'missing': True,
            })
        else:
            out.append({**rec, 'missing': False})
    return out


def all_topics() -> list[dict]:
    out = []
    for path in ('combo', 'graph', 'szamelm'):
        out.extend(list_topics_in_path(path))
    return out


def path_meta(path: str) -> dict | None:
    return PATH_META.get(path)
