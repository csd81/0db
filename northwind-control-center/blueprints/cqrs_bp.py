"""
cqrs_bp.py — Blueprint for the CQRS (Command Query Responsibility Segregation)
demonstration module.

Routes
------
GET  /cqrs/              — overview page with connection picker and audit log
POST /cqrs/execute       — run arbitrary SQL, routing it automatically
POST /cqrs/demo/<key>    — run a preset demo query
GET  /cqrs/audit         — return audit log as JSON (for live refresh)
POST /cqrs/clear-audit   — clear the audit log
"""

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, jsonify,
)

import meta_db
from auth import login_required
from services import cqrs_service as cqrs

cqrs_bp = Blueprint('cqrs', __name__, url_prefix='/cqrs')


def _int_or_zero(val) -> int:
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0


# ── Index ──────────────────────────────────────────────────────────────────────

@cqrs_bp.route('/')
@login_required
def index():
    connections = meta_db.list_connections()
    audit = cqrs.get_audit_log()
    demos = cqrs.demo_queries()
    return render_template(
        'cqrs/index.html',
        connections=connections,
        audit=list(reversed(audit)),   # newest first
        demos=demos,
        result=None,
        sql='',
        primary_conn_id=0,
        replica_conn_id=0,
    )


# ── Execute ────────────────────────────────────────────────────────────────────

@cqrs_bp.route('/execute', methods=['POST'])
@login_required
def execute():
    primary_conn_id = _int_or_zero(request.form.get('primary_conn_id'))
    replica_conn_id = _int_or_zero(request.form.get('replica_conn_id'))
    sql = request.form.get('sql', '').strip()

    connections = meta_db.list_connections()
    demos = cqrs.demo_queries()
    result = None
    error_msg = None

    if not primary_conn_id or not replica_conn_id:
        error_msg = 'Please select both a Primary and a Replica connection.'
    elif not sql:
        error_msg = 'SQL cannot be empty.'
    else:
        result = cqrs.cqrs_execute(primary_conn_id, replica_conn_id, sql)

    if error_msg:
        flash(error_msg, 'danger')

    audit = cqrs.get_audit_log()
    return render_template(
        'cqrs/index.html',
        connections=connections,
        audit=list(reversed(audit)),
        demos=demos,
        result=result,
        sql=sql,
        primary_conn_id=primary_conn_id,
        replica_conn_id=replica_conn_id,
    )


# ── Demo queries ───────────────────────────────────────────────────────────────

@cqrs_bp.route('/demo/<demo_key>', methods=['POST'])
@login_required
def demo(demo_key):
    primary_conn_id = _int_or_zero(request.form.get('primary_conn_id'))
    replica_conn_id = _int_or_zero(request.form.get('replica_conn_id'))

    connections = meta_db.list_connections()
    demos = cqrs.demo_queries()
    result = None

    if not primary_conn_id or not replica_conn_id:
        flash('Please select both a Primary and a Replica connection first.', 'danger')
        audit = cqrs.get_audit_log()
        return render_template(
            'cqrs/index.html',
            connections=connections,
            audit=list(reversed(audit)),
            demos=demos,
            result=None,
            sql='',
            primary_conn_id=primary_conn_id,
            replica_conn_id=replica_conn_id,
        )

    entry = cqrs.get_demo_query(demo_key)
    if not entry:
        flash(f'Unknown demo query: {demo_key!r}', 'warning')
        return redirect(url_for('cqrs.index'))

    sql = entry['sql']
    result = cqrs.cqrs_execute(primary_conn_id, replica_conn_id, sql)

    audit = cqrs.get_audit_log()
    return render_template(
        'cqrs/index.html',
        connections=connections,
        audit=list(reversed(audit)),
        demos=demos,
        result=result,
        sql=sql,
        primary_conn_id=primary_conn_id,
        replica_conn_id=replica_conn_id,
    )


# ── Audit JSON endpoint ────────────────────────────────────────────────────────

@cqrs_bp.route('/audit')
@login_required
def audit_json():
    """Return current audit log as JSON (newest first) for live refresh."""
    audit = list(reversed(cqrs.get_audit_log()))
    return jsonify(audit)


# ── Clear audit ────────────────────────────────────────────────────────────────

@cqrs_bp.route('/clear-audit', methods=['POST'])
@login_required
def clear_audit():
    cqrs.clear_audit_log()
    flash('Audit log cleared.', 'success')
    return redirect(url_for('cqrs.index'))
