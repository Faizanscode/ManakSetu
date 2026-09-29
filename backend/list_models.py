import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

for model in client.models.list():
    # check for supported generation methods or just list them
    print(f"Name: {model.name}, Display: {model.display_name}")
