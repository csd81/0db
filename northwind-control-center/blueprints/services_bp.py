from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from auth import login_required, admin_required
import services.system_service as svc

services_bp = Blueprint('services_bp', __name__, url_prefix='/services')


@services_bp.route('/')
@login_required
def index():
    services = svc.list_services()
    return render_template('services/index.html', services=services)


@services_bp.route('/status.json')
@login_required
def status_json():
    return jsonify(svc.list_services())


@services_bp.route('/<name>/start', methods=['POST'])
@admin_required
def start(name):
    err = svc.start_service(name)
    if err:
        flash(f'Start failed: {err}', 'danger')
    else:
        flash(f'{name} started.', 'success')
    return redirect(url_for('services_bp.index'))


@services_bp.route('/<name>/stop', methods=['POST'])
@admin_required
def stop(name):
    err = svc.stop_service(name)
    if err:
        flash(f'Stop failed: {err}', 'danger')
    else:
        flash(f'{name} stopped.', 'success')
    return redirect(url_for('services_bp.index'))


@services_bp.route('/<name>/restart', methods=['POST'])
@admin_required
def restart(name):
    err = svc.restart_service(name)
    if err:
        flash(f'Restart failed: {err}', 'danger')
    else:
        flash(f'{name} restarted.', 'success')
    return redirect(url_for('services_bp.index'))
