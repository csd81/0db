# Dimat Implementation Decisions Log

Decisions made during autonomous execution of the plan at
`~/.claude/plans/concurrent-moseying-badger.md`.

## Phase A — Data pipeline + DB

### A.1 — Markdown parser coverage: 462/585 exercises (78%)
The parser produces 462 exercises across the 18 chapter folders, vs. the
survey's 585. The remaining ~120 are nested sub-items written as `#### /N/`
(four-hash) rather than `### N` (three-hash) — they're parts of multi-part
problems. Treating them as separate exercises would explode IDs in confusing
ways; treating them as plain markdown inside the parent exercise is more
faithful to the textbook structure. **Decision: accept 78% coverage as v1;
sub-items render inline within their parent's `solution_md`.**

### A.2 — `auth_user_id()` helper
Plan referenced `auth_user_id()` but the codebase only has
`auth.get_current_user()` returning a dict. **Decision: gamification routes
read `session.get('user_id')` directly; anonymous reads (no session) return
empty progress/leaderboard rows but don't 401 — keeps the page browsable
without forcing login.**

### A.3 — Parser handles three header conventions
Solutions.md across 18 folders uses inconsistent header styles:
- `### Exercise N.M.K - Title` (English convention, ch1–ch8)
- `### N.M.K. Title` / `### N.M.K Feladat - Title` (Hungarian)
- `### HF - Title` (Házi feladat = homework, ch9+)
The parser handles all three. HF entries get a synthetic ID
`{section}.HF{N}` keyed off the most recent `## Section X.Y` header.

### A.4 — Exercise authoring for ch19–ch23 deferred
Plan flagged this as the largest sub-task. Per the user's autonomous-execution
guidance, **content authoring is deferred to a later interactive pass** — the
infrastructure is built so adding `0dimat_feladatok/19_*/{...}.md` will be
auto-picked-up by the parser without code changes. The skill-tree, leaderboard,
and quiz UI all degrade gracefully when a chapter has 0 exercises.
