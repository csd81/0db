"""
dimat_data.py — Parses 0dimat_feladatok/ markdown into structured exercise data.

Source-of-truth files live OUTSIDE this app at:
  /home/csd81/Desktop/0db/0dimat_feladatok/{NN}_{slug}/
    ├── README.md
    ├── exercise_checklist.md
    ├── solutions.md
    └── (chapter 1 also has) quiz.md

Web is a *view*; parsed dicts are cached in memory at startup. A reload()
function is exposed for hot-rebuild during development.

Exercise key convention used everywhere downstream:
  ch1, ch2, …, ch23, appendix
This matches the URL slugs at /demos/dimat/<ch>.
"""

from __future__ import annotations

import os
import re
import threading
from pathlib import Path

# Repo root → /home/csd81/Desktop/0db   (parent of northwind-control-center/)
_REPO_ROOT = Path(__file__).resolve().parents[2]
_FELADATOK_DIR = _REPO_ROOT / '0dimat_feladatok'

# Chapter-number ↔ folder slug map. ch0 has no exercise folder (intro only).
# ch19–ch23 + appendix have no folders yet; they fall back to []
_CH_TO_FOLDER = {
    'ch1':  '01_Halmazok',
    'ch2':  '02_Elemi_leszammlalasok',
    'ch3':  '03_Binomialis_egyutthatok',
    'ch4':  '04_Logikai_szitaformula',
    'ch5':  '05_Rekurziv_sorozatok',
    'ch6':  '06_Generatorfuggvenyek',
    'ch7':  '07_Extremalis_halmazok',
    'ch8':  '08_Particios_problemak',
    'ch9':  '09_Graf_Alapfogalmak',
    'ch10': '10_Euler_utak',
    'ch11': '11_Hamilton_utak',
    'ch12': '12_Graf_matrixok',
    'ch13': '13_Utkereso_algoritmusok',
    'ch14': '14_Fak',
    'ch15': '15_Feszitofak',
    'ch16': '16_Izomorfia',
    'ch17': '17_Sikgrafok',
    'ch18': '18_Szinezesek',
}

# Recommended-prereq edges for skill-tree visualisation. (no hard locks; pure UI hint.)
SKILL_TREE_EDGES = [
    ('ch0',  'ch1'),  ('ch1',  'ch2'),  ('ch2',  'ch3'),
    ('ch3',  'ch4'),  ('ch3',  'ch7'),  ('ch4',  'ch5'),
    ('ch5',  'ch6'),  ('ch6',  'ch7'),  ('ch7',  'ch8'),
    ('ch1',  'ch9'),  ('ch9',  'ch10'), ('ch9',  'ch11'),
    ('ch9',  'ch12'), ('ch10', 'ch13'), ('ch11', 'ch13'),
    ('ch12', 'ch13'), ('ch13', 'ch14'), ('ch14', 'ch15'),
    ('ch9',  'ch16'), ('ch9',  'ch17'), ('ch17', 'ch18'),
    ('ch9',  'ch19'), ('ch19', 'ch22'), ('ch9',  'ch20'),
    ('ch12', 'ch21'), ('ch15', 'ch23'), ('ch3',  'appendix'),
]

# Chapter pretty-titles (for headers, leaderboard, badges)
CH_TITLES = {
    'ch0':  'Bevezetés',
    'ch1':  'Halmazok',
    'ch2':  'Elemi leszámlálások',
    'ch3':  'Binomiális együtthatók',
    'ch4':  'Logikai szita',
    'ch5':  'Rekurzív sorozatok',
    'ch6':  'Generátorfüggvények',
    'ch7':  'Extremális halmazok',
    'ch8':  'Partíciós problémák',
    'ch9':  'Gráf alapfogalmak',
    'ch10': 'Euler-utak',
    'ch11': 'Hamilton-utak',
    'ch12': 'Gráf-mátrixok',
    'ch13': 'Útkereső algoritmusok',
    'ch14': 'Fák',
    'ch15': 'Feszítőfák',
    'ch16': 'Izomorfia',
    'ch17': 'Síkgráfok',
    'ch18': 'Színezések',
    'ch19': 'Kétpólusú gráfok',
    'ch20': 'Extremális gráfok',
    'ch21': 'Gráfok spektruma',
    'ch22': 'Hálózati folyamok',
    'ch23': 'Matroidok',
    'appendix': 'Függelék',
}

ALL_CHAPTERS = list(CH_TITLES.keys())

# In-memory cache. Populated by load_all() at startup.
_CACHE: dict[str, dict] = {}
_CACHE_LOCK = threading.Lock()


# ── Solution parser ────────────────────────────────────────────────────────────

