import requests
import json
import time

for i in range(5):
    print(f"Run {i}")
    try:
        r = requests.post("http://127.0.0.1:8002/api/recommendations/", json={"query": "We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard."})
        data = r.json()
        print("Success:", "recommendations" in data)
        with open(f"rec_{i}.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Error:", e)
    time.sleep(2)
