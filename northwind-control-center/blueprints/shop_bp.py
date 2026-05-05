"""
shop_bp.py — Northwind Global Webshop routes.
Polyglot: Redis cart · ES search · SQL ACID orders · Graph routing
"""

import os
import uuid

from flask import (Blueprint, abort, current_app, jsonify, redirect,
                   render_template, request, session, url_for)

from auth import login_required
from services import shop_service as ss
from services import stock_agent_service as sas

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_conn_str() -> str:
    c    = current_app.config
    user = (c.get('SQL_SA_USERNAME')
            or os.environ.get('SQL_SA_USERNAME')
            or c.get('SQL_USERNAME', ''))
    pw   = (c.get('SQL_SA_PASSWORD')
            or os.environ.get('SQL_SA_PASSWORD')
            or c.get('SQL_PASSWORD', ''))
    db   = os.environ.get('SQL_DATABASE') or c.get('SQL_DATABASE', 'Northwind')
    return (
        f"DRIVER={{{c['SQL_DRIVER']}}};SERVER={c['SQL_SERVER']};"
        f"DATABASE={db};UID={user};PWD={pw};"
        f"Encrypt={c['SQL_ENCRYPT']};TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )


def _session_id() -> str:
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())[:12]
    return session['sid']


def _cart_count() -> int:
    cart = ss.get_cart(_session_id())
    return sum(v['qty'] for v in cart.values())


# ── Catalog ───────────────────────────────────────────────────────────────────

@shop_bp.route('/')
@login_required
def catalog():
    conn_str   = _build_conn_str()
    categories = ss.get_categories(conn_str)
    cat_id     = request.args.get('category', type=int)
    page       = request.args.get('page', 1, type=int)
    result     = ss.get_catalog(conn_str, category_id=cat_id, page=page)
    return render_template(
        'shop/catalog.html',
        categories=categories,
        products=result['products'],
        total=result['total'],
        page=result['page'],
        pages=result['pages'],
        active_cat=cat_id,
        search_query=None,
        cart_count=_cart_count(),
    )


@shop_bp.route('/categories.json')
@login_required
def categories_json():
    return jsonify(ss.get_categories(_build_conn_str()))


@shop_bp.route('/catalog.json')
@login_required
def catalog_json():
    cat_id = request.args.get('category', type=int)
    page   = request.args.get('page', 1, type=int)
    return jsonify(ss.get_catalog(_build_conn_str(), category_id=cat_id, page=page))


@shop_bp.route('/search')
@login_required
def search():
    q       = request.args.get('q', '').strip()
    results = ss.search_products(q, conn_str=_build_conn_str()) if q else []
    # Normalise ES results to same field names as catalog
    for p in results:
        for field in ('UnitPrice', 'unit_price'):
            if field in p:
                try:
                    p['UnitPrice'] = float(p[field])
                except Exception:
                    p['UnitPrice'] = 0.0
        for field in ('UnitsInStock', 'units_in_stock'):
            if field in p:
                try:
                    p['UnitsInStock'] = int(p[field])
                except Exception:
                    p['UnitsInStock'] = 0
        if 'ReorderLevel' not in p:
            p['ReorderLevel'] = 0
        if 'ProductID' not in p and 'product_id' in p:
            p['ProductID'] = p['product_id']
        if 'ProductName' not in p and 'product_name' in p:
            p['ProductName'] = p['product_name']
    return render_template(
        'shop/catalog.html',
        categories=[],
        products=results,
        total=len(results),
        page=1, pages=1,
        active_cat=None,
        search_query=q,
        cart_count=_cart_count(),
    )


@shop_bp.route('/product/<int:pid>')
@login_required
def product_detail(pid):
    conn_str = _build_conn_str()
    product  = ss.get_product(conn_str, pid)
    if not product:
        abort(404)
    return render_template('shop/product.html',
                           product=product, cart_count=_cart_count())


# ── Cart ──────────────────────────────────────────────────────────────────────

@shop_bp.route('/cart')
@login_required
def cart_view():
    sid      = _session_id()
    cart     = ss.get_cart(sid)
    subtotal = round(sum(v['unit_price'] * v['qty'] for v in cart.values()), 2)
    freight  = round(subtotal * 0.05, 2)
    return render_template('shop/cart.html',
                           cart=cart,
                           subtotal=subtotal,
                           freight=freight,
                           total=round(subtotal + freight, 2),
                           cart_count=sum(v['qty'] for v in cart.values()))


@shop_bp.route('/cart/add', methods=['POST'])
@login_required
def cart_add():
    data       = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    name       = str(data.get('name', ''))
    qty        = int(data.get('qty', 1))
    unit_price = float(data.get('unit_price', 0))
    sid        = _session_id()
    ss.add_to_cart(sid, product_id, name, qty, unit_price)
    return jsonify({'ok': True, 'cart_count': _cart_count()})


@shop_bp.route('/cart/remove', methods=['POST'])
@login_required
def cart_remove():
    data       = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    ss.remove_from_cart(_session_id(), product_id)
    return jsonify({'ok': True, 'cart_count': _cart_count()})


@shop_bp.route('/cart/clear', methods=['POST'])
@login_required
def cart_clear():
    ss.clear_cart(_session_id())
    return jsonify({'ok': True, 'cart_count': 0})


# ── Checkout ──────────────────────────────────────────────────────────────────

