import json
import os

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base', 'seed', 'standards.json')

with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_categories = [
    {"id": "CAT-MOTORS", "name": "Electric Motors", "description": "AC and DC electric motors for general and specific purposes.", "sector_id": "SEC-ELEC"},
    {"id": "CAT-VALVES", "name": "Valves and Fittings", "description": "Valves, sluice valves, check valves, and pipeline fittings.", "sector_id": "SEC-MECH"}
]

existing_cat_ids = {c['id'] for c in data.get('categories', [])}
for c in new_categories:
    if c['id'] not in existing_cat_ids:
        data['categories'].append(c)

new_standards_data = [
    # Electrical (10)
    {"id": "IS-732", "num": "IS 732 : 1989", "title": "Code of practice for electrical wiring installations", "desc": "Code of practice for electrical wiring.", "cat": "CAT-ELECEQ"},
    {"id": "IS-3043", "num": "IS 3043 : 2018", "title": "Code of practice for earthing", "desc": "Code of practice for electrical earthing.", "cat": "CAT-ELECEQ"},
    {"id": "IS-3961-1", "num": "IS 3961 (Part 1) : 1967", "title": "Recommended current ratings for cables: Paper insulated lead sheathed cables", "desc": "Current ratings for paper insulated cables.", "cat": "CAT-CABLES"},
    {"id": "IS-3961-2", "num": "IS 3961 (Part 2) : 1967", "title": "Recommended current ratings for cables: PVC insulated and PVC sheathed heavy duty cables", "desc": "Current ratings for PVC heavy duty cables.", "cat": "CAT-CABLES"},
    {"id": "IS-3961-3", "num": "IS 3961 (Part 3) : 1968", "title": "Recommended current ratings for cables: Rubber insulated cables", "desc": "Current ratings for rubber insulated cables.", "cat": "CAT-CABLES"},
    {"id": "IS-8130", "num": "IS 8130 : 2013", "title": "Conductors for insulated electrical cables and flexible cords", "desc": "Specification for conductors for cables.", "cat": "CAT-CABLES"},
    {"id": "IS-10810-1", "num": "IS 10810 (Part 1) : 1984", "title": "Methods of test for cables: Annealing test for copper", "desc": "Annealing test for copper cables.", "cat": "CAT-CABLES"},
    {"id": "IS-10810-2", "num": "IS 10810 (Part 2) : 1984", "title": "Methods of test for cables: Tensile test for aluminium wires", "desc": "Tensile test for aluminium wires.", "cat": "CAT-CABLES"},
    {"id": "IS-10810-41", "num": "IS 10810 (Part 41) : 1984", "title": "Methods of test for cables: Mass of zinc coating on steel armour", "desc": "Test for zinc coating on steel armour.", "cat": "CAT-CABLES"},
    {"id": "IS-16481", "num": "IS 16481 : 2016", "title": "LVDC electrical power distribution system", "desc": "LVDC electrical power distribution.", "cat": "CAT-ELECEQ"},

    # Mechanical (10)
    {"id": "IS-210", "num": "IS 210 : 2009", "title": "Grey iron castings - Specification", "desc": "Specification for grey iron castings.", "cat": "CAT-STEEL"},
    {"id": "IS-318", "num": "IS 318 : 1981", "title": "Leaded tin bronze ingots and castings", "desc": "Leaded tin bronze ingots.", "cat": "CAT-STEEL"},
    {"id": "IS-1537", "num": "IS 1537 : 1976", "title": "Vertically cast iron pressure pipes for water, gas and sewage", "desc": "Cast iron pressure pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-1538", "num": "IS 1538 : 1993", "title": "Cast iron fittings for pressure pipes for water, gas and sewage", "desc": "Cast iron fittings for pressure pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-2004", "num": "IS 2004 : 1991", "title": "Carbon steel forgings for general engineering purposes", "desc": "Carbon steel forgings.", "cat": "CAT-STEEL"},
    {"id": "IS-2062", "num": "IS 2062 : 2011", "title": "Hot rolled medium and high tensile structural steel", "desc": "Hot rolled structural steel.", "cat": "CAT-STEEL"},
    {"id": "IS-5312-1", "num": "IS 5312 (Part 1) : 2004", "title": "Swing check type reflux (non-return) valves for water works purposes: Single door pattern", "desc": "Single door swing check valves.", "cat": "CAT-VALVES"},
    {"id": "IS-5312-2", "num": "IS 5312 (Part 2) : 1986", "title": "Swing check type reflux (non-return) valves for water works purposes: Multi-door pattern", "desc": "Multi-door swing check valves.", "cat": "CAT-VALVES"},
    {"id": "IS-13095", "num": "IS 13095 : 1991", "title": "Butterfly valves for general purposes", "desc": "Butterfly valves.", "cat": "CAT-VALVES"},
    {"id": "IS-14846", "num": "IS 14846 : 2000", "title": "Sluice valves for water works purposes (50 to 1200 mm size)", "desc": "Sluice valves for water works.", "cat": "CAT-VALVES"},

    # Water / Sanitation (8)
    {"id": "IS-783", "num": "IS 783 : 1985", "title": "Code of practice for laying of concrete pipes", "desc": "Laying of concrete pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-3114", "num": "IS 3114 : 1994", "title": "Code of practice for laying of cast iron pipes", "desc": "Laying of cast iron pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-3711", "num": "IS 3711 : 2012", "title": "Selection and testing of cast iron and ductile iron pipes and fittings for water and sewage applications", "desc": "Guidelines for CI and DI pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-10124-1", "num": "IS 10124 (Part 1) : 2009", "title": "Fabricated PVC fittings for potable water supplies: General requirements", "desc": "Fabricated PVC fittings general req.", "cat": "CAT-PIPES"},
    {"id": "IS-10124-2", "num": "IS 10124 (Part 2) : 2009", "title": "Fabricated PVC fittings for potable water supplies: Specific requirements for sockets", "desc": "PVC fittings sockets.", "cat": "CAT-PIPES"},
    {"id": "IS-10124-3", "num": "IS 10124 (Part 3) : 2009", "title": "Fabricated PVC fittings for potable water supplies: Specific requirements for straight reducers", "desc": "PVC fittings straight reducers.", "cat": "CAT-PIPES"},
    {"id": "IS-15801", "num": "IS 15801 : 2008", "title": "Polypropylene Random Copolymer (PP-R) pipes for hot and cold water supplies", "desc": "PP-R pipes.", "cat": "CAT-PIPES"},
    {"id": "IS-15778", "num": "IS 15778 : 2007", "title": "Chlorinated polyvinyl chloride (CPVC) pipes for potable hot and cold water distribution supplies", "desc": "CPVC pipes.", "cat": "CAT-PIPES"},

    # Industrial Safety / Fire Safety (7)
    {"id": "IS-2190", "num": "IS 2190 : 2010", "title": "Selection, installation and maintenance of first-aid fire extinguishers", "desc": "Maintenance of fire extinguishers.", "cat": "CAT-FIRE"},
    {"id": "IS-933", "num": "IS 933 : 1989", "title": "Portable chemical fire extinguisher, foam type", "desc": "Foam type fire extinguisher.", "cat": "CAT-FIRE"},
    {"id": "IS-934", "num": "IS 934 : 1993", "title": "Portable chemical fire extinguisher, soda acid type", "desc": "Soda acid fire extinguisher.", "cat": "CAT-FIRE"},
    {"id": "IS-15683", "num": "IS 15683 : 2018", "title": "Portable fire extinguishers - Performance and construction", "desc": "Portable fire extinguishers performance.", "cat": "CAT-FIRE"},
    {"id": "IS-2189", "num": "IS 2189 : 2008", "title": "Selection, installation and maintenance of automatic fire detection and alarm system", "desc": "Fire detection and alarm system.", "cat": "CAT-FIRE"},
    {"id": "IS-3521-1", "num": "IS 3521 (Part 1) : 2021", "title": "Industrial safety belts and harnesses: General requirements", "desc": "Industrial safety belts and harnesses.", "cat": "CAT-PPE"},
    {"id": "IS-3521-2", "num": "IS 3521 (Part 2) : 2021", "title": "Industrial safety belts and harnesses: Lanyards", "desc": "Lanyards for safety belts.", "cat": "CAT-PPE"},

    # Civil / Construction (5)
    {"id": "IS-800", "num": "IS 800 : 2007", "title": "General construction in steel - Code of practice", "desc": "Code of practice for steel construction.", "cat": "CAT-STEEL"},
    {"id": "IS-801", "num": "IS 801 : 1975", "title": "Code of practice for use of cold formed light gauge steel structural members in general building construction", "desc": "Cold formed light gauge steel members.", "cat": "CAT-STEEL"},
    {"id": "IS-1893-2", "num": "IS 1893 (Part 2) : 2014", "title": "Criteria for earthquake resistant design of structures: Liquid retaining tanks", "desc": "Earthquake resistant design for tanks.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1893-3", "num": "IS 1893 (Part 3) : 2014", "title": "Criteria for earthquake resistant design of structures: Bridges and retaining walls", "desc": "Earthquake resistant design for bridges.", "cat": "CAT-CONCRETE"},
    {"id": "IS-1893-4", "num": "IS 1893 (Part 4) : 2015", "title": "Criteria for earthquake resistant design of structures: Industrial structures including stack-like structures", "desc": "Earthquake resistant design for industrial structures.", "cat": "CAT-CONCRETE"},

    # Finishes / Paints (4)
    {"id": "IS-2395-1", "num": "IS 2395 (Part 1) : 1994", "title": "Painting of concrete, masonry and plaster surfaces - Code of practice: Operations and workmanship", "desc": "Code of practice for painting masonry.", "cat": "CAT-PAINTS"},
    {"id": "IS-2395-2", "num": "IS 2395 (Part 2) : 1994", "title": "Painting of concrete, masonry and plaster surfaces - Code of practice: Schedule", "desc": "Schedule for painting masonry.", "cat": "CAT-PAINTS"},
    {"id": "IS-1477-1", "num": "IS 1477 (Part 1) : 1971", "title": "Code of practice for painting of ferrous metals in buildings: Pretreatment", "desc": "Pretreatment for painting ferrous metals.", "cat": "CAT-PAINTS"},
    {"id": "IS-1477-2", "num": "IS 1477 (Part 2) : 1971", "title": "Code of practice for painting of ferrous metals in buildings: Painting", "desc": "Painting of ferrous metals.", "cat": "CAT-PAINTS"},

    # HVAC / Lighting (6)
    {"id": "IS-16444", "num": "IS 16444 : 2015", "title": "AC Static Direct Connected Watt-Hour Smart Meter Class 1 and 2", "desc": "Smart meter specifications.", "cat": "CAT-ELECEQ"},
    {"id": "IS-16102-1", "num": "IS 16102 (Part 1) : 2012", "title": "Self-ballasted LED lamps for general lighting services: Safety requirements", "desc": "Safety requirements for LED lamps.", "cat": "CAT-LIGHTING"},
    {"id": "IS-16102-2", "num": "IS 16102 (Part 2) : 2012", "title": "Self-ballasted LED lamps for general lighting services: Performance requirements", "desc": "Performance requirements for LED lamps.", "cat": "CAT-LIGHTING"},
    {"id": "IS-325", "num": "IS 325 : 1996", "title": "Three-phase induction motors", "desc": "Specification for three-phase induction motors.", "cat": "CAT-MOTORS"},
    {"id": "IS-996", "num": "IS 996 : 2009", "title": "Single-phase AC induction motors for general purpose", "desc": "Specification for single-phase AC motors.", "cat": "CAT-MOTORS"},
    {"id": "IS-8148", "num": "IS 8148 : 2018", "title": "Packaged air conditioners - Specification", "desc": "Specification for packaged air conditioners.", "cat": "CAT-HVAC"}
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
            "scope_text": s['desc'] + " This standard covers the technical specifications, requirements, and testing parameters for the relevant product or code of practice."
        })
        
        data['standard_sources'].append({
            "id": f"SRC-{s['id']}-01",
            "standard_id": s['id'],
            "organization": "Bureau of Indian Standards",
            "source_type": "Official Standard",
            "url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/isdetails"
        })

