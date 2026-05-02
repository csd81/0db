"""
mongo_service.py — MongoDB collection browser, document CRUD, and aggregation demos.
"""

import db_adapter
import meta_db


def get_db(conn_id: int):
    client = db_adapter.get_mongo_client(conn_id)
    rec = meta_db.get_connection_by_id(conn_id)
    dbname = rec['conn_params'].get('database', 'northwind')
    return client[dbname]


def list_collections(conn_id: int) -> tuple[list, str | None]:
    try:
        db = get_db(conn_id)
        return sorted(db.list_collection_names()), None
    except Exception as e:
        return [], str(e)


def get_collection_stats(conn_id: int, collection: str) -> dict:
    try:
        db = get_db(conn_id)
        col = db[collection]
        count = col.count_documents({})
        sample = list(col.find({}, {'_id': 0}).limit(1))
        keys = list(sample[0].keys()) if sample else []
        return {'count': count, 'fields': keys, 'error': None}
    except Exception as e:
        return {'count': 0, 'fields': [], 'error': str(e)}


def find_documents(conn_id: int, collection: str, filter_str: str = '{}',
                   limit: int = 50) -> tuple[list, list, str | None]:
    """Return (columns, rows, error). Rows are flattened dicts."""
    import json
    try:
        db = get_db(conn_id)
        col = db[collection]
        try:
            flt = json.loads(filter_str) if filter_str.strip() else {}
        except json.JSONDecodeError as je:
            return [], [], f'Invalid filter JSON: {je}'

        docs = list(col.find(flt, {'_id': 0}).limit(limit))
        if not docs:
            return [], [], None

        # Collect all keys in order
        seen = {}
        for doc in docs:
            for k in doc:
                seen[k] = True
        columns = list(seen.keys())
        rows = [[str(doc.get(c, '')) for c in columns] for doc in docs]
        return columns, rows, None
    except Exception as e:
        return [], [], str(e)


def insert_document(conn_id: int, collection: str, doc_str: str) -> str | None:
    import json
    try:
        db = get_db(conn_id)
        doc = json.loads(doc_str)
        db[collection].insert_one(doc)
        return None
    except Exception as e:
        return str(e)


def drop_collection(conn_id: int, collection: str) -> str | None:
    try:
        get_db(conn_id)[collection].drop()
        return None
    except Exception as e:
        return str(e)


# ── Northwind import ──────────────────────────────────────────────────────────

