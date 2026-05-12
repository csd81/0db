#!/usr/bin/env python3
"""
Apply regex transformations to convert plaintext exercise bodies into
KaTeX-renderable inline / display math.

Reads:   northwind-control-center/content/algo_exercises.json
Writes:  northwind-control-center/content/algo_exercises.json   (in place)

Strategy:
  Each `problem` and `solution` field gets a sequence of substitutions
  applied. Math fragments are wrapped in $...$ so the template's KaTeX
  auto-render picks them up. Exercises with `manual: true` are skipped
  (those are hand-polished — see overrides at the end of the script).

Limitations:
  - Superscripts/subscripts lost by pdftotext cannot be recovered without
    context. Where I can confidently guess (e.g. "2 N 1" near "Mersenne"),
    I rewrite by hand in the override block.
  - The script aims for "useful and readable", not "perfect LaTeX".
"""

from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path

try:
    import markdown as md_lib
    HAS_MD = True
except ImportError:
    HAS_MD = False

PATH = Path("/home/csd81/Desktop/0db/northwind-control-center/content/algo_exercises.json")


# ─────────────────── Symbol → LaTeX replacements ──────────────────────────────

LIGATURES = {
    "¤": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
    "½o": "ő", "½u": "ű", "½U": "Ű", "½O": "Ő",
}

# Page headers that leak through pdftotext
PAGE_HEADER_PATTERNS = [
    re.compile(r"\n+\s*\d{1,3}\s+FEJEZET\s+\d+\.[^\n]*\n+", re.IGNORECASE),
    re.compile(r"\n+\s*\d+\.\d+\.\s+A\s+(\\?\\?\$?\\?mathbb)?\{?Z\}?_?M?[^\n]*\n+", re.IGNORECASE),
    re.compile(r"\n+\s*\d{1,3}\s+\d+\.\d+\.\s+A\s+[A-Z][^\n]{0,80}\n+"),
]
FOOTNOTE_END_RE = re.compile(r"(?:\n\s*\d+\)\s*\n[^\n]{0,200})+$")
MULTI_SPACE_RE = re.compile(r"   +")


def pre_clean(text: str) -> str:
    """Remove pdftotext artifacts before latexification."""
    for a, b in LIGATURES.items():
        text = text.replace(a, b)
    for pat in PAGE_HEADER_PATTERNS:
        text = pat.sub("\n", text)
    text = FOOTNOTE_END_RE.sub("", text)
    # Collapse 3+ spaces → 1 (preserve word breaks but kill column alignment)
    text = MULTI_SPACE_RE.sub(" ", text)
    # Strip trailing/leading whitespace per line
    text = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    # Collapse 3+ blank lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text


UNICODE_MAP = {
    # Set / logic
    "∈": r"\in",
    "∉": r"\notin",
    "⊂": r"\subset",
    "⊆": r"\subseteq",
    "⊃": r"\supset",
    "⊇": r"\supseteq",
    "∩": r"\cap",
    "∪": r"\cup",
    "∅": r"\emptyset",
    "∀": r"\forall",
    "∃": r"\exists",
    "¬": r"\neg",
    "∧": r"\wedge",
    "∨": r"\vee",
    # Arithmetic / relations
    "≡": r"\equiv",
    "≠": r"\neq",
    "≤": r"\leq",
    "≥": r"\geq",
    "·": r"\cdot",
    "×": r"\times",
    "÷": r"\div",
    "±": r"\pm",
    "∓": r"\mp",
    "∞": r"\infty",
    # Greek
    "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
    "ε": r"\varepsilon", "ζ": r"\zeta", "η": r"\eta", "θ": r"\theta",
    "ι": r"\iota", "κ": r"\kappa", "λ": r"\lambda", "μ": r"\mu",
    "ν": r"\nu", "ξ": r"\xi", "π": r"\pi", "ρ": r"\rho",
    "σ": r"\sigma", "τ": r"\tau", "υ": r"\upsilon", "φ": r"\varphi",
    "ϕ": r"\varphi", "χ": r"\chi", "ψ": r"\psi", "ω": r"\omega",
    "Γ": r"\Gamma", "Δ": r"\Delta", "Θ": r"\Theta",
    "Λ": r"\Lambda", "Π": r"\Pi", "Σ": r"\Sigma", "Φ": r"\Phi",
    "Ψ": r"\Psi", "Ω": r"\Omega",
    # Number sets
    "ℕ": r"\mathbb{N}",
    "ℤ": r"\mathbb{Z}",
    "ℚ": r"\mathbb{Q}",
    "ℝ": r"\mathbb{R}",
    "ℂ": r"\mathbb{C}",
    "ℙ": r"\mathbb{P}",
    # Misc
    "√": r"\sqrt",
    "→": r"\to",
    "←": r"\leftarrow",
    "⇒": r"\Rightarrow",
    "⇐": r"\Leftarrow",
    "⇔": r"\Leftrightarrow",
    "…": r"\dots",
    "−": "-",   # Unicode minus → ASCII
    "•": r"\bullet",
    "‰": r"‰",
}


