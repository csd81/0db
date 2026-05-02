"""
cassandra_service.py — Cassandra keyspace/table browser, CQL execution, Northwind import.
"""

import db_adapter
import meta_db


def list_keyspaces(conn_id: int) -> tuple[list, str | None]:
    try:
        session = db_adapter.get_cassandra_session(conn_id)
        rows = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        ks = sorted(r.keyspace_name for r in rows
                    if r.keyspace_name not in ('system', 'system_auth',
                                               'system_distributed', 'system_traces',
                                               'system_schema'))
        return ks, None
    except Exception as e:
        return [], str(e)


def list_tables(conn_id: int, keyspace: str) -> tuple[list, str | None]:
    try:
        session = db_adapter.get_cassandra_session(conn_id)
        rows = session.execute(
            "SELECT table_name FROM system_schema.tables WHERE keyspace_name=%s",
            [keyspace]
        )
        return sorted(r.table_name for r in rows), None
    except Exception as e:
        return [], str(e)


def get_table_info(conn_id: int, keyspace: str, table: str) -> dict:
    try:
        session = db_adapter.get_cassandra_session(conn_id)
        cols = session.execute(
            "SELECT column_name, type, kind FROM system_schema.columns "
            "WHERE keyspace_name=%s AND table_name=%s",
            [keyspace, table]
        )
        columns = [{'name': r.column_name, 'type': r.type, 'kind': r.kind} for r in cols]
        return {'columns': columns, 'error': None}
    except Exception as e:
        return {'columns': [], 'error': str(e)}


def run_cql(conn_id: int, cql: str, keyspace: str | None = None) -> tuple[list, list, str | None]:
    """Execute a CQL statement. Returns (columns, rows, error)."""
    try:
        session = db_adapter.get_cassandra_session(conn_id)
        if keyspace:
            session.set_keyspace(keyspace)
        result = session.execute(cql)
        if result.column_names is None:
            return [], [], None
        columns = list(result.column_names)
        rows = [[str(getattr(row, col, '')) for col in columns] for row in result]
        return columns, rows, None
    except Exception as e:
        return [], [], str(e)


# ── Northwind import ──────────────────────────────────────────────────────────

_KEYSPACE = 'northwind'

_CREATE_KEYSPACE = f"""
CREATE KEYSPACE IF NOT EXISTS {_KEYSPACE}
WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
"""

_TABLES = {
    'categories': """
        CREATE TABLE IF NOT EXISTS northwind.categories (
            category_id   INT PRIMARY KEY,
            category_name TEXT,
            description   TEXT
        )
    """,
    'suppliers': """
        CREATE TABLE IF NOT EXISTS northwind.suppliers (
            supplier_id   INT PRIMARY KEY,
            company_name  TEXT,
            country       TEXT,
            city          TEXT
        )
    """,
    'products': """
        CREATE TABLE IF NOT EXISTS northwind.products (
            product_id    INT PRIMARY KEY,
            product_name  TEXT,
            category_id   INT,
            supplier_id   INT,
            unit_price    DECIMAL,
            units_in_stock INT,
            discontinued  BOOLEAN
        )
    """,
    'customers': """
        CREATE TABLE IF NOT EXISTS northwind.customers (
            customer_id   TEXT PRIMARY KEY,
            company_name  TEXT,
            contact_name  TEXT,
            country       TEXT,
            city          TEXT
        )
    """,
    'orders': """
        CREATE TABLE IF NOT EXISTS northwind.orders (
            order_id      INT PRIMARY KEY,
            customer_id   TEXT,
            employee_id   INT,
            order_date    TEXT,
            ship_country  TEXT,
            total         DECIMAL
        )
    """,
    # Wide-column pattern: order items by (order_id, product_id)
    'order_items': """
        CREATE TABLE IF NOT EXISTS northwind.order_items (
            order_id    INT,
            product_id  INT,
            unit_price  DECIMAL,
            quantity    INT,
            discount    DECIMAL,
            line_total  DECIMAL,
            PRIMARY KEY (order_id, product_id)
        )
    """,
    # Query-driven table: items by product (for "which orders contain product X")
    'items_by_product': """
        CREATE TABLE IF NOT EXISTS northwind.items_by_product (
            product_id  INT,
            order_id    INT,
            quantity    INT,
            line_total  DECIMAL,
            PRIMARY KEY (product_id, order_id)
        )
    """,
}