# Section header (NOT an exercise — sets context for following HF blocks):
#   ## Section 10.1 - Euler utak ...
#   ## 5.1 Lineáris rekurziók
_SECTION_HEADER_RE = re.compile(
    r'^##\s+(?:Section|Szakasz)?\s*([0-9]+(?:[.][0-9]+){0,2})\b',
    re.MULTILINE | re.IGNORECASE,
)

# Matches the various exercise headers found in solutions.md across chapters:
#   ### Exercise 5.0.1 - Title here     → numeric ID
#   ### 5.0.1. Title                    → numeric ID
#   ### Feladat 5.0.1                   → numeric ID
#   ### HF - Title                      → "homework" (Házi Feladat) — needs synthetic ID
#   ### HF: Title
#   ### HF1 - Title
_EX_HEADER_RE = re.compile(
    r'^###\s+'
    r'(?:'
        r'(?:Exercise|Feladat)\s*([0-9]+(?:[.][0-9]+){1,3})\.?'            # group 1: "Exercise N.M.K"
        r'|([0-9]+(?:[.][0-9]+){1,3})\.?'                                   # group 2: bare "N.M.K"
        r'|(HF[0-9]*)\b'                                                    # group 3: "HF" / "HF1" / etc.
    r')'
    r'\s*(?:[-–—:]\s*)?(.*?)$',                                             # group 4: anything else as title
    re.MULTILINE | re.IGNORECASE,
)

# Matches "**Solution:**" / "**Megoldás:**" / "## Solution" markers
_SOLUTION_MARK_RE = re.compile(
    r'(?im)^(?:\*\*\s*(?:Solution|Megoldás|Megoldas)\s*:?\s*\*\*|##+\s*(?:Solution|Megoldás|Megoldas)\b)',
)

# Matches "**Hint:**" / "**Útmutatás:**" markers
_HINT_MARK_RE = re.compile(
    r'(?im)^(?:\*\*\s*(?:Hint|Útmutatás|Tipp)\s*:?\s*\*\*)',
)


def _parse_solutions_md(text: str) -> list[dict]:
    """Split solutions.md into per-exercise dicts.
    Returns: [{id, title, problem_md, hint_md, solution_md}, ...]
    Robust to the format variations seen in the corpus.
    """
    if not text:
        return []
    matches = list(_EX_HEADER_RE.finditer(text))
    if not matches:
        return []

    # Pre-compute the most recent section number for each position so we can
    # synthesise stable IDs for `HF` headers (e.g. 9.1.HF1, 9.1.HF2).
    section_at: list[tuple[int, str]] = [(m.start(), m.group(1)) for m in _SECTION_HEADER_RE.finditer(text)]

    def section_for(pos: int) -> str:
        cur = ''
        for off, num in section_at:
            if off <= pos:
                cur = num
            else:
                break
        return cur

    hf_counter: dict[str, int] = {}

    out = []
    for i, m in enumerate(matches):
        numbered = m.group(1) or m.group(2)
        hf_marker = m.group(3)
        title_part = (m.group(4) or '').strip()

        if numbered:
            ex_id = numbered.strip().rstrip('.')
        else:
            # HF marker — synthesise a deterministic id keyed by section
            sec = section_for(m.start()) or '0'
            count = hf_counter.get(sec, 0) + 1
            hf_counter[sec] = count
            ex_id = f'{sec}.HF{count}'
        title = title_part
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()

        # Try to split body into problem | hint | solution
        hint_md = ''
        solution_md = ''
        problem_md = body

        sol_match = _SOLUTION_MARK_RE.search(body)
        if sol_match:
            problem_md = body[:sol_match.start()].strip()
            solution_md = body[sol_match.end():].strip()
            # Hint inside problem area?
            hint_match = _HINT_MARK_RE.search(problem_md)
            if hint_match:
                hint_md = problem_md[hint_match.end():].strip()
                problem_md = problem_md[:hint_match.start()].strip()

        # Strip leading "**Problem:**" / "**Feladat:**" labels if present
        problem_md = re.sub(
            r'^\*\*\s*(?:Problem|Feladat)\s*:?\s*\*\*\s*',
            '',
            problem_md,
            count=1,
            flags=re.IGNORECASE,
        ).strip()

        out.append({
            'id': ex_id,
            'title': title,
            'problem_md': problem_md,
            'hint_md': hint_md,
            'solution_md': solution_md,
        })
    return out


# ── Quiz parser (chapter 01 only currently) ────────────────────────────────────

