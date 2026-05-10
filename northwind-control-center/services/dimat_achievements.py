"""
dimat_achievements.py — Achievement registry + checker.

Achievements are evaluated lazily after every progress event. Each ACH spec is
a callable predicate that takes (user_id, conn) and returns True if earned.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import meta_db
from services import dimat_data


# ── Helpers (read meta_db rows for the user) ───────────────────────────────────

def _solved_count(conn, user_id: int) -> int:
    row = conn.execute(
        "SELECT COUNT(*) FROM dimat_progress WHERE user_id=? AND status='solved'",
        (user_id,),
    ).fetchone()
    return row[0] if row else 0


def _solved_count_no_reveal(conn, user_id: int) -> int:
    """Solved without ever having clicked Reveal on the same exercise."""
    row = conn.execute(
        "SELECT COUNT(*) FROM dimat_progress p "
        "WHERE p.user_id=? AND p.status='solved' "
        "AND NOT EXISTS (SELECT 1 FROM dimat_progress p2 "
        "                WHERE p2.user_id=p.user_id AND p2.ch=p.ch "
        "                AND p2.exercise_id=p.exercise_id AND p2.status='revealed')",
        (user_id,),
    ).fetchone()
    return row[0] if row else 0


def _solved_in_chapters(conn, user_id: int, chs: list[str]) -> bool:
    """True iff every chapter in `chs` has at least 1 solved exercise."""
    placeholders = ','.join(['?'] * len(chs))
    rows = conn.execute(
        f"SELECT DISTINCT ch FROM dimat_progress "
        f"WHERE user_id=? AND status='solved' AND ch IN ({placeholders})",
        (user_id, *chs),
    ).fetchall()
    return len({r[0] for r in rows}) == len(chs)


def _streak_days(conn, user_id: int) -> int:
    rows = conn.execute(
        "SELECT DISTINCT date(updated_at) AS d FROM dimat_progress WHERE user_id=? "
        "ORDER BY d DESC LIMIT 60",
        (user_id,),
    ).fetchall()
    if not rows:
        return 0
    today = datetime.utcnow().date()
    streak = 0
    for i, row in enumerate(rows):
        # row['d'] is YYYY-MM-DD
        try:
            d = datetime.strptime(row[0], '%Y-%m-%d').date()
        except (TypeError, ValueError):
            break
        if (today - d).days == streak:
            streak += 1
        else:
            break
    return streak


def _quiz_perfect_count(conn, user_id: int) -> int:
    return conn.execute(
        "SELECT COUNT(*) FROM dimat_quiz_results WHERE user_id=? AND score=total",
        (user_id,),
    ).fetchone()[0]


def _hard_quizzes_passed(conn, user_id: int) -> int:
    return conn.execute(
        "SELECT COUNT(*) FROM dimat_quiz_results "
        "WHERE user_id=? AND difficulty='hard' AND score*5 >= total*4",  # ≥80%
        (user_id,),
    ).fetchone()[0]


def _community_badges_count(conn, user_id: int) -> int:
    return conn.execute(
        "SELECT COUNT(*) FROM dimat_achievements "
        "WHERE user_id=? AND ach_key LIKE 'community_%'",
        (user_id,),
    ).fetchone()[0]


# ── Catalogue (32 achievements) ────────────────────────────────────────────────
# Each entry: (key, icon, title, description, predicate)

CATALOGUE = [
    ('first_blood',  '🎯', 'First Blood',         'Megoldottad az első feladatot',
     lambda uid, c: _solved_count(c, uid) >= 1),
    ('ten_solved',   '🔟', 'Tizes',               '10 feladat megoldva',
     lambda uid, c: _solved_count(c, uid) >= 10),
    ('fifty_solved', '5️⃣0️⃣', 'Half-Century',     '50 feladat megoldva',
     lambda uid, c: _solved_count(c, uid) >= 50),
    ('hundred',      '💯', 'Hundred Club',        '100 feladat megoldva',
     lambda uid, c: _solved_count(c, uid) >= 100),
    ('three_streak', '⚡', 'Three-Day Spark',     '3 napos streak',
     lambda uid, c: _streak_days(c, uid) >= 3),
    ('week_warrior', '🔥', 'Week Warrior',        '7 napos streak',
     lambda uid, c: _streak_days(c, uid) >= 7),
    ('marathon',     '♾️', 'Marathon',           '30 napos streak',
     lambda uid, c: _streak_days(c, uid) >= 30),
    ('combi_sage',   '🧮', 'Kombinatorika Sage', 'Megoldva: ch1–ch8',
     lambda uid, c: _solved_in_chapters(c, uid, [f'ch{i}' for i in range(1, 9)])),
    ('graph_master', '🕸️', 'Graph Theory Master','Megoldva: ch9–ch18',
     lambda uid, c: _solved_in_chapters(c, uid, [f'ch{i}' for i in range(9, 19)])),
    ('spectrum_pro', '🌈', 'Spectrum Pro',        'Megoldva: ch20–ch23',
     lambda uid, c: _solved_in_chapters(c, uid, ['ch20','ch21','ch22','ch23'])),
    ('perfect_one',  '💎', 'Perfectionist',       '100% egy fejezet kvízen',
     lambda uid, c: _quiz_perfect_count(c, uid) >= 1),
    ('perfect_five', '💠', 'Pentaperfect',        '100% öt különböző kvízen',
     lambda uid, c: _quiz_perfect_count(c, uid) >= 5),
    ('speedrun',     '⏱️', 'Speedrun',           'Kvíz <3 perc, ≥80%',
     lambda uid, c: c.execute(
         "SELECT 1 FROM dimat_quiz_results WHERE user_id=? AND duration_sec<180 "
         "AND score*5 >= total*4 LIMIT 1", (uid,)).fetchone() is not None),
    ('hard_mode',    '😈', 'Hard Mode Hero',      '5 Hard kvíz ≥80%-kal',
     lambda uid, c: _hard_quizzes_passed(c, uid) >= 5),
    ('triple_crown', '🔱', 'Triple-Crown',        'Egy nap: feladat + kvíz + mini-játék',
     lambda uid, c: c.execute(
         "SELECT 1 FROM dimat_progress p WHERE p.user_id=? AND p.status='solved' "
         "AND date(p.updated_at)=date('now') "
         "AND EXISTS(SELECT 1 FROM dimat_quiz_results q WHERE q.user_id=p.user_id "
         "           AND date(q.taken_at)=date('now')) LIMIT 1",
         (uid,)).fetchone() is not None),
    ('diamond',      '🏆', 'Diamond Hands',       '100 feladat saját erőből (no reveal)',
     lambda uid, c: _solved_count_no_reveal(c, uid) >= 100),
    ('srs_devotee',  '🧠', 'SRS Devotee',         '14 nap egymás után Napi Ismétlés',
     lambda uid, c: c.execute(
         "SELECT COUNT(DISTINCT date(last_seen_at)) FROM dimat_srs WHERE user_id=? "
         "AND last_seen_at >= datetime('now','-14 days')", (uid,)).fetchone()[0] >= 14),
    ('community_3',  '🌟', 'Community Champion',  '3 hónap közösségi cél elérve',
     lambda uid, c: _community_badges_count(c, uid) >= 3),
    ('owl',          '🦉', 'Owl',                 '≥80% egy kvízen 22:00–04:00 között',
     lambda uid, c: c.execute(
         "SELECT 1 FROM dimat_quiz_results WHERE user_id=? "
         "AND score*5 >= total*4 "
         "AND (CAST(strftime('%H', taken_at) AS INTEGER) >= 22 "
         "  OR CAST(strftime('%H', taken_at) AS INTEGER) < 4) LIMIT 1",
         (uid,)).fetchone() is not None),
    ('explorer',     '🗺️', 'Explorer',           'Próbáltál ≥1 feladatot 10 fejezetből',
     lambda uid, c: c.execute(
         "SELECT COUNT(DISTINCT ch) FROM dimat_progress WHERE user_id=?",
         (uid,)).fetchone()[0] >= 10),
    ('completionist','✅', 'Completionist',       'Egy fejezet összes feladata megoldva',
     lambda uid, c: _has_completed_chapter(c, uid)),
    ('quiz_taker',   '🎯', 'Quiz Taker',          '10 kvízt teljesítettél',
     lambda uid, c: c.execute(
         "SELECT COUNT(*) FROM dimat_quiz_results WHERE user_id=?",
         (uid,)).fetchone()[0] >= 10),
    ('night_owl',    '🌙', 'Night Owl',           '5 feladat 00:00–05:00 között',
     lambda uid, c: c.execute(
         "SELECT COUNT(*) FROM dimat_progress WHERE user_id=? AND status='solved' "
         "AND CAST(strftime('%H', updated_at) AS INTEGER) < 5",
         (uid,)).fetchone()[0] >= 5),
    ('early_bird',   '🐦', 'Early Bird',          '5 feladat 05:00–08:00 között',
     lambda uid, c: c.execute(
         "SELECT COUNT(*) FROM dimat_progress WHERE user_id=? AND status='solved' "
         "AND CAST(strftime('%H', updated_at) AS INTEGER) BETWEEN 5 AND 7",
         (uid,)).fetchone()[0] >= 5),
    ('curious_cat',  '🐈', 'Curious Cat',         '20 megoldás megnézve',
     lambda uid, c: c.execute(
         "SELECT COUNT(*) FROM dimat_progress WHERE user_id=? AND status='revealed'",
         (uid,)).fetchone()[0] >= 20),
    ('finishing_kick','🏁','Finishing Kick',     '5 fejezet 100%-ban befejezve',
     lambda uid, c: _completed_chapter_count(c, uid) >= 5),
    ('bookworm',     '📚', 'Bookworm',            'Minden kvízbe belenéztél',
     lambda uid, c: c.execute(
         "SELECT COUNT(DISTINCT ch) FROM dimat_quiz_results WHERE user_id=?",
         (uid,)).fetchone()[0] >= 18),
    ('fast_learner', '⚡', 'Fast Learner',       '10 feladat egy nap',
     lambda uid, c: c.execute(
         "SELECT COUNT(*) FROM dimat_progress WHERE user_id=? AND status='solved' "
         "AND date(updated_at)=date('now')",
         (uid,)).fetchone()[0] >= 10),
    ('ironman',      '🏋️', 'Ironman',           '500 feladat összesen',
     lambda uid, c: _solved_count(c, uid) >= 500),
    ('skill_tree',   '🗺️', 'Skill Tree',         '15 fejezet legalább megérintve',
     lambda uid, c: c.execute(
         "SELECT COUNT(DISTINCT ch) FROM dimat_progress WHERE user_id=?",
         (uid,)).fetchone()[0] >= 15),
    ('all_chapters', '🌐', 'Universalist',        'Minden fejezethez ≥1 megoldás',
     lambda uid, c: c.execute(
         "SELECT COUNT(DISTINCT ch) FROM dimat_progress WHERE user_id=? AND status='solved'",
         (uid,)).fetchone()[0] >= 24),  # 25 chapters incl. appendix; 24 forgivingly
    ('legend',       '👑', 'Legend',              'Az összes 31 másik achievement',
     lambda uid, c: c.execute(
         "SELECT COUNT(*) FROM dimat_achievements WHERE user_id=? AND ach_key != 'legend'",
         (uid,)).fetchone()[0] >= 31),
]


def _has_completed_chapter(conn, user_id: int) -> bool:
    return _completed_chapter_count(conn, user_id) >= 1


def _completed_chapter_count(conn, user_id: int) -> int:
    """How many chapters has the user solved every available exercise in?"""
    rows = conn.execute(
        "SELECT ch, COUNT(*) AS solved FROM dimat_progress "
        "WHERE user_id=? AND status='solved' GROUP BY ch",
        (user_id,),
    ).fetchall()
    n = 0
    for r in rows:
        ch_data = dimat_data.get_chapter(r['ch'])
        total = len(ch_data.get('exercises', []))
        if total > 0 and r['solved'] >= total:
            n += 1
    return n


# ── Public API ─────────────────────────────────────────────────────────────────

CAT_INDEX = {a[0]: a for a in CATALOGUE}


def list_all() -> list[dict]:
    return [
        {'key': k, 'icon': i, 'title': t, 'description': d}
        for (k, i, t, d, _) in CATALOGUE
    ]


def list_earned(user_id: int) -> list[dict]:
    if not user_id:
        return []
    conn = meta_db.dimat_conn()
    rows = conn.execute(
        "SELECT ach_key, earned_at FROM dimat_achievements WHERE user_id=?",
        (user_id,),
    ).fetchall()
    earned = []
    for r in rows:
        spec = CAT_INDEX.get(r['ach_key'])
        if spec:
            earned.append({
                'key': spec[0], 'icon': spec[1], 'title': spec[2],
                'description': spec[3], 'earned_at': r['earned_at'],
            })
    return earned


def check(user_id: int) -> list[dict]:
    """Run every predicate; return list of *newly-earned* achievements."""
    if not user_id:
        return []
    conn = meta_db.dimat_conn()
    lock = meta_db.dimat_lock()
    earned_keys = {
        r[0] for r in conn.execute(
            "SELECT ach_key FROM dimat_achievements WHERE user_id=?",
            (user_id,),
        ).fetchall()
    }
    newly = []
    for key, icon, title, desc, pred in CATALOGUE:
        if key in earned_keys:
            continue
        try:
            if pred(user_id, conn):
                with lock:
                    conn.execute(
                        "INSERT OR IGNORE INTO dimat_achievements (user_id, ach_key) "
                        "VALUES (?, ?)",
                        (user_id, key),
                    )
                    conn.commit()
                newly.append({'key': key, 'icon': icon, 'title': title, 'description': desc})
        except Exception:
            # A predicate may legitimately fail mid-bootstrap (e.g. table rows missing) —
            # don't block the rest of the check.
            continue
    return newly
