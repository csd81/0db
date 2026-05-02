"""
meta_db.py — Central Meta-Database manager.

Stores users, registered DB connections, and replication job configs in a
local SQLite file (instance/meta.db).  The module holds a single persistent
sqlite3.Connection opened with check_same_thread=False so APScheduler
background threads can read freely.  All writes are serialised through
_write_lock to prevent SQLITE_BUSY errors.

IMPORTANT: If FERNET_KEY in .env is lost or rotated, all encrypted passwords
stored in the connections table become unrecoverable.  Re-enter them manually.
"""

import json
import os
import sqlite3
import threading
import warnings
from datetime import datetime
from hashlib import sha256

from cryptography.fernet import Fernet, InvalidToken

_conn: sqlite3.Connection | None = None
_write_lock = threading.Lock()
_fernet: Fernet | None = None


# ── Startup ────────────────────────────────────────────────────────────────────

def init_meta_db(app) -> None:
    global _conn, _fernet

    # Fernet setup
    key = app.config.get('FERNET_KEY', '')
    if not key:
        key = Fernet.generate_key().decode()
        warnings.warn(
            "FERNET_KEY not set in .env — generated a temporary in-memory key. "
            "Stored passwords will be unrecoverable after restart. "
            "Add FERNET_KEY to your .env file.",
            RuntimeWarning,
            stacklevel=2,
        )
    _fernet = Fernet(key.encode() if isinstance(key, str) else key)

    # SQLite file
    db_path = app.config.get('META_DB_PATH', 'instance/meta.db')
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    _conn = sqlite3.connect(db_path, check_same_thread=False)
    _conn.row_factory = sqlite3.Row
    _create_schema()
    _seed_admin()


def _create_schema() -> None:
    with _write_lock:
        _conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                role          TEXT    NOT NULL DEFAULT 'readonly',
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS connections (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                name               TEXT NOT NULL,
                db_type            TEXT NOT NULL,
                conn_params        TEXT NOT NULL,
                encrypted_password TEXT,
                created_at         DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS replication_jobs (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                job_type        TEXT NOT NULL,
                master_conn_id  INTEGER REFERENCES connections(id),
                slave_conn_id   INTEGER REFERENCES connections(id),
                interval_secs   INTEGER DEFAULT 60,
                status          TEXT DEFAULT 'stopped',
                last_replicated_id INTEGER DEFAULT 0,
                last_run        DATETIME,
                last_error      TEXT,
                created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        _conn.commit()


def _seed_admin() -> None:
    row = _conn.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
    if not row:
        with _write_lock:
            _conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ('admin', _hash_pw('admin'), 'admin'),
            )
            _conn.commit()


# ── Password helpers ───────────────────────────────────────────────────────────

def _hash_pw(password: str) -> str:
    return sha256(password.encode()).hexdigest()


def _encrypt(password: str) -> str:
    return _fernet.encrypt(password.encode()).decode()


def _decrypt(token: str) -> str:
    try:
        return _fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        return ''


# ── Users ──────────────────────────────────────────────────────────────────────

def verify_user(username: str, password: str) -> dict | None:
    row = _conn.execute(
        "SELECT id, username, role FROM users WHERE username = ? AND password_hash = ?",
        (username, _hash_pw(password)),
    ).fetchone()
    return dict(row) if row else None


def list_users() -> list[dict]:
    rows = _conn.execute(
        "SELECT id, username, role, created_at FROM users ORDER BY id"
    ).fetchall()
    return [dict(r) for r in rows]


def create_user(username: str, password: str, role: str = 'readonly') -> tuple[bool, str | None]:
    try:
        with _write_lock:
            _conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, _hash_pw(password), role),
            )
            _conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' already exists."


def delete_user(user_id: int) -> None:
    with _write_lock:
        _conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        _conn.commit()


def change_password(user_id: int, new_password: str) -> None:
    with _write_lock:
        _conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (_hash_pw(new_password), user_id),
        )
        _conn.commit()


# ── Connections ────────────────────────────────────────────────────────────────

