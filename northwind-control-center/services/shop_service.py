"""
shop_service.py — Northwind Global Webshop (hybrid simulation).

Real:       SQL Server — ACID orders, inventory, catalog, analytics
Simulated:  Redis-style cart      → Python dict + threading.Lock
Simulated:  Elasticsearch search  → difflib fuzzy match on in-memory index
Real:       Graph routing         → get_instant_route() from graph_routing_service
"""

import threading
import uuid
from difflib import get_close_matches

import pyodbc


# ─────────────────────────────────────────────────────────────────────────────
# Simulated Redis cart  (in-memory dict, thread-safe)
# Mirrors: SET shop:cart:{sid} → GETEX with TTL
# ─────────────────────────────────────────────────────────────────────────────

_cart_lock: threading.Lock   = threading.Lock()
_CARTS:     dict[str, dict]  = {}   # session_id → {str(pid): {name,qty,unit_price}}


def get_cart(session_id: str) -> dict:
    with _cart_lock:
        return dict(_CARTS.get(session_id, {}))


def add_to_cart(session_id: str, product_id: int, name: str,
                qty: int, unit_price: float):
    pid = str(product_id)
    with _cart_lock:
        cart = _CARTS.setdefault(session_id, {})
        if pid in cart:
            cart[pid]['qty'] += qty
        else:
            cart[pid] = {'name': name, 'qty': qty, 'unit_price': unit_price}


def remove_from_cart(session_id: str, product_id: int):
    pid = str(product_id)
    with _cart_lock:
        _CARTS.get(session_id, {}).pop(pid, None)


def clear_cart(session_id: str):
    with _cart_lock:
        _CARTS.pop(session_id, None)


# ─────────────────────────────────────────────────────────────────────────────
# Simulated Elasticsearch search  (difflib fuzzy on SQL-loaded product index)
# Mirrors: GET northwind_products/_search?q=... fuzziness=AUTO
# ─────────────────────────────────────────────────────────────────────────────

_index_lock:    threading.Lock = threading.Lock()
_PRODUCT_INDEX: list[dict]     = []   # loaded once from SQL, then held in memory


def _ensure_product_index(conn_str: str) -> list:
    global _PRODUCT_INDEX
    with _index_lock:
        if _PRODUCT_INDEX:
            return _PRODUCT_INDEX
        try:
            with pyodbc.connect(conn_str, timeout=5) as c:
                cur = c.cursor()
                cur.execute("""
                    SELECT p.ProductID, p.ProductName, p.UnitPrice,
                           p.UnitsInStock, p.ReorderLevel, p.QuantityPerUnit,
                           c.CategoryName, s.CompanyName AS Supplier, p.CategoryID
                    FROM Products p
                    JOIN Categories c ON p.CategoryID = c.CategoryID
                    JOIN Suppliers  s ON p.SupplierID = s.SupplierID
                    WHERE p.Discontinued = 0
                    ORDER BY p.ProductName
                """)
                cols           = [d[0] for d in cur.description]
                _PRODUCT_INDEX = []
                for row in cur.fetchall():
                    p = dict(zip(cols, row))
                    p['UnitPrice']    = float(p['UnitPrice'] or 0)
                    p['UnitsInStock'] = int(p['UnitsInStock'] or 0)
                    p['ReorderLevel'] = int(p['ReorderLevel'] or 0)
                    _PRODUCT_INDEX.append(p)
        except Exception:
            _PRODUCT_INDEX = []
    return _PRODUCT_INDEX


def search_products(query: str, conn_str: str = '') -> list:
    """
    Python difflib fuzzy search — simulates Elasticsearch multi_match fuzziness=AUTO.
    Substring match first (fast path); difflib SequenceMatcher as fallback.
    """
    if not query:
        return []
    products = _ensure_product_index(conn_str)
    q        = query.lower()

    # Fast path: substring match
    hits = [p for p in products if q in p['ProductName'].lower()
                                or q in p['CategoryName'].lower()
                                or q in p['Supplier'].lower()]
    if hits:
        return hits[:20]

    # Fuzzy fallback via difflib (typo tolerance)
    names   = [p['ProductName'] for p in products]
    matches = set(get_close_matches(query, names, n=10, cutoff=0.55))
    return [p for p in products if p['ProductName'] in matches]