def import_northwind(conn_id: int, source_conn_id: int) -> tuple[dict, str | None]:
    """
    Read core Northwind tables from a SQL connection and load them into MongoDB
    as embedded documents (denormalized). Returns stats dict.
    """
    import db_adapter as da

    db = get_db(conn_id)
    stats = {}

    try:
        # Categories
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT CategoryID, CategoryName, Description FROM Categories')
        cats = {r[0]: {'id': r[0], 'name': r[1], 'description': r[2]} for r in rows}

        # Suppliers
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT SupplierID, CompanyName, Country FROM Suppliers')
        suppliers = {r[0]: {'id': r[0], 'name': r[1], 'country': r[2]} for r in rows}

        # Products — embed category + supplier
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT ProductID, ProductName, CategoryID, SupplierID, '
            'UnitPrice, UnitsInStock, Discontinued FROM Products')
        products = {}
        prod_docs = []
        for r in rows:
            doc = {
                'product_id': r[0], 'name': r[1],
                'category': cats.get(r[2], {}),
                'supplier': suppliers.get(r[3], {}),
                'unit_price': float(r[4]) if r[4] else 0.0,
                'units_in_stock': r[5],
                'discontinued': bool(r[6]),
            }
            products[r[0]] = doc
            prod_docs.append(doc)
        db['products'].drop()
        if prod_docs:
            db['products'].insert_many(prod_docs)
        stats['products'] = len(prod_docs)

        # Customers
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT CustomerID, CompanyName, ContactName, Country, City FROM Customers')
        custs = {}
        cust_docs = []
        for r in rows:
            doc = {'customer_id': r[0], 'company': r[1],
                   'contact': r[2], 'country': r[3], 'city': r[4]}
            custs[r[0]] = doc
            cust_docs.append(doc)
        db['customers'].drop()
        if cust_docs:
            db['customers'].insert_many(cust_docs)
        stats['customers'] = len(cust_docs)

        # Order details map
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT OrderID, ProductID, UnitPrice, Quantity, Discount '
            'FROM [Order Details]')
        od_map: dict[int, list] = {}
        for r in rows:
            od_map.setdefault(r[0], []).append({
                'product': products.get(r[1], {'product_id': r[1]}),
                'unit_price': float(r[2]),
                'quantity': r[3],
                'discount': float(r[4]),
                'line_total': round(float(r[2]) * r[3] * (1 - float(r[4])), 2),
            })

        # Orders — embed customer + order lines
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT OrderID, CustomerID, EmployeeID, OrderDate, ShipCountry FROM Orders')
        order_docs = []
        for r in rows:
            doc = {
                'order_id': r[0],
                'customer': custs.get(r[1], {'customer_id': r[1]}),
                'employee_id': r[2],
                'order_date': str(r[3]) if r[3] else None,
                'ship_country': r[4],
                'items': od_map.get(r[0], []),
                'total': round(sum(i['line_total'] for i in od_map.get(r[0], [])), 2),
            }
            order_docs.append(doc)
        db['orders'].drop()
        if order_docs:
            db['orders'].insert_many(order_docs)
        stats['orders'] = len(order_docs)

        return stats, None
    except Exception as e:
        return stats, str(e)


# ── Aggregation demos ─────────────────────────────────────────────────────────

_AGG_QUERIES = {
    'revenue_by_category': {
        'label': 'Revenue by category',
        'collection': 'orders',
        'pipeline': [
            {'$unwind': '$items'},
            {'$group': {
                '_id': '$items.product.category.name',
                'revenue': {'$sum': '$items.line_total'},
                'orders': {'$addToSet': '$order_id'},
            }},
            {'$project': {
                'category': '$_id', '_id': 0,
                'revenue': {'$round': ['$revenue', 2]},
                'order_count': {'$size': '$orders'},
            }},
            {'$sort': {'revenue': -1}},
        ],
    },
    'orders_by_country': {
        'label': 'Orders by country',
        'collection': 'orders',
        'pipeline': [
            {'$group': {'_id': '$ship_country', 'count': {'$sum': 1},
                        'total': {'$sum': '$total'}}},
            {'$project': {'country': '$_id', '_id': 0,
                          'orders': '$count',
                          'revenue': {'$round': ['$total', 2]}}},
            {'$sort': {'orders': -1}},
            {'$limit': 15},
        ],
    },
    'top_products': {
        'label': 'Top 10 products by revenue',
        'collection': 'orders',
        'pipeline': [
            {'$unwind': '$items'},
            {'$group': {'_id': '$items.product.name',
                        'revenue': {'$sum': '$items.line_total'}}},
            {'$project': {'product': '$_id', '_id': 0,
                          'revenue': {'$round': ['$revenue', 2]}}},
            {'$sort': {'revenue': -1}},
            {'$limit': 10},
        ],
    },
}


def agg_queries() -> list[dict]:
    return [{'key': k, **v} for k, v in _AGG_QUERIES.items()]


def run_aggregation(conn_id: int, query_key: str) -> tuple[list, list, str | None]:
    q = _AGG_QUERIES.get(query_key)
    if not q:
        return [], [], 'Unknown aggregation key'
    try:
        db = get_db(conn_id)
        docs = list(db[q['collection']].aggregate(q['pipeline']))
        if not docs:
            return [], [], None
        cols = list(docs[0].keys())
        rows = [[str(doc.get(c, '')) for c in cols] for doc in docs]
        return cols, rows, None
    except Exception as e:
        return [], [], str(e)
