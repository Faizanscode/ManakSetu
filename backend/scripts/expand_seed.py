import json
import os
import datetime

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# New Sectors
sectors_to_add = [
    {"id": "SEC-ELEC", "name": "Electrical Engineering", "description": "Electrical systems, components, and equipment."},
    {"id": "SEC-MECH", "name": "Mechanical Engineering", "description": "Mechanical systems, machinery, and valves."},
    {"id": "SEC-SAFE", "name": "Industrial Safety", "description": "Personal protective equipment and safety standards."},
    {"id": "SEC-PLUMB", "name": "Water and Sanitation", "description": "Plumbing, pipes, and sanitation systems."}
]
existing_sector_ids = {s['id'] for s in data.get('sectors', [])}
for s in sectors_to_add:
    if s['id'] not in existing_sector_ids:
        data['sectors'].append(s)

# New Categories
categories_to_add = [
    {"id": "CAT-TILES", "name": "Tiles and Flooring", "description": "Ceramic, vitrified, and other flooring tiles.", "sector_id": "SEC-CIVIL"},
    {"id": "CAT-PAINTS", "name": "Paints and Coatings", "description": "Paints, enamels, and varnishes.", "sector_id": "SEC-CIVIL"},
    {"id": "CAT-WOOD", "name": "Doors, Windows, and Wood", "description": "Plywood, flush doors, frames.", "sector_id": "SEC-CIVIL"},
    {"id": "CAT-PIPES", "name": "Pipes and Plumbing", "description": "PVC, steel pipes, and sanitaryware.", "sector_id": "SEC-PLUMB"},
    {"id": "CAT-CABLES", "name": "Electrical Cables", "description": "Wiring and insulated cables.", "sector_id": "SEC-ELEC"},
    {"id": "CAT-ELECEQ", "name": "Electrical Equipment", "description": "Switches, appliances, and installations.", "sector_id": "SEC-ELEC"},
    {"id": "CAT-VALVES", "name": "Valves and Fittings", "description": "Sluice, butterfly, and check valves.", "sector_id": "SEC-MECH"},
    {"id": "CAT-PPE", "name": "Personal Protective Equipment", "description": "Helmets, footwear, and safety gear.", "sector_id": "SEC-SAFE"}
]
existing_cat_ids = {c['id'] for c in data.get('categories', [])}
for c in categories_to_add:
    if c['id'] not in existing_cat_ids:
        data['categories'].append(c)

