import json
import os

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# New Categories
categories_to_add = [
    {"id": "CAT-HVAC", "name": "HVAC and Refrigeration", "description": "Air conditioning and refrigeration systems.", "sector_id": "SEC-MECH"},
    {"id": "CAT-LIGHTING", "name": "Lighting and Luminaires", "description": "Luminaires, indoor and outdoor lighting.", "sector_id": "SEC-ELEC"}
]

existing_cat_ids = {c['id'] for c in data.get('categories', [])}
for c in categories_to_add:
    if c['id'] not in existing_cat_ids:
        data['categories'].append(c)

new_standards_data = [
    # Civil / Construction (10)
    {"id": "IS-2911-1-2", "num": "IS 2911 (Part 1/Sec 2) : 2010", "title": "Design and construction of pile foundations - Bored cast-in-situ concrete piles", "desc": "Bored cast-in-situ concrete piles.", "cat": "CAT-SOILS"},
    {"id": "IS-2911-1-3", "num": "IS 2911 (Part 1/Sec 3) : 2010", "title": "Design and construction of pile foundations - Driven precast concrete piles", "desc": "Driven precast concrete piles.", "cat": "CAT-SOILS"},
    {"id": "IS-2911-1-4", "num": "IS 2911 (Part 1/Sec 4) : 2010", "title": "Design and construction of pile foundations - Bored precast concrete piles", "desc": "Bored precast concrete piles.", "cat": "CAT-SOILS"},
    {"id": "IS-2911-2", "num": "IS 2911 (Part 2) : 1980", "title": "Design and construction of pile foundations - Timber piles", "desc": "Timber piles.", "cat": "CAT-SOILS"},
    {"id": "IS-2911-3", "num": "IS 2911 (Part 3) : 1980", "title": "Design and construction of pile foundations - Under-reamed piles", "desc": "Under-reamed piles.", "cat": "CAT-SOILS"},
    {"id": "IS-2911-4", "num": "IS 2911 (Part 4) : 2013", "title": "Design and construction of pile foundations - Load test on piles", "desc": "Load test on piles.", "cat": "CAT-SOILS"},
    {"id": "IS-1080", "num": "IS 1080 : 1985", "title": "Code of practice for design and construction of shallow foundations in soils (other than raft, ring and shell)", "desc": "Code of practice for shallow foundations.", "cat": "CAT-SOILS"},
    {"id": "IS-2950-1", "num": "IS 2950 (Part 1) : 1981", "title": "Code of practice for design and construction of raft foundations", "desc": "Code of practice for raft foundations.", "cat": "CAT-SOILS"},
    {"id": "IS-14458-1", "num": "IS 14458 (Part 1) : 1998", "title": "Retaining wall for hill area - Guidelines - Selection of type of wall", "desc": "Guidelines for retaining walls in hill areas.", "cat": "CAT-SOILS"},
    {"id": "IS-14458-2", "num": "IS 14458 (Part 2) : 1997", "title": "Retaining wall for hill area - Guidelines - Design of retaining/breast walls", "desc": "Design of retaining/breast walls.", "cat": "CAT-SOILS"},

    # Building Materials / Concrete / Masonry (8)
    {"id": "IS-650", "num": "IS 650 : 1991", "title": "Standard sand for testing of cement", "desc": "Specification for standard sand.", "cat": "CAT-CONCRETE"},
    {"id": "IS-5513", "num": "IS 5513 : 1996", "title": "Vicat apparatus - Specification", "desc": "Specification for Vicat apparatus for cement testing.", "cat": "CAT-CONCRETE"},
    {"id": "IS-5514", "num": "IS 5514 : 1996", "title": "Apparatus used in Le-Chatelier test - Specification", "desc": "Specification for Le-Chatelier apparatus.", "cat": "CAT-CONCRETE"},
    {"id": "IS-10086", "num": "IS 10086 : 1982", "title": "Specification for moulds for use in tests of cement and concrete", "desc": "Specification for moulds for cement testing.", "cat": "CAT-CONCRETE"},
    {"id": "IS-10510", "num": "IS 10510 : 1983", "title": "Specification for vee-bee consistometer", "desc": "Specification for vee-bee consistometer.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1199-1", "num": "IS 1199 (Part 1) : 2018", "title": "Fresh concrete - Methods of sampling, testing and analysis", "desc": "Methods of sampling fresh concrete.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1199-2", "num": "IS 1199 (Part 2) : 2018", "title": "Fresh concrete - Determination of properties of fresh concrete", "desc": "Determination of properties of fresh concrete.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1199-3", "num": "IS 1199 (Part 3) : 2018", "title": "Fresh concrete - Determination of workability", "desc": "Determination of workability of fresh concrete.", "cat": "CAT-CONCRETE"},

    # Water / Plumbing / Sanitation (6)
    {"id": "IS-1239-2", "num": "IS 1239 (Part 2) : 2011", "title": "Steel tubes, tubulars and other wrought steel fittings - Mild steel tubulars and other wrought steel pipe fittings", "desc": "Wrought steel pipe fittings.", "cat": "CAT-PIPES"},
    {"id": "IS-4736", "num": "IS 4736 : 1986", "title": "Hot-dip zinc coatings on mild steel tubes", "desc": "Hot-dip zinc coatings for steel tubes.", "cat": "CAT-PIPES"},
    {"id": "IS-7328", "num": "IS 7328 : 1992", "title": "High density polyethylene materials for moulding and extrusion", "desc": "HDPE materials specification.", "cat": "CAT-PIPES"},
    {"id": "IS-4984", "num": "IS 4984 : 2016", "title": "High density polyethylene pipes for water supply", "desc": "HDPE pipes for water supply.", "cat": "CAT-PIPES"},
    {"id": "IS-14333", "num": "IS 14333 : 1996", "title": "High density polyethylene pipes for sewerage", "desc": "HDPE pipes for sewerage.", "cat": "CAT-PIPES"},
    {"id": "IS-12288", "num": "IS 12288 : 1987", "title": "Code of practice for use and laying of ductile iron pipes", "desc": "Code of practice for ductile iron pipes.", "cat": "CAT-PIPES"},

    # Electrical / Power / Wiring (7)
    {"id": "IS-2026-2", "num": "IS 2026 (Part 2) : 2010", "title": "Power transformers: Temperature-rise", "desc": "Temperature-rise in power transformers.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-2026-3", "num": "IS 2026 (Part 3) : 2009", "title": "Power transformers: Insulation levels, dielectric tests and external clearances in air", "desc": "Insulation levels and dielectric tests.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-2026-4", "num": "IS 2026 (Part 4) : 1977", "title": "Power transformers: Terminal markings, tappings and connections", "desc": "Terminal markings and connections.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-2026-5", "num": "IS 2026 (Part 5) : 2011", "title": "Power transformers: Ability to withstand short circuit", "desc": "Ability to withstand short circuit in transformers.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-10322-1", "num": "IS 10322 (Part 1) : 2014", "title": "Luminaires: General requirements and tests", "desc": "General requirements for luminaires.", "cat": "CAT-LIGHTING"},
    {"id": "IS-10322-5-1", "num": "IS 10322 (Part 5/Sec 1) : 2012", "title": "Luminaires: Particular requirements - Fixed general purpose luminaires", "desc": "Fixed general purpose luminaires.", "cat": "CAT-LIGHTING"},
    {"id": "IS-10322-5-2", "num": "IS 10322 (Part 5/Sec 2) : 2012", "title": "Luminaires: Particular requirements - Recessed luminaires", "desc": "Recessed luminaires.", "cat": "CAT-LIGHTING"},

    # Mechanical / Engineering (6)
    {"id": "IS-1367-1", "num": "IS 1367 (Part 1) : 2014", "title": "Technical supply conditions for threaded steel fasteners: Introduction and general information", "desc": "Introduction and general info for threaded steel fasteners.", "cat": "CAT-FASTENERS"},
    {"id": "IS-1367-2", "num": "IS 1367 (Part 2) : 2002", "title": "Technical supply conditions for threaded steel fasteners: Tolerances for fasteners", "desc": "Tolerances for fasteners.", "cat": "CAT-FASTENERS"},
    {"id": "IS-1367-6", "num": "IS 1367 (Part 6) : 2018", "title": "Technical supply conditions for threaded steel fasteners: Mechanical properties and test methods for nuts", "desc": "Mechanical properties of nuts.", "cat": "CAT-FASTENERS"},
    {"id": "IS-3138", "num": "IS 3138 : 1966", "title": "Hexagonal bolts and nuts (M42 to M150)", "desc": "Hexagonal bolts and nuts large sizes.", "cat": "CAT-FASTENERS"},
    {"id": "IS-4218-1", "num": "IS 4218 (Part 1) : 2001", "title": "ISO general purpose metric screw threads: Basic profile", "desc": "Basic profile for metric screw threads.", "cat": "CAT-FASTENERS"},
    {"id": "IS-4218-2", "num": "IS 4218 (Part 2) : 2001", "title": "ISO general purpose metric screw threads: General plan", "desc": "General plan for metric screw threads.", "cat": "CAT-FASTENERS"},

    # Industrial Safety / PPE / Fire Safety (5)
    {"id": "IS-15298-1", "num": "IS 15298 (Part 1) : 2015", "title": "Personal protective equipment - Test methods for footwear", "desc": "Test methods for safety footwear.", "cat": "CAT-PPE"},
    {"id": "IS-15298-3", "num": "IS 15298 (Part 3) : 2019", "title": "Personal protective equipment - Protective footwear", "desc": "Protective footwear specification.", "cat": "CAT-PPE"},
    {"id": "IS-15298-4", "num": "IS 15298 (Part 4) : 2017", "title": "Personal protective equipment - Occupational footwear", "desc": "Occupational footwear specification.", "cat": "CAT-PPE"},
    {"id": "IS-3016", "num": "IS 3016 : 1982", "title": "Code of practice for fire precautions in welding and cutting operations", "desc": "Fire precautions in welding and cutting.", "cat": "CAT-FIRE"},
    {"id": "IS-2878", "num": "IS 2878 : 2004", "title": "Fire extinguisher, carbon dioxide type (portable and trolley mounted)", "desc": "CO2 fire extinguishers.", "cat": "CAT-FIRE"},

    # Paints / Coatings / Building Finishes (4)
    {"id": "IS-101-1-2", "num": "IS 101 (Part 1/Sec 2) : 1987", "title": "Methods of sampling and test for paints: Preliminary examination and preparation of samples", "desc": "Preparation of paint samples.", "cat": "CAT-PAINTS"},
    {"id": "IS-101-1-3", "num": "IS 101 (Part 1/Sec 3) : 1986", "title": "Methods of sampling and test for paints: Preparation of panels", "desc": "Preparation of panels for paint testing.", "cat": "CAT-PAINTS"},
    {"id": "IS-101-2-1", "num": "IS 101 (Part 2/Sec 1) : 1988", "title": "Methods of sampling and test for paints: Test on liquid paints (General and physical)", "desc": "Physical tests on liquid paints.", "cat": "CAT-PAINTS"},
    {"id": "IS-15477", "num": "IS 15477 : 2019", "title": "Adhesives for use with ceramic, mosaic and stone tiles", "desc": "Adhesives for tiles.", "cat": "CAT-TILES"},

    # Additional (4) - HVAC
    {"id": "IS-659", "num": "IS 659 : 1964", "title": "Safety code for air conditioning", "desc": "Safety code for AC systems.", "cat": "CAT-HVAC"},
    {"id": "IS-660", "num": "IS 660 : 1963", "title": "Safety code for mechanical refrigeration", "desc": "Safety code for refrigeration.", "cat": "CAT-HVAC"},
    {"id": "IS-1391-1", "num": "IS 1391 (Part 1) : 2017", "title": "Room air conditioners - Unitary air conditioners", "desc": "Unitary room air conditioners.", "cat": "CAT-HVAC"},
    {"id": "IS-1391-2", "num": "IS 1391 (Part 2) : 2018", "title": "Room air conditioners - Split air conditioners", "desc": "Split room air conditioners.", "cat": "CAT-HVAC"}
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
        
        # Version
        edition = s['num'].split(':')[-1].strip()
        data['standard_versions'].append({
            "id": f"VER-{s['id']}-01",
            "standard_id": s['id'],
            "edition": edition,
            "publication_date": f"{edition}-01-01",
            "status": "CURRENT"
        })
        
        # Scope
        data['standard_scopes'].append({
            "id": f"SCO-{s['id']}-01",
            "standard_id": s['id'],
            "scope_text": s['desc'] + " This standard covers the fundamental specifications, dimensions, and testing requirements applicable for procurement and manufacturing."
        })
        
        # Source
        data['standard_sources'].append({
            "id": f"SRC-{s['id']}-01",
            "standard_id": s['id'],
            "organization": "Bureau of Indian Standards",
            "source_type": "Official Standard",
            "url": f"https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/isdetails"
        })

# Keywords map update
keywords_to_add = [
    {"id": "KW-HVAC", "word": "hvac"},
    {"id": "KW-AIR_CONDITIONING", "word": "air conditioning"},
    {"id": "KW-REFRIGERATION", "word": "refrigeration"},
    {"id": "KW-LIGHTING", "word": "lighting"},
    {"id": "KW-LUMINAIRE", "word": "luminaire"},
]

existing_kw_words = {k['word']: k['id'] for k in data.get('keywords', [])}
for k in keywords_to_add:
    if k['word'] not in existing_kw_words:
        data['keywords'].append(k)
        existing_kw_words[k['word']] = k['id']

standard_keyword_mappings = {
    "IS-659": ["hvac", "air conditioning", "safety"],
    "IS-660": ["hvac", "refrigeration", "safety"],
    "IS-1391-1": ["hvac", "air conditioning"],
    "IS-1391-2": ["hvac", "air conditioning"],
    "IS-10322-1": ["lighting", "luminaire", "electrical"],
    "IS-10322-5-1": ["lighting", "luminaire"],
    "IS-10322-5-2": ["lighting", "luminaire"]
}

existing_sk = {(sk['standard_id'], sk['keyword_id']) for sk in data.get('standard_keywords', [])}
for std_id, words in standard_keyword_mappings.items():
    if std_id not in existing_standard_ids:
        for word in words:
            if word in existing_kw_words:
                kw_id = existing_kw_words[word]
                if (std_id, kw_id) not in existing_sk:
                    data['standard_keywords'].append({
                        "standard_id": std_id,
                        "keyword_id": kw_id
                    })
                    existing_sk.add((std_id, kw_id))

with open(SEED_DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Added {len(new_standards_data)} new standards for Batch 2.")
