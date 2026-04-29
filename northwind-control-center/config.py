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
