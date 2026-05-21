"""
One-time script: grant flask_user read access to EuropeGraph.
Run from repo root:  python scripts/grant_europe_graph_access.py

Without this, the browser at /browser/ fails with SQL error 4060 when
the user selects EuropeGraph as the target database.
"""
import os
import sys
from pathlib import Path

import pyodbc
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / 'northwind-control-center' / '.env')
load_dotenv(Path(__file__).parent.parent / '.env', override=False)

server   = os.environ['SQL_SERVER']
driver   = os.environ.get('SQL_DRIVER', 'ODBC Driver 18 for SQL Server')
encrypt  = os.environ.get('SQL_ENCRYPT', 'yes')
trust    = os.environ.get('SQL_TRUST_SERVER_CERT', 'yes')
sa_user  = os.environ.get('SQL_SA_USERNAME') or os.environ.get('SQL_USERNAME')
sa_pass  = os.environ.get('SQL_SA_PASSWORD') or os.environ.get('SQL_PASSWORD')
app_user = os.environ.get('SQL_USERNAME', 'flask_user')

if not sa_pass:
    print('ERROR: SA password not found in .env', file=sys.stderr)
    sys.exit(1)

conn_str = (
    f'DRIVER={{{driver}}};SERVER={server};DATABASE=EuropeGraph;'
    f'UID={sa_user};PWD={sa_pass};'
    f'Encrypt={encrypt};TrustServerCertificate={trust};'
)

print(f'Connecting to EuropeGraph as {sa_user} …')
conn = pyodbc.connect(conn_str, autocommit=True)
cur  = conn.cursor()

cur.execute(
    "IF NOT EXISTS ("
    "  SELECT 1 FROM sys.database_principals WHERE name = ?"
    ") EXEC('CREATE USER [' + ? + '] FOR LOGIN [' + ? + ']')",
    app_user, app_user, app_user,
)
print(f'  User [{app_user}] present in EuropeGraph.')

cur.execute(
    "IF IS_ROLEMEMBER('db_datareader', ?) = 0 "
    "  EXEC('ALTER ROLE [db_datareader] ADD MEMBER [' + ? + ']')",
    app_user, app_user,
)
print(f'  [{app_user}] has db_datareader on EuropeGraph.')

cur.close()
conn.close()
print(f'Done — {app_user} can now browse EuropeGraph in the browser UI.')
