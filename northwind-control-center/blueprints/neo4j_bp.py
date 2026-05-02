from flask import Blueprint, render_template, request, flash, redirect, url_for
import meta_db
import services.neo4j_service as nj
from auth import login_required

neo4j_bp = Blueprint('neo4j_bp', __name__, url_prefix='/neo4j')


@neo4j_bp.route('/')
@login_required
def index():
    conns = [c for c in meta_db.list_connections() if c['db_type'] == 'neo4j']
    conn_id = request.args.get('conn_id', type=int)
    schema = {}
    if conn_id:
        schema = nj.get_schema(conn_id)
    return render_template(
        'neo4j/index.html',
        conns=conns,
        conn_id=conn_id,
        schema=schema,
        queries=nj.built_in_queries(),
        columns=None, rows=None, error=None, cypher='',
    )


@neo4j_bp.route('/<int:conn_id>/run', methods=['POST'])
@login_required
def run(conn_id):
    cypher = request.form.get('cypher', '').strip()
    builtin_key = request.form.get('builtin_key', '')

    if builtin_key and not cypher:
        match = next((q for q in nj.built_in_queries() if q['key'] == builtin_key), None)
        if match:
            cypher = match['cypher']

    columns, rows, error = nj.run_cypher(conn_id, cypher) if cypher else ([], [], 'No query provided.')

    conns = [c for c in meta_db.list_connections() if c['db_type'] == 'neo4j']
    schema = nj.get_schema(conn_id)
    return render_template(
        'neo4j/index.html',
        conns=conns,
        conn_id=conn_id,
        schema=schema,
        queries=nj.built_in_queries(),
        selected_key=builtin_key,
        columns=columns, rows=rows, error=error, cypher=cypher,
    )
