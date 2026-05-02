from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
import meta_db
from auth import admin_required, login_required

auth = Blueprint('auth', __name__, url_prefix='/auth')

_DEFAULT_CONN = {'id': '', 'name': 'Default SQL Server (.env)', 'db_type': 'sqlserver'}


def _connection_list():
    return [_DEFAULT_CONN] + [
        {'id': c['id'], 'name': c['name'], 'db_type': c['db_type']}
        for c in meta_db.list_connections()
    ]


def _apply_connection(conn_id_str: str):
    if conn_id_str:
        rec = meta_db.get_connection_by_id(int(conn_id_str))
        session['active_conn_id']   = int(conn_id_str)
        session['active_db_type']   = rec['db_type']
        session['active_conn_name'] = rec['name']
    else:
        session['active_conn_id']   = None
        session['active_db_type']   = 'sqlserver'
        session['active_conn_name'] = 'Default SQL Server'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('home'))

    connections = _connection_list()
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = meta_db.verify_user(username, password)
        if user:
            session['user_id']       = user['id']
            session['user_username'] = user['username']
            session['user_role']     = user['role']
            _apply_connection(request.form.get('active_conn_id', ''))
            return redirect(url_for('home'))
        error = 'Invalid username or password.'

    return render_template('auth/login.html', error=error, connections=connections)


@auth.route('/switch', methods=['GET', 'POST'])
@login_required
def switch_connection():
    connections = _connection_list()
    if request.method == 'POST':
        _apply_connection(request.form.get('active_conn_id', ''))
        flash(f"Switched to {session['active_conn_name']}.", 'success')
        return redirect(url_for('home'))
    return render_template('auth/switch.html', connections=connections)


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth.route('/users')
@admin_required
def users():
    user_list = meta_db.list_users()
    return render_template('auth/users.html', users=user_list)


@auth.route('/users/new', methods=['POST'])
@admin_required
def create_user():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    role = request.form.get('role', 'readonly')
    if not username or not password:
        flash('Username and password are required.', 'danger')
    else:
        ok, err = meta_db.create_user(username, password, role)
        if ok:
            flash(f"User '{username}' created.", 'success')
        else:
            flash(err, 'danger')
    return redirect(url_for('auth.users'))


@auth.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session.get('user_id'):
        flash("You can't delete your own account.", 'danger')
    else:
        meta_db.delete_user(user_id)
        flash('User deleted.', 'success')
    return redirect(url_for('auth.users'))
