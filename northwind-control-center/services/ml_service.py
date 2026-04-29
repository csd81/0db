"""
ML / AI Insights service.

Three features:
  1. Order Value Prediction  — GradientBoostingRegressor trained on historical order items
  2. Inventory Risk Scoring  — rule-based scoring on stock, reorder level, recent velocity
  3. Anomaly Detection       — statistical flagging of unusual discounts, values and freight
"""

import threading
import numpy as np
from db import run_select

try:
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score as sklearn_r2
    _SKLEARN = True
except ImportError:
    _SKLEARN = False

# ── Shared model state (in-memory for demo; replace with pickle for persistence) ──

_lock = threading.Lock()
_state = {
    'model': None,
    'le_country': None,
    'le_category': None,
    'percentiles': None,   # [p33, p67] used for L/M/H classification
    'trained_at': None,
    'n_samples': 0,
    'r2': None,
    'feature_importances': {},
}


# ── Public helpers ─────────────────────────────────────────────────────────────

def sklearn_available():
    return _SKLEARN


def model_status():
    with _lock:
        return {
            'trained': _state['model'] is not None,
            'trained_at': _state['trained_at'],
            'n_samples': _state['n_samples'],
            'r2': _state['r2'],
            'feature_importances': _state['feature_importances'],
        }


def get_form_options():
    """Dropdown options for the prediction form — always read from DB."""
    try:
        _, cat_rows = run_select(
            "SELECT DISTINCT CategoryName FROM Categories ORDER BY CategoryName"
        )
        _, cou_rows = run_select(
            "SELECT DISTINCT Country FROM Customers WHERE Country IS NOT NULL ORDER BY Country"
        )
        return {
            'categories': [r[0] for r in cat_rows],
            'countries': [r[0] for r in cou_rows],
            'years': list(range(1996, 2000)),
        }, None
    except Exception as e:
        return {'categories': [], 'countries': [], 'years': [1996, 1997, 1998]}, str(e)


# ── Feature 1: Order Value Prediction ─────────────────────────────────────────

_FEATURE_NAMES = ['CategoryID', 'Country (encoded)', 'UnitPrice', 'Discount', 'Year']


