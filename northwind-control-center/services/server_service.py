"""
server_service.py — SQL Server process status, user/role info, database list.
"""
import socket
import subprocess

import pyodbc
from flask import current_app

import db


def _run(cmd, timeout=8):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return -1, '', str(e)


# ── Service detection / control ───────────────────────────────────────────────

def get_sql_service_status() -> dict:
    """Detect how SQL Server is running and return a status dict."""
    # Docker: look for a container that maps port 1433
    rc, out, _ = _run(['docker', 'ps', '--filter', 'publish=1433',
                        '--format', '{{.Names}}\t{{.Status}}'])
    if rc == 0 and out:
        parts = out.splitlines()[0].split('\t')
        return {'type': 'docker', 'name': parts[0],
                'running': True, 'status': parts[1] if len(parts) > 1 else 'Up'}

    # Docker stopped container on port 1433?
    rc2, out2, _ = _run(['docker', 'ps', '-a', '--filter', 'publish=1433',
                          '--format', '{{.Names}}\t{{.Status}}'])
    if rc2 == 0 and out2:
        parts = out2.splitlines()[0].split('\t')
        return {'type': 'docker', 'name': parts[0],
                'running': False, 'status': parts[1] if len(parts) > 1 else 'Exited'}

    # systemd
    rc3, _, _ = _run(['systemctl', 'is-active', 'mssql-server'])
    if rc3 == 0:
        return {'type': 'systemd', 'name': 'mssql-server', 'running': True,  'status': 'active'}
    if rc3 == 3:
        return {'type': 'systemd', 'name': 'mssql-server', 'running': False, 'status': 'inactive'}

    # Fallback: just probe the TCP port
    server = current_app.config.get('SQL_SERVER', 'localhost')
    try:
        s = socket.create_connection((server, 1433), timeout=2)
        s.close()
        return {'type': 'port', 'name': f'{server}:1433', 'running': True,  'status': 'reachable'}
    except Exception:
        return {'type': 'port', 'name': f'{server}:1433', 'running': False, 'status': 'unreachable'}


def start_sql_server(service_type: str, name: str) -> str | None:
    """Start the SQL Server service. Returns None on success, error string on failure."""
    if service_type == 'docker':
        rc, _, err = _run(['docker', 'start', name], timeout=30)
        return None if rc == 0 else err
    if service_type == 'systemd':
        rc, _, err = _run(['sudo', 'systemctl', 'start', 'mssql-server'], timeout=30)
        return None if rc == 0 else err
    return 'Cannot start: unknown service type'


def stop_sql_server(service_type: str, name: str) -> str | None:
    """Stop the SQL Server service. Returns None on success, error string on failure."""
    if service_type == 'docker':
        rc, _, err = _run(['docker', 'stop', name], timeout=30)
        return None if rc == 0 else err
    if service_type == 'systemd':
        rc, _, err = _run(['sudo', 'systemctl', 'stop', 'mssql-server'], timeout=30)
        return None if rc == 0 else err
    return 'Cannot stop: unknown service type'


# ── User / role info ──────────────────────────────────────────────────────────

def get_user_info() -> dict:
    """Return login name, db user, roles for the current flask_user connection."""
    try:
        cols, rows = db.run_select("""
            SELECT
                SYSTEM_USER                        AS login_name,
                USER_NAME()                        AS db_user,
                @@SERVERNAME                       AS server_name,
                DB_NAME()                          AS db_name,
                IS_SRVROLEMEMBER('sysadmin')       AS is_sysadmin,
                IS_SRVROLEMEMBER('serveradmin')    AS is_serveradmin,
                IS_MEMBER('db_owner')              AS is_db_owner,
                IS_MEMBER('db_datareader')         AS is_reader,
                IS_MEMBER('db_datawriter')         AS is_writer
        """)
        if not rows:
            return {}
        info = dict(zip(cols, rows[0]))
        roles = []
        if info.get('is_sysadmin'):    roles.append('sysadmin')
        if info.get('is_serveradmin'): roles.append('serveradmin')
        if info.get('is_db_owner'):    roles.append('db_owner')
        if info.get('is_reader'):      roles.append('db_datareader')
        if info.get('is_writer'):      roles.append('db_datawriter')
        info['roles'] = roles
        return info
    except Exception as e:
        return {'error': str(e)}


# ── Database list ─────────────────────────────────────────────────────────────

def get_databases() -> tuple[list, str | None]:
    """Return (list of db dicts, error). Tries SA credentials for full list + sizes."""
    c = current_app.config
    sa_user = c.get('SQL_SA_USERNAME', '')
    sa_pass = c.get('SQL_SA_PASSWORD', '')

    if sa_user and sa_pass:
        try:
            conn_str = (
                f"DRIVER={{{c['SQL_DRIVER']}}};"
                f"SERVER={c['SQL_SERVER']};"
                f"DATABASE=master;"
                f"UID={sa_user};"
                f"PWD={sa_pass};"
                f"Encrypt={c['SQL_ENCRYPT']};"
                f"TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
            )
            conn = pyodbc.connect(conn_str, timeout=5, autocommit=True)
            cur = conn.cursor()
            cur.execute("""
                SELECT d.name, d.state_desc,
                       CAST(SUM(f.size) * 8.0 / 1024 AS INT) AS size_mb
                FROM sys.databases d
                JOIN sys.master_files f ON d.database_id = f.database_id
                GROUP BY d.name, d.state_desc
                ORDER BY d.name
            """)
            rows = cur.fetchall()
            conn.close()
            return [{'name': r[0], 'state': r[1], 'size_mb': r[2]} for r in rows], None
        except Exception as e:
            pass  # fall through to user-level query

    # Fallback: whatever flask_user can see
    try:
        cols, rows = db.run_select(
            "SELECT name, state_desc FROM sys.databases ORDER BY name"
        )
        return [{'name': r[0], 'state': r[1], 'size_mb': None} for r in rows], None
    except Exception as e:
        return [], str(e)
