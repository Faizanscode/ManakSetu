import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(user='postgres', password='password', host='localhost', port=5432)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'manaksetu'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute('CREATE DATABASE manaksetu')
        print("Database 'manaksetu' created successfully.")
    else:
        print("Database 'manaksetu' already exists.")
    cursor.close()
    conn.close()

    conn2 = psycopg2.connect(user='postgres', password='password', host='localhost', port=5432, dbname='manaksetu')
    conn2.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor2 = conn2.cursor()
    cursor2.execute('CREATE EXTENSION IF NOT EXISTS vector')
    print("Extension 'vector' ensured.")
    cursor2.close()
    conn2.close()
except Exception as e:
    print("Error:", e)
