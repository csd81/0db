"""
elasticsearch_service.py — Elasticsearch index browser, full-text search, and aggregation demos.
"""

import db_adapter
import meta_db

# ── Built-in quick queries ────────────────────────────────────────────────────

_BUILTIN_QUERIES = [
    {'key': 'beverages',  'label': 'Beverages',         'query_text': 'beverages'},
    {'key': 'chai',       'label': 'Chai',               'query_text': 'chai'},
    {'key': 'anise',      'label': 'Anise',              'query_text': 'anise'},
    {'key': 'seafood',    'label': 'Seafood',            'query_text': 'seafood'},
    {'key': 'chocolate',  'label': 'Chocolate',          'query_text': 'chocolate'},
    {'key': 'sauce',      'label': 'Sauce',              'query_text': 'sauce'},
]

# ── Built-in aggregations ─────────────────────────────────────────────────────

_AGG_DEMOS = {
    'price_range_buckets': {
        'label': 'Products by price range',
        'index': 'northwind_products',
        'body': {
            'size': 0,
            'aggs': {
                'price_ranges': {
                    'range': {
                        'field': 'unit_price',
                        'ranges': [
                            {'key': '$0–$10',   'from': 0,  'to': 10},
                            {'key': '$10–$25',  'from': 10, 'to': 25},
                            {'key': '$25–$50',  'from': 25, 'to': 50},
                            {'key': '$50–$100', 'from': 50, 'to': 100},
                            {'key': '$100+',    'from': 100},
                        ],
                    }
                }
            },
        },
    },
    'avg_price_by_category': {
        'label': 'Average price by category',
        'index': 'northwind_categories',
        'body': {
            'size': 0,
            'aggs': {
                'categories': {
                    'terms': {
                        'field': 'category_name.keyword',
                        'size': 20,
                    },
                    'aggs': {
                        'avg_price': {
                            'avg': {'field': 'avg_unit_price'}
                        }
                    }
                }
            },
        },
    },
}


# ── Client factory ────────────────────────────────────────────────────────────

def get_client(conn_id: int):
    """Build and return an Elasticsearch client for the given connection id."""
    from elasticsearch import Elasticsearch

    rec = meta_db.get_connection_by_id(conn_id)
    if rec is None:
        raise ValueError(f"Connection id={conn_id} not found in meta.db")

    params = rec['conn_params']
    password = rec.get('password', '')

    url = params.get('url', 'https://localhost:9200')
    username = params.get('username', 'elastic')

    client = Elasticsearch(
        url,
        basic_auth=(username, password),
        verify_certs=False,
        ssl_show_warn=False,
    )
    return client


# ── Index listing ─────────────────────────────────────────────────────────────

def list_indices(conn_id: int) -> tuple[list, str | None]:
    """Return (list of index dicts, error).

    Each dict has keys: name, docs_count, store_size.
    """
    try:
        client = get_client(conn_id)
        raw = client.cat.indices(format='json', h='index,docs.count,store.size', s='index')
        indices = []
        for item in raw:
            indices.append({
                'name':        item.get('index', ''),
                'docs_count':  item.get('docs.count', '0') or '0',
                'store_size':  item.get('store.size', '0b') or '0b',
            })
        # Filter out system indices that start with '.'
        indices = [i for i in indices if not i['name'].startswith('.')]
        return indices, None
    except Exception as e:
        return [], str(e)


# ── Index info ────────────────────────────────────────────────────────────────

def get_index_info(conn_id: int, index_name: str) -> dict:
    """Return dict with 'fields' (list of field names) and 'doc_count' (int)."""
    try:
        client = get_client(conn_id)

        # Mapping fields
        mapping = client.indices.get_mapping(index=index_name)
        props = {}
        for _idx, idx_data in mapping.items():
            props.update(idx_data.get('mappings', {}).get('properties', {}))
        fields = list(props.keys())

        # Document count
        count_resp = client.count(index=index_name)
        doc_count = count_resp.get('count', 0)

        return {'fields': fields, 'doc_count': doc_count, 'error': None}
    except Exception as e:
        return {'fields': [], 'doc_count': 0, 'error': str(e)}


