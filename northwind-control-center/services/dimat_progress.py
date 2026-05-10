"""
dimat_progress.py — Progress, XP, leaderboard, and 'me' aggregation.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta

import meta_db
from services import dimat_data


XP_SOLVED = 10
XP_REVEALED = 5
XP_QUIZ_PASS_BASE = 25     # ≥80%
XP_QUIZ_HALF_BASE = 10     # ≥50%
XP_GAME_BASE = 30
XP_DAILY_DAMP = 1.0        # placeholder for future per-day cap

DIFFICULTY_MULT = {'easy': 0.7, 'normal': 1.0, 'hard': 1.5}


def record_progress(user_id: int, ch: str, exercise_id: str, status: str) -> dict:
    """Insert/update a progress row. Returns the awarded XP delta + new totals."""
    if status not in ('attempted', 'revealed', 'solved'):
        return {'ok': False, 'error': 'bad status'}
    if not user_id:
        return {'ok': True, 'xp_delta': 0, 'anonymous': True}
    conn = meta_db.dimat_conn()
    lock = meta_db.dimat_lock()

    existing = conn.execute(
        "SELECT status, xp_awarded FROM dimat_progress "
        "WHERE user_id=? AND ch=? AND exercise_id=?",
        (user_id, ch, exercise_id),
    ).fetchone()

    target_xp = 0
    if status == 'solved':
        target_xp = XP_SOLVED
    elif status == 'revealed':
        target_xp = XP_REVEALED

    prior_xp = existing['xp_awarded'] if existing else 0
    # Promote upward only: solved beats revealed beats attempted; never demote
    rank = {'attempted': 1, 'revealed': 2, 'solved': 3}
    if existing and rank.get(existing['status'], 0) >= rank.get(status, 0):
        return {'ok': True, 'xp_delta': 0, 'unchanged': True}

    xp_delta = max(0, target_xp - prior_xp)

    with lock:
        conn.execute(
            """
            INSERT INTO dimat_progress (user_id, ch, exercise_id, status, xp_awarded, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, ch, exercise_id) DO UPDATE SET
                status      = excluded.status,
                xp_awarded  = excluded.xp_awarded,
                updated_at  = CURRENT_TIMESTAMP
            """,
            (user_id, ch, exercise_id, status, max(prior_xp, target_xp)),
        )
        conn.commit()

    # Increment community goal on solves only
    if status == 'solved':
        try:
            from services import dimat_community
            dimat_community.increment(1)
        except Exception:
            pass
    return {'ok': True, 'xp_delta': xp_delta, 'status': status}


def record_quiz(user_id: int, ch: str, score: int, total: int,
                duration_sec: int, difficulty: str = 'normal',
                wrong_qids: list[str] | None = None) -> dict:
    if not user_id:
        return {'ok': True, 'xp_delta': 0, 'anonymous': True}
    if total <= 0:
        return {'ok': False, 'error': 'empty quiz'}
    mult = DIFFICULTY_MULT.get(difficulty, 1.0)
    pct = score / total
    if pct >= 0.8:
        base = XP_QUIZ_PASS_BASE
    elif pct >= 0.5:
        base = XP_QUIZ_HALF_BASE
    else:
        base = 0
    xp = int(round(base * mult))
    conn = meta_db.dimat_conn()
    with meta_db.dimat_lock():
        conn.execute(
            "INSERT INTO dimat_quiz_results "
            "(user_id, ch, score, total, duration_sec, difficulty, xp_awarded, wrong_qids) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, ch, score, total, duration_sec, difficulty, xp,
             json.dumps(wrong_qids or [])),
        )
        conn.commit()
    # Wrong answers feed SRS
    try:
        from services import dimat_srs
        for qid in (wrong_qids or []):
            dimat_srs.schedule_initial(user_id, ch, qid)
    except Exception:
        pass
    return {'ok': True, 'xp_delta': xp, 'pct': pct}


def record_game(user_id: int, ch: str, score: int, max_score: int = 100) -> dict:
    if not user_id:
        return {'ok': True, 'xp_delta': 0}
    if max_score <= 0:
        return {'ok': False}
    pct = max(0, min(1.0, score / max_score))
    xp = int(round(XP_GAME_BASE * pct))
    # Reuse quiz_results table with ch suffix to keep things simple? No —
    # game results live as quiz_results rows tagged difficulty='game'
    conn = meta_db.dimat_conn()
    with meta_db.dimat_lock():
        conn.execute(
            "INSERT INTO dimat_quiz_results "
            "(user_id, ch, score, total, duration_sec, difficulty, xp_awarded) "
            "VALUES (?, ?, ?, ?, 0, 'game', ?)",
            (user_id, ch, score, max_score, xp),
        )
        conn.commit()
    return {'ok': True, 'xp_delta': xp}


def total_xp(user_id: int) -> int:
    if not user_id:
        return 0
    conn = meta_db.dimat_conn()
    p = conn.execute(
        "SELECT COALESCE(SUM(xp_awarded), 0) FROM dimat_progress WHERE user_id=?",
        (user_id,),
    ).fetchone()[0]
    q = conn.execute(
        "SELECT COALESCE(SUM(xp_awarded), 0) FROM dimat_quiz_results WHERE user_id=?",
        (user_id,),
    ).fetchone()[0]
    return int(p + q)


def streak_days(user_id: int) -> int:
    if not user_id:
        return 0
    conn = meta_db.dimat_conn()
    rows = conn.execute(
        "SELECT DISTINCT date(updated_at) AS d FROM dimat_progress WHERE user_id=? "
        "ORDER BY d DESC LIMIT 60",
        (user_id,),
    ).fetchall()
    if not rows:
        return 0
    today = datetime.utcnow().date()
    streak = 0
    expected = today
    for row in rows:
        try:
            d = datetime.strptime(row[0], '%Y-%m-%d').date()
        except (TypeError, ValueError):
            break
        if d == expected:
            streak += 1
            expected = expected - timedelta(days=1)
        elif d == today and streak == 0:
            # tolerate today being missing while everything else is consecutive
            expected = expected - timedelta(days=1)
        else:
            break
    return streak


def me(user_id: int) -> dict:
    if not user_id:
        return {
            'authenticated': False, 'xp': 0, 'streak': 0,
            'solved': 0, 'revealed': 0, 'chapters_touched': 0,
            'achievements': [],
        }
    conn = meta_db.dimat_conn()
    solved = conn.execute(
        "SELECT COUNT(*) FROM dimat_progress WHERE user_id=? AND status='solved'",
        (user_id,),
    ).fetchone()[0]
    revealed = conn.execute(
        "SELECT COUNT(*) FROM dimat_progress WHERE user_id=? AND status='revealed'",
        (user_id,),
    ).fetchone()[0]
    chs_touched = conn.execute(
        "SELECT COUNT(DISTINCT ch) FROM dimat_progress WHERE user_id=?",
        (user_id,),
    ).fetchone()[0]
    per_ch = {}
    for row in conn.execute(
        "SELECT ch, status, COUNT(*) FROM dimat_progress WHERE user_id=? "
        "GROUP BY ch, status",
        (user_id,),
    ).fetchall():
        per_ch.setdefault(row[0], {})[row[1]] = row[2]
    from services import dimat_achievements
    return {
        'authenticated': True,
        'xp': total_xp(user_id),
        'streak': streak_days(user_id),
        'solved': solved,
        'revealed': revealed,
        'chapters_touched': chs_touched,
        'per_chapter': per_ch,
        'achievements': dimat_achievements.list_earned(user_id),
        'total_exercises': dimat_data.total_exercise_count(),
    }


def leaderboard(ch: str | None = None, period: str = 'all', limit: int = 20) -> list[dict]:
    """Top users by total XP. period in {'week','month','all'}."""
    conn = meta_db.dimat_conn()
    # Build per-table WHERE clauses (the time column differs between tables)
    p_clauses: list[str] = ['p.user_id = u.id']
    q_clauses: list[str] = ['q.user_id = u.id']
    p_params: list = []
    q_params: list = []
    if period == 'week':
        p_clauses.append("p.updated_at >= datetime('now','-7 days')")
        q_clauses.append("q.taken_at >= datetime('now','-7 days')")
    elif period == 'month':
        p_clauses.append("p.updated_at >= datetime('now','-30 days')")
        q_clauses.append("q.taken_at >= datetime('now','-30 days')")
    if ch:
        p_clauses.append('p.ch = ?')
        q_clauses.append('q.ch = ?')
        p_params.append(ch)
        q_params.append(ch)
    p_where = ' AND '.join(p_clauses)
    q_where = ' AND '.join(q_clauses)
    sql = f"""
        SELECT u.id, u.username, u.role,
               (SELECT COALESCE(SUM(xp_awarded), 0) FROM dimat_progress p WHERE {p_where})
             + (SELECT COALESCE(SUM(xp_awarded), 0) FROM dimat_quiz_results q WHERE {q_where})
               AS xp
        FROM users u
        ORDER BY xp DESC
        LIMIT ?
    """
    rows = conn.execute(sql, (*p_params, *q_params, limit)).fetchall()
    return [{'username': r['username'], 'xp': int(r['xp']), 'role': r['role']}
            for r in rows if r['xp'] > 0]
