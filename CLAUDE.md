## Repo purpose

Course materials (lecture notes + T-SQL exercises) for an advanced database management class taught in Hungarian against **MS SQL Server 2016+** using the **Northwind** sample database. No application code, no build system — the "output" is SQL scripts students run in SSMS and Hungarian PDFs/Markdown translated from the original notes.

Two modules, and they are independent:
- `db1/` — core T-SQL / procedural programming / transactions, taught from `jegyzet_adatb-II.pdf` (and its `.txt` extraction). Exercises are numbered `feladat1.sql` … `feladat26.sql` ("feladat" = "exercise"); suffixed variants (`feladat9_tran.sql`, `feladat19_readcommitted.sql` vs `feladat19_repeatableread.sql`, `feladat20a.sql`, `feladat3a.sql`, etc.) are intentional alternates that illustrate a contrast — don't merge or "deduplicate" them.
- `db2/` — advanced topics (HA/DR, replication, security, MDM, etc.). The authoritative source is `jegyzet_haladó_AB_Vassányi_István_2026.pdf`; everything else in `db2/` is downstream: `.txt` is a text extraction, `.tex` + `jegyzet_halado.pdf` are a regenerated LaTeX+PDF with images positioned from the original, and `jegyzet_halado_AB_Vassanyi_Istvan_2026.hu.claude.md` is the Hungarian markdown translation that is the main thing currently being edited.

## Northwind is modified — don't assume stock schema

The install scripts (`db1/instnwnd.sql`, `db1/instnwnd_self_contained.sql`) load stock Northwind, but the course adds columns that exercises and demos depend on:
- `Employees.Salary`
- `Employees.Emp_categ_id`
- `Customers.territory_id` (FK)
- `Customers.Balance` (money) — referenced by `db1/feladat19_*.sql` and `db2/order_processing_demo.sql`; missing in stock Northwind, so a fresh install needs `ALTER TABLE` before those run.

`db1/install_northwind.sql` uses `:r instnwnd.sql`, so it only works in **SSMS SQLCMD mode** (Query → SQLCMD Mode) or via `sqlcmd -i`. Running it as plain T-SQL fails on the `:r`.

## Exercises contain deliberate errors

Some `feladat*.sql` files include commented-out "broken" lines alongside the corrected version — they are teaching artifacts showing a common mistake and its fix (see `db2/order_processing_demo.sql` for an explicit `-- Original broken line from the notes:` example). Do **not** delete these as dead code. If you change one, keep both the broken and the corrected form and the surrounding comment.

Hungarian `PRINT` messages (`'HIBA: ...'`, `'... sz. rendelés sikeresen felvéve.'`) are course-facing output strings — preserve them when editing.

## Translation work (`db2/`) — terminology is enforced, not advisory

`db2/TERMS.md` is the canonical English↔Hungarian glossary. When touching the Hungarian markdown/tex/txt:
- Use the **Suggested Hungarian Translation** column; avoid the **Incorrect Machine Translation** column. These were chosen because MT systems pick the physical meaning of polysemous terms (`Table` → `Asztal`, `Leaf` → `Levél`, `Log` → `Rönk`, `Coupling` → `Tengelykapcsoló`, `Dump` → `Szemétlerakás`) — watch for this class of error.
- Terms in TERMS.md §10 ("Multiple Accepted Forms") have two or three equally valid Hungarian renderings. **Pick one and keep it stable across the document** — don't flip a term between `Kiadvány`/`Publikáció` or `Feliratkozás`/`Előfizetés` on one reviewer's preference. Consistency over local optimum.
- Address the reader informally (**te**, not **ön**) throughout the translation — this was decided in commit `4d71e52` and re-applied in later review passes.
- Keep industry-standard English terms where Hungarian IT education normally does (`Job`, `Trigger`, `Commit`, `Rollback`, `Collation`, `Dump`).

## What commands exist

There is no Makefile, package manager, or test suite. Only these operations are meaningful:
- Run a `.sql` file: execute in SSMS against the `Northwind` database (`USE northwind; GO` at top of most scripts), or `sqlcmd -S <server> -d Northwind -i <file>.sql`. Scripts using `:r` need SQLCMD mode.
- Rebuild the Hungarian PDF from `db2/jegyzet_halado.tex`: `pdflatex` (xelatex/lualatex preferred — the tex file prefers `DejaVu Sans` under xetex/luatex). The generated PDF is committed; only regenerate when the tex changes.

There is no linter, no tests, no CI.

## Files that already exist and overlap with this one

- `GEMINI.md` (staged, not yet committed) — a similar orientation doc aimed at Gemini. If you update high-level facts here, check whether GEMINI.md needs the same edit so they don't drift.
- `db1/README.md` — Hungarian-language description of the modified Northwind schema and the specific added fields. Read this before writing or reviewing anything that touches Northwind tables.
