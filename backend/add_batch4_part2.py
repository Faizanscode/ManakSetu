import json
import os

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_standards_data = [
    {"id": "IS-2339", "num": "IS 2339 : 1963", "title": "Aluminium paint for general purposes, in dual container", "desc": "Aluminium paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-15489", "num": "IS 15489 : 2004", "title": "Plastic emulsion paint", "desc": "Plastic emulsion paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-144", "num": "IS 144 : 1950", "title": "Ready mixed paint, brushing, dark grey", "desc": "Ready mixed paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-4038", "num": "IS 4038 : 1986", "title": "Foot valves for water works purposes", "desc": "Foot valves.", "cat": "CAT-VALVES"},
    {"id": "IS-778", "num": "IS 778 : 1984", "title": "Copper alloy gate, globe and check valves for water works purposes", "desc": "Copper alloy valves.", "cat": "CAT-VALVES"},
    {"id": "IS-1989-1", "num": "IS 1989 (Part 1) : 1986", "title": "Leather safety boots and shoes", "desc": "Leather safety boots.", "cat": "CAT-PPE"},
    {"id": "IS-12254", "num": "IS 12254 : 1993", "title": "Polyvinyl chloride (PVC) boots", "desc": "PVC boots.", "cat": "CAT-PPE"},
    {"id": "IS-269", "num": "IS 269 : 2015", "title": "Ordinary Portland Cement - Specification", "desc": "Ordinary Portland Cement.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1489-1", "num": "IS 1489 (Part 1) : 2015", "title": "Portland Pozzolana Cement - Specification", "desc": "Portland Pozzolana Cement.", "cat": "CAT-CONCRETE"},
    {"id": "IS-4648", "num": "IS 4648 : 1968", "title": "Guide for electrical layout in residential buildings", "desc": "Electrical layout guide.", "cat": "CAT-ELECEQ"},
    {"id": "IS-1255", "num": "IS 1255 : 1983", "title": "Code of practice for installation and maintenance of power cables", "desc": "Power cables installation.", "cat": "CAT-ELECEQ"},
    {"id": "IS-11892", "num": "IS 11892 : 1986", "title": "Rubber insulated cables for working voltages up to 1100 V", "desc": "Rubber insulated cables.", "cat": "CAT-ELECEQ"},
    {"id": "IS-12818", "num": "IS 12818 : 2010", "title": "Unplasticized PVC screen and casing pipes for bore/tube wells", "desc": "PVC casing pipes.", "cat": "CAT-PIPES"}
]

existing_standard_ids = {s['id'] for s in data.get('standards', [])}
added = 0

for s in new_standards_data:
    if s['id'] not in existing_standard_ids:
        # Check if category exists
        cat_match = [c for c in data['categories'] if c['id'] == s['cat']]
        if not cat_match:
            print(f"Error: Category {s['cat']} not found!")
            continue
            
        sector_id = cat_match[0]['sector_id']
        
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
            "scope_text": s['desc'] + " This standard covers essential procurement specifications."
        })
        
        data['standard_sources'].append({
            "id": f"SRC-{s['id']}-01",
            "standard_id": s['id'],
            "organization": "Bureau of Indian Standards",
            "source_type": "Official Standard",
            "url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/isdetails"
        })
        added += 1

with open(SEED_DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Batch 4 part 2 completed. Added {added} standards.")
