import requests
import json

payload = {
    "query": "We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard."
}

res = requests.post("http://127.0.0.1:8002/api/recommendations/", json=payload)
print(res.status_code)
print(json.dumps(res.json(), indent=2))