def train_model():
    if not _SKLEARN:
        return False, 'scikit-learn is not installed. Run: pip install scikit-learn'

    from datetime import datetime

    try:
        _, rows = run_select(
            """
            SELECT
                c.CategoryID,
                c.CategoryName,
                cu.Country,
                CAST(od.UnitPrice AS FLOAT),
                CAST(od.Discount  AS FLOAT),
                YEAR(o.OrderDate) AS order_year,
                CAST(od.UnitPrice * od.Quantity * (1.0 - od.Discount) AS FLOAT) AS item_value
            FROM [Order Details] od
            JOIN Orders     o  ON od.OrderID  = o.OrderID
            JOIN Products   p  ON od.ProductID = p.ProductID
            JOIN Categories c  ON p.CategoryID = c.CategoryID
            JOIN Customers  cu ON o.CustomerID = cu.CustomerID
            WHERE o.OrderDate IS NOT NULL
            """
        )
    except Exception as e:
        return False, f'Database error: {e}'

    if len(rows) < 20:
        return False, 'Not enough training data (need at least 20 rows).'

    le_cat = LabelEncoder().fit([r[1] for r in rows])
    le_cou = LabelEncoder().fit([r[2] for r in rows])

    X = np.array([
        [
            float(r[0]),                        # CategoryID
            float(le_cou.transform([r[2]])[0]), # Country encoded
            r[3],                               # UnitPrice
            r[4],                               # Discount
            float(r[5]),                        # Year
        ]
        for r in rows
    ])
    y = np.array([r[6] for r in rows])

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(
        n_estimators=150, max_depth=4, learning_rate=0.1, random_state=42
    )
    model.fit(X_tr, y_tr)

    r2 = round(float(sklearn_r2(y_te, model.predict(X_te))), 3)
    importances = {
        name: round(float(imp), 3)
        for name, imp in zip(_FEATURE_NAMES, model.feature_importances_)
    }

    p33 = float(np.percentile(y, 33))
    p67 = float(np.percentile(y, 67))

    with _lock:
        _state['model'] = model
        _state['le_country'] = le_cou
        _state['le_category'] = le_cat
        _state['percentiles'] = [p33, p67]
        _state['trained_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        _state['n_samples'] = len(rows)
        _state['r2'] = r2
        _state['feature_importances'] = importances

    return True, None


def predict_order_value(category_name, country, unit_price, discount, year):
    with _lock:
        model = _state['model']
        le_cou = _state['le_country']
        le_cat = _state['le_category']
        p33, p67 = _state['percentiles'] or [0, 0]

    if model is None:
        return None, 'Model not trained yet. Click "Train Model" first.'

    # Graceful fallback for unseen labels
    if country not in le_cou.classes_:
        fallback_country = le_cou.classes_[0]
    else:
        fallback_country = country

    cat_encoded = (
        float(list(le_cat.classes_).index(category_name))
        if category_name in le_cat.classes_
        else 0.0
    )

    X = np.array([[
        cat_encoded,
        float(le_cou.transform([fallback_country])[0]),
        float(unit_price),
        float(discount),
        float(year),
    ]])

    pred = max(0.0, float(model.predict(X)[0]))

    if pred < p33:
        cls, cls_color = 'L', 'success'
        cls_label = 'Low value'
    elif pred < p67:
        cls, cls_color = 'M', 'warning'
        cls_label = 'Medium value'
    else:
        cls, cls_color = 'H', 'danger'
        cls_label = 'High value'

    return {
        'predicted_value': round(pred, 2),
        'value_class': cls,
        'class_color': cls_color,
        'class_label': cls_label,
        'thresholds': {'p33': round(p33, 2), 'p67': round(p67, 2)},
        'country_warning': country not in le_cou.classes_,
    }, None


# ── Feature 2: Inventory Risk Scoring ─────────────────────────────────────────

def get_inventory_risk():
    try:
        _, rows = run_select(
            """
            SELECT
                p.ProductID,
                p.ProductName,
                c.CategoryName,
                ISNULL(p.UnitsInStock, 0),
                ISNULL(p.ReorderLevel, 0),
                ISNULL(p.UnitsOnOrder, 0),
                ISNULL((
                    SELECT SUM(od.Quantity)
                    FROM [Order Details] od
                    JOIN Orders o ON od.OrderID = o.OrderID
                    WHERE od.ProductID = p.ProductID
                      AND o.OrderDate >= DATEADD(day, -30,
                          (SELECT MAX(OrderDate) FROM Orders))
                ), 0),
                ISNULL((
                    SELECT SUM(od.Quantity)
                    FROM [Order Details] od
                    JOIN Orders o ON od.OrderID = o.OrderID
                    WHERE od.ProductID = p.ProductID
                      AND o.OrderDate >= DATEADD(day, -90,
                          (SELECT MAX(OrderDate) FROM Orders))
                ), 0)
            FROM Products p
            JOIN Categories c ON p.CategoryID = c.CategoryID
            WHERE p.Discontinued = 0
            ORDER BY p.UnitsInStock
            """
        )
    except Exception as e:
        return [], str(e)

    result = []
    for row in rows:
        pid, pname, cat, stock, reorder, on_order, s30, s90 = (
            row[0], row[1], row[2], int(row[3]), int(row[4]),
            int(row[5]), int(row[6]), int(row[7])
        )

        stock_ratio = max(0.0, (reorder - stock) / max(reorder, 1))
        velocity = s30 / max(stock + on_order, 1)
        velocity = min(velocity, 1.0)
        score = round(0.6 * stock_ratio + 0.4 * velocity, 3)

        if score < 0.25:
            label, color = 'Low', 'success'
        elif score < 0.55:
            label, color = 'Medium', 'warning'
        else:
            label, color = 'High', 'danger'

        result.append({
            'product_id': pid,
            'product_name': pname,
            'category': cat,
            'stock': stock,
            'reorder_level': reorder,
            'on_order': on_order,
            'sales_30d': s30,
            'sales_90d': s90,
            'risk_score': score,
            'risk_label': label,
            'risk_color': color,
            'score_pct': int(score * 100),
        })

    result.sort(key=lambda x: x['risk_score'], reverse=True)
    return result, None


def risk_summary(items):
    counts = {'High': 0, 'Medium': 0, 'Low': 0}
    for item in items:
        counts[item['risk_label']] = counts.get(item['risk_label'], 0) + 1
    return counts


# ── Feature 3: Anomaly Detection ──────────────────────────────────────────────

def get_anomalies():
    try:
        _, rows = run_select(
            """
            SELECT
                od.OrderID,
                o.OrderDate,
                p.ProductName,
                c.CategoryName,
                cu.Country,
                CAST(od.UnitPrice  AS FLOAT),
                od.Quantity,
                CAST(od.Discount   AS FLOAT),
                CAST(od.UnitPrice * od.Quantity * (1.0 - od.Discount) AS FLOAT),
                CAST(ISNULL(o.Freight, 0) AS FLOAT)
            FROM [Order Details] od
            JOIN Orders     o  ON od.OrderID  = o.OrderID
            JOIN Products   p  ON od.ProductID = p.ProductID
            JOIN Categories c  ON p.CategoryID = c.CategoryID
            JOIN Customers  cu ON o.CustomerID = cu.CustomerID
            WHERE o.OrderDate IS NOT NULL
            """
        )
    except Exception as e:
        return [], str(e)

    if not rows:
        return [], None

    values    = np.array([r[8] for r in rows], dtype=float)
    discounts = np.array([r[7] for r in rows], dtype=float)
    freights  = np.array([r[9] for r in rows], dtype=float)

    p95_val  = float(np.percentile(values,    95))
    p95_frgt = float(np.percentile(freights,  95))
    d_mean   = float(np.mean(discounts))
    d_std    = float(np.std(discounts))
    discount_threshold = d_mean + 2 * d_std

    SEVERITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}

    anomalies = []
    seen_orders = {}  # deduplicate freight flag per order

    for i, row in enumerate(rows):
        v, d, f = values[i], discounts[i], freights[i]
        reasons = []
        severity = 'low'

        if v > p95_val:
            reasons.append(f'High item value (€{v:,.0f} > p95 €{p95_val:,.0f})')
            severity = 'high'

        if d > 0 and d_std > 0 and d > discount_threshold:
            reasons.append(f'Unusual discount ({d*100:.0f}% vs avg {d_mean*100:.0f}%+2σ)')
            severity = 'high' if severity == 'high' else 'medium'

        order_id = row[0]
        if f > p95_frgt and order_id not in seen_orders:
            reasons.append(f'High freight (€{f:,.0f} > p95 €{p95_frgt:,.0f})')
            seen_orders[order_id] = True
            if severity == 'low':
                severity = 'medium'

        if reasons:
            anomalies.append({
                'order_id': order_id,
                'order_date': str(row[1])[:10] if row[1] else '',
                'product': row[2],
                'category': row[3],
                'country': row[4],
                'unit_price': row[5],
                'quantity': int(row[6]),
                'discount_pct': round(d * 100, 1),
                'item_value': round(v, 2),
                'freight': round(f, 2),
                'reasons': reasons,
                'severity': severity,
                'severity_color': {'high': 'danger', 'medium': 'warning', 'low': 'info'}[severity],
            })

    anomalies.sort(key=lambda x: (SEVERITY_ORDER.get(x['severity'], 3), -x['item_value']))
    return anomalies[:150], None


def anomaly_summary(items):
    counts = {'high': 0, 'medium': 0, 'low': 0}
    for item in items:
        counts[item['severity']] = counts.get(item['severity'], 0) + 1
    return counts