# ─────────────────── Math-region rewrites ─────────────────────────────────────

# Patterns applied AFTER unicode replacement. Each entry: (regex, replacement).
# These transform plaintext fragments and wrap them in $…$ so KaTeX renders them.

PATTERNS: list[tuple[str, str]] = [
    # (mod N) and (mod N1, N2 ...) — most reliable target
    (r"\(\s*mod\s+([^\)]+?)\s*\)", r"$\\pmod{\1}$"),
    (r"\(\s*MOD\s+([^\)]+?)\s*\)", r"$\\operatorname{MOD}{\1}$"),

    # lnko/lkkt/gcd/lcm followed by parens → operatorname inside math
    (r"\blnko\s*\(([^()]{0,80}?)\)", r"$\\operatorname{lnko}(\1)$"),
    (r"\blkkt\s*\(([^()]{0,80}?)\)", r"$\\operatorname{lkkt}(\1)$"),
    (r"\bgcd\s*\(([^()]{0,80}?)\)", r"$\\gcd(\1)$"),
    (r"\blcm\s*\(([^()]{0,80}?)\)", r"$\\operatorname{lcm}(\1)$"),

    # phi(n) / varphi(n) function applications
    (r"\bphi\s*\(([^()]{0,40}?)\)", r"$\\varphi(\1)$"),
    (r"\bvarphi\s*\(([^()]{0,40}?)\)", r"$\\varphi(\1)$"),

    # Z[i], Z[ρ], Z[α], Z[√m], Z[u] generic
    (r"\bZ\s*\[\s*i\s*\]", r"$\\mathbb{Z}[i]$"),
    (r"\bZ\s*\[\s*\\rho\s*\]", r"$\\mathbb{Z}[\\rho]$"),
    (r"\bZ\s*\[\s*\\alpha\s*\]", r"$\\mathbb{Z}[\\alpha]$"),
    (r"\bZ\s*\[\s*\\varepsilon\s*\]", r"$\\mathbb{Z}[\\varepsilon]$"),
    (r"\bZ\s*\[\s*u\s*\]", r"$\\mathbb{Z}[u]$"),
    (r"\bZ\s*\[\s*x\s*\]", r"$\\mathbb{Z}[x]$"),
    (r"\bR\s*\[\s*x\s*\]", r"$\\mathbb{R}[x]$"),
    (r"\bQ\s*\[\s*x\s*\]", r"$\\mathbb{Q}[x]$"),
    (r"\bC\s*\[\s*x\s*\]", r"$\\mathbb{C}[x]$"),

    # Z_m maradékosztály (Zm without subscript notation in source)
    (r"\bZm\b", r"$\\mathbb{Z}_m$"),
    (r"\bZn\b", r"$\\mathbb{Z}_n$"),
    (r"\bZp\b", r"$\\mathbb{Z}_p$"),
    (r"\bZ\*m\b", r"$\\mathbb{Z}_m^*$"),
    (r"\bZ\*n\b", r"$\\mathbb{Z}_n^*$"),
    (r"\bZ\*p\b", r"$\\mathbb{Z}_p^*$"),

    # GF(p^k) finite field
    (r"\bGF\(([0-9]+)\)", r"$\\operatorname{GF}(\1)$"),

    # Subscript-less variables that appear with subscript-like spaces:
    # "m1, m2, mr" patterns — leave alone, hard to disambiguate.

    # Common phrases — just typography
    (r"\bin\\s+(\\\\mathbb\{[PNQRZC]\})\b", r"$\\in \1$"),
]


# Collapse adjacent inline math: $A$ + $B$ → $A B$ (where they touch)
COLLAPSE = re.compile(r"\$([^$]+?)\$\s*\$([^$]+?)\$")


