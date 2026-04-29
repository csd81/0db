from db import run_select


def _safe(sql, params=None):
    try:
        _, rows = run_select(sql, params)
        return rows, None
    except Exception as e:
        return [], str(e)


def get_sales_by_month():
    rows, err = _safe(
        """
        SELECT
            YEAR(o.OrderDate) AS yr,
            MONTH(o.OrderDate) AS mo,
            CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
        FROM Orders o
        JOIN [Order Details] od ON o.OrderID = od.OrderID
        WHERE o.OrderDate IS NOT NULL
        GROUP BY YEAR(o.OrderDate), MONTH(o.OrderDate)
        ORDER BY yr, mo
        """
    )
    labels = [f"{r[0]}-{r[1]:02d}" for r in rows]
    values = [float(r[2]) for r in rows]
    return {'labels': labels, 'values': values, 'error': err}


def get_sales_by_category():
    rows, err = _safe(
        """
        SELECT
            c.CategoryName,
            CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
        FROM Categories c
        JOIN Products p ON c.CategoryID = p.CategoryID
        JOIN [Order Details] od ON p.ProductID = od.ProductID
        GROUP BY c.CategoryName
        ORDER BY revenue DESC
        """
    )
    labels = [r[0] for r in rows]
    values = [float(r[1]) for r in rows]
    return {'labels': labels, 'values': values, 'error': err}


def get_top_products(n=10):
    rows, err = _safe(
        f"""
        SELECT TOP {n}
            p.ProductName,
            SUM(od.Quantity) AS units_sold,
            CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
        FROM Products p
        JOIN [Order Details] od ON p.ProductID = od.ProductID
        GROUP BY p.ProductName
        ORDER BY revenue DESC
        """
    )
    labels = [r[0] for r in rows]
    units = [int(r[1]) for r in rows]
    revenue = [float(r[2]) for r in rows]
    return {'labels': labels, 'units': units, 'revenue': revenue, 'error': err}


def get_orders_by_country():
    rows, err = _safe(
        """
        SELECT
            c.Country,
            COUNT(DISTINCT o.OrderID) AS order_count,
            CAST(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS DECIMAL(12,2)) AS revenue
        FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID
        JOIN [Order Details] od ON o.OrderID = od.OrderID
        WHERE c.Country IS NOT NULL
        GROUP BY c.Country
        ORDER BY order_count DESC
        """
    )
    labels = [r[0] for r in rows]
    counts = [int(r[1]) for r in rows]
    revenue = [float(r[2]) for r in rows]
    return {'labels': labels, 'counts': counts, 'revenue': revenue, 'error': err}


def get_ship_status():
    rows, err = _safe(
        """
        SELECT
            CASE WHEN ShippedDate IS NOT NULL THEN 'Shipped' ELSE 'Pending' END AS status,
            COUNT(*) AS cnt
        FROM Orders
        GROUP BY CASE WHEN ShippedDate IS NOT NULL THEN 'Shipped' ELSE 'Pending' END
        """
    )
    labels = [r[0] for r in rows]
    values = [int(r[1]) for r in rows]
    return {'labels': labels, 'values': values, 'error': err}
