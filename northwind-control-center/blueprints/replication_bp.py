import json

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

import meta_db
from auth import login_required, admin_required
from services import replication_service as rs

replication = Blueprint('replication', __name__, url_prefix='/replication')


@replication.route('/')
@login_required
def status():
    jobs = meta_db.list_replication_jobs()
    job_statuses = [rs.get_log_shipping_status(j['id']) for j in jobs]
    connections = meta_db.list_connections()
    return render_template('replication/status.html',
                           jobs=job_statuses, connections=connections)


@replication.route('/new', methods=['POST'])
@admin_required
def new_job():
    name = request.form.get('name', '').strip()
    master = int(request.form.get('master_conn_id', 0))
    slave = int(request.form.get('slave_conn_id', 0))
    interval = int(request.form.get('interval_secs', 60))
    if not name or not master or not slave:
        flash('Name, master, and slave are required.', 'danger')
    elif master == slave:
        flash('Master and slave must be different connections.', 'danger')
    else:
        meta_db.create_replication_job(name, 'log_shipping', master, slave, interval)
        flash(f"Job '{name}' created.", 'success')
    return redirect(url_for('replication.status'))


@replication.route('/<int:job_id>/start', methods=['POST'])
@admin_required
def start_job(job_id):
    from app import scheduler
    rs.start_replication_job(job_id, scheduler, current_app._get_current_object())
    flash('Replication job started.', 'success')
    return redirect(url_for('replication.status'))


@replication.route('/<int:job_id>/stop', methods=['POST'])
@admin_required
def stop_job(job_id):
    from app import scheduler
    rs.stop_replication_job(job_id, scheduler)
    flash('Replication job stopped.', 'success')
    return redirect(url_for('replication.status'))


@replication.route('/<int:job_id>/trigger', methods=['POST'])
@admin_required
def trigger_job(job_id):
    job = meta_db.get_replication_job(job_id)
    if job:
        rs.run_log_shipping(job_id, job['master_conn_id'], job['slave_conn_id'],
                            current_app._get_current_object())
        flash('Manual replication run complete.', 'success')
    return redirect(url_for('replication.status'))


@replication.route('/<int:job_id>/delete', methods=['POST'])
@admin_required
def delete_job(job_id):
    from app import scheduler
    rs.stop_replication_job(job_id, scheduler)
    meta_db.delete_replication_job(job_id)
    flash('Job deleted.', 'success')
    return redirect(url_for('replication.status'))


@replication.route('/<int:job_id>/conflicts')
@login_required
def conflicts(job_id):
    job = meta_db.get_replication_job(job_id)
    table = request.args.get('table', '')
    conflicts_list = []
    if table:
        node_ids = [job['master_conn_id'], job['slave_conn_id']]
        conflicts_list = rs.detect_conflicts(node_ids, table)
    connections = meta_db.list_connections()
    return render_template('replication/conflict.html',
                           job=job, conflicts=conflicts_list,
                           table=table, connections=connections)


@replication.route('/<int:job_id>/resolve', methods=['POST'])
@admin_required
def resolve(job_id):
    job = meta_db.get_replication_job(job_id)
    table = request.form.get('table', '')
    pk_col = request.form.get('pk_col', '')
    pk_val = request.form.get('pk_val', '')
    winner_conn_id = int(request.form.get('winner_conn_id', 0))
    winning_data = json.loads(request.form.get('winning_data', '{}'))

    all_ids = [job['master_conn_id'], job['slave_conn_id']]
    loser_ids = [i for i in all_ids if i != winner_conn_id]

    ok, err = rs.resolve_conflict(winner_conn_id, loser_ids, table, pk_col, pk_val, winning_data)
    if ok:
        flash('Conflict resolved — all nodes updated.', 'success')
    else:
        flash(f'Resolution failed: {err}', 'danger')
    return redirect(url_for('replication.conflicts', job_id=job_id, table=table))