def latexify(text: str) -> str:
    if not text:
        return text
    # 0) Defensive pdftotext-artifact cleanup
    text = pre_clean(text)
    # 1) Unicode replacement (excluding inside existing $...$ — but at this stage
    #    there are no $...$ yet, so safe to do globally).
    for u, latex in UNICODE_MAP.items():
        text = text.replace(u, latex)
    # 2) Regex rewrites
    for pat, repl in PATTERNS:
        text = re.sub(pat, repl, text)
    # 3) Collapse adjacent inline math up to 3 passes
    for _ in range(3):
        new = COLLAPSE.sub(r"$\1 \2$", text)
        if new == text:
            break
        text = new
    return text


# ─────────────────── Hand-polished overrides ──────────────────────────────────
# These exercises are rewritten by hand in clean KaTeX. The script writes them
# verbatim into the JSON and sets `manual: true` so future runs don't clobber.

OVERRIDES: dict[str, dict[str, str]] = {

    # ─── Chapter 4 — Euklidesz ──────────────────────────────────────
    "4.3.3.1": {
        "problem": (
            "Keresse meg az alábbi számok legnagyobb közös osztóját:\n\n"
            "**a)** $7732$ és $149$\n\n"
            "**b)** $94542$ és $24981$"
        ),
        "solution": (
            "**a)** $\\operatorname{lnko}(7732, 149)$ meghatározása "
            "(a maradékokat $\\langle\\cdot\\rangle$ jelöli):\n\n"
            "$$\\begin{aligned}"
            "\\langle 7732 \\rangle &= \\langle 149 \\rangle \\cdot 51 + \\langle 133 \\rangle \\\\"
            "\\langle 149 \\rangle &= \\langle 133 \\rangle \\cdot 1 + \\langle 16 \\rangle \\\\"
            "\\langle 133 \\rangle &= \\langle 16 \\rangle \\cdot 8 + \\langle 5 \\rangle \\\\"
            "\\langle 16 \\rangle &= \\langle 5 \\rangle \\cdot 3 + \\langle 1 \\rangle \\\\"
            "\\langle 5 \\rangle &= \\langle 1 \\rangle \\cdot 5 + \\langle 0 \\rangle"
            "\\end{aligned}$$\n\n"
            "Tehát $\\operatorname{lnko}(7732, 149) = \\mathbf{1}$.\n\n"
            "**b)** $\\operatorname{lnko}(94542, 24981)$ meghatározása:\n\n"
            "$$\\begin{aligned}"
            "\\langle 94542 \\rangle &= \\langle 24981 \\rangle \\cdot 3 + \\langle 19599 \\rangle \\\\"
            "\\langle 24981 \\rangle &= \\langle 19599 \\rangle \\cdot 1 + \\langle 5382 \\rangle \\\\"
            "\\langle 19599 \\rangle &= \\langle 5382 \\rangle \\cdot 3 + \\langle 3453 \\rangle \\\\"
            "\\langle 5382 \\rangle &= \\langle 3453 \\rangle \\cdot 1 + \\langle 1929 \\rangle \\\\"
            "\\langle 3453 \\rangle &= \\langle 1929 \\rangle \\cdot 1 + \\langle 1524 \\rangle \\\\"
            "\\langle 1929 \\rangle &= \\langle 1524 \\rangle \\cdot 1 + \\langle 405 \\rangle \\\\"
            "\\langle 1524 \\rangle &= \\langle 405 \\rangle \\cdot 3 + \\langle 309 \\rangle \\\\"
            "\\langle 405 \\rangle &= \\langle 309 \\rangle \\cdot 1 + \\langle 96 \\rangle \\\\"
            "\\langle 309 \\rangle &= \\langle 96 \\rangle \\cdot 3 + \\langle 21 \\rangle \\\\"
            "\\langle 96 \\rangle &= \\langle 21 \\rangle \\cdot 4 + \\langle 12 \\rangle \\\\"
            "\\langle 21 \\rangle &= \\langle 12 \\rangle \\cdot 1 + \\langle 9 \\rangle \\\\"
            "\\langle 12 \\rangle &= \\langle 9 \\rangle \\cdot 1 + \\langle 3 \\rangle \\\\"
            "\\langle 9 \\rangle &= \\langle 3 \\rangle \\cdot 3 + \\langle 0 \\rangle"
            "\\end{aligned}$$\n\n"
            "Tehát $\\operatorname{lnko}(94542, 24981) = \\mathbf{3}$."
        ),
    },

    # ─── Chapter 5 — Lineáris Diophantikus ──────────────────────────
    "4.3.4.1": {
        "problem": (
            "Adja meg az alábbi (lineáris Diophantikus) egyenletek egész gyökeit:\n\n"
            "**a)** $3141 x + 6120 y = 4$\n\n"
            "**b)** $5682 x + 4836 y = 30$\n\n"
            "**c)** $10518 x + 5682 y = 6$\n\n"
            "**d)** $4512 x + 1111 y = 3248$\n\n"
            "**e)** $1683 x + 114 y = 3$"
        ),
        "solution": (
            "**a)** $6120 x + 3141 y = 4$ — Euklideszi algoritmus:\n\n"
            "$$\\begin{aligned}"
            "\\langle 6120 \\rangle &= \\langle 3141 \\rangle \\cdot 1 + \\langle 2979 \\rangle \\\\"
            "\\langle 3141 \\rangle &= \\langle 2979 \\rangle \\cdot 1 + \\langle 162 \\rangle \\\\"
            "\\langle 2979 \\rangle &= \\langle 162 \\rangle \\cdot 18 + \\langle 63 \\rangle \\\\"
            "\\langle 162 \\rangle &= \\langle 63 \\rangle \\cdot 2 + \\langle 36 \\rangle \\\\"
            "\\langle 63 \\rangle &= \\langle 36 \\rangle \\cdot 1 + \\langle 27 \\rangle \\\\"
            "\\langle 36 \\rangle &= \\langle 27 \\rangle \\cdot 1 + \\langle 9 \\rangle \\\\"
            "\\langle 27 \\rangle &= \\langle 9 \\rangle \\cdot 3 + \\langle 0 \\rangle"
            "\\end{aligned}$$\n\n"
            "Mivel $\\operatorname{lnko}(6120, 3141) = 9$ és $9 \\nmid 4$, az egyenletnek "
            "**nincs egész megoldása**."
        ),
    },

    # ─── Chapter 7 — Kínai Maradéktétel ─────────────────────────────
    "4.3.5.1": {
        "problem": (
            "Oldja meg az alábbi kongruenciarendszereket:\n\n"
            "**a)** $\\begin{cases} x \\equiv 2 \\pmod 7 \\\\ x \\equiv 3 \\pmod 9 \\\\ x \\equiv 0 \\pmod{11} \\end{cases}$\n\n"
            "**b)** $\\begin{cases} x \\equiv 5 \\pmod 7 \\\\ x \\equiv 2 \\pmod{12} \\\\ x \\equiv 3 \\pmod{25} \\\\ x \\equiv 0 \\pmod{11} \\end{cases}$"
        ),
        "solution": (
            "**a)** $7, 9, 11$ páronként relatív prímek, így "
            "$M = \\operatorname{lkkt}(7, 9, 11) = 7 \\cdot 9 \\cdot 11 = 693$. "
            "Megoldjuk a $y_i \\cdot (M/m_i) \\equiv 1$ kongruenciákat:\n\n"
            "$$\\begin{aligned}"
            "y_1 \\cdot 99 &\\equiv 1 \\pmod 7 \\;\\Rightarrow\\; y_1 \\equiv 1 \\\\"
            "y_2 \\cdot 77 &\\equiv 1 \\pmod 9 \\;\\Rightarrow\\; y_2 \\equiv 5 \\\\"
            "y_3 \\cdot 63 &\\equiv 1 \\pmod{11} \\;\\Rightarrow\\; y_3 \\equiv 8"
            "\\end{aligned}$$\n\n"
            "A CRT-képlet szerint:\n\n"
            "$$x \\equiv 2 \\cdot 1 \\cdot 99 + 3 \\cdot 5 \\cdot 77 + 0 \\cdot 8 \\cdot 63 "
            "\\equiv 1353 \\equiv \\mathbf{660} \\pmod{693}.$$\n\n"
            "**b)** $7, 12, 25, 11$ páronként relatív prímek "
            "($M = 7 \\cdot 12 \\cdot 25 \\cdot 11 = 23\\,100$). A megfelelő $y_i$-k:\n\n"
            "$$y_1 = -2 \\equiv 5,\\quad y_2 = 5,\\quad y_3 = -1 \\equiv 24,\\quad y_4 = -1 \\equiv 10.$$\n\n"
            "$$x \\equiv 5 \\cdot 5 \\cdot 3300 + 2 \\cdot 5 \\cdot 1925 + 3 \\cdot 24 \\cdot 924 + 0 "
            "\\equiv 168\\,278 \\equiv \\mathbf{6578} \\pmod{23\\,100}.$$"
        ),
    },

    # ─── Chapter 10 — RSA factorization challenges ──────────────────
    "4.2.4.0": {
        "problem": (
            "Faktorizálja az alábbi számokat:\n\n"
            "**a)** $n = 440\\,747$\n\n"
            "**b)** $n = 2\\,347\\,589$\n\n"
            "**c)** $n = 97\\,189\\,241$\n\n"
            "**d)** $n = 17\\,967\\,876\\,255\\,379$\n\n"
            "**e)** $n = 444\\,113\\,096\\,135\\,661\\,846\\,937$"
        ),
        "solution": (
            "**a)** $440\\,747 = 613 \\cdot 719$\n\n"
            "**b)** $2\\,347\\,589 = 1483 \\cdot 1583$\n\n"
            "**c)** $97\\,189\\,241 = 7151 \\cdot 13\\,591$\n\n"
            "**d)** $17\\,967\\,876\\,255\\,379 = 81\\,371 \\cdot 220\\,814\\,249$\n\n"
            "**e)** $444\\,113\\,096\\,135\\,661\\,846\\,937 = 3\\,719\\,977\\,867 \\cdot 119\\,385\\,951\\,211$\n\n"
            "**f)** $2^{67} - 1 = 193\\,707\\,721 \\cdot 761\\,838\\,257\\,287$ "
            "(F. N. Cole előadása, AMS 1903 — szótlanul felírta a táblára)\n\n"
            "_A 129-jegyű $n_g$ feltörése: lásd a 10. fejezet RSA-129 történetét._"
        ),
    },

    # ─── Chapter 6 — Euler / Fermat / nagy hatványozás ──────────────
    "4.2.3.1": {
        "problem": (
            "**a)** Számítsa ki $\\varphi(p)$ és $\\varphi(p \\cdot q)$ értékét tetszőleges "
            "$p, q \\in \\mathbb{P}$ prímszámokra.\n\n"
            "**b)** Határozza meg tetszőleges $n \\in \\mathbb{N}$ természetes szám "
            "Euler-féle $\\varphi$-függvényének értékét.\n\n"
            "**c)** Határozza meg $\\varphi(1500)$, $\\varphi(2520)$ és $\\varphi(13\\,860)$ értékeit.\n\n"
            "**d)** Mutassa meg, hogy $\\varphi$ (gyengén) multiplikatív számelméleti függvény."
        ),
        "solution": (
            "**a)** $\\varphi(p) = p - 1$, &nbsp; $\\varphi(pq) = (p-1)(q-1)$.\n\n"
            "**b)** Ha $n = p_1^{\\alpha_1} \\cdots p_r^{\\alpha_r}$ a kanonikus alak, akkor\n"
            "$$\\varphi(n) = n \\prod_{i=1}^r \\left(1 - \\frac{1}{p_i}\\right).$$\n\n"
            "**c)** $1500 = 2^2 \\cdot 3 \\cdot 5^3$ &nbsp;⟹&nbsp; "
            "$\\varphi(1500) = 1500 \\cdot \\tfrac{1}{2} \\cdot \\tfrac{2}{3} \\cdot \\tfrac{4}{5} = \\mathbf{400}$.\n\n"
            "$2520 = 2^3 \\cdot 3^2 \\cdot 5 \\cdot 7$ &nbsp;⟹&nbsp; "
            "$\\varphi(2520) = 2520 \\cdot \\tfrac{1}{2} \\cdot \\tfrac{2}{3} \\cdot \\tfrac{4}{5} \\cdot \\tfrac{6}{7} = \\mathbf{576}$.\n\n"
            "$13\\,860 = 2^2 \\cdot 3^2 \\cdot 5 \\cdot 7 \\cdot 11$ &nbsp;⟹&nbsp; "
            "$\\varphi(13\\,860) = \\mathbf{3168}$.\n\n"
            "**d)** Lásd a tankönyv 6.50 Állítás bizonyítását: $\\mathbb{Z}_m^*$-beli elemek "
            "számolásával $\\varphi(mn) = \\varphi(m)\\varphi(n)$, ha $\\operatorname{lnko}(m,n) = 1$."
        ),
    },

    "4.2.3.2": {
        "problem": (
            "Számítsa ki az alábbi hatványokat:\n\n"
            "**a)** $6456^{4652} \\pmod{9786}$\n\n"
            "**b)** $4326^{1818} \\pmod{1003}$\n\n"
            "**c)** $2222^{5555} \\pmod{137}$"
        ),
        "solution": (
            "**a)** $k = 4652 = 1001000101100_2$, ismételt négyzetreemelés $\\bmod\\, 9786$:\n\n"
            "$$\\begin{aligned}"
            "u_0 = 6456,\\; & u_1 = 1362,\\; u_2 = 5490,\\; u_3 = 9006,\\; u_4 = 1668,\\\\"
            "u_5 = 3000,\\; & u_6 = 6666,\\; u_7 = 7116,\\; u_8 = 4692,\\; u_9 = 6150,\\\\"
            "u_{10} = 9396,\\; & u_{11} = 5310,\\; u_{12} = 2634"
            "\\end{aligned}$$\n\n"
            "A $k$-ban 1-es bitek pozícióinál szorzunk:\n\n"
            "$$6456^{4652} \\equiv u_2 \\cdot u_3 \\cdot u_5 \\cdot u_9 \\cdot u_{12}"
            "\\equiv 5490 \\cdot 9006 \\cdot 3000 \\cdot 6150 \\cdot 2634 \\equiv \\mathbf{6864} \\pmod{9786}.$$\n\n"
            "**b)** Hasonlóan: $4326^{1818} \\equiv \\mathbf{226} \\pmod{1003}$.\n\n"
            "**c)** $\\varphi(137) = 136$ (mert 137 prím), és $5555 = 40 \\cdot 136 + 115$, tehát "
            "$2222^{5555} \\equiv 2222^{115} \\equiv \\mathbf{99} \\pmod{137}$ "
            "(Euler-tétel + nagy hatványozás)."
        ),
    },
}


