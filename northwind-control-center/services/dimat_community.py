"""
dimat_community.py — Monthly community-wide goal counter + badge issuance.

Every solve increments the current month's row. When threshold is reached,
every user who's been active this month receives the period badge
(`community_<YYYY>_<MM>`).
"""

from __future__ import annotations

from datetime import datetime

import meta_db


def _period() -> str:
    return datetime.utcnow().strftime('%Y-%m')


def _ensure_period_row(conn, period: str) -> dict:
    row = conn.execute(
        "SELECT period, problems_solved, goal, reached_at FROM dimat_community_goal "
        "WHERE period=?",
        (period,),
    ).fetchone()
    if row:
        return dict(row)
    with meta_db.dimat_lock():
        conn.execute(
            "INSERT OR IGNORE INTO dimat_community_goal (period, problems_solved, goal) "
            "VALUES (?, 0, 10000)",
            (period,),
        )
        conn.commit()
    row = conn.execute(
        "SELECT period, problems_solved, goal, reached_at FROM dimat_community_goal "
        "WHERE period=?",
        (period,),
    ).fetchone()
    return dict(row)


def increment(amount: int = 1) -> dict:
    """Bump the counter; if threshold crossed for the first time, set reached_at
    and return {'crossed': True} so the caller can issue badges."""
    conn = meta_db.dimat_conn()
    period = _period()
    state = _ensure_period_row(conn, period)
    with meta_db.dimat_lock():
        conn.execute(
            "UPDATE dimat_community_goal SET problems_solved = problems_solved + ? "
            "WHERE period=?",
            (amount, period),
        )
        conn.commit()
    state = _ensure_period_row(conn, period)
    crossed = False
    if state['problems_solved'] >= state['goal'] and not state['reached_at']:
        with meta_db.dimat_lock():
            conn.execute(
                "UPDATE dimat_community_goal SET reached_at=CURRENT_TIMESTAMP "
                "WHERE period=? AND reached_at IS NULL",
                (period,),
            )
            conn.commit()
        crossed = True
        _issue_period_badge_to_active(period)
    return {'period': period, **state, 'crossed': crossed}


def status() -> dict:
    conn = meta_db.dimat_conn()
    return _ensure_period_row(conn, _period())


def _issue_period_badge_to_active(period: str) -> None:
    """Grant `community_YYYY_MM` to every user who has any progress this period."""
    conn = meta_db.dimat_conn()
    ach_key = 'community_' + period.replace('-', '_')
    active = conn.execute(
        "SELECT DISTINCT user_id FROM dimat_progress "
        "WHERE strftime('%Y-%m', updated_at)=?",
        (period,),
    ).fetchall()
    with meta_db.dimat_lock():
        for r in active:
            conn.execute(
                "INSERT OR IGNORE INTO dimat_achievements (user_id, ach_key) VALUES (?, ?)",
                (r[0], ach_key),
            )
        conn.commit()
