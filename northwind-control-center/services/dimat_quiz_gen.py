"""
dimat_quiz_gen.py — Generate multiple-choice quizzes from solutions.md.

Strategy: pick 10 exercises with usable solutions, transform each into a
question whose stem is the problem statement and whose correct answer is a
short snippet extracted from the solution. Distractors come from sibling
solutions — surprisingly effective because sibling exercises are
topically-related but the correct sentence is rarely identical.

The generator is deterministic per chapter (seeded by chapter id) so
"Today's quiz" is stable across users for the daily-challenge feature.
"""

from __future__ import annotations

import hashlib
import random
import re

from services import dimat_data

_NUM_QS = 10

# Heuristic phrases to extract a "key claim" from a solution markdown blob.
# We pick the first sentence containing one of these patterns.
_KEY_PHRASES = [
    r'\bAnswer:\s*([^\n]+)',
    r'\bConclusion:\s*([^\n]+)',
    r'\bResult:\s*([^\n]+)',
    r'\bTherefore[,:]?\s*([^\n]+)',
    r'\bTehát[,:]?\s*([^\n]+)',
    r'\bAzaz[,:]?\s*([^\n]+)',
    r'\bIgazoljuk\s*[,:]?\s*([^\n]+)',
]


def _key_claim(solution_md: str) -> str:
    """Extracts a short answer string from a solution. Falls back to first sentence."""
    if not solution_md:
        return ''
    for pat in _KEY_PHRASES:
        m = re.search(pat, solution_md, re.IGNORECASE)
        if m:
            return _short(m.group(1))
    # First non-empty line that's not just a header
    for line in solution_md.splitlines():
        line = line.strip()
        if line and not line.startswith(('#', '|', '-', '*', '>')):
            return _short(line)
    return _short(solution_md.replace('\n', ' '))


def _short(s: str, max_len: int = 140) -> str:
    s = re.sub(r'\s+', ' ', s).strip().strip('*_').strip()
    if len(s) > max_len:
        s = s[:max_len].rsplit(' ', 1)[0] + '…'
    return s


def _hash_seed(*parts: str) -> int:
    h = hashlib.sha256(('|'.join(parts)).encode()).hexdigest()
    return int(h[:12], 16)


def generate_for_chapter(ch: str, difficulty: str = 'normal',
                         seed_extra: str = '') -> list[dict]:
    """Returns up to 10 quiz items for `ch`. If a hand-curated `quiz.md`
    exists for the chapter (currently only ch1), it is preferred verbatim.
    """
    data = dimat_data.get_chapter(ch)
    if data.get('quiz'):
        items = list(data['quiz'])
        rng = random.Random(_hash_seed(ch, difficulty, seed_extra))
        rng.shuffle(items)
        return items[:_NUM_QS]

    exes = [e for e in data.get('exercises', []) if e.get('solution_md')]
    if len(exes) < 2:
        return []

    rng = random.Random(_hash_seed(ch, difficulty, seed_extra))
    pool = list(exes)
    rng.shuffle(pool)
    chosen = pool[:_NUM_QS]

    out = []
    for i, ex in enumerate(chosen):
        correct = _key_claim(ex['solution_md'])
        if not correct:
            continue
        # Build distractors: pick 3 random sibling exercises' key claims
        siblings = [e for e in pool if e['id'] != ex['id']]
        rng.shuffle(siblings)
        distractors: list[str] = []
        for s in siblings:
            d = _key_claim(s.get('solution_md', ''))
            if d and d != correct and d not in distractors:
                distractors.append(d)
            if len(distractors) >= 3:
                break
        if len(distractors) < 3:
            continue

        opts = [{'k': 'A', 'text': correct}] + [
            {'k': 'BCDE'[j], 'text': distractors[j]} for j in range(3)
        ]
        rng.shuffle(opts)
        # Re-letter after shuffle so user-facing letters are stable
        for j, opt in enumerate(opts):
            opt['k'] = 'ABCDE'[j]
        # Find the new letter of the correct one
        ans = next(o['k'] for o in opts if o['text'] == correct)

        # In Hard mode, add a 5th distractor from a different chapter when possible
        if difficulty == 'hard' and len(opts) == 4:
            other_ch = None
            for cand_ch in dimat_data.ALL_CHAPTERS:
                if cand_ch != ch:
                    cand_data = dimat_data.get_chapter(cand_ch)
                    if cand_data.get('exercises'):
                        other_ch = cand_data
                        break
            if other_ch:
                cand_ex = rng.choice(other_ch['exercises'])
                d5 = _key_claim(cand_ex.get('solution_md', ''))
                if d5 and d5 != correct and d5 not in [o['text'] for o in opts]:
                    opts.append({'k': 'E', 'text': d5})

        # In Easy mode, drop one obviously different option (the longest one
        # that isn't the correct answer — usually the most "off-topic")
        if difficulty == 'easy' and len(opts) >= 4:
            wrong = [o for o in opts if o['text'] != correct]
            wrong_sorted = sorted(wrong, key=lambda o: -len(o['text']))
            opts = [o for o in opts if o is not wrong_sorted[0]]
            for j, opt in enumerate(opts):
                opt['k'] = 'ABCDE'[j]
            ans = next(o['k'] for o in opts if o['text'] == correct)

        question_stem = ex.get('problem_md') or ex.get('title') or ''
        out.append({
            'id': f"{ex['id']}",
            'q': _short(question_stem, 320),
            'options': opts,
            'answer': ans,
            'explanation': _short(ex.get('solution_md', ''), 400),
        })
    return out


def daily_challenge(seed_extra: str = '') -> list[dict]:
    """Pull 1–2 questions from each of 5 randomly-chosen chapters."""
    rng = random.Random(_hash_seed('daily', seed_extra))
    chs = [c for c in dimat_data.ALL_CHAPTERS
           if dimat_data.get_chapter(c).get('exercises')]
    rng.shuffle(chs)
    chosen_chs = chs[:5]
    out = []
    for ch in chosen_chs:
        qs = generate_for_chapter(ch, 'normal', seed_extra=seed_extra + ch)
        out.extend(qs[:2])
        if len(out) >= 10:
            break
    return out[:10]
