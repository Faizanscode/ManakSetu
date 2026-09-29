import requests
import json
import time

BASE_URL = "http://127.0.0.1:8002"
print("Running Batch 1 Regression Tests...")

def test_get(path):
    print(f"Testing {path}...")
    res = requests.get(f"{BASE_URL}{path}")
    if res.status_code == 200:
        print("  OK")
    else:
        print(f"  FAIL: {res.status_code}")
        print(res.text)

test_get("/api/health")
test_get("/api/standards")
test_get("/api/standards/search?q=concrete")
test_get("/api/standards/categories")
test_get("/api/standards/sectors")
test_get("/api/history/")

print("\n--- Real Recommendation Tests ---")
scenarios = [
    {
        "name": "CIVIL",
        "req": "We need reinforcement steel bars for RCC columns, beams and slabs. The bars should have suitable strength, bendability, weldability, dimensional accuracy and quality certification."
    },
    {
        "name": "ELECTRICAL",
        "req": "We need low-voltage power cables for power distribution between the main electrical panel and industrial machinery. The cables should have suitable conductor size, insulation, voltage rating and mechanical protection."
    },
    {
        "name": "WATER / PLUMBING",
        "req": "We need pipes and fittings for a building water supply system. The products should be suitable for water distribution and have appropriate pressure and dimensional characteristics."
    },
    {
        "name": "SAFETY",
        "req": "We need industrial safety helmets for workers at a construction site. The helmets should provide appropriate head protection and comply with applicable Indian safety requirements."
    },
    {
        "name": "PAINT / COATING",
        "req": "We need protective exterior coating for a reinforced concrete building exposed to weather. The coating should provide suitable durability and resistance to environmental exposure."
    }
]

for s in scenarios:
    print(f"\nTesting Scenario: {s['name']}")
    
    # 1. Analyze
    print("  -> POST /api/analyze/")
    res = requests.post(f"{BASE_URL}/api/analyze/", json={"query": s['req']})
    if res.status_code != 200:
        print(f"  FAIL: {res.status_code} {res.text}")
        continue
    analysis = res.json()
    print("     Analysis OK.")
    
    # 2. Recommend
    print("  -> POST /api/recommendations/")
    rec_res = requests.post(f"{BASE_URL}/api/recommendations/", json={
        "query": s['req']
    })
    
    if rec_res.status_code != 200:
        print(f"  FAIL: {rec_res.status_code} {rec_res.text}")
        continue
        
    recommendations = rec_res.json().get('recommendations', [])
    print(f"     Recommendations OK. Found {len(recommendations)} standards.")
    for idx, r in enumerate(recommendations[:3]):
        print(f"       {idx+1}. {r.get('standard_number', '')} ({r.get('relevance_score', 0):.2f})")
    
    # 3. Save to history
    print("  -> POST /api/history/")
    hist_res = requests.post(f"{BASE_URL}/api/history/", json={
        "title": s['name'],
        "procurement_requirement": s['req'],
        "extracted_requirement": analysis,
        "recommendations": rec_res.json()
    })
    if hist_res.status_code == 200:
        print("     History OK.")
    else:
        print(f"     FAIL History: {hist_res.status_code} {hist_res.text}")

print("\nRegression tests complete.")
