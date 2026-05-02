"""
replication_service.py — Log shipping and merge replication for SQLite nodes.

APScheduler calls run_log_shipping() in a background thread.
All job functions use `with app.app_context():` for Flask context.
NOTE: Works only in single-process mode (python app.py / gunicorn --workers=1).
"""

import json
import sqlite3
from datetime import datetime

import meta_db
import db_adapter
from services.transaction_service import ensure_transaction_log, replay_log_entry


# ── Log Shipping ───────────────────────────────────────────────────────────────

def run_log_shipping(job_id: int, master_conn_id: int, slave_conn_id: int, app) -> None:
    """APScheduler job target. Reads new TransactionLog entries from master, applies to slave."""
    with app.app_context():
        job = meta_db.get_replication_job(job_id)
        if not job:
            return

        last_id = job.get('last_replicated_id', 0) or 0
        applied = 0
        error = None

        try:
            master_rec = meta_db.get_connection_by_id(master_conn_id)
            slave_rec = meta_db.get_connection_by_id(slave_conn_id)

            master_conn = sqlite3.connect(master_rec['conn_params']['database'], check_same_thread=False)
            slave_conn = sqlite3.connect(slave_rec['conn_params']['database'], check_same_thread=False)

            ensure_transaction_log(master_conn)
            ensure_transaction_log(slave_conn)

            cur = master_conn.execute(
                "SELECT * FROM TransactionLog WHERE LogID > ? ORDER BY LogID",
                (last_id,),
            )
            cols = [d[0] for d in cur.description]
            entries = [dict(zip(cols, row)) for row in cur.fetchall()]

            new_last_id = last_id
            for entry in entries:
                ok, err = replay_log_entry(slave_conn, entry)
                if ok:
                    new_last_id = max(new_last_id, entry['LogID'])
                    applied += 1
                else:
                    error = err
                    break

            master_conn.close()
            slave_conn.close()

        except Exception as e:
            error = str(e)

        meta_db.update_job_status(
            job_id,
            status='error' if error else 'running',
            last_run=datetime.utcnow(),
            last_error=error,
            last_replicated_id=new_last_id if not error else last_id,
        )


# ── Merge / Conflict Detection ─────────────────────────────────────────────────

def detect_conflicts(node_conn_ids: list[int], table: str, since_timestamp: str | None = None) -> list[dict]:
    """
    Compare TransactionLog UPDATE entries across nodes for the same RecordID.
    Returns list of conflicts: {record_id, table, node_conflicts: [{node_id, timestamp, new_data}]}.
    """
    per_node: dict[str, dict] = {}  # record_id → {node_id: {timestamp, new_data}}

    for conn_id in node_conn_ids:
        rec = meta_db.get_connection_by_id(conn_id)
        if not rec or rec['db_type'] != 'sqlite':
            continue
        try:
            conn = sqlite3.connect(rec['conn_params']['database'], check_same_thread=False)
            ensure_transaction_log(conn)
            sql = "SELECT RecordID, NewData, Timestamp FROM TransactionLog WHERE TableName=? AND Operation='UPDATE'"
            params = [table]
            if since_timestamp:
                sql += " AND Timestamp >= ?"
                params.append(since_timestamp)
            cur = conn.execute(sql, params)
            for row in cur.fetchall():
                record_id, new_data, ts = row[0], row[1], row[2]
                if record_id not in per_node:
                    per_node[record_id] = {}
                per_node[record_id][conn_id] = {'timestamp': ts, 'new_data': new_data}
            conn.close()
        except Exception:
            continue

    conflicts = []
    for record_id, node_map in per_node.items():
        if len(node_map) >= 2:
            node_conflicts = [
                {'node_id': nid, 'timestamp': v['timestamp'],
                 'new_data': json.loads(v['new_data']) if v['new_data'] else {}}
                for nid, v in node_map.items()
            ]
            conflicts.append({
                'record_id': record_id,
                'table': table,
                'node_conflicts': node_conflicts,
            })

    return conflicts


def resolve_conflict(winner_conn_id: int, loser_conn_ids: list[int],
                     table: str, pk_col: str, pk_val,
                     winning_data: dict) -> tuple[bool, str | None]:
    """Apply winning_data to all loser nodes."""
    try:
        for conn_id in loser_conn_ids:
            rec = meta_db.get_connection_by_id(conn_id)
            conn = sqlite3.connect(rec['conn_params']['database'], check_same_thread=False)
            ensure_transaction_log(conn)

            set_clause = ', '.join(f'[{c}] = ?' for c in winning_data)
            conn.execute(
                f"UPDATE [{table}] SET {set_clause} WHERE [{pk_col}] = ?",
                list(winning_data.values()) + [pk_val],
            )
            conn.execute(
                "INSERT INTO TransactionLog (TableName, Operation, RecordID, NewData) VALUES (?, 'UPDATE', ?, ?)",
                (table, str(pk_val), json.dumps(winning_data)),
            )
            conn.commit()
            conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def get_log_shipping_status(job_id: int) -> dict:
    job = meta_db.get_replication_job(job_id)
    if not job:
        return {}

    master_log_count = 0
    slave_log_count = 0
    try:
        master_rec = meta_db.get_connection_by_id(job['master_conn_id'])
        conn = sqlite3.connect(master_rec['conn_params']['database'], check_same_thread=False)
        row = conn.execute("SELECT COUNT(*) FROM TransactionLog").fetchone()
        master_log_count = row[0] if row else 0
        conn.close()
    except Exception:
        pass
    try:
        slave_rec = meta_db.get_connection_by_id(job['slave_conn_id'])
        conn = sqlite3.connect(slave_rec['conn_params']['database'], check_same_thread=False)
        row = conn.execute("SELECT COUNT(*) FROM TransactionLog").fetchone()
        slave_log_count = row[0] if row else 0
        conn.close()
    except Exception:
        pass

    return {
        **job,
        'master_log_count': master_log_count,
        'slave_log_count': slave_log_count,
        'pending_entries': master_log_count - (job.get('last_replicated_id') or 0),
    }


# ── APScheduler job management ─────────────────────────────────────────────────

def register_all_jobs(scheduler, app) -> None:
    """Restore running log-shipping jobs from meta.db on startup."""
    for job in meta_db.list_replication_jobs():
        if job['status'] == 'running' and job['job_type'] == 'log_shipping':
            _add_scheduler_job(scheduler, job, app)


def start_replication_job(job_id: int, scheduler, app) -> None:
    job = meta_db.get_replication_job(job_id)
    if not job:
        return
    _add_scheduler_job(scheduler, job, app)
    meta_db.update_job_status(job_id, 'running', None, None)


def stop_replication_job(job_id: int, scheduler) -> None:
    jid = f'repl_{job_id}'
    try:
        scheduler.remove_job(jid)
    except Exception:
        pass
    meta_db.update_job_status(job_id, 'stopped', None, None)


def _add_scheduler_job(scheduler, job: dict, app) -> None:
    scheduler.add_job(
        func=run_log_shipping,
        trigger='interval',
        seconds=job['interval_secs'],
        id=f"repl_{job['id']}",
        args=[job['id'], job['master_conn_id'], job['slave_conn_id'], app],
        replace_existing=True,
        misfire_grace_time=30,
    )
