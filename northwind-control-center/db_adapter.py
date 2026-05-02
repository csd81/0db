"""
db_adapter.py — Multi-database connection router.

Supports SQLite (sqlite3) and SQL Server (pyodbc).
Connections are cached in Flask g keyed by conn_id for request lifetime.
Does NOT affect the existing db.py / SQL Server connection used by the original modules.
"""

import sqlite3

import psycopg2
import psycopg2.extras
import pymysql
import pymysql.cursors
import pyodbc
import redis as _redis
from neo4j import GraphDatabase
from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from flask import g

import meta_db


def get_adapter_connection(conn_id: int):
    """Return a cached connection for this request, opening it if needed."""
    cache_key = f'_adapter_{conn_id}'
    conn = g.get(cache_key)
    if conn is not None:
        return conn

    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found in meta.db")

    db_type = rec['db_type']
    params = rec['conn_params']
    password = rec.get('password', '')

    if db_type == 'sqlite':
        path = params.get('database', ':memory:')
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
    elif db_type == 'sqlserver':
        driver = params.get('driver', 'ODBC Driver 18 for SQL Server')
        server = params.get('server', 'localhost')
        database = params.get('database', '')
        username = params.get('username', '')
        encrypt = params.get('encrypt', 'yes')
        trust_cert = params.get('trust_server_cert', 'yes')
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"UID={username};PWD={password};"
            f"Encrypt={encrypt};TrustServerCertificate={trust_cert};"
            "Connection Timeout=10;"
        )
        conn = pyodbc.connect(conn_str)
    elif db_type == 'postgresql':
        conn = psycopg2.connect(
            host=params.get('host', 'localhost'),
            port=int(params.get('port', 5432)),
            dbname=params.get('database', 'postgres'),
            user=params.get('username', 'postgres'),
            password=password,
        )
        conn.autocommit = True
    elif db_type == 'mysql':
        conn = pymysql.connect(
            host=params.get('host', 'localhost'),
            port=int(params.get('port', 3306)),
            database=params.get('database', ''),
            user=params.get('username', 'root'),
            password=password,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
    else:
        raise ValueError(f"Unsupported db_type: {db_type!r}")

    setattr(g, cache_key, conn)
    return conn


def adapter_select(conn_id: int, sql: str, params=None) -> tuple[list, list]:
    """Execute a SELECT and return (column_names, rows_as_lists)."""
    conn = get_adapter_connection(conn_id)
    rec = meta_db.get_connection_by_id(conn_id)
    db_type = rec['db_type']

    if db_type == 'mysql':
        cur = conn.cursor()
        cur.execute(sql, params or [])
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = [list(r.values()) for r in cur.fetchall()]
    else:
        cur = conn.execute(sql, params or [])
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = [list(r) for r in cur.fetchall()]

    return columns, rows


def adapter_execute(conn_id: int, sql: str, params=None) -> int:
    """Execute a non-SELECT statement, commit, and return rowcount."""
    conn = get_adapter_connection(conn_id)
    rec = meta_db.get_connection_by_id(conn_id)
    db_type = rec['db_type']

    if db_type == 'mysql':
        cur = conn.cursor()
        cur.execute(sql, params or [])
        return cur.rowcount
    else:
        cur = conn.execute(sql, params or [])
        conn.commit()
        return cur.rowcount


def adapter_test(conn_id: int) -> tuple[bool, str | None]:
    """Open a fresh connection (not cached) and run a trivial query."""
    try:
        rec = meta_db.get_connection_by_id(conn_id)
        if rec is None:
            return False, "Connection record not found."
        db_type = rec['db_type']
        params = rec['conn_params']
        password = rec.get('password', '')

        if db_type == 'sqlite':
            path = params.get('database', ':memory:')
            c = sqlite3.connect(path, timeout=5)
            c.execute("SELECT 1")
            c.close()
        elif db_type == 'sqlserver':
            driver = params.get('driver', 'ODBC Driver 18 for SQL Server')
            server = params.get('server', 'localhost')
            database = params.get('database', '')
            username = params.get('username', '')
            encrypt = params.get('encrypt', 'yes')
            trust_cert = params.get('trust_server_cert', 'yes')
            conn_str = (
                f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
                f"UID={username};PWD={password};"
                f"Encrypt={encrypt};TrustServerCertificate={trust_cert};"
                "Connection Timeout=5;"
            )
            c = pyodbc.connect(conn_str)
            c.execute("SELECT 1")
            c.close()
        elif db_type == 'postgresql':
            c = psycopg2.connect(
                host=params.get('host', 'localhost'),
                port=int(params.get('port', 5432)),
                dbname=params.get('database', 'postgres'),
                user=params.get('username', 'postgres'),
                password=password,
            )
            c.cursor().execute("SELECT 1")
            c.close()
        elif db_type == 'mysql':
            c = pymysql.connect(
                host=params.get('host', 'localhost'),
                port=int(params.get('port', 3306)),
                database=params.get('database', ''),
                user=params.get('username', 'root'),
                password=password,
                connect_timeout=5,
            )
            c.cursor().execute("SELECT 1")
            c.close()
        elif db_type == 'mongodb':
            _u = params.get('username', '') or None
            _p = password or None
            _c = MongoClient(
                host=params.get('host', 'localhost'),
                port=int(params.get('port', 27017)),
                username=_u, password=_p,
                serverSelectionTimeoutMS=5000,
            )
            _c.admin.command('ping')
            _c.close()
        elif db_type == 'redis':
            c = _redis.Redis(
                host=params.get('host', 'localhost'),
                port=int(params.get('port', 6379)),
                db=int(params.get('db', 0)),
                password=password or None,
                socket_timeout=5,
                decode_responses=True,
            )
            c.ping()
        elif db_type == 'neo4j':
            d = GraphDatabase.driver(
                params.get('uri', 'bolt://localhost:7687'),
                auth=(params.get('username', 'neo4j'), password),
                connection_timeout=5,
            )
            d.verify_connectivity()
            d.close()
        elif db_type == 'cassandra':
            _ap = None
            if params.get('username'):
                _ap = PlainTextAuthProvider(params['username'], password or '')
            _cl = Cluster(
                contact_points=[params.get('host', 'localhost')],
                port=int(params.get('port', 9042)),
                auth_provider=_ap,
                connect_timeout=10,
            )
            _s = _cl.connect()
            _s.execute("SELECT release_version FROM system.local")
            _cl.shutdown()
        elif db_type == 'rqlite':
            import requests as _req
            r = _req.get(params.get('url', 'http://127.0.0.1:4001') + '/status', timeout=5)
            r.raise_for_status()
        elif db_type == 'elasticsearch':
            from elasticsearch import Elasticsearch
            _ec = Elasticsearch(
                params.get('url', 'https://localhost:9200'),
                basic_auth=(params.get('username', 'elastic'), password),
                verify_certs=False, ssl_show_warn=False,
                request_timeout=5,
            )
            _ec.info()
        else:
            return False, f"Unsupported db_type: {db_type!r}"

        return True, None
    except Exception as e:
        return False, str(e)


def get_mongo_client(conn_id: int):
    """Return a cached MongoClient for this request."""
    cache_key = f'_mongo_{conn_id}'
    client = g.get(cache_key)
    if client is not None:
        return client

    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found in meta.db")
    params = rec['conn_params']
    password = rec.get('password', '') or None
    username = params.get('username', '') or None

    host = params.get('host', 'localhost')
    port = int(params.get('port', 27017))

    if username and password:
        client = MongoClient(host=host, port=port, username=username, password=password,
                             serverSelectionTimeoutMS=5000)
    else:
        client = MongoClient(host=host, port=port, serverSelectionTimeoutMS=5000)

    setattr(g, cache_key, client)
    return client


def get_redis_client(conn_id: int):
    """Return a cached Redis client for this request."""
    cache_key = f'_redis_{conn_id}'
    client = g.get(cache_key)
    if client is not None:
        return client

    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found in meta.db")
    params = rec['conn_params']
    password = rec.get('password', '') or None

    client = _redis.Redis(
        host=params.get('host', 'localhost'),
        port=int(params.get('port', 6379)),
        db=int(params.get('db', 0)),
        password=password,
        decode_responses=True,
    )
    setattr(g, cache_key, client)
    return client


def get_neo4j_driver(conn_id: int):
    """Return a cached Neo4j driver for this request."""
    cache_key = f'_neo4j_{conn_id}'
    driver = g.get(cache_key)
    if driver is not None:
        return driver

    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found in meta.db")
    params = rec['conn_params']
    password = rec.get('password', '')

    driver = GraphDatabase.driver(
        params.get('uri', 'bolt://localhost:7687'),
        auth=(params.get('username', 'neo4j'), password),
    )
    setattr(g, cache_key, driver)
    return driver


def get_cassandra_session(conn_id: int):
    """Return a cached Cassandra session for this request."""
    cache_key = f'_cassandra_{conn_id}'
    sess = g.get(cache_key)
    if sess is not None:
        return sess

    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found in meta.db")
    params = rec['conn_params']
    password = rec.get('password', '') or ''
    username = params.get('username', '') or ''

    auth = PlainTextAuthProvider(username, password) if username else None
    cluster = Cluster(
        contact_points=[params.get('host', 'localhost')],
        port=int(params.get('port', 9042)),
        auth_provider=auth,
        connect_timeout=10,
    )
    session = cluster.connect()
    # Store cluster on g so teardown can shut it down
    setattr(g, f'_cassandra_cluster_{conn_id}', cluster)
    setattr(g, cache_key, session)
    return session


def close_adapter_connections(e=None) -> None:
    """Teardown hook: close all adapter connections opened during this request."""
    for key in list(vars(g)):
        if any(key.startswith(p) for p in ('_adapter_', '_neo4j_', '_redis_', '_mongo_')):
            obj = getattr(g, key, None)
            if obj:
                try:
                    obj.close()
                except Exception:
                    pass
        elif key.startswith('_cassandra_cluster_'):
            cluster = getattr(g, key, None)
            if cluster:
                try:
                    cluster.shutdown()
                except Exception:
                    pass
