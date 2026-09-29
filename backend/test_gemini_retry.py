import time
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()
attempts = 0
while attempts < 10:
    try:
        print('Attempt', attempts)
        resp = client.models.generate_content(
            model='gemini-3.8-flash',
            contents='Return JSON with a single field named status whose value is ok.'
        )
        print(resp.text)
        break
    except Exception as e:
        print(e)
        time.sleep(2)
        attempts += 1
