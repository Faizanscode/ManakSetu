import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()
print(f"genai version: {genai.__version__}")
client = genai.Client()
response = client.models.generate_content(
    model='gemini-3.8-flash',
    contents='Return JSON with a single field named status whose value is ok.'
)
print(response.text)
