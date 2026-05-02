import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQL_SERVER = os.environ.get('SQL_SERVER', 'localhost')
    SQL_DATABASE = os.environ.get('SQL_DATABASE', 'Northwind')
    SQL_USERNAME = os.environ.get('SQL_USERNAME', '')
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD', '')
    SQL_DRIVER = os.environ.get('SQL_DRIVER', 'ODBC Driver 18 for SQL Server')
    SQL_ENCRYPT = os.environ.get('SQL_ENCRYPT', 'yes')
    SQL_TRUST_SERVER_CERT = os.environ.get('SQL_TRUST_SERVER_CERT', 'yes')

    # Meta-DB (local SQLite storing users, registered connections, replication jobs)
    META_DB_PATH = os.environ.get('META_DB_PATH', 'instance/meta.db')

    # WinRM access to the SQL Server VM for native .bak backup + download
    WINRM_HOST     = os.environ.get('WINRM_HOST', '')
    WINRM_USERNAME = os.environ.get('WINRM_USERNAME', 'admin')
    WINRM_PASSWORD = os.environ.get('WINRM_PASSWORD', '')
    WINRM_BAK_PATH = os.environ.get('WINRM_BAK_PATH', r'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER01\MSSQL\Backup\northwind.bak')

    # SSH access to the SQL Server VM for streaming native .bak downloads
    SSH_HOST     = os.environ.get('SSH_HOST', '')
    SSH_PORT     = int(os.environ.get('SSH_PORT', 22))
    SSH_USERNAME = os.environ.get('SSH_USERNAME', '')
    SSH_KEY_PATH = os.environ.get('SSH_KEY_PATH', os.path.expanduser('~/.ssh/google_compute_engine'))
    BACKUP_REMOTE_PATH  = os.environ.get('BACKUP_REMOTE_PATH', '/var/opt/mssql/data/northwind.bak')
    GCS_BUCKET          = os.environ.get('GCS_BUCKET', '')
    GCS_HMAC_ACCESS_ID  = os.environ.get('GCS_HMAC_ACCESS_ID', '')
    GCS_HMAC_SECRET     = os.environ.get('GCS_HMAC_SECRET', '')

    # Fernet key for encrypting stored database passwords.
    # WARNING: losing or rotating this key makes all stored passwords unrecoverable.
    # Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    FERNET_KEY = os.environ.get('FERNET_KEY', '')
