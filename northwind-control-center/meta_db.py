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

# Keys persisted to app_config; excludes bootstrapping keys (FERNET_KEY, SECRET_KEY, META_DB_PATH)
_STORABLE_KEYS = {
    'SQL_SERVER', 'SQL_DATABASE', 'SQL_USERNAME', 'SQL_PASSWORD',
    'SQL_SA_USERNAME', 'SQL_SA_PASSWORD', 'SQL_DRIVER', 'SQL_ENCRYPT', 'SQL_TRUST_SERVER_CERT',
    'WINRM_HOST', 'WINRM_USERNAME', 'WINRM_PASSWORD', 'WINRM_BAK_PATH',
    'SSH_HOST', 'SSH_PORT', 'SSH_USERNAME', 'SSH_KEY_PATH', 'BACKUP_REMOTE_PATH',
    'GCS_BUCKET', 'GCS_HMAC_ACCESS_ID', 'GCS_HMAC_SECRET',
}
_PASSWORD_KEYS = {'SQL_PASSWORD', 'SQL_SA_PASSWORD', 'WINRM_PASSWORD', 'GCS_HMAC_SECRET'}


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

            CREATE TABLE IF NOT EXISTS app_config (
                key       TEXT PRIMARY KEY,
                value     TEXT,
                encrypted INTEGER DEFAULT 0
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

            -- ── Dimat (Discrete Math) gamification tables ──────────────────
            CREATE TABLE IF NOT EXISTS dimat_progress (
                user_id     INTEGER NOT NULL,
                ch          TEXT    NOT NULL,
                exercise_id TEXT    NOT NULL,
                status      TEXT    NOT NULL,
                xp_awarded  INTEGER DEFAULT 0,
                updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, ch, exercise_id)
            );
            CREATE TABLE IF NOT EXISTS dimat_quiz_results (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL,
                ch           TEXT    NOT NULL,
                score        INTEGER NOT NULL,
                total        INTEGER NOT NULL,
                duration_sec INTEGER DEFAULT 0,
                difficulty   TEXT    DEFAULT 'normal',
                xp_awarded   INTEGER DEFAULT 0,
                wrong_qids   TEXT,
                taken_at     DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS dimat_achievements (
                user_id    INTEGER NOT NULL,
                ach_key    TEXT    NOT NULL,
                earned_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, ach_key)
            );
            CREATE TABLE IF NOT EXISTS dimat_srs (
                user_id        INTEGER NOT NULL,
                ch             TEXT    NOT NULL,
                question_id    TEXT    NOT NULL,
                ease           REAL    DEFAULT 2.5,
                interval_days  INTEGER DEFAULT 1,
                due_at         DATETIME,
                mistake_count  INTEGER DEFAULT 0,
                last_seen_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, ch, question_id)
            );
            CREATE TABLE IF NOT EXISTS dimat_community_goal (
                period          TEXT PRIMARY KEY,
                problems_solved INTEGER DEFAULT 0,
                goal            INTEGER DEFAULT 10000,
                reached_at      DATETIME
            );
            CREATE INDEX IF NOT EXISTS idx_dimat_progress_user ON dimat_progress(user_id);
            CREATE INDEX IF NOT EXISTS idx_dimat_quiz_user_ch ON dimat_quiz_results(user_id, ch);
            CREATE INDEX IF NOT EXISTS idx_dimat_srs_due ON dimat_srs(user_id, due_at);
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


# ── App Config (persistent key/value, survives restarts) ──────────────────────

def set_app_config(key: str, value: str) -> None:
    encrypted = key in _PASSWORD_KEYS
    stored = _encrypt(str(value)) if encrypted else str(value)
    with _write_lock:
        _conn.execute(
            "INSERT OR REPLACE INTO app_config (key, value, encrypted) VALUES (?, ?, ?)",
            (key, stored, int(encrypted)),
        )
        _conn.commit()


def get_app_config(key: str, default=None):
    row = _conn.execute(
        "SELECT value, encrypted FROM app_config WHERE key = ?", (key,)
    ).fetchone()
    if row is None:
        return default
    value, encrypted = row
    return _decrypt(value) if encrypted and value else value


def get_all_app_config() -> dict:
    rows = _conn.execute("SELECT key, value, encrypted FROM app_config").fetchall()
    result = {}
    for key, value, encrypted in rows:
        result[key] = _decrypt(value) if encrypted and value else value
    return result


def load_config_into_app(app) -> None:
    """Load persisted config into app.config.
    First run (empty table): seeds from current app.config (.env values).
    Subsequent runs: overrides app.config with stored values."""
    stored = get_all_app_config()
    if not stored:
        for key in _STORABLE_KEYS:
            value = app.config.get(key)
            if value is not None:
                set_app_config(key, str(value))
    else:
        for key, value in stored.items():
            if key in _STORABLE_KEYS:
                app.config[key] = value


# ── Dimat: shared accessor + low-level helpers ─────────────────────────────────
# All functions below operate on the existing _conn / _write_lock; they
# tolerate user_id=0 (anonymous reader) by storing rows but never reading
# anonymous progress on subsequent visits.

def dimat_conn():
    """Return the meta_db connection so dimat_* services can issue SQL directly."""
    return _conn


def dimat_lock():
    """Return the write lock so dimat_* services can serialise their writes."""
    return _write_lock