def import_northwind(conn_id: int, source_conn_id: int) -> tuple[dict, str | None]:
    import db_adapter as da
    from decimal import Decimal

    session = db_adapter.get_cassandra_session(conn_id)
    stats = {}

    try:
        session.execute(_CREATE_KEYSPACE)
        for ddl in _TABLES.values():
            session.execute(ddl)
        session.set_keyspace(_KEYSPACE)

        # Categories
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT CategoryID, CategoryName, Description FROM Categories')
        for r in rows:
            session.execute(
                "INSERT INTO categories (category_id, category_name, description) VALUES (%s,%s,%s)",
                (r[0], r[1], r[2]))
        stats['categories'] = len(rows)

        # Suppliers
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT SupplierID, CompanyName, Country, City FROM Suppliers')
        for r in rows:
            session.execute(
                "INSERT INTO suppliers (supplier_id, company_name, country, city) VALUES (%s,%s,%s,%s)",
                (r[0], r[1], r[2], r[3]))
        stats['suppliers'] = len(rows)

        # Products
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT ProductID, ProductName, CategoryID, SupplierID, '
            'UnitPrice, UnitsInStock, Discontinued FROM Products')
        for r in rows:
            session.execute(
                "INSERT INTO products (product_id, product_name, category_id, supplier_id, "
                "unit_price, units_in_stock, discontinued) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (r[0], r[1], r[2], r[3],
                 Decimal(str(r[4])) if r[4] is not None else Decimal('0'),
                 r[5], bool(r[6])))
        stats['products'] = len(rows)

        # Customers
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT CustomerID, CompanyName, ContactName, Country, City FROM Customers')
        for r in rows:
            session.execute(
                "INSERT INTO customers (customer_id, company_name, contact_name, country, city) "
                "VALUES (%s,%s,%s,%s,%s)",
                (r[0], r[1], r[2], r[3], r[4]))
        stats['customers'] = len(rows)

        # Order details
        cols, od_rows = da.adapter_select(source_conn_id,
            'SELECT OrderID, ProductID, UnitPrice, Quantity, Discount FROM [Order Details]')
        od_map: dict[int, list] = {}
        for r in od_rows:
            up = Decimal(str(r[2])) if r[2] else Decimal('0')
            disc = Decimal(str(r[4])) if r[4] else Decimal('0')
            lt = round(up * r[3] * (1 - disc), 2)
            od_map.setdefault(r[0], []).append((r[0], r[1], up, r[3], disc, lt))

        # Orders
        cols, rows = da.adapter_select(source_conn_id,
            'SELECT OrderID, CustomerID, EmployeeID, OrderDate, ShipCountry FROM Orders')
        for r in rows:
            items = od_map.get(r[0], [])
            total = sum(i[5] for i in items)
            session.execute(
                "INSERT INTO orders (order_id, customer_id, employee_id, order_date, "
                "ship_country, total) VALUES (%s,%s,%s,%s,%s,%s)",
                (r[0], r[1], r[2], str(r[3]) if r[3] else None, r[4], Decimal(str(total))))
            for item in items:
                session.execute(
                    "INSERT INTO order_items (order_id, product_id, unit_price, quantity, "
                    "discount, line_total) VALUES (%s,%s,%s,%s,%s,%s)", item)
                session.execute(
                    "INSERT INTO items_by_product (product_id, order_id, quantity, line_total) "
                    "VALUES (%s,%s,%s,%s)",
                    (item[1], item[0], item[3], item[5]))
        stats['orders'] = len(rows)
        stats['order_items'] = sum(len(v) for v in od_map.values())

        return stats, None
    except Exception as e:
        return stats, str(e)


# ── Built-in CQL queries ───────────────────────────────────────────────────────

_BUILTIN = [
    {
        'key': 'all_products',
        'label': 'All products',
        'cql': 'SELECT product_id, product_name, unit_price, units_in_stock FROM northwind.products LIMIT 20',
    },
    {
        'key': 'orders_by_country',
        'label': 'Orders — Germany',
        'cql': "SELECT order_id, customer_id, order_date, total FROM northwind.orders WHERE ship_country='Germany' ALLOW FILTERING",
    },
    {
        'key': 'items_for_order',
        'label': 'Items in order 10248',
        'cql': 'SELECT * FROM northwind.order_items WHERE order_id=10248',
    },
    {
        'key': 'orders_for_product',
        'label': 'Orders containing product 11',
        'cql': 'SELECT * FROM northwind.items_by_product WHERE product_id=11',
    },
]


def builtin_queries() -> list[dict]:
    return _BUILTIN
