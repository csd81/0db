"""
system_service.py — Start/stop/restart system database services via systemctl.

Security: service names always come from the hardcoded _SERVICES whitelist,
never from user input. subprocess is called with an array, never shell=True.
"""

import subprocess
import psutil

_SERVICES = {
    'elasticsearch': 'elasticsearch',
    'mssql-server':  'mssql-server',
    'neo4j':         'neo4j',
    'mongodb':       'mongod',
    'redis':         'redis-server',
    'mariadb':       'mariadb',
    'cassandra':     'cassandra',
    'postgresql':    'postgresql',
}

_ICONS = {
    'elasticsearch': 'bi-search',
    'mssql-server':  'bi-server',
    'neo4j':         'bi-diagram-3-fill',
    'mongodb':       'bi-file-earmark-text',
    'redis':         'bi-lightning-fill',
    'mariadb':       'bi-database',
    'cassandra':     'bi-hdd-stack',
    'postgresql':    'bi-elephant',
}


def _systemctl(args: list[str]) -> tuple[str, str, int]:
    """Run systemctl with args. Returns (stdout, stderr, returncode)."""
    result = subprocess.run(
        ['systemctl'] + args,
        capture_output=True, text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def _get_main_pid(unit: str) -> int | None:
    stdout, _, rc = _systemctl(['show', '-p', 'MainPID', '--value', unit])
    if rc == 0:
        try:
            pid = int(stdout.strip())
            return pid if pid > 0 else None
        except ValueError:
            return None
    return None


def _get_mem_mb(pid: int | None) -> float | None:
    if pid is None:
        return None
    try:
        proc = psutil.Process(pid)
        mem = proc.memory_info().rss / (1024 * 1024)
        return round(mem, 1)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def list_services() -> list[dict]:
    services = []
    for name, unit in _SERVICES.items():
        stdout, _, rc = _systemctl(['is-active', unit])
        active = stdout == 'active'
        pid = _get_main_pid(unit) if active else None
        mem_mb = _get_mem_mb(pid)
        services.append({
            'name':   name,
            'unit':   unit,
            'active': active,
            'pid':    pid,
            'mem_mb': mem_mb,
            'icon':   _ICONS.get(name, 'bi-database'),
        })
    return services


def _control_service(name: str, action: str) -> str | None:
    """Start, stop, or restart a service by logical name. Returns error string or None."""
    unit = _SERVICES.get(name)
    if not unit:
        return f'Unknown service: {name!r}'
    result = subprocess.run(
        ['sudo', 'systemctl', action, unit],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return result.stderr.strip() or f'systemctl {action} {unit} failed (exit {result.returncode})'
    return None


def start_service(name: str) -> str | None:
    return _control_service(name, 'start')


def stop_service(name: str) -> str | None:
    return _control_service(name, 'stop')


def restart_service(name: str) -> str | None:
    return _control_service(name, 'restart')
