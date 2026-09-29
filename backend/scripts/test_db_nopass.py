import psycopg2

try:
    conn = psycopg2.connect(dbname="manaksetu", user="postgres", host="127.0.0.1", port=5432)
    print("SUCCESS: Connected to postgres without password")
except Exception as e:
    print(f"FAILED postgres without password: {e}")

try:
    conn = psycopg2.connect(dbname="manaksetu", user="iamfa", host="127.0.0.1", port=5432)
    print("SUCCESS: Connected to iamfa without password")
except Exception as e:
    print(f"FAILED iamfa without password: {e}")
