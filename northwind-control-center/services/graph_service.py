from db import run_select

GRAPH_QUERIES = {
    'employee_hierarchy': {
        'label': 'Employee Hierarchy (relational)',
        'description': 'Manager → employee reporting structure from Employees.ReportsTo',
        'requires_graph_tables': False,
        'sql': """
            SELECT
                e.EmployeeID,
                e.FirstName + ' ' + e.LastName AS employee,
                e.Title,
                e.ReportsTo AS manager_id,
                ISNULL(m.FirstName + ' ' + m.LastName, '(top)') AS manager,
                ISNULL(m.Title, '') AS manager_title
            FROM Employees e
            LEFT JOIN Employees m ON e.ReportsTo = m.EmployeeID
            ORDER BY e.ReportsTo, e.LastName
        """,
        'cytoscape': {
            'node_id': 'EmployeeID',
            'node_label': 'employee',
            'edge_from': 'manager_id',
            'edge_to': 'EmployeeID',
        },
    },
    'product_cooccurrence': {
        'label': 'Product Co-occurrence (relational)',
        'description': 'Products frequently ordered together in the same order',
        'requires_graph_tables': False,
        'sql': """
            SELECT TOP 40
                p1.ProductName AS product_a,
                p2.ProductName AS product_b,
                COUNT(*) AS times_together
            FROM [Order Details] od1
            JOIN [Order Details] od2 ON od1.OrderID = od2.OrderID
                AND od1.ProductID < od2.ProductID
            JOIN Products p1 ON od1.ProductID = p1.ProductID
            JOIN Products p2 ON od2.ProductID = p2.ProductID
            GROUP BY p1.ProductName, p2.ProductName
            ORDER BY times_together DESC
        """,
    },
    'sales_by_product_year': {
        'label': 'Sales by Product & Year (graph MATCH)',
        'description': 'Revenue per product per year via graph MATCH syntax — requires graph tables',
        'requires_graph_tables': True,
        'sql': """
            SELECT
                p.productname,
                YEAR(o.orderdate) AS sales_year,
                CAST(SUM(e.value) AS DECIMAL(12,2)) AS revenue
            FROM dbo.g_products p, dbo.g_orders o, dbo.g_order_contains e
            WHERE MATCH(o-(e)->p)
            GROUP BY p.productname, YEAR(o.orderdate)
            ORDER BY revenue DESC
        """,
    },
    'customer_product': {
        'label': 'Customer → Product Paths (graph MATCH)',
        'description': 'What each customer ordered, via graph tables — requires graph tables',
        'requires_graph_tables': True,
        'sql': """
            SELECT TOP 50
                c.companyname AS customer,
                p.productname AS product,
                SUM(e.quantity) AS qty_ordered
            FROM dbo.g_customers c,
                 dbo.g_orders o,
                 dbo.g_customer_places cp,
                 dbo.g_order_contains e,
                 dbo.g_products p
            WHERE MATCH(c-(cp)->o-(e)->p)
            GROUP BY c.companyname, p.productname
            ORDER BY qty_ordered DESC
        """,
    },
}


def list_graph_queries():
    return [
        {'key': k, 'label': v['label'], 'description': v['description'],
         'requires_graph_tables': v['requires_graph_tables']}
        for k, v in GRAPH_QUERIES.items()
    ]


def run_graph_query(query_key):
    spec = GRAPH_QUERIES.get(query_key)
    if not spec:
        return None, None, 'Unknown query.'
    try:
        cols, rows = run_select(spec['sql'])
        return cols, rows, None
    except Exception as e:
        msg = str(e)
        if spec['requires_graph_tables']:
            msg += ' — did you run sql/06_graph.sql to create and populate the graph tables?'
        return None, None, msg


def get_cytoscape_data(query_key):
    spec = GRAPH_QUERIES.get(query_key)
    if not spec or 'cytoscape' not in spec:
        return None

    cols, rows, err = run_graph_query(query_key)
    if err or not rows:
        return None

    cy = spec['cytoscape']
    col_idx = {c: i for i, c in enumerate(cols)}
    node_id_col = cy['node_id']
    node_label_col = cy['node_label']
    edge_from_col = cy['edge_from']
    edge_to_col = cy['edge_to']

    seen_nodes = set()
    elements = []

    for row in rows:
        nid = str(row[col_idx[node_id_col]])
        nlabel = str(row[col_idx[node_label_col]])
        if nid not in seen_nodes:
            elements.append({'data': {'id': nid, 'label': nlabel}})
            seen_nodes.add(nid)

        manager_id = row[col_idx[edge_from_col]]
        if manager_id is not None:
            mid = str(manager_id)
            elements.append({
                'data': {
                    'id': f"e-{mid}-{nid}",
                    'source': mid,
                    'target': nid,
                }
            })

    return elements
