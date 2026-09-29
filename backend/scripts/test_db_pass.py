import psycopg2

passwords = ["", "postgres", "password", "root", "admin", "1234"]
success = False
for p in passwords:
    try:
        conn = psycopg2.connect(dbname="manaksetu", user="postgres", password=p, host="127.0.0.1", port=5432)
        print(f"SUCCESS: password is '{p}'")
        success = True
        conn.close()
        break
    except Exception as e:
        pass
if not success:
    print("FAILED to find password")
