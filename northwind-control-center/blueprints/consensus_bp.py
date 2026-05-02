import json

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash

from auth import login_required, admin_required
from services import pow_service as pow_svc

consensus = Blueprint('consensus', __name__, url_prefix='/consensus')


@consensus.route('/')
@login_required
def index():
    state = pow_svc.get_consensus_state()
    return render_template('consensus/index.html', state=state)


@consensus.route('/start', methods=['POST'])
@admin_required
def start():
    try:
        payload = json.loads(request.form.get('payload', '{}'))
    except json.JSONDecodeError:
        flash('Invalid JSON payload.', 'danger')
        return redirect(url_for('consensus.index'))
    difficulty = int(request.form.get('difficulty', 4))
    n_nodes = int(request.form.get('n_nodes', 3))
    difficulty = max(1, min(difficulty, 6))
    n_nodes = max(2, min(n_nodes, 5))
    pow_svc.start_consensus_round(payload, difficulty, n_nodes)
    return redirect(url_for('consensus.index'))


@consensus.route('/state')
@login_required
def state():
    return jsonify(pow_svc.get_consensus_state())


@consensus.route('/reset', methods=['POST'])
@admin_required
def reset():
    pow_svc.reset_consensus()
    return redirect(url_for('consensus.index'))