# New Standards
new_standards_data = [
    # Tiles
    {"id": "IS-15622", "num": "IS 15622 : 2017", "title": "Pressed Ceramic Tiles — Specification", "desc": "Specification for pressed ceramic tiles (glazed and unglazed) for walls and floors.", "cat": "CAT-TILES"},
    {"id": "IS-13712", "num": "IS 13712 : 2019", "title": "Ceramic Tiles — Definitions, Classifications, Characteristics and Marking", "desc": "Definitions and classification for ceramic tiles.", "cat": "CAT-TILES"},
    {"id": "IS-504", "num": "IS 504 : 2020", "title": "Ceramic Glazed Tiles — Specification", "desc": "Specification specifically covering ceramic glazed tiles.", "cat": "CAT-TILES"},
    {"id": "IS-13630", "num": "IS 13630 (Part 1) : 2019", "title": "Ceramic Tiles — Methods of Test, Part 1", "desc": "Test methods for determining dimensions and surface quality of ceramic tiles.", "cat": "CAT-TILES"},
    {"id": "IS-4457", "num": "IS 4457 : 2007", "title": "Specification for Ceramic Unglazed Vitreous Acid-Resisting Tiles", "desc": "Specification for acid-resisting ceramic unglazed vitreous tiles.", "cat": "CAT-TILES"},
    
    # Paints
    {"id": "IS-15489", "num": "IS 15489 : 2004", "title": "Plastic Emulsion Paint — Specification", "desc": "Specification for plastic emulsion paint for interior and exterior use.", "cat": "CAT-PAINTS"},
    {"id": "IS-2932", "num": "IS 2932 : 2003", "title": "Enamel, Synthetic, Exterior: (a) Undercoating (b) Finishing — Specification", "desc": "Specification for synthetic enamel paint for exterior use.", "cat": "CAT-PAINTS"},
    {"id": "IS-2339", "num": "IS 2339 : 2020", "title": "Aluminium Paint for General Purposes, in Dual Container — Specification", "desc": "Specification for dual-container aluminium paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-133", "num": "IS 133 : 2013", "title": "Enamel, Interior: (a) Undercoating (b) Finishing — Specification", "desc": "Specification for interior enamel paint.", "cat": "CAT-PAINTS"},
    {"id": "IS-5410", "num": "IS 5410 : 1992", "title": "Cement Paint — Specification", "desc": "Specification for cement paint for exterior wall finishes.", "cat": "CAT-PAINTS"},

    # Pipes
    {"id": "IS-4985", "num": "IS 4985 : 2021", "title": "Unplasticized PVC (uPVC) Pipes for Potable Water Supplies — Specification", "desc": "Specification for uPVC pipes used in potable water systems.", "cat": "CAT-PIPES"},
    {"id": "IS-15328", "num": "IS 15328 : 2003", "title": "Unplasticized non-pressure PVC (PVC-U) Pipes for Underground Drainage", "desc": "Specification for PVC-U pipes for sewerage and drainage.", "cat": "CAT-PIPES"},
    {"id": "IS-17546", "num": "IS 17546 : 2021", "title": "Chlorinated Polyvinyl Chloride (CPVC) Pipe Fittings", "desc": "Specification for CPVC fittings for hot and cold water plumbing.", "cat": "CAT-PIPES"},
    {"id": "IS-1239-1", "num": "IS 1239 (Part 1) : 2004", "title": "Steel Tubes, Tubulars and Other Wrought Steel Fittings", "desc": "Steel tubes and fittings for water, gas, and air.", "cat": "CAT-PIPES"},
    {"id": "IS-17875", "num": "IS 17875 : 2022", "title": "Stainless Steel Seamless Pipes and Tubes", "desc": "Stainless steel seamless pipes for general service.", "cat": "CAT-PIPES"},
    {"id": "IS-17650-1", "num": "IS 17650 (Part 1) : 2021", "title": "Water Efficient Plumbing Products — Sanitaryware", "desc": "Efficiency specifications for sanitary plumbing products.", "cat": "CAT-PIPES"},
    {"id": "IS-5329", "num": "IS 5329 : 1983", "title": "Code of Practice for Sanitary Pipe Work Above Ground for Buildings", "desc": "Guidelines for above ground sanitary pipe installations.", "cat": "CAT-PIPES"},

    # Electrical
    {"id": "IS-694", "num": "IS 694 : 2010", "title": "PVC Insulated Cables for Working Voltages up to 1,100 V", "desc": "Specification for low voltage PVC insulated cables.", "cat": "CAT-CABLES"},
    {"id": "IS-1554-1", "num": "IS 1554 (Part 1) : 1988", "title": "PVC Insulated (Heavy Duty) Electric Cables", "desc": "Heavy duty electric cables for up to 1100 V.", "cat": "CAT-CABLES"},
    {"id": "IS-732", "num": "IS 732 : 2019", "title": "Code of Practice for Electrical Wiring Installations", "desc": "Standard practices for wiring installations.", "cat": "CAT-ELECEQ"},
    {"id": "IS-3043", "num": "IS 3043 : 2018", "title": "Code of Practice for Earthing", "desc": "Guidelines for electrical earthing systems.", "cat": "CAT-ELECEQ"},
    {"id": "IS-302-1", "num": "IS 302 (Part 1) : 2008", "title": "Safety of Household and Similar Electrical Appliances", "desc": "General safety requirements for electrical appliances.", "cat": "CAT-ELECEQ"},
    {"id": "IS-1293", "num": "IS 1293 : 2019", "title": "Plugs and Socket-Outlets of Rated Voltage up to 250 Volts", "desc": "Specification for standard electrical plugs and sockets.", "cat": "CAT-ELECEQ"},
    {"id": "IS-374", "num": "IS 374 : 1979", "title": "Electric Ceiling Type Fans and Regulators", "desc": "Specification for ceiling fans.", "cat": "CAT-ELECEQ"},
    {"id": "IS-2705", "num": "IS 2705 : 1992", "title": "Current Transformers", "desc": "Specification for current transformers for electrical measurement.", "cat": "CAT-ELECEQ"},

    # Safety
    {"id": "IS-2925", "num": "IS 2925 : 1984", "title": "Industrial Safety Helmets — Specification", "desc": "Requirements for safety helmets used in industry and construction.", "cat": "CAT-PPE"},
    {"id": "IS-15298-2", "num": "IS 15298 (Part 2) : 2016", "title": "Personal Protective Equipment — Safety Footwear", "desc": "Specification for safety footwear.", "cat": "CAT-PPE"},
    {"id": "IS-9473", "num": "IS 9473 : 2002", "title": "Respiratory Protective Devices — Filtering Half Masks", "desc": "Specification for protective face masks against particles.", "cat": "CAT-PPE"},
    {"id": "IS-3521", "num": "IS 3521 : 1999", "title": "Industrial Safety Belts and Harnesses", "desc": "Specification for safety belts and fall arrest harnesses.", "cat": "CAT-PPE"},
    {"id": "IS-1179", "num": "IS 1179 : 1967", "title": "Equipment for Eye and Face Protection during Welding", "desc": "Safety requirements for welding protection gear.", "cat": "CAT-PPE"},

    # Valves
    {"id": "IS-778", "num": "IS 778 : 1984", "title": "Copper Alloy Gate, Globe and Check Valves", "desc": "Specification for small copper alloy valves.", "cat": "CAT-VALVES"},
    {"id": "IS-14846", "num": "IS 14846 : 2000", "title": "Sluice Valves for Water Works Purposes", "desc": "Specification for sluice valves (gate valves) used in water works.", "cat": "CAT-VALVES"},
    {"id": "IS-13095", "num": "IS 13095 : 1991", "title": "Butterfly Valves for General Purposes", "desc": "Specification for butterfly valves.", "cat": "CAT-VALVES"},
    {"id": "IS-9338", "num": "IS 9338 : 1984", "title": "Cast Iron Screw-Down Stop Valves and Stop and Check Valves", "desc": "Specification for cast iron stop valves.", "cat": "CAT-VALVES"},
    {"id": "IS-5312-1", "num": "IS 5312 (Part 1) : 2004", "title": "Swing Check Type Reflux (Non-Return) Valves", "desc": "Specification for swing check valves.", "cat": "CAT-VALVES"},

    # Civil additional
    {"id": "IS-13920", "num": "IS 13920 : 2016", "title": "Ductile Design and Detailing of Reinforced Concrete Structures", "desc": "Code for ductile design of structures subject to seismic forces.", "cat": "CAT-CONCRETE"},
    {"id": "IS-875-1", "num": "IS 875 (Part 1) : 1987", "title": "Code of Practice for Design Loads - Dead Loads", "desc": "Design loads for buildings and structures.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1893-1", "num": "IS 1893 (Part 1) : 2016", "title": "Criteria for Earthquake Resistant Design of Structures", "desc": "Earthquake resistant design criteria.", "cat": "CAT-CONCRETE"},
    {"id": "IS-432-1", "num": "IS 432 (Part 1) : 1982", "title": "Mild Steel and Medium Tensile Steel Bars", "desc": "Specification for mild steel reinforcement bars.", "cat": "CAT-STEEL"},
    {"id": "IS-280", "num": "IS 280 : 2006", "title": "Mild Steel Wire for General Engineering Purposes", "desc": "Specification for mild steel wire.", "cat": "CAT-STEEL"},

    # Doors/Wood
    {"id": "IS-2202-1", "num": "IS 2202 (Part 1) : 1991", "title": "Wooden Flush Door Shutters", "desc": "Specification for wooden flush doors.", "cat": "CAT-WOOD"},
    {"id": "IS-303", "num": "IS 303 : 1989", "title": "Plywood for General Purposes", "desc": "Specification for general purpose plywood.", "cat": "CAT-WOOD"},
    {"id": "IS-1038", "num": "IS 1038 : 1983", "title": "Steel Doors, Windows and Ventilators", "desc": "Specification for steel doors and windows.", "cat": "CAT-WOOD"},
    {"id": "IS-1948", "num": "IS 1948 : 1961", "title": "Aluminium Doors, Windows and Ventilators", "desc": "Specification for aluminium doors and windows.", "cat": "CAT-WOOD"},
    {"id": "IS-4021", "num": "IS 4021 : 1995", "title": "Timber Door, Window and Ventilator Frames", "desc": "Specification for timber frames for doors and windows.", "cat": "CAT-WOOD"}
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
    {"id": "KW-TILE", "word": "tiles"},
    {"id": "KW-FLOORING", "word": "flooring"},
    {"id": "KW-PAINT", "word": "paint"},
    {"id": "KW-COATING", "word": "coating"},
    {"id": "KW-PIPE", "word": "pipes"},
    {"id": "KW-PVC", "word": "pvc"},
    {"id": "KW-PLUMBING", "word": "plumbing"},
    {"id": "KW-CABLE", "word": "cable"},
    {"id": "KW-ELECTRICAL", "word": "electrical"},
    {"id": "KW-SAFETY", "word": "safety"},
    {"id": "KW-PPE", "word": "ppe"},
    {"id": "KW-VALVE", "word": "valve"},
    {"id": "KW-WOOD", "word": "wood"},
    {"id": "KW-DOOR", "word": "door"},
    {"id": "KW-CERAMIC", "word": "ceramic"}
]
existing_kw_words = {k['word']: k['id'] for k in data.get('keywords', [])}
for k in keywords_to_add:
    if k['word'] not in existing_kw_words:
        data['keywords'].append(k)
        existing_kw_words[k['word']] = k['id']

