import requests

tests = [
    "Transformer procurement",
    "Electric motor procurement",
    "Switchgear/circuit breaker procurement",
    "Industrial pump procurement",
    "Plumbing/CPVC pipe procurement",
    "Water-treatment/water-supply procurement",
    "Fire extinguisher procurement",
    "Fire alarm system procurement",
    "Industrial safety footwear/PPE procurement",
    "HVAC/air-conditioning procurement",
    "LED lighting procurement",
    "Civil construction material procurement"
]

for test in tests:
    print(f"\n--- Testing: {test} ---")
    resp = requests.post("http://127.0.0.1:8002/api/recommendations/", json={
        "query": test,
        "max_recommendations": 3
    })
    if resp.status_code == 200:
        data = resp.json()
        for rec in data.get('recommendations', []):
            print(f"[{rec.get('standard_number')}] {rec.get('title')}")
    else:
        print("Error", resp.status_code)
