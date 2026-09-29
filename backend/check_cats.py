import json
import re

with open('knowledge_base/seed/standards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cats_now = {c['id'] for c in data.get('categories', [])}
cats_now.update(['CAT-MOTORS', 'CAT-VALVES'])

with open('add_batch3.py', 'r', encoding='utf-8') as f:
    code = f.read()

for m in re.findall(r'"cat":\s*"(CAT-[^"]+)"', code):
    if m not in cats_now:
        print('MISSING:', m)
