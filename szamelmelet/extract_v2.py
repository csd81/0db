#!/usr/bin/env python3
"""
Re-extract exercises AND solutions from AlgFgy-e-210218-cimlap.pdf.

Fixes from v1:
  - Uses correct local paths (was hard-coded to /home/rama/...)
  - Handles 4-level numbering (4.2.1.0), 4.3.4.5), etc.) — the old script's
    regex only matched 3-level, missing 68 exercises in sections 4.2 and 4.3
    (precisely the number-theory ones).
  - Splits Part I (Feladatok) vs Part II (Megoldások) and pairs them.

Output:
  /home/csd81/Desktop/0db/northwind-control-center/content/algo_exercises.json

Schema:
  {
    "feladatok": {
      "4.2.1.1": {"id": "4.2.1.1", "section": "4.2.1", "chapter": 4, ...,
                  "problem": "...", "solution": "..." or null},
      ...
    },
    "sections": {"4.2.1": "Alapműveletek", ...},
  }
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PDF = Path("/home/csd81/Desktop/0db/szamelmelet/AlgFgy-e-210218-cimlap.pdf")
OUT = Path("/home/csd81/Desktop/0db/northwind-control-center/content/algo_exercises.json")


def run_pdftotext() -> str:
    txt = Path("/tmp/algfgy_layout.txt")
    if not txt.exists() or txt.stat().st_mtime < PDF.stat().st_mtime:
        subprocess.run(["pdftotext", "-layout", str(PDF), str(txt)], check=True)
    return txt.read_text(encoding="utf-8")


# Exercise number: 3- or 4-level dot notation, e.g. "1.1.1)" or "4.2.1.0)"
EX_RE = re.compile(
    r"(?P<lead>(?:^|\n)\s*)"             # boundary
    r"(?P<num>\d+\.\d+\.\d+(?:\.\d+)?)\)",  # 3- or 4-level
)

SECTION_RE = re.compile(r"^\s*(\d+(?:\.\d+){1,2})\.\s+([^\d\n][^\n]{1,80})$", re.MULTILINE)


def split_parts(full: str) -> tuple[str, str]:
    """Return (feladatok_text, megoldasok_text)."""
    # The TOC mentions both "I.   Feladatok" and "II.      Megoldások" near top.
    # The real body markers are 'I. rész\n\nFeladatok' and 'II. rész\n\nMegoldások'.
    body_feladatok = full.find("I. rész")
    body_megoldasok = full.find("II. rész", body_feladatok + 10)
    # Skip past the marker block (~ 4 lines).
    def skip_marker(idx: int) -> int:
        end = full.find("\n", idx)
        # Skip header lines until first chapter content (number followed by '. fejezet' or section heading)
        return end + 1 if end > 0 else idx
    p1 = skip_marker(body_feladatok)
    p2 = skip_marker(body_megoldasok)
    return full[p1:body_megoldasok], full[p2:]


HUN_FIXES = [
    ("½o", "ő"), ("½u", "ű"), ("½U", "Ű"), ("½O", "Ő"),
    ("De…níció", "Definíció"), ("…", "fi"),  # ligature 'fi'
]


def clean_body(body: str) -> str:
    # Strip running page headers leaking into the body
    body = re.sub(r"\n\s*FEJEZET\s+\d+\.[^\n]*\n", "\n", body)
    body = re.sub(r"\n\s*\d+(?:\.\d+){1,2}\.\s+[A-ZÁÉÍÓÖŐÚÜŰ][^\n]{0,80}\n(?=\s*\n|\d)", "\n", body)
    body = re.sub(r"\n\s*\d+\s+\d+\.\s+A\s+Z[MN][^\n]*\n", "\n", body)
    # Standalone page numbers and "65", "138", etc.
    body = re.sub(r"\n\s*\d{1,3}\s*\n", "\n", body)
    # Footnote refs like "  21)\n  ..."  at end of body
    body = re.sub(r"(?:\n\s*\d+\)\s*\n[^\n]*)+$", "", body)
    # Collapse 3+ blank lines
    body = re.sub(r"\n\s*\n\s*\n+", "\n\n", body)
    # Hungarian char fixes
    for a, b in HUN_FIXES:
        body = body.replace(a, b)
    # Trim trailing whitespace per line
    body = "\n".join(line.rstrip() for line in body.splitlines()).strip()
    return body


def extract_exercises(block: str) -> list[tuple[str, str]]:
    """Find all exercise markers in `block`, return list of (number, body)."""
    matches = list(EX_RE.finditer(block))
    out: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        body = clean_body(block[start:end])
        out.append((m.group("num"), body))
    return out


def extract_section_titles(block: str) -> dict[str, str]:
    """Find section headings like '4.2.1. Alapműveletek' (1-3 levels)."""
    sections: dict[str, str] = {}
    for m in SECTION_RE.finditer(block):
        num = m.group(1)
        title = m.group(2).strip().rstrip(".")
        # Filter obvious noise (e.g., references with numbers)
        if any(ch.isdigit() for ch in title.split()[0]):
            continue
        if num not in sections and len(title) < 80:
            sections[num] = title
    return sections


# Map exercise id → chapter in the *Algoritmikus számelmélet* textbook.
# This is a curated mapping (not derived) from the AlgFgy book structure
# and the AlgSzÁm book chapters.
def algo_chapter_for(ex_id: str) -> int | None:
    """Return the textbook chapter (1-13) most relevant to this exercise, or None."""
    # AlgFgy chapter (first digit)
    parts = ex_id.split(".")
    main = parts[0]
    sub2 = ".".join(parts[:2]) if len(parts) >= 2 else ""
    sub3 = ".".join(parts[:3]) if len(parts) >= 3 else ""

    # Chapter 4 Gyűrűk → algoritmikus subsections
    if sub3 == "4.2.1":
        return 6   # Z_m alapműveletek (kongruenciák)
    if sub3 == "4.2.2":
        return 6   # általános/középiskolás (oszthatóság, maradékok)
    if sub3 == "4.2.3":
        return 6   # Euler / Fermat / nagy hatvány
    if sub3 == "4.2.4":
        return 10  # RSA
    if sub3 == "4.2.5":
        return 6   # struktúrák
    if sub3 == "4.3.1":
        return 13  # Euklideszi gyűrűk alapfogalmak
    if sub3 == "4.3.2":
        return 8   # prímfelbontás
    if sub3 == "4.3.3":
        return 4   # Euklidesz algoritmusa
    if sub3 == "4.3.4":
        return 5   # Lineáris Diophantikus
    if sub3 == "4.3.5":
        return 7   # Kínai maradéktétel
    if sub3 == "4.3.6":
        return 6   # magasabbfokú kongruenciák
    if sub2 == "4.4":
        return 13  # polinomok
    if sub2 == "4.1":
        return 13  # gyűrűk alapfogalmak
    if main == "5":
        return 13  # testek
    if main == "6":
        return 13  # hálók, Boole-algebrák
    return None    # chapters 1-3 of AlgFgy aren't directly mapped


def main() -> int:
    full = run_pdftotext()
    feladatok_txt, megoldasok_txt = split_parts(full)
    print(f"Feladatok block: {len(feladatok_txt):,} chars")
    print(f"Megoldások block: {len(megoldasok_txt):,} chars")

    f_list = extract_exercises(feladatok_txt)
    s_list = extract_exercises(megoldasok_txt)
    print(f"Problems found: {len(f_list)}, with {len({n for n, _ in f_list})} unique numbers")
    print(f"Solutions found: {len(s_list)}, with {len({n for n, _ in s_list})} unique numbers")

    # Pair each problem with its first matching solution.
    sol_lookup: dict[str, str] = {}
    for num, body in s_list:
        if num not in sol_lookup:
            sol_lookup[num] = body

    sections = extract_section_titles(feladatok_txt)
    print(f"Sections found: {len(sections)}")

    feladatok: dict[str, dict] = {}
    by_chapter: dict[int, list[str]] = {}
    for num, body in f_list:
        if num in feladatok:
            continue
        ch = algo_chapter_for(num)
        section_id = ".".join(num.split(".")[:3])
        feladatok[num] = {
            "id": num,
            "section": section_id,
            "section_title": sections.get(section_id) or sections.get(".".join(num.split(".")[:2])) or "",
            "chapter": int(num.split(".")[0]),
            "algo_chapter": ch,
            "problem": body,
            "solution": sol_lookup.get(num),
        }
        if ch is not None:
            by_chapter.setdefault(ch, []).append(num)

    # Stats
    with_sol = sum(1 for v in feladatok.values() if v["solution"])
    print(f"\nFinal: {len(feladatok)} exercises, {with_sol} with solutions")
    print(f"Distribution by AlgSzÁm chapter:")
    for ch, ids in sorted(by_chapter.items()):
        sols = sum(1 for i in ids if feladatok[i]["solution"])
        print(f"  ch{ch:2d}: {len(ids):3d} exercises ({sols} with solutions)")
    unmapped = [n for n, v in feladatok.items() if v["algo_chapter"] is None]
    print(f"  unmapped (AlgFgy ch 1-3): {len(unmapped)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "feladatok": feladatok,
        "sections": sections,
        "by_chapter": {str(k): v for k, v in by_chapter.items()},
        "unmapped": unmapped,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT} ({OUT.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
