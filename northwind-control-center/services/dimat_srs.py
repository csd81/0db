"""
dimat_srs.py — SM-2 spaced-repetition scheduler over the dimat_srs table.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta

import meta_db


def _now() -> datetime:
    return datetime.utcnow()


def schedule_initial(user_id: int, ch: str, question_id: str) -> None:
    """Add a freshly-missed question to the SRS queue with due_at = now + 1d."""
    if not user_id:
        return
    conn = meta_db.dimat_conn()
    lock = meta_db.dimat_lock()
    due = _now() + timedelta(days=1)
    with lock:
        conn.execute(
            """
            INSERT INTO dimat_srs (user_id, ch, question_id, ease, interval_days,
                                   due_at, mistake_count, last_seen_at)
            VALUES (?, ?, ?, 2.5, 1, ?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, ch, question_id) DO UPDATE SET
                mistake_count = mistake_count + 1,
                last_seen_at  = CURRENT_TIMESTAMP
            """,
            (user_id, ch, question_id, due.isoformat()),
        )
        conn.commit()


def grade(user_id: int, ch: str, question_id: str, q: int) -> dict:
    """Apply SM-2 update with quality grade q (0–5)."""
    if not user_id:
        return {'ok': False, 'reason': 'anonymous'}
    q = max(0, min(5, int(q)))
    conn = meta_db.dimat_conn()
    lock = meta_db.dimat_lock()
    row = conn.execute(
        "SELECT ease, interval_days FROM dimat_srs "
        "WHERE user_id=? AND ch=? AND question_id=?",
        (user_id, ch, question_id),
    ).fetchone()
    ease = row['ease'] if row else 2.5
    interval = row['interval_days'] if row else 1

    if q < 3:
        # Failed → reset interval to 1, lower ease floor 1.3
        interval = 1
        ease = max(1.3, ease - 0.2)
    else:
        # SM-2 ease adjustment
        ease = max(1.3, ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
        if interval <= 1:
            interval = 6 if q >= 4 else 3
        else:
            interval = int(round(interval * ease))
    due = _now() + timedelta(days=interval)
    with lock:
        conn.execute(
            """
            INSERT INTO dimat_srs (user_id, ch, question_id, ease, interval_days,
                                   due_at, mistake_count, last_seen_at)
            VALUES (?, ?, ?, ?, ?, ?, 0, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, ch, question_id) DO UPDATE SET
                ease          = excluded.ease,
                interval_days = excluded.interval_days,
                due_at        = excluded.due_at,
                last_seen_at  = CURRENT_TIMESTAMP
            """,
            (user_id, ch, question_id, ease, interval, due.isoformat()),
        )
        conn.commit()
    return {'ok': True, 'next_due': due.isoformat(), 'ease': ease, 'interval_days': interval}


def list_due(user_id: int, limit: int = 20) -> list[dict]:
    if not user_id:
        return []
    conn = meta_db.dimat_conn()
    rows = conn.execute(
        "SELECT ch, question_id, ease, interval_days, due_at, mistake_count "
        "FROM dimat_srs WHERE user_id=? AND (due_at IS NULL OR due_at <= ?) "
        "ORDER BY due_at LIMIT ?",
        (user_id, _now().isoformat(), limit),
    ).fetchall()
    return [dict(r) for r in rows]