def _parse_quiz_md(text: str) -> list[dict]:
    """Parse quiz.md into list of {id, q, options, answer, explanation}.
    Format used in 01_Halmazok/quiz.md:
      ### Q1: question text
      A) opt1
      B) opt2
      C) opt3
      D) opt4
      <details><summary>Answer</summary> X) ... explanation </details>
    """
    if not text:
        return []
    blocks = re.split(r'(?m)^###\s+Q?(\d+)\b[\.:]?\s*', text)
    if len(blocks) < 3:
        return []
    out = []
    # blocks looks like: ['', '1', 'body of Q1...', '2', 'body of Q2...', ...]
    for i in range(1, len(blocks) - 1, 2):
        qid = blocks[i].strip()
        body = blocks[i + 1].strip()
        # First line is the question
        lines = body.splitlines()
        q_lines = []
        opts = []
        rest = []
        in_opts = False
        for ln in lines:
            opt_m = re.match(r'^\s*([A-E])[)\.]\s*(.*)', ln)
            if opt_m:
                in_opts = True
                opts.append({'k': opt_m.group(1), 'text': opt_m.group(2).strip()})
            elif in_opts:
                rest.append(ln)
            else:
                q_lines.append(ln)
        question = ' '.join(l.strip() for l in q_lines if l.strip()).strip()
        rest_text = '\n'.join(rest)
        # Find the answer letter inside the rest_text
        ans_m = re.search(r'(?i)\bAnswer\s*[:\-]?\s*\*{0,2}\s*([A-E])', rest_text)
        if not ans_m:
            ans_m = re.search(r'^\s*([A-E])[)\.]\s*\*{0,2}\s*\(?Correct', rest_text, re.MULTILINE)
        answer = ans_m.group(1).upper() if ans_m else (opts[0]['k'] if opts else 'A')
        # Explanation is the rest after the answer marker
        expl = re.sub(r'<\/?(details|summary)[^>]*>', '', rest_text).strip()

        if question and opts:
            out.append({
                'id': f'q{qid}',
                'q': question,
                'options': opts,
                'answer': answer,
                'explanation': expl[:600],
            })
    return out


# ── Loader ─────────────────────────────────────────────────────────────────────

def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except (FileNotFoundError, UnicodeDecodeError):
        return ''


def _load_chapter(ch: str) -> dict:
    folder_name = _CH_TO_FOLDER.get(ch)
    title = CH_TITLES.get(ch, ch)
    out = {
        'ch': ch,
        'title': title,
        'exercises': [],
        'quiz': [],
        'has_folder': False,
        'readme_md': '',
    }
    if not folder_name:
        return out
    folder = _FELADATOK_DIR / folder_name
    if not folder.is_dir():
        return out
    out['has_folder'] = True
    out['readme_md'] = _read_text(folder / 'README.md')
    out['exercises'] = _parse_solutions_md(_read_text(folder / 'solutions.md'))
    quiz_text = _read_text(folder / 'quiz.md')
    if quiz_text:
        out['quiz'] = _parse_quiz_md(quiz_text)
    return out


def load_all() -> None:
    """Populate cache for every chapter. Idempotent — call from app factory."""
    with _CACHE_LOCK:
        for ch in ALL_CHAPTERS:
            _CACHE[ch] = _load_chapter(ch)


def reload() -> None:
    """Clear and re-populate cache. Useful in dev when markdown files change."""
    with _CACHE_LOCK:
        _CACHE.clear()
    load_all()


def get_chapter(ch: str) -> dict:
    """Returns the cached parsed data for a chapter, or empty stub if missing."""
    if not _CACHE:
        load_all()
    return _CACHE.get(ch, {
        'ch': ch, 'title': CH_TITLES.get(ch, ch),
        'exercises': [], 'quiz': [], 'has_folder': False, 'readme_md': '',
    })


def list_chapters() -> list[dict]:
    """Light overview for index pages: ch, title, exercise count."""
    if not _CACHE:
        load_all()
    return [
        {
            'ch': ch,
            'title': CH_TITLES.get(ch, ch),
            'count': len(_CACHE.get(ch, {}).get('exercises', [])),
            'has_folder': _CACHE.get(ch, {}).get('has_folder', False),
        }
        for ch in ALL_CHAPTERS
    ]


def total_exercise_count() -> int:
    if not _CACHE:
        load_all()
    return sum(len(c.get('exercises', [])) for c in _CACHE.values())


def get_skill_tree() -> dict:
    """Returns nodes + edges for the /learn/dimat skill-tree view (no hard locks)."""
    return {
        'nodes': [
            {'ch': ch, 'title': CH_TITLES.get(ch, ch),
             'count': len(_CACHE.get(ch, {}).get('exercises', []))}
            for ch in ALL_CHAPTERS
        ],
        'edges': [{'from': u, 'to': v} for u, v in SKILL_TREE_EDGES],
    }
