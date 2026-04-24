#!/usr/bin/env python3
"""Split the Hungarian Markdown notes into per-chapter files."""

import re
import os

INPUT = "/home/csorfolydaniel/0db/db2/jegyzet_halado_AB_Vassanyi_Istvan_2026.hu.claude.md"
BASE = "/home/csorfolydaniel/0db/chapters"

# (start_line_1indexed, dir)  — end is implicitly the next chapter start - 1
CHAPTERS = [
    (1,    "c1"),
    (485,  "c2"),
    (791,  "c3"),
    (1240, "c4"),
    (1438, "c5"),
    (1808, "c6"),
    (2122, "c7"),
    (2360, "c8"),
    (2774, "c9"),
    (2886, "c10"),
    (2890, "c11"),
    (3253, "c12"),
]

# Chapter headings begin with "# N." — SQL/bash comments also start with "#"
# so we use a numbered-chapter pattern to find real chapter boundaries.
CHAPTER_RE = re.compile(r'^# \d+\.')


def main():
    with open(INPUT, encoding="utf-8") as f:
        all_lines = f.readlines()
    total = len(all_lines)

    starts = [s - 1 for s, _ in CHAPTERS]   # 0-indexed
    ends = starts[1:] + [total]              # exclusive end for each chapter

    for (start, dirname), end in zip(CHAPTERS, ends):
        chapter_lines = all_lines[start - 1 : end]
        dirpath = os.path.join(BASE, dirname)
        os.makedirs(dirpath, exist_ok=True)

        outpath = os.path.join(dirpath, f"{dirname}.hu.md")
        with open(outpath, "w", encoding="utf-8") as f:
            f.writelines(chapter_lines)

        print(f"  {dirname}/  {len(chapter_lines):4d} lines  → {outpath}")


if __name__ == "__main__":
    main()