MATH_DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
MATH_INLINE_RE = re.compile(r"\$([^$\n]+?)\$")


def _protect_math(text: str) -> tuple[str, list[str]]:
    """Replace $...$ and $$...$$ with placeholder tokens markdown won't touch."""
    saved: list[str] = []

    def stash_display(m: re.Match) -> str:
        saved.append(f"$${m.group(1)}$$")
        return f"@@MATHBLOCK{len(saved)-1}@@"

    def stash_inline(m: re.Match) -> str:
        saved.append(f"${m.group(1)}$")
        return f"@@MATHBLOCK{len(saved)-1}@@"

    text = MATH_DISPLAY_RE.sub(stash_display, text)
    text = MATH_INLINE_RE.sub(stash_inline, text)
    return text, saved


def _restore_math(html: str, saved: list[str]) -> str:
    for i, s in enumerate(saved):
        html = html.replace(f"@@MATHBLOCK{i}@@", s)
    return html


def render_markdown(text: str) -> str:
    """Render text → HTML. $...$ regions are protected so markdown doesn't eat
    LaTeX backslashes (\\\\, \\begin, etc.)."""
    if not text:
        return ""
    protected, saved = _protect_math(text)
    if HAS_MD:
        html = md_lib.markdown(
            protected,
            extensions=["extra", "sane_lists", "fenced_code", "tables"],
            output_format="html5",
        )
    else:
        escaped = html_lib.escape(protected, quote=False)
        paragraphs = [p.strip() for p in escaped.split("\n\n") if p.strip()]
        html = "\n".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs)
    return _restore_math(html, saved)


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    fe = data["feladatok"]

    auto_count = 0
    manual_count = 0
    for ex_id, ex in fe.items():
        if ex_id in OVERRIDES:
            ov = OVERRIDES[ex_id]
            if "problem" in ov:
                ex["problem"] = ov["problem"]
            if "solution" in ov:
                ex["solution"] = ov["solution"]
            ex["manual"] = True
            ex["format"] = "markdown"
            manual_count += 1
        elif ex.get("manual"):
            pass
        else:
            ex["problem"] = latexify(ex.get("problem") or "")
            if ex.get("solution"):
                ex["solution"] = latexify(ex["solution"])
            ex["format"] = "auto"
            auto_count += 1
        # Pre-render HTML versions for the template
        ex["problem_html"] = render_markdown(ex.get("problem") or "")
        ex["solution_html"] = render_markdown(ex["solution"]) if ex.get("solution") else None

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Auto-converted: {auto_count}")
    print(f"Hand-polished overrides applied: {manual_count}")
    print(f"Total: {len(fe)}")
    print(f"Markdown lib available: {HAS_MD}")
    print(f"Wrote {PATH} ({PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
