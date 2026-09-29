import requests
r = requests.get('http://127.0.0.1:8002/api/standards?limit=1000')
if r.status_code == 200:
    data = r.json()
    print(f'Items returned: {len(data)}')
    print(f'Total count header: {r.headers.get("X-Total-Count")}')
else:
    print(r.status_code)