@shop_bp.route('/checkout')
@login_required
def checkout():
    sid  = _session_id()
    cart = ss.get_cart(sid)
    if not cart:
        return redirect(url_for('shop.cart_view'))
    subtotal = round(sum(v['unit_price'] * v['qty'] for v in cart.values()), 2)
    freight  = round(subtotal * 0.05, 2)
    return render_template(
        'shop/checkout.html',
        cart=cart,
        subtotal=subtotal,
        freight=freight,
        total=round(subtotal + freight, 2),
        cart_count=sum(v['qty'] for v in cart.values()),
        customer_id=session.get('checkout_customer', ''),
        ship_city=session.get('checkout_ship_city', ''),
    )


@shop_bp.route('/checkout/submit', methods=['POST'])
@login_required
def checkout_submit():
    data        = request.get_json() or {}
    customer_id = data.get('customer_id', '').strip().upper()
    ship_city   = data.get('ship_city', '').strip()
    if not customer_id or not ship_city:
        return jsonify({'error': 'Missing customer_id or ship_city'}), 400
    sid  = _session_id()
    cart = ss.get_cart(sid)
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400
    session['checkout_customer']  = customer_id
    session['checkout_ship_city'] = ship_city
    job_id = ss.place_order(_build_conn_str(), sid, customer_id, ship_city)
    session['last_job_id'] = job_id
    return jsonify({'job_id': job_id, 'status': 'RECEIVED'}), 202


@shop_bp.route('/checkout/status/<job_id>')
@login_required
def checkout_status(job_id):
    state = ss.get_order_status(job_id)
    if state is None:
        return jsonify({'error': 'unknown job_id'}), 404
    return jsonify(state)


# ── Order success ─────────────────────────────────────────────────────────────

@shop_bp.route('/order/<int:order_id>')
@login_required
def order_success(order_id):
    conn_str = _build_conn_str()
    order    = ss.get_order_detail(conn_str, order_id)
    if not order:
        abort(404)
    logistics = None
    job_id    = request.args.get('job') or session.get('last_job_id')
    if job_id:
        state = ss.get_order_status(job_id)
        if state:
            logistics = state.get('logistics')
    return render_template('shop/order_success.html',
                           order=order, logistics=logistics, cart_count=0)


# ── Dashboard ─────────────────────────────────────────────────────────────────

@shop_bp.route('/dashboard')
@login_required
def dashboard():
    customers = ss.get_customers_list(_build_conn_str())
    return render_template('shop/dashboard.html',
                           customers=customers,
                           customer=None, orders=[],
                           monthly=[], categories=[], reorder=[],
                           cart_count=_cart_count())


@shop_bp.route('/dashboard/<customer_id>')
@login_required
def dashboard_customer(customer_id):
    conn_str   = _build_conn_str()
    customer   = ss.get_customer(conn_str, customer_id)
    if not customer:
        abort(404)
    customers  = ss.get_customers_list(conn_str)
    orders     = ss.get_order_history(conn_str, customer_id)
    monthly    = ss.get_monthly_revenue(conn_str, customer_id)
    categories = ss.get_category_spend(conn_str, customer_id)
    reorder    = ss.get_reorder_suggestions(conn_str, customer_id)
    return render_template('shop/dashboard.html',
                           customers=customers,
                           customer=customer,
                           orders=orders,
                           monthly=monthly,
                           categories=categories,
                           reorder=reorder,
                           cart_count=_cart_count())


# ── Stock Agent (SQL Server Agent demo) ───────────────────────────────────────

@shop_bp.route('/stock-agent')
@login_required
def stock_agent():
    conn_str   = _build_conn_str()
    sp_err     = sas.ensure_sp_refill(conn_str)
    low_stock  = sas.get_low_stock(conn_str)
    summary    = sas.get_stock_summary(conn_str)
    history    = sas.get_job_history()
    sched      = sas.get_scheduler_state()
    return render_template(
        'shop/stock_agent.html',
        sp_ddl=sas.SP_DDL,
        sp_err=sp_err,
        low_stock=low_stock,
        summary=summary,
        history=history,
        sched=sched,
        cart_count=_cart_count(),
    )


@shop_bp.route('/stock-agent/run', methods=['POST'])
@login_required
def stock_agent_run():
    result = sas.run_refill_now(_build_conn_str())
    ss.invalidate_product_index()
    return jsonify(result)


@shop_bp.route('/stock-agent/scheduler', methods=['POST'])
@login_required
def stock_agent_scheduler():
    data   = request.get_json() or {}
    action = data.get('action', '')
    conn_str = _build_conn_str()
    if action == 'start':
        secs = int(data.get('interval', 3600))
        sas.start_scheduler(conn_str, secs)
    elif action == 'stop':
        sas.stop_scheduler()
    elif action == 'set_interval':
        secs = int(data.get('interval', 3600))
        sas.set_interval(secs)
    return jsonify({'ok': True, 'state': sas.get_scheduler_state()})


@shop_bp.route('/stock-agent/status.json')
@login_required
def stock_agent_status():
    conn_str = _build_conn_str()
    return jsonify({
        'summary':   sas.get_stock_summary(conn_str),
        'low_stock': sas.get_low_stock(conn_str),
        'history':   sas.get_job_history()[:10],
        'scheduler': sas.get_scheduler_state(),
    })