# ── Northwind import ──────────────────────────────────────────────────────────

def import_northwind(conn_id: int, source_conn_id: int) -> tuple[dict, str | None]:
    """Import Northwind Products and Categories from a SQL source into ES.

    Returns (stats dict, error).
    """
    try:
        client = get_client(conn_id)
        stats = {}

        # ── Products ──────────────────────────────────────────────────────────
        _cols, rows = db_adapter.adapter_select(
            source_conn_id,
            'SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, '
            'UnitsInStock, Discontinued FROM Products'
        )

        # Recreate index
        if client.indices.exists(index='northwind_products'):
            client.indices.delete(index='northwind_products')

        client.indices.create(
            index='northwind_products',
            body={
                'mappings': {
                    'properties': {
                        'product_id':        {'type': 'integer'},
                        'product_name':      {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
                        'quantity_per_unit': {'type': 'text'},
                        'unit_price':        {'type': 'float'},
                        'units_in_stock':    {'type': 'integer'},
                        'discontinued':      {'type': 'boolean'},
                    }
                }
            }
        )

        product_count = 0
        for row in rows:
            doc = {
                'product_id':        int(row[0]) if row[0] is not None else None,
                'product_name':      str(row[1]) if row[1] is not None else '',
                'quantity_per_unit': str(row[2]) if row[2] is not None else '',
                'unit_price':        float(row[3]) if row[3] is not None else 0.0,
                'units_in_stock':    int(row[4]) if row[4] is not None else 0,
                'discontinued':      bool(row[5]),
            }
            client.index(index='northwind_products', id=doc['product_id'], document=doc)
            product_count += 1

        stats['products'] = product_count

        # ── Categories ────────────────────────────────────────────────────────
        _cols, cat_rows = db_adapter.adapter_select(
            source_conn_id,
            'SELECT CategoryID, CategoryName, Description FROM Categories'
        )

        if client.indices.exists(index='northwind_categories'):
            client.indices.delete(index='northwind_categories')

        client.indices.create(
            index='northwind_categories',
            body={
                'mappings': {
                    'properties': {
                        'category_id':   {'type': 'integer'},
                        'category_name': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
                        'description':   {'type': 'text'},
                        'avg_unit_price':{'type': 'float'},
                    }
                }
            }
        )

        category_count = 0
        for row in cat_rows:
            doc = {
                'category_id':    int(row[0]) if row[0] is not None else None,
                'category_name':  str(row[1]) if row[1] is not None else '',
                'description':    str(row[2]) if row[2] is not None else '',
                'avg_unit_price': 0.0,
            }
            client.index(index='northwind_categories', id=doc['category_id'], document=doc)
            category_count += 1

        stats['categories'] = category_count

        # Refresh so the data is immediately searchable
        client.indices.refresh(index='northwind_products')
        client.indices.refresh(index='northwind_categories')

        return stats, None
    except Exception as e:
        return {}, str(e)


# ── Full-text search ──────────────────────────────────────────────────────────

def search(conn_id: int, index: str, query_text: str,
           fuzziness: str = 'AUTO') -> tuple[list, list, int, str | None]:
    """Run a multi_match fuzzy search.

    Returns (columns, rows, total_hits, error).
    Rows are lists (one per hit); columns are derived from the first hit's _source keys.
    """
    try:
        client = get_client(conn_id)

        body = {
            'query': {
                'multi_match': {
                    'query':     query_text,
                    'fields':    ['*'],
                    'fuzziness': fuzziness,
                    'operator':  'or',
                }
            },
            'size': 50,
        }

        resp = client.search(index=index, body=body)
        hits = resp['hits']['hits']
        total_hits = resp['hits']['total']['value']

        if not hits:
            return [], [], total_hits, None

        # Derive columns from the union of all _source keys (preserving order)
        seen_cols: dict[str, bool] = {}
        for hit in hits:
            for k in hit.get('_source', {}):
                seen_cols[k] = True
        columns = list(seen_cols.keys())

        rows = []
        for hit in hits:
            src = hit.get('_source', {})
            rows.append([str(src.get(c, '')) for c in columns])

        return columns, rows, total_hits, None
    except Exception as e:
        return [], [], 0, str(e)


# ── Aggregation demos ─────────────────────────────────────────────────────────

def aggregation_demos(conn_id: int) -> list[dict]:
    """Return list of {key, label, agg} for the built-in aggregations."""
    return [{'key': k, 'label': v['label'], 'index': v['index']}
            for k, v in _AGG_DEMOS.items()]


def run_aggregation(conn_id: int, agg_key: str) -> tuple[list, list, str | None]:
    """Run a built-in aggregation. Returns (columns, rows, error)."""
    demo = _AGG_DEMOS.get(agg_key)
    if not demo:
        return [], [], f'Unknown aggregation key: {agg_key!r}'

    try:
        client = get_client(conn_id)
        resp = client.search(index=demo['index'], body=demo['body'])
        aggs = resp.get('aggregations', {})

        rows: list[list] = []
        columns: list[str] = []

        if agg_key == 'price_range_buckets':
            buckets = aggs.get('price_ranges', {}).get('buckets', [])
            columns = ['price_range', 'doc_count']
            for b in buckets:
                rows.append([b.get('key', ''), str(b.get('doc_count', 0))])

        elif agg_key == 'avg_price_by_category':
            buckets = aggs.get('categories', {}).get('buckets', [])
            columns = ['category', 'product_count', 'avg_price']
            for b in buckets:
                avg = b.get('avg_price', {}).get('value')
                avg_str = f'{avg:.2f}' if avg is not None else 'N/A'
                rows.append([b.get('key', ''), str(b.get('doc_count', 0)), avg_str])

        return columns, rows, None
    except Exception as e:
        return [], [], str(e)


# ── Delete index ──────────────────────────────────────────────────────────────

def delete_index(conn_id: int, index_name: str) -> str | None:
    """Delete an index by name. Returns error string or None."""
    try:
        client = get_client(conn_id)
        client.indices.delete(index=index_name)
        return None
    except Exception as e:
        return str(e)


# ── Built-in queries ──────────────────────────────────────────────────────────

def builtin_queries() -> list[dict]:
    """Return list of {key, label, query_text} for quick-search buttons."""
    return list(_BUILTIN_QUERIES)


# ── Query Studio integration ──────────────────────────────────────────────────

def run_query(conn_id: int, query_text: str) -> tuple[list, list, int, str | None]:
    """
    Query Studio hook. Uses ES SQL API for SQL-like syntax, falls back to
    full-text search if the query doesn't look like SQL.
    Returns (columns, rows, elapsed_ms, error).
    """
    import time
    start = time.perf_counter()
    try:
        client = get_client(conn_id)
        stripped = query_text.strip().upper()

        # Try ES SQL if query looks like SQL SELECT
        if stripped.startswith('SELECT') or stripped.startswith('SHOW') or stripped.startswith('DESCRIBE'):
            resp = client.sql.query(body={'query': query_text, 'fetch_size': 200})
            columns = [col['name'] for col in resp.get('columns', [])]
            rows = [list(r) for r in resp.get('rows', [])]
        else:
            # Treat as full-text search against all product indices
            indices, _ = list_indices(conn_id)
            idx_name = 'northwind_products' if any(i['name'] == 'northwind_products' for i in indices) else '_all'
            cols, rows, total, err = search(conn_id, idx_name, query_text)
            if err:
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                return [], [], elapsed_ms, err
            columns = cols

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return columns, rows, elapsed_ms, None
    except Exception as e:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return [], [], elapsed_ms, str(e)
