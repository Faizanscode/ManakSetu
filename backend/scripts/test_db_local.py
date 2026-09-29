import psycopg2

try:
    conn = psycopg2.connect(dbname="manaksetu")
    print("SUCCESS: Connected to postgres via local default")
except Exception as e:
    print(f"FAILED postgres via local default: {e}")
