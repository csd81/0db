"""
auth.py — RBAC decorators for the Control Plane.
"""

from functools import wraps

from flask import redirect, session, url_for, abort


def get_current_user() -> dict | None:
    uid = session.get('user_id')
    if not uid:
        return None
    return {
        'id': uid,
        'username': session.get('user_username', ''),
        'role': session.get('user_role', 'readonly'),
    }


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated
