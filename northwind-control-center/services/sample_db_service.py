"""
sample_db_service.py — One-click sample database loaders for each engine type.
Downloads datasets to instance/samples/ on first use.
"""
import gzip
import os
import shutil
import sqlite3
import subprocess
import urllib.request
import zipfile

import meta_db
import db_adapter

_SAMPLES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'instance', 'samples')
)


def _ensure_samples_dir():
    os.makedirs(_SAMPLES_DIR, exist_ok=True)


def load_chinook(conn_id: int) -> str | None:
    """
    Load the Chinook SQLite sample database into a sqlite-type connection.
    Downloads Chinook_Sqlite.sqlite from GitHub if not cached locally.
    Returns None on success, error string on failure.
    """
    try:
        rec = meta_db.get_connection_by_id(conn_id)
        if not rec or rec['db_type'] != 'sqlite':
            return "Connection must be sqlite type."
        target_path = rec['conn_params'].get('database', '')
        if not target_path:
            return "SQLite connection has no file path configured."

        _ensure_samples_dir()
        cache_path = os.path.join(_SAMPLES_DIR, 'Chinook_Sqlite.sqlite')
        if not os.path.exists(cache_path):
            url = 'https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite'
            urllib.request.urlretrieve(url, cache_path)

        src = sqlite3.connect(cache_path)
        dst = sqlite3.connect(target_path)
        src.row_factory = sqlite3.Row

        tables = [r[0] for r in src.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()]

        for table in tables:
            schema_row = src.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone()
            if not schema_row:
                continue
            dst.execute(f"DROP TABLE IF EXISTS [{table}]")
            dst.execute(schema_row[0])
            rows = src.execute(f"SELECT * FROM [{table}]").fetchall()
            if rows:
                placeholders = ','.join(['?'] * len(rows[0]))
                dst.executemany(
                    f"INSERT INTO [{table}] VALUES ({placeholders})",
                    [tuple(r) for r in rows]
                )

        dst.commit()
        src.close()
        dst.close()
        return None
    except Exception as e:
        return str(e)


def load_dvdrental(conn_id: int) -> str | None:
    """
    Load the dvdrental PostgreSQL sample database into a postgresql-type connection.
    Downloads dvdrental.zip and restores via pg_restore.
    Returns None on success, error string on failure.
    """
    try:
        rec = meta_db.get_connection_by_id(conn_id)
        if not rec or rec['db_type'] != 'postgresql':
            return "Connection must be postgresql type."

        _ensure_samples_dir()
        zip_path = os.path.join(_SAMPLES_DIR, 'dvdrental.zip')
        tar_path = os.path.join(_SAMPLES_DIR, 'dvdrental.tar')

        if not os.path.exists(tar_path):
            if not os.path.exists(zip_path):
                url = 'https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip'
                urllib.request.urlretrieve(url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(_SAMPLES_DIR)

        params = rec['conn_params']
        password = rec.get('password', '') or ''
        host = params.get('host', 'localhost')
        port = str(params.get('port', '5432'))
        username = params.get('username', 'postgres')
        database = params.get('database', 'postgres')

        env = {**os.environ, 'PGPASSWORD': password}
        result = subprocess.run(
            ['pg_restore', '--no-owner', '--no-privileges',
             '-h', host, '-p', port, '-U', username, '-d', database, tar_path],
            env=env, capture_output=True, text=True
        )
        # pg_restore exits 1 on warnings (acceptable); only fail on exit > 1
        if result.returncode > 1:
            return (result.stderr or 'pg_restore failed')[:500]
        return None
    except FileNotFoundError:
        return "pg_restore not found. Install postgresql-client."
    except Exception as e:
        return str(e)


def load_world_db(conn_id: int) -> str | None:
    """
    Load the MySQL World sample database into a mysql/mariadb-type connection.
    Downloads world.sql.gz from MySQL's official samples if not cached.
    Returns None on success, error string on failure.
    """
    try:
        rec = meta_db.get_connection_by_id(conn_id)
        if not rec or rec['db_type'] not in ('mysql', 'mariadb'):
            return "Connection must be mysql or mariadb type."

        _ensure_samples_dir()
        gz_path = os.path.join(_SAMPLES_DIR, 'world.sql.gz')
        sql_path = os.path.join(_SAMPLES_DIR, 'world.sql')

        if not os.path.exists(sql_path):
            if not os.path.exists(gz_path):
                url = 'https://downloads.mysql.com/docs/world.sql.gz'
                urllib.request.urlretrieve(url, gz_path)
            with gzip.open(gz_path, 'rb') as f_in, open(sql_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        with open(sql_path, 'r', encoding='utf-8', errors='replace') as f:
            sql_text = f.read()

        # Split on semicolons, skip blank lines and pure-comment chunks
        statements = []
        for chunk in sql_text.split(';'):
            stripped = chunk.strip()
            if stripped and not all(line.startswith('--') for line in stripped.splitlines() if line.strip()):
                statements.append(stripped)

        params = rec['conn_params']
        password = rec.get('password', '') or ''
        import pymysql
        conn = pymysql.connect(
            host=params.get('host', 'localhost'),
            port=int(params.get('port', 3306)),
            user=params.get('username', 'root'),
            password=password,
            autocommit=True,
            charset='utf8mb4',
        )
        cur = conn.cursor()
        errors = []
        for stmt in statements:
            try:
                cur.execute(stmt)
            except Exception as e:
                err_str = str(e)
                if 'already exists' not in err_str and 'Duplicate' not in err_str:
                    errors.append(err_str[:120])
        conn.close()

        if errors:
            return f"{len(errors)} error(s) during load. First: {errors[0]}"
        return None
    except Exception as e:
        return str(e)
