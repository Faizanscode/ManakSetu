import psycopg2

try:
    conn = psycopg2.connect(dbname="manaksetu", user="postgres", host="localhost", port=5432)
    print("SUCCESS: Connected to postgres without password on localhost (IPv6)")
except Exception as e:
    print(f"FAILED postgres without password on localhost: {e}")
