import requests
import time
import json

BASE_URL = 'http://127.0.0.1:8002'
QUERY = "We need to procure 100 low-voltage power cables for a new industrial facility. The cables will be used for power distribution between the main electrical panel and machinery. They should have suitable conductor size and current-carrying capacity, adequate insulation, flame-retardant properties, resistance to moisture and mechanical stress, and appropriate voltage rating. The cables should comply with applicable Indian electrical and BIS standards and be supplied with routine test certificates."

def test_phase3():
    print("\n=== Phase 3: Analyze Requirement ===")
    start = time.time()
    res = requests.post(f'{BASE_URL}/api/analyze/', json={'query': QUERY}, timeout=60)
    elapsed = time.time() - start
    print(f'  Status: {res.status_code}, Time: {elapsed:.2f}s')
    if res.status_code == 200:
        data = res.json()
        print(f'  Products: {data["extracted"]["products"][:2]}')
        return data
    else:
        print(f'  Error: {res.text[:200]}')
        return None

def test_phase4():
    print("\n=== Phase 4: Find Applicable Standards ===")
    start = time.time()
    res = requests.post(f'{BASE_URL}/api/recommendations/', json={'query': QUERY}, timeout=60)
    elapsed = time.time() - start
    print(f'  Status: {res.status_code}, Time: {elapsed:.2f}s')
    if res.status_code == 200:
        data = res.json()
        print(f'  Found {len(data["recommendations"])} recommendations')
        return data
    else:
        print(f'  Error: {res.text[:200]}')
        return None

def test_phase6(analysis_data, rec_data):
    print("\n=== Phase 6: Check Specification Gaps ===")
    if not rec_data:
        print("  Skipping — no recommendations data")
        return None
    payload = {
        'requirement': QUERY,
        'recommendations': rec_data['recommendations']
    }
    start = time.time()
    res = requests.post(f'{BASE_URL}/api/gaps/', json=payload, timeout=60)
    elapsed = time.time() - start
    print(f'  Status: {res.status_code}, Time: {elapsed:.2f}s')
    if res.status_code == 200:
        data = res.json()
        print(f'  Found {data["summary"]["total_gaps"]} gaps (HIGH:{data["summary"]["high"]}, MEDIUM:{data["summary"]["medium"]})')
        return data
    else:
        print(f'  Error: {res.text[:200]}')
        return None

def test_phase7(analysis_data, rec_data, gap_data):
    print("\n=== Phase 7: Generate Specification Draft ===")
    if not rec_data:
        print("  Skipping — no recommendations data")
        return None
    payload = {
        'requirement': QUERY,
        'analysis': analysis_data,
        'recommendations': rec_data['recommendations'],
        'gaps': gap_data['gaps'] if gap_data else []
    }
    start = time.time()
    res = requests.post(f'{BASE_URL}/api/specifications/generate', json=payload, timeout=60)
    elapsed = time.time() - start
    print(f'  Status: {res.status_code}, Time: {elapsed:.2f}s')
    if res.status_code == 200:
        data = res.json()
        print(f'  Spec title: {data["specification"]["title"][:80]}')
        return data
    else:
        print(f'  Error: {res.text[:200]}')
        return None

if __name__ == '__main__':
    print("Starting full regression test for ManakSetu...")
    total_start = time.time()

    analysis = test_phase3()
    recs = test_phase4()
    gaps = test_phase6(analysis, recs)
    spec = test_phase7(analysis, recs, gaps)

    total = time.time() - total_start
    print(f"\n=== TOTAL TIME: {total:.2f}s ===")
    print("Phase 3:", "OK" if analysis else "FAILED")
    print("Phase 4:", "OK" if recs else "FAILED")
    print("Phase 6:", "OK" if gaps else "FAILED")
    print("Phase 7:", "OK" if spec else "FAILED")