def list_connections() -> list[dict]:
    rows = _conn.execute(
        "SELECT id, name, db_type, conn_params, created_at FROM connections ORDER BY id"
    ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d['conn_params'] = json.loads(d['conn_params'])
        result.append(d)
    return result


def get_connection_by_id(conn_id: int) -> dict | None:
    row = _conn.execute(
        "SELECT id, name, db_type, conn_params, encrypted_password FROM connections WHERE id = ?",
        (conn_id,),
    ).fetchone()
    if not row:
        return None
    d = dict(row)
    d['conn_params'] = json.loads(d['conn_params'])
    if d['encrypted_password']:
        d['password'] = _decrypt(d['encrypted_password'])
    else:
        d['password'] = ''
    return d


def create_connection(name: str, db_type: str, conn_params: dict, password: str = '') -> int:
    enc_pw = _encrypt(password) if password else None
    with _write_lock:
        cur = _conn.execute(
            "INSERT INTO connections (name, db_type, conn_params, encrypted_password) VALUES (?, ?, ?, ?)",
            (name, db_type, json.dumps(conn_params), enc_pw),
        )
        _conn.commit()
    return cur.lastrowid


def update_connection(conn_id: int, name: str, db_type: str, conn_params: dict, password: str = '') -> None:
    enc_pw = _encrypt(password) if password else None
    with _write_lock:
        if enc_pw:
            _conn.execute(
                "UPDATE connections SET name=?, db_type=?, conn_params=?, encrypted_password=? WHERE id=?",
                (name, db_type, json.dumps(conn_params), enc_pw, conn_id),
            )
        else:
            _conn.execute(
                "UPDATE connections SET name=?, db_type=?, conn_params=? WHERE id=?",
                (name, db_type, json.dumps(conn_params), conn_id),
            )
        _conn.commit()


def delete_connection(conn_id: int) -> None:
    with _write_lock:
        _conn.execute("DELETE FROM connections WHERE id = ?", (conn_id,))
        _conn.commit()


# ── Replication Jobs ───────────────────────────────────────────────────────────

def list_replication_jobs() -> list[dict]:
    rows = _conn.execute("""
        SELECT rj.*, mc.name AS master_name, sc.name AS slave_name
        FROM replication_jobs rj
        LEFT JOIN connections mc ON rj.master_conn_id = mc.id
        LEFT JOIN connections sc ON rj.slave_conn_id  = sc.id
        ORDER BY rj.id
    """).fetchall()
    return [dict(r) for r in rows]


def get_replication_job(job_id: int) -> dict | None:
    row = _conn.execute(
        "SELECT * FROM replication_jobs WHERE id = ?", (job_id,)
    ).fetchone()
    return dict(row) if row else None


def create_replication_job(name: str, job_type: str, master_conn_id: int,
                            slave_conn_id: int, interval_secs: int = 60) -> int:
    with _write_lock:
        cur = _conn.execute(
            """INSERT INTO replication_jobs
               (name, job_type, master_conn_id, slave_conn_id, interval_secs)
               VALUES (?, ?, ?, ?, ?)""",
            (name, job_type, master_conn_id, slave_conn_id, interval_secs),
        )
        _conn.commit()
    return cur.lastrowid


def update_job_status(job_id: int, status: str, last_run: datetime | None,
                      last_error: str | None, last_replicated_id: int | None = None) -> None:
    with _write_lock:
        if last_replicated_id is not None:
            _conn.execute(
                """UPDATE replication_jobs
                   SET status=?, last_run=?, last_error=?, last_replicated_id=?
                   WHERE id=?""",
                (status, last_run, last_error, last_replicated_id, job_id),
            )
        else:
            _conn.execute(
                "UPDATE replication_jobs SET status=?, last_run=?, last_error=? WHERE id=?",
                (status, last_run, last_error, job_id),
            )
        _conn.commit()


def delete_replication_job(job_id: int) -> None:
    with _write_lock:
        _conn.execute("DELETE FROM replication_jobs WHERE id = ?", (job_id,))
        _conn.commit()
