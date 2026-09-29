import json
import os

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# New Categories
categories_to_add = [
    {"id": "CAT-SOILS", "name": "Soils and Foundations", "description": "Methods of testing soils and foundation design.", "sector_id": "SEC-CIVIL"},
    {"id": "CAT-FASTENERS", "name": "Fasteners and Washers", "description": "Bolts, screws, nuts, and washers.", "sector_id": "SEC-MECH"},
    {"id": "CAT-FIRE", "name": "Fire Safety", "description": "Fire extinguishers, alarms, and fire safety codes.", "sector_id": "SEC-SAFE"},
    {"id": "CAT-TRANSFORMERS", "name": "Transformers", "description": "Power and distribution transformers.", "sector_id": "SEC-ELEC"}
]

existing_cat_ids = {c['id'] for c in data.get('categories', [])}
for c in categories_to_add:
    if c['id'] not in existing_cat_ids:
        data['categories'].append(c)

new_standards_data = [
    # Soils and Foundations
    {"id": "IS-2720-1", "num": "IS 2720 (Part 1) : 1983", "title": "Methods of test for soils: Part 1 Preparation of dry soil samples for various tests", "desc": "Preparation of dry soil samples.", "cat": "CAT-SOILS"},
    {"id": "IS-2720-2", "num": "IS 2720 (Part 2) : 1973", "title": "Methods of test for soils: Part 2 Determination of water content", "desc": "Determination of water content in soils.", "cat": "CAT-SOILS"},
    {"id": "IS-2720-4", "num": "IS 2720 (Part 4) : 1985", "title": "Methods of test for soils: Part 4 Grain size analysis", "desc": "Grain size analysis of soils.", "cat": "CAT-SOILS"},
    {"id": "IS-2720-5", "num": "IS 2720 (Part 5) : 1985", "title": "Methods of test for soils: Part 5 Determination of liquid and plastic limit", "desc": "Determination of liquid and plastic limit of soils.", "cat": "CAT-SOILS"},
    {"id": "IS-2911-1-1", "num": "IS 2911 (Part 1/Sec 1) : 2010", "title": "Design and construction of pile foundations - Code of practice", "desc": "Code of practice for pile foundations.", "cat": "CAT-SOILS"},
    {"id": "IS-1904", "num": "IS 1904 : 1986", "title": "Code of practice for design and construction of foundations in soils: General requirements", "desc": "General requirements for foundations.", "cat": "CAT-SOILS"},

    # Concrete and Cement
    {"id": "IS-2386-1", "num": "IS 2386 (Part 1) : 1963", "title": "Methods of test for aggregates for concrete: Part 1 Particle size and shape", "desc": "Particle size and shape of concrete aggregates.", "cat": "CAT-CONCRETE"},
    {"id": "IS-2386-2", "num": "IS 2386 (Part 2) : 1963", "title": "Methods of test for aggregates for concrete: Part 2 Estimation of deleterious materials and organic impurities", "desc": "Estimation of deleterious materials in aggregates.", "cat": "CAT-CONCRETE"},
    {"id": "IS-2386-3", "num": "IS 2386 (Part 3) : 1963", "title": "Methods of test for aggregates for concrete: Part 3 Specific gravity, density, voids, absorption and bulking", "desc": "Specific gravity and density of aggregates.", "cat": "CAT-CONCRETE"},
    {"id": "IS-2386-4", "num": "IS 2386 (Part 4) : 1963", "title": "Methods of test for aggregates for concrete: Part 4 Mechanical properties", "desc": "Mechanical properties of concrete aggregates.", "cat": "CAT-CONCRETE"},
    
    # Building Materials / Bricks / Mortar
    {"id": "IS-1200-1", "num": "IS 1200 (Part 1) : 1992", "title": "Method of measurement of building and civil engineering works: Part 1 Earthwork", "desc": "Measurement methods for earthwork.", "cat": "CAT-CONCRETE"},
    {"id": "IS-2116", "num": "IS 2116 : 1980", "title": "Sand for masonry mortars - Specification", "desc": "Specification for sand in masonry mortars.", "cat": "CAT-CONCRETE"},
    {"id": "IS-2250", "num": "IS 2250 : 1981", "title": "Code of practice for preparation and use of masonry mortars", "desc": "Preparation and use of masonry mortars.", "cat": "CAT-CONCRETE"},
    {"id": "IS-3495", "num": "IS 3495 (Parts 1 to 4) : 1992", "title": "Methods of tests of burnt clay building bricks", "desc": "Methods of tests for burnt clay building bricks.", "cat": "CAT-BRICKS"},
    {"id": "IS-2185-1", "num": "IS 2185 (Part 1) : 2005", "title": "Concrete masonry units - Specification: Part 1 Hollow and solid concrete blocks", "desc": "Hollow and solid concrete blocks.", "cat": "CAT-BRICKS"},
    {"id": "IS-15388", "num": "IS 15388 : 2003", "title": "Silica fume - Specification", "desc": "Specification for silica fume for concrete.", "cat": "CAT-CONCRETE"},

    # Electrical
    {"id": "IS-398-1", "num": "IS 398 (Part 1) : 1996", "title": "Aluminum conductors for overhead transmission purposes", "desc": "Aluminum conductors for transmission.", "cat": "CAT-CABLES"},
    {"id": "IS-398-2", "num": "IS 398 (Part 2) : 1996", "title": "Aluminum conductors, galvanized steel-reinforced", "desc": "Galvanized steel-reinforced aluminum conductors.", "cat": "CAT-CABLES"},
    {"id": "IS-1180-1", "num": "IS 1180 (Part 1) : 2014", "title": "Outdoor type oil immersed distribution transformers up to and including 2500 kVA, 33 kV", "desc": "Specification for outdoor distribution transformers.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-2026-1", "num": "IS 2026 (Part 1) : 2011", "title": "Power transformers: General", "desc": "General specification for power transformers.", "cat": "CAT-TRANSFORMERS"},
    {"id": "IS-1554-2", "num": "IS 1554 (Part 2) : 1988", "title": "PVC insulated (heavy duty) electric cables: For working voltages from 3.3 kV up to and including 11 kV", "desc": "Heavy duty PVC insulated cables for 3.3kV to 11kV.", "cat": "CAT-CABLES"},
    {"id": "IS-7098-1", "num": "IS 7098 (Part 1) : 1988", "title": "Crosslinked polyethylene insulated PVC sheathed cables: For working voltage up to and including 1100 V", "desc": "XLPE insulated PVC sheathed cables up to 1100V.", "cat": "CAT-CABLES"},

    # Pipes
    {"id": "IS-3589", "num": "IS 3589 : 2001", "title": "Steel pipes for water and sewage (168.3 to 2540 mm outside diameter)", "desc": "Large diameter steel pipes for water and sewage.", "cat": "CAT-PIPES"},
    {"id": "IS-14735", "num": "IS 14735 : 1999", "title": "Unplasticized PVC injection moulded fittings for non-pressure underground drainage and sewerage", "desc": "uPVC fittings for underground drainage.", "cat": "CAT-PIPES"},
    {"id": "IS-783", "num": "IS 783 : 1985", "title": "Code of practice for laying of concrete pipes", "desc": "Laying of concrete pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-3114", "num": "IS 3114 : 1994", "title": "Code of practice for laying of cast iron pipes", "desc": "Laying of cast iron pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-1536", "num": "IS 1536 : 2001", "title": "Centrifugally cast (spun) iron pressure pipes for water, gas and sewage", "desc": "Spun iron pressure pipes.", "cat": "CAT-PIPES"},

    # Mechanical Fasteners
    {"id": "IS-1364-1", "num": "IS 1364 (Part 1) : 2002", "title": "Hexagon head bolts, screws and nuts of product grades A and B: Part 1 Hexagon head bolts (size range M1.6 to M64)", "desc": "Hexagon head bolts grades A and B.", "cat": "CAT-FASTENERS"},
    {"id": "IS-1364-2", "num": "IS 1364 (Part 2) : 2002", "title": "Hexagon head bolts, screws and nuts of product grades A and B: Part 2 Hexagon head screws (size range M1.6 to M64)", "desc": "Hexagon head screws grades A and B.", "cat": "CAT-FASTENERS"},
    {"id": "IS-2016", "num": "IS 2016 : 1967", "title": "Plain washers", "desc": "Specification for plain washers.", "cat": "CAT-FASTENERS"},
    {"id": "IS-1367-3", "num": "IS 1367 (Part 3) : 2002", "title": "Technical supply conditions for threaded steel fasteners: Part 3 Mechanical properties", "desc": "Mechanical properties of carbon and alloy steel fasteners.", "cat": "CAT-FASTENERS"},

    # Safety
    {"id": "IS-11714", "num": "IS 11714 : 1986", "title": "Specification for safety face shields", "desc": "Specification for safety face shields.", "cat": "CAT-PPE"},
    {"id": "IS-1989-1", "num": "IS 1989 (Part 1) : 1986", "title": "Leather safety boots and shoes: Part 1 For miners", "desc": "Leather safety boots for miners.", "cat": "CAT-PPE"},
    {"id": "IS-10592", "num": "IS 10592 : 1982", "title": "Specification for industrial emergency showers, eye and face fountains and combination units", "desc": "Emergency showers and eye fountains.", "cat": "CAT-PPE"},
    {"id": "IS-14489", "num": "IS 14489 : 2018", "title": "Code of practice on occupational safety and health audit", "desc": "Occupational safety and health audit guidelines.", "cat": "CAT-PPE"},

    # Paints
    {"id": "IS-101-1-1", "num": "IS 101 (Part 1/Sec 1) : 1986", "title": "Methods of sampling and test for paints, varnishes and related products", "desc": "Test methods for paints and varnishes.", "cat": "CAT-PAINTS"},
    {"id": "IS-2074", "num": "IS 2074 : 1992", "title": "Ready mixed paint, air drying, red oxide-zinc chrome, priming - Specification", "desc": "Red oxide-zinc chrome priming paint.", "cat": "CAT-PAINTS"},

    # Fire Safety
    {"id": "IS-2190", "num": "IS 2190 : 2010", "title": "Selection, installation and maintenance of first-aid fire extinguishers - Code of practice", "desc": "Code of practice for fire extinguishers.", "cat": "CAT-FIRE"},
    {"id": "IS-15683", "num": "IS 15683 : 2018", "title": "Portable fire extinguishers - Performance and construction - Specification", "desc": "Specification for portable fire extinguishers.", "cat": "CAT-FIRE"},
    {"id": "IS-2189", "num": "IS 2189 : 2008", "title": "Selection, installation and maintenance of automatic fire detection and alarm system - Code of practice", "desc": "Code of practice for fire detection systems.", "cat": "CAT-FIRE"}
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

# New Keywords
keywords_to_add = [
    {"id": "KW-SOIL", "word": "soil"},
    {"id": "KW-FOUNDATION", "word": "foundation"},
    {"id": "KW-AGGREGATE", "word": "aggregate"},
    {"id": "KW-FASTENER", "word": "fastener"},
    {"id": "KW-BOLT", "word": "bolt"},
    {"id": "KW-WASHER", "word": "washer"},
    {"id": "KW-FIRE", "word": "fire"},
    {"id": "KW-EXTINGUISHER", "word": "extinguisher"},
    {"id": "KW-TRANSFORMER", "word": "transformer"}
]

existing_kw_words = {k['word']: k['id'] for k in data.get('keywords', [])}
for k in keywords_to_add:
    if k['word'] not in existing_kw_words:
        data['keywords'].append(k)
        existing_kw_words[k['word']] = k['id']

# Map keywords to standards
standard_keyword_mappings = {
    "IS-2720-1": ["soil", "foundation", "construction"],
    "IS-2720-2": ["soil", "foundation"],
    "IS-2720-4": ["soil", "foundation"],
    "IS-2720-5": ["soil", "foundation"],
    "IS-2911-1-1": ["foundation", "construction"],
    "IS-1904": ["foundation", "construction"],
    "IS-2386-1": ["aggregate", "concrete", "construction"],
    "IS-2386-2": ["aggregate", "concrete"],
    "IS-2386-3": ["aggregate", "concrete"],
    "IS-2386-4": ["aggregate", "concrete"],
    "IS-1200-1": ["construction"],
    "IS-2116": ["construction"],
    "IS-2250": ["construction"],
    "IS-3495": ["construction"],
    "IS-2185-1": ["concrete", "construction"],
    "IS-15388": ["concrete", "construction"],
    "IS-398-1": ["cable", "electrical"],
    "IS-398-2": ["cable", "electrical", "steel"],
    "IS-1180-1": ["transformer", "electrical"],
    "IS-2026-1": ["transformer", "electrical"],
    "IS-1554-2": ["cable", "electrical", "pvc"],
    "IS-7098-1": ["cable", "electrical"],
    "IS-3589": ["pipes", "steel", "plumbing"],
    "IS-14735": ["pipes", "pvc", "plumbing"],
    "IS-783": ["pipes", "concrete", "plumbing"],
    "IS-3114": ["pipes", "plumbing"],
    "IS-1536": ["pipes", "plumbing"],
    "IS-1364-1": ["fastener", "bolt", "steel"],
    "IS-1364-2": ["fastener", "bolt", "steel"],
    "IS-2016": ["fastener", "washer"],
    "IS-1367-3": ["fastener", "steel"],
    "IS-11714": ["safety", "ppe"],
    "IS-1989-1": ["safety", "ppe"],
    "IS-10592": ["safety", "ppe"],
    "IS-14489": ["safety"],
    "IS-101-1-1": ["paint", "coating"],
    "IS-2074": ["paint", "coating"],
    "IS-2190": ["fire", "extinguisher", "safety"],
    "IS-15683": ["fire", "extinguisher", "safety"],
    "IS-2189": ["fire", "safety"]
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

print(f"Added {len(new_standards_data)} new standards to standards.json!")