keywords_to_add = [
    {"id": "KW-EARTHING", "word": "earthing"},
    {"id": "KW-VALVE", "word": "valve"},
    {"id": "KW-MOTOR", "word": "motor"},
    {"id": "KW-STEEL", "word": "steel"},
    {"id": "KW-PAINTING", "word": "painting"}
]

existing_kw_words = {k['word']: k['id'] for k in data.get('keywords', [])}
for k in keywords_to_add:
    if k['word'] not in existing_kw_words:
        data['keywords'].append(k)
        existing_kw_words[k['word']] = k['id']

standard_keyword_mappings = {
    "IS-3043": ["earthing", "electrical"],
    "IS-3961-1": ["electrical", "cable"],
    "IS-5312-1": ["valve", "water supply"],
    "IS-5312-2": ["valve", "water supply"],
    "IS-13095": ["valve"],
    "IS-14846": ["valve", "water supply"],
    "IS-325": ["motor", "electrical"],
    "IS-996": ["motor", "electrical"],
    "IS-800": ["steel", "structural"],
    "IS-2062": ["steel", "structural"],
    "IS-2395-1": ["painting", "masonry"],
    "IS-1477-1": ["painting", "steel"]
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

print(f"Added {len(new_standards_data)} new standards for Batch 3.")
