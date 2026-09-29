import json
import os

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_standards_data = [
    {"id": "IS-1180-1", "num": "IS 1180 (Part 1) : 2014", "title": "Outdoor Type Oil Immersed Distribution Transformers", "desc": "Distribution transformers specification.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-304", "num": "IS 304 : 1981", "title": "Tumbler switches for a.c. and d.c.", "desc": "Tumbler switches.", "cat": "CAT-ELECEQ"},
    {"id": "IS-1293", "num": "IS 1293 : 2005", "title": "Plugs and socket-outlets of rated voltage up to 250V", "desc": "Plugs and socket-outlets.", "cat": "CAT-ELECEQ"},
    {"id": "IS-3854", "num": "IS 3854 : 1997", "title": "Switches for domestic and similar purposes", "desc": "Domestic switches.", "cat": "CAT-ELECEQ"},
]

existing_standard_ids = {s['id'] for s in data.get('standards', [])}

for s in new_standards_data:
    if s['id'] not in existing_standard_ids:
        sector_id = next(c['sector_id'] for c in data['categories'] if c['id'] == s['cat'])
        
        data['standards'].append({
            "id": s['id'],
            "standard_number": s['num'],
            "title": s['title'],
            "short_description": s['desc'],
            "sector_id": sector_id,
            "category_id": s['cat'],
            "status": "CURRENT"
        })
        
        edition = s['num'].split(':')[-1].strip()
        data['standard_versions'].append({
            "id": f"VER-{s['id']}-01",
            "standard_id": s['id'],
            "edition": edition,
            "publication_date": f"{edition}-01-01",
            "status": "CURRENT"
        })
        
        data['standard_scopes'].append({
            "id": f"SCO-{s['id']}-01",
            "standard_id": s['id'],
            "scope_text": s['desc'] + " This standard covers essential requirements."
        })
        
        data['standard_sources'].append({
            "id": f"SRC-{s['id']}-01",
            "standard_id": s['id'],
            "organization": "Bureau of Indian Standards",
            "source_type": "Official Standard",
            "url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/isdetails"
        })

with open(SEED_DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Added 4 final standards.")
