#!/usr/bin/env python3
"""
Parse the Szalkai KombFeladatok-megoldasok.md file into structured JSON for
the Flask app. Each exercise is split into problem and solution parts,
rendered to HTML, and tagged with its category (Combinatorics / Graph
theory) and book-chapter reference.

Reads:  content/dimat_feladatok/KombFeladatok-megoldasok.md
Writes: content/dimat_feladatok/kombfeladatok.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import markdown as md_lib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'content' / 'dimat_feladatok' / 'KombFeladatok-megoldasok.md'
OUT = ROOT / 'content' / 'dimat_feladatok' / 'kombfeladatok.json'

# Match exercise headers. Variations seen in the source:
#   ### 01. 4.9. (Skatulyaelv - születésnapok)        — solo, parens
#   ### 49. 9.3. (Összeg: k × C(n,k))                 — title has nested ( )
#   ### 32-33. 7.13-7.14. (Kocka-gráf utak)           — composite range
#   ### 105-106. 16.7-16.8. (Komponensek keresése)
# We accept a range in both id and bookref, greedy title until end-of-line.
EX_HDR = re.compile(
    r'^###\s+'
    r'(?P<id>\d+(?:-\d+)?)\.\s+'
    r'(?P<bookref>\d+\.\d+(?:-\d+\.\d+)?)\.\s*'
    r'\((?P<title>.+)\)\s*$',
    re.MULTILINE,
)
SECTION_HDR = re.compile(r'^##\s+(?P<sect>I+)\.\s*(?P<sectname>[^\n]+)$', re.MULTILINE)

# Math-region protector (so markdown doesn't eat \\, \begin{}, etc.)
MATH_DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
MATH_INLINE = re.compile(r'\$([^$\n]+?)\$')


def _protect_math(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def stash_d(m): saved.append(f'$${m.group(1)}$$'); return f'@@M{len(saved)-1}@@'
    def stash_i(m): saved.append(f'${m.group(1)}$'); return f'@@M{len(saved)-1}@@'

    text = MATH_DISPLAY.sub(stash_d, text)
    text = MATH_INLINE.sub(stash_i, text)
    return text, saved


def _restore_math(html: str, saved: list[str]) -> str:
    for i, s in enumerate(saved):
        html = html.replace(f'@@M{i}@@', s)
    return html


def render_md(text: str) -> str:
    if not text.strip():
        return ''
    protected, saved = _protect_math(text)
    html = md_lib.markdown(
        protected,
        extensions=['extra', 'sane_lists', 'fenced_code', 'tables'],
        output_format='html5',
    )
    return _restore_math(html, saved)


def split_problem_solution(body: str) -> tuple[str, str]:
    """Find the first **Megoldás** marker; everything before = problem,
    everything from there = solution. The marker line is included in the
    solution. If no marker found, the whole body is the problem."""
    # Several variants: '**Megoldás:**', '**Megoldás a):**', etc.
    m = re.search(r'(?m)^\*\*Megoldás', body)
    if not m:
        return body.strip(), ''
    return body[:m.start()].strip(), body[m.start():].strip()


def main():
    text = SRC.read_text(encoding='utf-8')

    # Find section boundaries (I, II, ...). Build (start_offset, section_name) ranges.
    section_marks = list(SECTION_HDR.finditer(text))
    sections: list[tuple[int, str, str]] = []  # (start, roman, name)
    for m in section_marks:
        sections.append((m.start(), m.group('sect'), m.group('sectname').strip()))
    # Map offset → section
    def section_at(offset: int) -> tuple[str, str]:
        sect = ('', '')
        for s in sections:
            if s[0] <= offset:
                sect = (s[1], s[2])
            else:
                break
        return sect

    matches = list(EX_HDR.finditer(text))
    print(f'Found {len(matches)} exercises')

    exercises: list[dict] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        # Strip trailing '---' separators
        body = re.sub(r'\n+---\s*\n*$', '', body).strip()
        problem_md, solution_md = split_problem_solution(body)

        sect_roman, sect_name = section_at(m.start())
        book_ref = m.group('bookref')
        chapter_ref = int(book_ref.split('.')[0])
        raw_id = m.group('id')
        # For composite IDs like "32-33", n is the first number for sort order
        first_id = int(raw_id.split('-')[0])

        exercises.append({
            'id': raw_id,                            # "01", "32-33", ...
            'n': first_id,
            'book_ref': book_ref,                   # "4.9" or "7.13-7.14"
            'chapter_ref': chapter_ref,             # 4
            'title': m.group('title').strip(),
            'section': sect_roman,                  # "I" or "II"
            'section_name': sect_name,
            'problem_md': problem_md,
            'problem_html': render_md(problem_md),
            'solution_md': solution_md,
            'solution_html': render_md(solution_md),
        })

    # Group exercises by section + chapter
    by_section: dict[str, list[dict]] = {}
    by_chapter: dict[int, list[str]] = {}
    for ex in exercises:
        by_section.setdefault(ex['section'], []).append(ex['id'])
        by_chapter.setdefault(ex['chapter_ref'], []).append(ex['id'])

    # Stats by chapter
    print(f'\nSection breakdown:')
    for sect, ids in sorted(by_section.items()):
        print(f"  Section {sect}: {len(ids)} exercises")
    print(f'\nChapter breakdown:')
    for ch, ids in sorted(by_chapter.items()):
        print(f"  ch{ch}: {len(ids)} exercises")

    data = {
        'source': 'Szalkai István — KombFeladatok-megoldasok (2023)',
        'count': len(exercises),
        'exercises': {ex['id']: ex for ex in exercises},
        'by_section': by_section,
        'by_chapter': {str(k): v for k, v in by_chapter.items()},
        'sections': {s[1]: s[2] for s in sections},
    }

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nWrote {OUT} ({OUT.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
