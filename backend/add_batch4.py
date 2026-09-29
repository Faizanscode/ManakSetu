import json
import os

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_categories = [
    {"id": "CAT-PUMPS", "name": "Pumps and Pumping Equipment", "description": "Centrifugal, submersible, and specialized pumps.", "sector_id": "SEC-MECH"},
    {"id": "CAT-SANITARY", "name": "Sanitary Appliances", "description": "Water closets, wash basins, urinals, and related fixtures.", "sector_id": "SEC-WATER"},
    {"id": "CAT-MEASUREMENT", "name": "Civil Measurement and Estimation", "description": "Methods of measurement for civil engineering works.", "sector_id": "SEC-CIVIL"},
    {"id": "CAT-HARDWARE", "name": "Builder's Hardware", "description": "Hinges, locks, and architectural hardware.", "sector_id": "SEC-CIVIL"}
]

existing_cat_ids = {c['id'] for c in data.get('categories', [])}
for c in new_categories:
    if c['id'] not in existing_cat_ids:
        data['categories'].append(c)

new_standards_data = [
    # Electrical (9)
    {"id": "IS-2026-2", "num": "IS 2026 (Part 2) : 2010", "title": "Power transformers: Temperature-rise", "desc": "Temperature-rise requirements for power transformers.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-2026-3", "num": "IS 2026 (Part 3) : 2009", "title": "Power transformers: Insulation levels, dielectric tests", "desc": "Insulation levels and tests.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-11171", "num": "IS 11171 : 1985", "title": "Specification for dry-type power transformers", "desc": "Dry-type power transformers.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-8623-1", "num": "IS 8623 (Part 1) : 1993", "title": "Low-voltage switchgear and controlgear assemblies: Requirements for type-tested assemblies", "desc": "Requirements for switchgear assemblies.", "cat": "CAT-ELECEQ"},
    {"id": "IS-10118-1", "num": "IS 10118 (Part 1) : 1982", "title": "Code of practice for selection, installation and maintenance of switchgear and controlgear: General", "desc": "Switchgear installation code of practice.", "cat": "CAT-ELECEQ"},
    {"id": "IS-13947-2", "num": "IS 13947 (Part 2) : 1993", "title": "Low-voltage switchgear and controlgear: Circuit-breakers", "desc": "Circuit-breakers.", "cat": "CAT-ELECEQ"},
    {"id": "IS-13947-4-1", "num": "IS 13947 (Part 4/Sec 1) : 1993", "title": "Low-voltage switchgear and controlgear: Contactors and motor-starters", "desc": "Contactors and starters.", "cat": "CAT-ELECEQ"},
    {"id": "IS-12615", "num": "IS 12615 : 2018", "title": "Line operated three phase a.c. motors (IE CODE) - Efficiency classes", "desc": "Efficiency classes for AC motors.", "cat": "CAT-MOTORS"},
    {"id": "IS-13529", "num": "IS 13529 : 1992", "title": "Guide on effects of unbalanced voltages on the performance of three-phase cage induction motors", "desc": "Induction motor performance guide.", "cat": "CAT-MOTORS"},

    # Mechanical (9)
    {"id": "IS-1520", "num": "IS 1520 : 2000", "title": "Horizontal centrifugal pumps for clear, cold, fresh water", "desc": "Horizontal centrifugal pumps.", "cat": "CAT-PUMPS"},
    {"id": "IS-5120", "num": "IS 5120 : 1977", "title": "Technical requirements for rotodynamic special purpose pumps", "desc": "Rotodynamic pumps.", "cat": "CAT-PUMPS"},
    {"id": "IS-8034", "num": "IS 8034 : 2002", "title": "Submersible pumpsets for clear, cold, fresh water", "desc": "Submersible pumpsets.", "cat": "CAT-PUMPS"},
    {"id": "IS-14220", "num": "IS 14220 : 1994", "title": "Openwell submersible pumpsets", "desc": "Openwell submersible pumpsets.", "cat": "CAT-PUMPS"},
    {"id": "IS-780", "num": "IS 780 : 1984", "title": "Sluice valves for water works purposes (50 to 300 mm size)", "desc": "Sluice valves (50-300 mm).", "cat": "CAT-VALVES"},
    {"id": "IS-2906", "num": "IS 2906 : 1984", "title": "Specification for sluice valves for water works purposes (350 to 1200 mm size)", "desc": "Sluice valves (350-1200 mm).", "cat": "CAT-VALVES"},
    {"id": "IS-1703", "num": "IS 1703 : 2000", "title": "Water fittings: Copper alloy float valves (horizontal plunger type)", "desc": "Copper alloy float valves.", "cat": "CAT-VALVES"},
    {"id": "IS-2692", "num": "IS 2692 : 1989", "title": "Ferrules for water services", "desc": "Ferrules for water services.", "cat": "CAT-PIPES"},
    {"id": "IS-1879", "num": "IS 1879 : 2010", "title": "Malleable cast iron pipe fittings", "desc": "Malleable cast iron pipe fittings.", "cat": "CAT-PIPES"},

    # Water / Sanitation (7)
    {"id": "IS-774", "num": "IS 774 : 2004", "title": "Flushing cisterns for water closets and urinals", "desc": "Flushing cisterns.", "cat": "CAT-SANITARY"},
    {"id": "IS-2556-1", "num": "IS 2556 (Part 1) : 1994", "title": "Vitreous sanitary appliances (vitreous china) - General requirements", "desc": "Vitreous sanitary appliances general req.", "cat": "CAT-SANITARY"},
    {"id": "IS-2556-2", "num": "IS 2556 (Part 2) : 2004", "title": "Vitreous sanitary appliances: Wash-down water closets", "desc": "Wash-down water closets.", "cat": "CAT-SANITARY"},
    {"id": "IS-2556-3", "num": "IS 2556 (Part 3) : 2004", "title": "Vitreous sanitary appliances: Squatting pans", "desc": "Squatting pans.", "cat": "CAT-SANITARY"},
    {"id": "IS-2556-4", "num": "IS 2556 (Part 4) : 2004", "title": "Vitreous sanitary appliances: Wash basins", "desc": "Wash basins.", "cat": "CAT-SANITARY"},
    {"id": "IS-1742", "num": "IS 1742 : 1983", "title": "Code of practice for building drainage", "desc": "Code of practice for building drainage.", "cat": "CAT-SANITARY"},
    {"id": "IS-1239-1", "num": "IS 1239 (Part 1) : 2004", "title": "Steel tubes, tubulars and other wrought steel fittings: Part 1 Steel tubes", "desc": "Steel tubes for plumbing.", "cat": "CAT-PIPES"},

    # Industrial Safety / Fire / PPE (7)
    {"id": "IS-884", "num": "IS 884 : 1985", "title": "Specification for first-aid hose-reel for fire fighting", "desc": "First-aid hose-reel for fire fighting.", "cat": "CAT-FIRE"},
    {"id": "IS-903", "num": "IS 903 : 1993", "title": "Fire hose delivery couplings, branch pipe, nozzles and nozzle spanner", "desc": "Fire hose couplings and nozzles.", "cat": "CAT-FIRE"},
    {"id": "IS-937", "num": "IS 937 : 1981", "title": "Specification for washers for water fittings for fire fighting purposes", "desc": "Washers for fire fighting water fittings.", "cat": "CAT-FIRE"},
    {"id": "IS-5983", "num": "IS 5983 : 1980", "title": "Specification for eye protectors", "desc": "Eye protectors for industrial safety.", "cat": "CAT-PPE"},
    {"id": "IS-14352", "num": "IS 14352 : 1996", "title": "Fireman's axes", "desc": "Fireman's axes specification.", "cat": "CAT-FIRE"},
    {"id": "IS-4912", "num": "IS 4912 : 1978", "title": "Safety requirements for floor and wall openings, railings and toe boards", "desc": "Safety requirements for floor and wall openings.", "cat": "CAT-PPE"},
    {"id": "IS-9944", "num": "IS 9944 : 1992", "title": "Natural and synthetic rubber mackintoshes", "desc": "Rubber mackintoshes for protection.", "cat": "CAT-PPE"},

    # HVAC / Refrigeration (5)
    {"id": "IS-1391-1", "num": "IS 1391 (Part 1) : 2017", "title": "Room air conditioners - Unitary air conditioners", "desc": "Unitary room air conditioners.", "cat": "CAT-HVAC"},
    {"id": "IS-1391-2", "num": "IS 1391 (Part 2) : 2018", "title": "Room air conditioners - Split air conditioners", "desc": "Split room air conditioners.", "cat": "CAT-HVAC"},
    {"id": "IS-11338", "num": "IS 11338 : 1985", "title": "Testing and performance rating of room air-conditioners", "desc": "Testing of room air-conditioners.", "cat": "CAT-HVAC"},
    {"id": "IS-659", "num": "IS 659 : 1964", "title": "Safety code for air conditioning", "desc": "Safety code for air conditioning.", "cat": "CAT-HVAC"},
    {"id": "IS-3103", "num": "IS 3103 : 1975", "title": "Code of practice for industrial ventilation", "desc": "Code of practice for industrial ventilation.", "cat": "CAT-HVAC"},

    # Lighting (4)
    {"id": "IS-1913-1", "num": "IS 1913 (Part 1) : 1978", "title": "General and safety requirements for luminaires: Tubular fluorescent lamps", "desc": "Luminaires for fluorescent lamps.", "cat": "CAT-LIGHTING"},
    {"id": "IS-10322-1", "num": "IS 10322 (Part 1) : 2014", "title": "Luminaires - Part 1: General requirements and tests", "desc": "General requirements for luminaires.", "cat": "CAT-LIGHTING"},
    {"id": "IS-10322-5-1", "num": "IS 10322 (Part 5/Sec 1) : 2012", "title": "Luminaires - Fixed general purpose luminaires", "desc": "Fixed general purpose luminaires.", "cat": "CAT-LIGHTING"},
    {"id": "IS-10322-5-2", "num": "IS 10322 (Part 5/Sec 2) : 2012", "title": "Luminaires - Recessed luminaires", "desc": "Recessed luminaires.", "cat": "CAT-LIGHTING"},

    # Civil / Construction (5)
    {"id": "IS-1200-1", "num": "IS 1200 (Part 1) : 1992", "title": "Method of measurement of building and civil engineering works: Earthwork", "desc": "Measurement of earthwork.", "cat": "CAT-MEASUREMENT"},
    {"id": "IS-1200-2", "num": "IS 1200 (Part 2) : 1974", "title": "Method of measurement: Concrete works", "desc": "Measurement of concrete works.", "cat": "CAT-MEASUREMENT"},
    {"id": "IS-3370-1", "num": "IS 3370 (Part 1) : 2009", "title": "Code of practice for concrete structures for the storage of liquids: General requirements", "desc": "Concrete structures for liquid storage.", "cat": "CAT-CONCRETE"},
    {"id": "IS-3370-2", "num": "IS 3370 (Part 2) : 2009", "title": "Code of practice for concrete structures for the storage of liquids: Reinforced concrete structures", "desc": "Reinforced concrete liquid storage.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1343", "num": "IS 1343 : 2012", "title": "Prestressed concrete - Code of practice", "desc": "Code of practice for prestressed concrete.", "cat": "CAT-CONCRETE"},

    # Paints / Hardware (4)
    {"id": "IS-2074", "num": "IS 2074 : 1992", "title": "Ready mixed paint, air drying, red oxide-zinc chrome, priming", "desc": "Red oxide-zinc chrome primer paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-104", "num": "IS 104 : 2017", "title": "Ready mixed paint, brushing, zinc chrome, priming", "desc": "Zinc chrome primer paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-133", "num": "IS 133 : 2013", "title": "Enamel, interior: (a) undercoating (b) finishing", "desc": "Interior enamel paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-205", "num": "IS 205 : 1992", "title": "Non-ferrous metal butt hinges", "desc": "Non-ferrous metal butt hinges.", "cat": "CAT-HARDWARE"}
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

# Relationships (Only matching known IDs)
relationships_to_add = [
    {"id": "REL-IS1391-IS11338", "source_id": "IS-1391-1", "target_id": "IS-11338", "type": "TEST_METHOD"},
    {"id": "REL-IS3370-IS456", "source_id": "IS-3370-1", "target_id": "IS-456", "type": "REFERENCE"},
    {"id": "REL-IS1343-IS456", "source_id": "IS-1343", "target_id": "IS-456", "type": "REFERENCE"},
    {"id": "REL-IS2556-IS2556-2", "source_id": "IS-2556-1", "target_id": "IS-2556-2", "type": "PRODUCT_STANDARD"},
    {"id": "REL-IS2026-IS2026-2", "source_id": "IS-2026-1", "target_id": "IS-2026-2", "type": "RELATED"}
]

existing_rel_ids = {r['id'] for r in data.get('standard_relationships', [])}
for r in relationships_to_add:
    if r['id'] not in existing_rel_ids:
        # Verify both exist
        all_ids = {s['id'] for s in data['standards']}
        if r['source_id'] in all_ids and r['target_id'] in all_ids:
            data.setdefault('standard_relationships', []).append(r)
            existing_rel_ids.add(r['id'])

with open(SEED_DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Batch 4 completed. Added {added} standards.")
