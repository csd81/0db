import base64
import pyodbc
import boto3
from botocore.config import Config as BotoConfig
import paramiko
import winrm
from flask import current_app

from db import run_select, run_command

_GCS_ENDPOINT = 'https://storage.googleapis.com'
_CHUNK = 65536


def _autocommit_conn():
    """Open a pyodbc connection with autocommit=True — required for BACKUP/RESTORE."""
    c = current_app.config
    conn_str = (
        f"DRIVER={{{c['SQL_DRIVER']}}};"
        f"SERVER={c['SQL_SERVER']};"
        f"DATABASE={c['SQL_DATABASE']};"
        f"UID={c['SQL_USERNAME']};"
        f"PWD={c['SQL_PASSWORD']};"
        f"Encrypt={c['SQL_ENCRYPT']};"
        f"TrustServerCertificate={c['SQL_TRUST_SERVER_CERT']};"
    )
    return pyodbc.connect(conn_str, autocommit=True)


# ── Credential management ─────────────────────────────────────────────────────

def ensure_gcs_credential(bucket: str, access_id: str, secret: str) -> str | None:
    """
    Create a SQL Server S3 credential for GCS if it doesn't already exist.
    The credential name is the S3-style URL of the bucket.
    Returns None on success, error string on failure.
    """
    cred_name = f's3://storage.googleapis.com/{bucket}'
    try:
        conn = _autocommit_conn()
        cur = conn.cursor()
        cur.execute("SELECT name FROM sys.credentials WHERE name = ?", (cred_name,))
        if cur.fetchone():
            conn.close()
            return None

        cur.execute(
            f"""
            CREATE CREDENTIAL [{cred_name}]
            WITH IDENTITY = 'S3 Access Key',
            SECRET = '{access_id}:{secret}'
            """
        )
        conn.close()
        return None
    except Exception as e:
        return str(e)


# ── Backup ────────────────────────────────────────────────────────────────────

def backup_to_gcs(bucket: str, access_id: str, secret: str,
                  object_name: str = 'northwind.bak') -> tuple[str, str | None]:
    """
    Trigger BACKUP DATABASE to a GCS bucket via SQL Server 2022 S3-compatible URL.
    Returns (gcs_object_key, error_or_None).
    """
    err = ensure_gcs_credential(bucket, access_id, secret)
    if err:
        return '', f'Credential error: {err}'

    url = f's3://storage.googleapis.com/{bucket}/{object_name}'
    try:
        conn = _autocommit_conn()
        conn.execute(
            f"""
            BACKUP DATABASE [{_db_name()}]
            TO URL = N'{url}'
            WITH FORMAT, INIT, COMPRESSION,
                 NAME = N'Northwind-GCS-Full',
                 STATS = 10
            """
        )
        conn.close()
        return object_name, None
    except Exception as e:
        msg = str(e)
        if 'no results' in msg.lower():
            return object_name, None
        return '', msg


# ── Streaming download ────────────────────────────────────────────────────────

def stream_from_gcs(bucket: str, access_id: str, secret: str, key: str):
    """
    Generator that streams a GCS object in 64 KB chunks using the S3-compatible API.
    """
    s3 = boto3.client(
        's3',
        endpoint_url=_GCS_ENDPOINT,
        aws_access_key_id=access_id,
        aws_secret_access_key=secret,
        config=BotoConfig(signature_version='s3v4'),
    )
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body']
    while True:
        chunk = body.read(_CHUNK)
        if not chunk:
            break
        yield chunk


# ── Helpers ───────────────────────────────────────────────────────────────────

def _db_name() -> str:
    try:
        _, rows = run_select("SELECT DB_NAME()")
        return rows[0][0] if rows else 'Northwind'
    except Exception:
        return 'Northwind'


# ── WinRM backup (backup to VM disk, stream back over WinRM) ─────────────────

def trigger_backup_to_disk(bak_path: str) -> str | None:
    """
    BACKUP DATABASE to a local path on the Windows VM.
    Returns None on success, error string on failure.
    """
    try:
        conn = _autocommit_conn()
        cur = conn.cursor()
        cur.execute(
            f"""
            BACKUP DATABASE [{_db_name()}]
            TO DISK = N'{bak_path}'
            WITH FORMAT, INIT, COMPRESSION,
                 NAME = N'Northwind-WinRM-Full'
            """
        )
        # Drain all result sets / info messages so we wait for true completion
        while True:
            try:
                cur.fetchall()
            except Exception:
                pass
            if not cur.nextset():
                break
        conn.close()
        return None
    except Exception as e:
        return str(e)


def verify_file_winrm(host: str, username: str, password: str, bak_path: str) -> tuple[int, str | None]:
    """
    Check the file exists on the VM and return its size in bytes.
    Returns (size, None) on success or (0, error) on failure.
    """
    try:
        session = winrm.Session(host, auth=(username, password), transport='ntlm')
        r = session.run_ps(f'(Get-Item "{bak_path}").Length')
        if r.status_code != 0:
            return 0, r.std_err.decode(errors='replace')
        return int(r.std_out.strip()), None
    except Exception as e:
        return 0, str(e)


def stream_from_winrm(host: str, username: str, password: str, bak_path: str, file_size: int):
    """
    Stream a file from the Windows VM over WinRM in 256 KB base64-encoded chunks.
    Yields raw bytes. Call verify_file_winrm first to confirm the file exists.
    """
    session = winrm.Session(host, auth=(username, password), transport='ntlm')
    chunk_size = 256 * 1024
    offset = 0
    escaped = bak_path.replace("'", "''")

    while offset < file_size:
        ps = f"""
$buf = New-Object byte[] {chunk_size}
$fs = [System.IO.File]::OpenRead('{escaped}')
$null = $fs.Seek({offset}, [System.IO.SeekOrigin]::Begin)
$read = $fs.Read($buf, 0, {chunk_size})
$fs.Close()
if ($read -gt 0) {{ [Convert]::ToBase64String($buf, 0, $read) }}
"""
        r = session.run_ps(ps)
        if r.status_code != 0:
            err = r.std_err.decode(errors='replace')
            raise RuntimeError(f'WinRM chunk read failed at offset {offset}: {err}')
        chunk_b64 = r.std_out.strip()
        if not chunk_b64:
            break
        yield base64.b64decode(chunk_b64)
        offset += chunk_size


# ── Legacy SFTP approach (kept for reference, not used) ──────────────────────

def stream_bak(host: str, port: int, username: str, key_path: str, remote_path: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=port, username=username, key_filename=key_path, timeout=10)
        sftp = ssh.open_sftp()
        remote_file = sftp.open(remote_path, 'rb')
        try:
            while True:
                chunk = remote_file.read(_CHUNK)
                if not chunk:
                    break
                yield chunk
        finally:
            remote_file.close()
            sftp.close()
    finally:
        ssh.close()
