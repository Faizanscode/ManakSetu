import json
import os

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Categories shouldn't need modifying if we reuse existing ones.
new_standards_data = [
    {"id": "IS-302-1", "num": "IS 302-1 : 2008", "title": "Safety of household and similar electrical appliances", "desc": "Electrical appliance safety.", "cat": "CAT-ELECEQ"},
    {"id": "IS-14155", "num": "IS 14155 : 1994", "title": "Domestic water purifiers for use with municipal water supply", "desc": "Water purifiers.", "cat": "CAT-PIPES"},
    {"id": "IS-14735", "num": "IS 14735 : 1999", "title": "Unplasticized PVC pipes for potable water supplies", "desc": "UPVC pipes for water supply.", "cat": "CAT-PIPES"},
    {"id": "IS-2026-1", "num": "IS 2026 (Part 1) : 2011", "title": "Power transformers: General", "desc": "Power transformers general requirements.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-2705-1", "num": "IS 2705 (Part 1) : 1992", "title": "Current transformers: General requirements", "desc": "Current transformers.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-12118-1", "num": "IS 12118 (Part 1) : 1987", "title": "Two-part polysulphide-based sealants: General requirements", "desc": "Polysulphide sealants.", "cat": "CAT-PAINTS"},
    {"id": "IS-11149", "num": "IS 11149 : 1984", "title": "Rubber gaskets", "desc": "Rubber gaskets for pipeline and general use.", "cat": "CAT-VALVES"},
    {"id": "IS-1121-1", "num": "IS 1121 (Part 1) : 1974", "title": "Methods of test for determination of strength properties of natural building stones: Compressive strength", "desc": "Compressive strength of stones.", "cat": "CAT-CONCRETE"},
    {"id": "IS-15652", "num": "IS 15652 : 2006", "title": "Insulating mats for electrical purposes", "desc": "Insulating mats for safety.", "cat": "CAT-PPE"},
    {"id": "IS-4151", "num": "IS 4151 : 2015", "title": "Protective helmets for two wheeler riders", "desc": "Protective helmets.", "cat": "CAT-PPE"},
    {"id": "IS-15298-2", "num": "IS 15298 (Part 2) : 2016", "title": "Personal protective equipment - Safety footwear", "desc": "Safety footwear.", "cat": "CAT-PPE"},
    {"id": "IS-13947-1", "num": "IS 13947 (Part 1) : 1993", "title": "Low-voltage switchgear and controlgear: General rules", "desc": "Switchgear general rules.", "cat": "CAT-ELECEQ"},
]

existing_standard_ids = {s['id'] for s in data.get('standards', [])}

for s in new_standards_data:
    if s['id'] not in existing_standard_ids:
        # Resolve sector
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

print(f"Added {len([s for s in new_standards_data if s['id'] not in existing_standard_ids])} remaining standards.")