def invalidate_product_index():
    """Call after stock mutations to force index reload on next search."""
    global _PRODUCT_INDEX
    with _index_lock:
        _PRODUCT_INDEX = []


# ─────────────────────────────────────────────────────────────────────────────
# SQL Server catalog  (read-only pyodbc queries)
# ─────────────────────────────────────────────────────────────────────────────

def _conn(conn_str: str):
    return pyodbc.connect(conn_str, timeout=5)


def get_categories(conn_str: str) -> list:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute(
                "SELECT CategoryID, CategoryName, Description "
                "FROM Categories ORDER BY CategoryName"
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception:
        return []


def get_catalog(conn_str: str, category_id=None,
                page: int = 1, per_page: int = 24) -> dict:
    try:
        with _conn(conn_str) as c:
            cur    = c.cursor()
            where  = "WHERE p.Discontinued=0"
            params = []
            if category_id:
                where += " AND p.CategoryID=?"
                params.append(int(category_id))
            cur.execute(f"SELECT COUNT(*) FROM Products p {where}", *params)
            total  = cur.fetchone()[0]
            offset = (page - 1) * per_page
            cur.execute(f"""
                SELECT p.ProductID, p.ProductName, p.UnitPrice, p.UnitsInStock,
                       p.ReorderLevel, c.CategoryName, s.CompanyName AS Supplier,
                       p.QuantityPerUnit, p.CategoryID
                FROM Products p
                JOIN Categories c ON p.CategoryID = c.CategoryID
                JOIN Suppliers  s ON p.SupplierID = s.SupplierID
                {where}
                ORDER BY p.ProductName
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
            """, *params, offset, per_page)
            cols     = [d[0] for d in cur.description]
            products = []
            for row in cur.fetchall():
                p = dict(zip(cols, row))
                p['UnitPrice']    = float(p['UnitPrice'] or 0)
                p['UnitsInStock'] = int(p['UnitsInStock'] or 0)
                p['ReorderLevel'] = int(p['ReorderLevel'] or 0)
                products.append(p)
        return {
            'products': products,
            'total':    total,
            'page':     page,
            'pages':    max(1, -(-total // per_page)),
        }
    except Exception as e:
        return {'products': [], 'total': 0, 'page': 1, 'pages': 1, 'error': str(e)}


def get_product(conn_str: str, product_id: int) -> dict | None:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT p.ProductID, p.ProductName, p.UnitPrice, p.UnitsInStock,
                       p.ReorderLevel, p.QuantityPerUnit, p.Discontinued,
                       c.CategoryName, s.CompanyName AS Supplier,
                       s.Country AS SupplierCountry
                FROM Products p
                JOIN Categories c ON p.CategoryID = c.CategoryID
                JOIN Suppliers  s ON p.SupplierID = s.SupplierID
                WHERE p.ProductID = ?
            """, product_id)
            row = cur.fetchone()
            if not row:
                return None
            cols    = [d[0] for d in cur.description]
            product = dict(zip(cols, row))
            product['UnitPrice']    = float(product['UnitPrice'] or 0)
            product['UnitsInStock'] = int(product['UnitsInStock'] or 0)
            product['ReorderLevel'] = int(product['ReorderLevel'] or 0)

            # Co-purchase: top 5 products ordered together via self-join
            cur.execute("""
                SELECT TOP 5
                       p2.ProductID, p2.ProductName, p2.UnitPrice,
                       COUNT(*) AS CoCount
                FROM [Order Details] od1
                JOIN [Order Details] od2 ON od1.OrderID = od2.OrderID
                                         AND od2.ProductID <> od1.ProductID
                JOIN Products p2 ON od2.ProductID = p2.ProductID
                WHERE od1.ProductID = ? AND p2.Discontinued = 0
                GROUP BY p2.ProductID, p2.ProductName, p2.UnitPrice
                ORDER BY CoCount DESC
            """, product_id)
            cols2 = [d[0] for d in cur.description]
            product['co_purchase'] = []
            for r in cur.fetchall():
                cp = dict(zip(cols2, r))
                cp['UnitPrice'] = float(cp['UnitPrice'] or 0)
                product['co_purchase'].append(cp)

            # Monthly order volume last 12 months — GROUP BY YEAR/MONTH
            cur.execute("""
                SELECT YEAR(o.OrderDate) AS yr, MONTH(o.OrderDate) AS mo,
                       SUM(od.Quantity)  AS qty
                FROM [Order Details] od
                JOIN Orders o ON o.OrderID = od.OrderID
                WHERE od.ProductID = ?
                  AND o.OrderDate >= DATEADD(MONTH, -12, GETDATE())
                GROUP BY YEAR(o.OrderDate), MONTH(o.OrderDate)
                ORDER BY yr, mo
            """, product_id)
            product['monthly'] = [
                {'yr': r[0], 'mo': r[1], 'qty': int(r[2])}
                for r in cur.fetchall()
            ]
        return product
    except Exception:
        return None


def get_customers_list(conn_str: str) -> list:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute(
                "SELECT CustomerID, CompanyName, Country "
                "FROM Customers ORDER BY CompanyName"
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception:
        return []


def get_customer(conn_str: str, customer_id: str) -> dict | None:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT CustomerID, CompanyName, ContactName, City, Country, Phone
                FROM Customers WHERE CustomerID = ?
            """, customer_id)
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
    except Exception:
        return None


def get_order_history(conn_str: str, customer_id: str) -> list:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            # ROW_NUMBER() window function for order rank display
            cur.execute("""
                SELECT o.OrderID,
                       o.OrderDate,
                       o.ShippedDate,
                       SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS Total,
                       COUNT(od.ProductID)                                  AS Lines,
                       ROW_NUMBER() OVER (ORDER BY o.OrderDate DESC)        AS rn,
                       CASE WHEN o.ShippedDate IS NULL
                            THEN 'Pending' ELSE 'Shipped' END               AS Status
                FROM Orders o
                JOIN [Order Details] od ON o.OrderID = od.OrderID
                WHERE o.CustomerID = ?
                GROUP BY o.OrderID, o.OrderDate, o.ShippedDate
                ORDER BY o.OrderDate DESC
            """, customer_id)
            cols   = [d[0] for d in cur.description]
            orders = []
            for row in cur.fetchall():
                d = dict(zip(cols, row))
                d['Total']  = round(float(d['Total'] or 0), 2)
                d['Lines']  = int(d['Lines'] or 0)
                d['rn']     = int(d['rn'])
                if d['OrderDate']:
                    d['OrderDate']   = str(d['OrderDate'])[:10]
                if d['ShippedDate']:
                    d['ShippedDate'] = str(d['ShippedDate'])[:10]
                orders.append(d)
        return orders
    except Exception:
        return []


def get_monthly_revenue(conn_str: str, customer_id: str) -> list:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT YEAR(o.OrderDate)  AS yr,
                       MONTH(o.OrderDate) AS mo,
                       SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
                FROM Orders o
                JOIN [Order Details] od ON o.OrderID = od.OrderID
                WHERE o.CustomerID = ?
                  AND o.OrderDate >= DATEADD(MONTH, -12, GETDATE())
                GROUP BY YEAR(o.OrderDate), MONTH(o.OrderDate)
                ORDER BY yr, mo
            """, customer_id)
            return [
                {'yr': r[0], 'mo': r[1], 'revenue': round(float(r[2]), 2)}
                for r in cur.fetchall()
            ]
    except Exception:
        return []


def get_category_spend(conn_str: str, customer_id: str) -> list:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT c.CategoryName,
                       SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS spend
                FROM Orders o
                JOIN [Order Details] od ON o.OrderID = od.OrderID
                JOIN Products p         ON od.ProductID = p.ProductID
                JOIN Categories c       ON p.CategoryID = c.CategoryID
                WHERE o.CustomerID = ?
                GROUP BY c.CategoryName
                ORDER BY spend DESC
            """, customer_id)
            return [
                {'category': r[0], 'spend': round(float(r[1]), 2)}
                for r in cur.fetchall()
            ]
    except Exception:
        return []


def get_reorder_suggestions(conn_str: str, customer_id: str) -> list:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT DISTINCT p.ProductID, p.ProductName, p.UnitPrice,
                                p.UnitsInStock, p.ReorderLevel
                FROM Orders o
                JOIN [Order Details] od ON o.OrderID = od.OrderID
                JOIN Products p         ON od.ProductID = p.ProductID
                WHERE o.CustomerID = ?
                  AND p.UnitsInStock <= p.ReorderLevel
                  AND p.Discontinued = 0
                ORDER BY p.ProductName
            """, customer_id)
            cols = [d[0] for d in cur.description]
            rows = []
            for row in cur.fetchall():
                d = dict(zip(cols, row))
                d['UnitPrice']    = float(d['UnitPrice'] or 0)
                d['UnitsInStock'] = int(d['UnitsInStock'] or 0)
                d['ReorderLevel'] = int(d['ReorderLevel'] or 0)
                rows.append(d)
        return rows
    except Exception:
        return []


def get_order_detail(conn_str: str, order_id: int) -> dict | None:
    try:
        with _conn(conn_str) as c:
            cur = c.cursor()
            cur.execute("""
                SELECT o.OrderID, o.OrderDate, o.ShippedDate,
                       o.ShipCity, o.ShipCountry, o.Freight,
                       cust.CompanyName AS Customer,
                       s.CompanyName    AS Shipper
                FROM Orders o
                JOIN Customers cust ON o.CustomerID = cust.CustomerID
                LEFT JOIN Shippers s ON o.ShipVia = s.ShipperID
                WHERE o.OrderID = ?
            """, order_id)
            row = cur.fetchone()
            if not row:
                return None
            cols  = [d[0] for d in cur.description]
            order = dict(zip(cols, row))
            if order['OrderDate']:
                order['OrderDate']   = str(order['OrderDate'])[:10]
            if order['ShippedDate']:
                order['ShippedDate'] = str(order['ShippedDate'])[:10]
            order['Freight'] = float(order['Freight'] or 0)

            cur.execute("""
                SELECT p.ProductName, od.Quantity, od.UnitPrice, od.Discount,
                       od.UnitPrice * od.Quantity * (1 - od.Discount) AS LineTotal
                FROM [Order Details] od
                JOIN Products p ON od.ProductID = p.ProductID
                WHERE od.OrderID = ?
                ORDER BY p.ProductName
            """, order_id)
            cols2 = [d[0] for d in cur.description]
            lines = []
            for r in cur.fetchall():
                d = dict(zip(cols2, r))
                d['UnitPrice'] = float(d['UnitPrice'] or 0)
                d['Discount']  = float(d['Discount'] or 0)
                d['LineTotal'] = float(d['LineTotal'] or 0)
                lines.append(d)
            order['lines']    = lines
            order['subtotal'] = round(sum(l['LineTotal'] for l in lines), 2)
        return order
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Async order processor  (daemon thread — same pattern as mapreduce_service.py)
# ─────────────────────────────────────────────────────────────────────────────

_order_lock: threading.Lock  = threading.Lock()
_ORDERS:     dict[str, dict] = {}   # job_id → state


def place_order(conn_str: str, session_id: str,
                customer_id: str, ship_city: str) -> str:
    """Return job_id immediately (202 Accepted). Daemon thread handles T-SQL."""
    cart   = get_cart(session_id)
    job_id = str(uuid.uuid4())[:8]
    items  = [{'product_id': int(k), **v} for k, v in cart.items()]
    state  = {
        'status':      'RECEIVED',
        'step':        '',
        'order_id':    None,
        'customer_id': customer_id,
        'items':       items,
        'ship_city':   ship_city,
        'subtotal':    0.0,
        'freight':     0.0,
        'error':       None,
        'error_code':  None,
        'logistics':   None,
    }
    with _order_lock:
        _ORDERS[job_id] = state
    # Pass snapshots — thread never reads back from _ORDERS for business data
    threading.Thread(
        target=_process_order,
        args=(job_id, conn_str, session_id, list(items), ship_city, customer_id),
        daemon=True,
    ).start()
    return job_id


def _set_step(job_id: str, status: str, step: str = ''):
    with _order_lock:
        _ORDERS[job_id]['status'] = status
        _ORDERS[job_id]['step']   = step


def _process_order(job_id: str, conn_str: str, session_id: str,
                   items: list, ship_city: str, customer_id: str):
    conn = None
    try:
        _set_step(job_id, 'PROCESSING', 'VALIDATING_STOCK')
        conn = pyodbc.connect(conn_str, timeout=10)
        conn.autocommit = False
        cur = conn.cursor()

        # Step 1: Lock stock rows, check availability
        for item in items:
            pid = item['product_id']
            cur.execute(
                "SELECT UnitsInStock "
                "FROM Products WITH (UPDLOCK, ROWLOCK) "
                "WHERE ProductID = ?",
                pid,
            )
            row = cur.fetchone()
            if row is None or int(row[0] or 0) < item['qty']:
                conn.rollback()
                with _order_lock:
                    _ORDERS[job_id].update({
                        'status':     'FAILED',
                        'error':      f'Insufficient stock for product {pid}',
                        'error_code': 'INSUFFICIENT_STOCK',
                    })
                return

        _set_step(job_id, 'PROCESSING', 'INSERTING_ORDER')

        # Step 2: Insert order header — OUTPUT INSERTED.OrderID
        subtotal = sum(i['unit_price'] * i['qty'] for i in items)
        freight  = round(subtotal * 0.05, 2)
        cur.execute("""
            INSERT INTO Orders
                (CustomerID, EmployeeID, OrderDate, RequiredDate, ShipCity, Freight)
            OUTPUT INSERTED.OrderID
            VALUES (?, 1, GETDATE(), DATEADD(DAY, 7, GETDATE()), ?, ?)
        """, customer_id, ship_city, freight)
        order_id = cur.fetchone()[0]

        # Step 3: Insert order lines + deduct stock
        for item in items:
            cur.execute("""
                INSERT INTO [Order Details]
                    (OrderID, ProductID, UnitPrice, Quantity, Discount)
                VALUES (?, ?, ?, ?, 0)
            """, order_id, item['product_id'], item['unit_price'], item['qty'])
            cur.execute(
                "UPDATE Products SET UnitsInStock = UnitsInStock - ? "
                "WHERE ProductID = ?",
                item['qty'], item['product_id'],
            )

        conn.commit()

        with _order_lock:
            _ORDERS[job_id].update({
                'subtotal': round(subtotal, 2),
                'freight':  freight,
                'order_id': order_id,
            })

        _set_step(job_id, 'PROCESSING', 'CALCULATING_ROUTE')

        # Step 4: Graph A* London → ship_city
        from services.graph_routing_service import get_instant_route
        logistics = get_instant_route(conn_str, 'London', ship_city)

        with _order_lock:
            _ORDERS[job_id].update({
                'logistics': logistics,
                'status':    'CONFIRMED',
                'step':      '',
            })

        clear_cart(session_id)
        invalidate_product_index()   # stock changed — refresh search index

    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        with _order_lock:
            _ORDERS[job_id].update({
                'status':     'FAILED',
                'error':      str(e),
                'error_code': 'SERVER_ERROR',
            })
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


def get_order_status(job_id: str) -> dict | None:
    with _order_lock:
        state = _ORDERS.get(job_id)
        return dict(state) if state else None