# Map keywords to standards
standard_keyword_mappings = {
    "IS-15622": ["tiles", "ceramic", "flooring", "construction"],
    "IS-13712": ["tiles", "ceramic", "flooring"],
    "IS-504": ["tiles", "ceramic"],
    "IS-13630": ["tiles", "ceramic"],
    "IS-4457": ["tiles", "ceramic", "flooring"],
    "IS-15489": ["paint", "coating", "construction"],
    "IS-2932": ["paint", "coating"],
    "IS-2339": ["paint", "coating"],
    "IS-133": ["paint", "coating"],
    "IS-5410": ["paint", "coating", "cement"],
    "IS-4985": ["pipes", "pvc", "plumbing"],
    "IS-15328": ["pipes", "pvc", "plumbing"],
    "IS-17546": ["pipes", "pvc", "plumbing"],
    "IS-1239-1": ["pipes", "steel", "plumbing"],
    "IS-17875": ["pipes", "steel", "plumbing"],
    "IS-17650-1": ["plumbing"],
    "IS-5329": ["pipes", "plumbing", "construction"],
    "IS-694": ["cable", "electrical", "pvc"],
    "IS-1554-1": ["cable", "electrical", "pvc"],
    "IS-732": ["electrical", "construction"],
    "IS-3043": ["electrical"],
    "IS-302-1": ["electrical", "safety"],
    "IS-1293": ["electrical"],
    "IS-374": ["electrical"],
    "IS-2705": ["electrical"],
    "IS-2925": ["safety", "ppe"],
    "IS-15298-2": ["safety", "ppe"],
    "IS-9473": ["safety", "ppe"],
    "IS-3521": ["safety", "ppe"],
    "IS-1179": ["safety", "ppe"],
    "IS-778": ["valve", "plumbing"],
    "IS-14846": ["valve", "plumbing"],
    "IS-13095": ["valve", "plumbing"],
    "IS-9338": ["valve", "plumbing"],
    "IS-5312-1": ["valve", "plumbing"],
    "IS-13920": ["concrete", "construction"],
    "IS-875-1": ["construction"],
    "IS-1893-1": ["construction"],
    "IS-432-1": ["steel", "construction"],
    "IS-280": ["steel"],
    "IS-2202-1": ["wood", "door", "construction"],
    "IS-303": ["wood", "construction"],
    "IS-1038": ["door", "steel", "construction"],
    "IS-1948": ["door", "construction"],
    "IS-4021": ["wood", "door", "construction"]
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
