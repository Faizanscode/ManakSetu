import requests
import json
import sys

def main():
    print("Testing gap detection...")
    
    # We will just get a recommendation first to pass into gaps
    req_body = {
        "query": "We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification."
    }
    
    resp1 = requests.post("http://127.0.0.1:8003/api/recommendations/", json=req_body)
    if resp1.status_code != 200:
        print("Failed to get recommendations:", resp1.text)
        sys.exit(1)
        
    rec_data = resp1.json()
    
    gap_req = {
        "requirement": req_body["query"],
        "recommendations": rec_data.get("recommendations", [])
    }
    
    print("Sending request to /api/gaps/...")
    resp2 = requests.post("http://127.0.0.1:8003/api/gaps/", json=gap_req)
    
    print(f"Status Code: {resp2.status_code}")
    print(json.dumps(resp2.json(), indent=2))
    
if __name__ == "__main__":
    main()
