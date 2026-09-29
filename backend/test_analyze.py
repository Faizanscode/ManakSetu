import requests
import time
import json

payload = {
    'query': 'We need to procure 100 low-voltage power cables for a new industrial facility. The cables will be used for power distribution between the main electrical panel and machinery. They should have suitable conductor size and current-carrying capacity, adequate insulation, flame-retardant properties, resistance to moisture and mechanical stress, and appropriate voltage rating. The cables should comply with applicable Indian electrical and BIS standards and be supplied with routine test certificates.'
}

print("Starting request to /api/analyze/...")
start = time.time()
try:
    res = requests.post('http://127.0.0.1:8002/api/analyze/', json=payload, timeout=30)
    elapsed = time.time() - start
    print(f'Took {elapsed:.2f}s')
    print('Status:', res.status_code)
    if res.status_code == 200:
        data = res.json()
        print('extracted keys:', list(data.get('extracted', {}).keys()))
        print('embedding_status:', data.get('embedding_status'))
    else:
        print('Error body:', res.text[:500])
except requests.exceptions.Timeout:
    elapsed = time.time() - start
    print(f'TIMED OUT after {elapsed:.2f}s')
except Exception as e:
    elapsed = time.time() - start
    print(f'Error after {elapsed:.2f}s: {e}')
