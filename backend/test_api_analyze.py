import requests
import sys

payload = {
    "query": "We need to procure portable fire extinguishers for a government office building. The extinguishers should be suitable for the identified classes of fire, have appropriate extinguishing capacity, operating pressure, corrosion-resistant construction, safety features, and clear operating instructions. The supplier should provide inspection and test certificates and comply with applicable Indian Standards."
}

try:
    response = requests.post("http://127.0.0.1:8002/api/analyze/", json=payload)
    print(f"Status: {response.status_code}")
    print(response.json())
    if response.status_code != 200:
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
