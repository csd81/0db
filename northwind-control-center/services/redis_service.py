"""
redis_service.py — Redis key browser, info, and query caching demo.
"""

import json
import time
import db_adapter
import meta_db


def get_server_info(conn_id: int) -> tuple[dict, str | None]:
    try:
        r = db_adapter.get_redis_client(conn_id)
        info = r.info()
        keyspace = r.info('keyspace')
        return {
            'version':    info.get('redis_version', '?'),
            'uptime_sec': info.get('uptime_in_seconds', 0),
            'used_memory': info.get('used_memory_human', '?'),
            'connected_clients': info.get('connected_clients', 0),
            'total_commands': info.get('total_commands_processed', 0),
            'keyspace': keyspace,
        }, None
    except Exception as e:
        return {}, str(e)


def scan_keys(conn_id: int, pattern: str = '*', count: int = 100) -> tuple[list, str | None]:
    """Return up to `count` keys matching pattern with their types and TTLs."""
    try:
        r = db_adapter.get_redis_client(conn_id)
        keys = []
        cursor = 0
        while True:
            cursor, batch = r.scan(cursor, match=pattern, count=50)
            for key in batch:
                ktype = r.type(key)
                ttl = r.ttl(key)
                keys.append({'key': key, 'type': ktype, 'ttl': ttl})
                if len(keys) >= count:
                    break
            if cursor == 0 or len(keys) >= count:
                break
        keys.sort(key=lambda k: k['key'])
        return keys, None
    except Exception as e:
        return [], str(e)


def get_value(conn_id: int, key: str) -> tuple[str | None, str, str | None]:
    """Return (value_str, type, error)."""
    try:
        r = db_adapter.get_redis_client(conn_id)
        ktype = r.type(key)
        if ktype == 'string':
            val = r.get(key)
        elif ktype == 'list':
            val = json.dumps(r.lrange(key, 0, 99))
        elif ktype == 'hash':
            val = json.dumps(r.hgetall(key), indent=2)
        elif ktype == 'set':
            val = json.dumps(list(r.smembers(key)))
        elif ktype == 'zset':
            val = json.dumps(r.zrange(key, 0, 99, withscores=True))
        else:
            val = f'(unsupported type: {ktype})'
        return val, ktype, None
    except Exception as e:
        return None, 'unknown', str(e)


def set_value(conn_id: int, key: str, value: str, ttl: int | None = None) -> str | None:
    try:
        r = db_adapter.get_redis_client(conn_id)
        if ttl and ttl > 0:
            r.setex(key, ttl, value)
        else:
            r.set(key, value)
        return None
    except Exception as e:
        return str(e)


def delete_key(conn_id: int, key: str) -> str | None:
    try:
        r = db_adapter.get_redis_client(conn_id)
        r.delete(key)
        return None
    except Exception as e:
        return str(e)


def flush_db(conn_id: int) -> str | None:
    try:
        r = db_adapter.get_redis_client(conn_id)
        r.flushdb()
        return None
    except Exception as e:
        return str(e)


# ── Query cache demo ───────────────────────────────────────────────────────────

_DEMO_QUERIES = {
    'top_products': {
        'label': 'Top 10 products by revenue',
        'sql': """
            SELECT TOP 10 p.ProductName,
                   ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS Revenue
            FROM [Order Details] od
            JOIN Products p ON p.ProductID = od.ProductID
            GROUP BY p.ProductName
            ORDER BY Revenue DESC
        """.strip(),
        'cache_key': 'nwcc:top_products',
    },
    'orders_by_country': {
        'label': 'Order count by country',
        'sql': """
            SELECT ShipCountry, COUNT(*) AS Orders
            FROM Orders
            GROUP BY ShipCountry
            ORDER BY Orders DESC
        """.strip(),
        'cache_key': 'nwcc:orders_by_country',
    },
    'category_sales': {
        'label': 'Revenue by category',
        'sql': """
            SELECT c.CategoryName,
                   ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS Revenue
            FROM [Order Details] od
            JOIN Products p ON p.ProductID = od.ProductID
            JOIN Categories c ON c.CategoryID = p.CategoryID
            GROUP BY c.CategoryName
            ORDER BY Revenue DESC
        """.strip(),
        'cache_key': 'nwcc:category_sales',
    },
}


def demo_queries() -> list[dict]:
    return [{'key': k, **v} for k, v in _DEMO_QUERIES.items()]


def run_cached_query(redis_conn_id: int, query_key: str, ttl: int = 60) -> dict:
    """
    Run a demo query against the default SQL Server connection, caching
    the result in Redis. Returns timing and hit/miss info.
    """
    import db as _db
    import services.query_service as qs

    q = _DEMO_QUERIES.get(query_key)
    if not q:
        return {'error': 'Unknown query key'}

    r = db_adapter.get_redis_client(redis_conn_id)
    cache_key = q['cache_key']
    remaining_ttl = r.ttl(cache_key)

    t0 = time.perf_counter()
    cached = r.get(cache_key)
    t_redis = time.perf_counter() - t0

    if cached:
        data = json.loads(cached)
        return {
            'hit': True,
            'label': q['label'],
            'columns': data['columns'],
            'rows': data['rows'],
            'elapsed_redis_ms': round(t_redis * 1000, 2),
            'elapsed_sql_ms': None,
            'ttl': remaining_ttl,
            'cache_key': cache_key,
        }

    # Cache miss — run against SQL Server
    t1 = time.perf_counter()
    columns, rows, elapsed_ms, error = qs.run_user_query(q['sql'], 'READ COMMITTED', True)
    t_sql = time.perf_counter() - t1

    if error:
        return {'error': error, 'hit': False, 'label': q['label']}

    payload = json.dumps({'columns': columns, 'rows': rows})
    r.setex(cache_key, ttl, payload)

    return {
        'hit': False,
        'label': q['label'],
        'columns': columns,
        'rows': rows,
        'elapsed_redis_ms': round(t_redis * 1000, 2),
        'elapsed_sql_ms': round(t_sql * 1000, 2),
        'ttl': ttl,
        'cache_key': cache_key,
    }
