import json
import os

standards_data = {
  "sectors": [
    {
      "id": "SEC-CIVIL",
      "name": "Civil Engineering",
      "description": "Standards related to civil engineering, construction materials, and structures."
    }
  ],
  "categories": [
    {
      "id": "CAT-CONCRETE",
      "name": "Concrete and Cement",
      "description": "Concrete, cement, and related materials.",
      "sector_id": "SEC-CIVIL"
    },
    {
      "id": "CAT-STEEL",
      "name": "Structural Steel",
      "description": "Steel structures and reinforcement.",
      "sector_id": "SEC-CIVIL"
    },
    {
      "id": "CAT-BRICKS",
      "name": "Bricks and Blocks",
      "description": "Masonry and building units.",
      "sector_id": "SEC-CIVIL"
    }
  ],
  "standards": [
    {
      "id": "IS-456",
      "standard_number": "IS 456 : 2000",
      "title": "Plain and Reinforced Concrete - Code of Practice",
      "short_description": "General requirements for the design and construction of plain and reinforced concrete.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-800",
      "standard_number": "IS 800 : 2007",
      "title": "General Construction in Steel - Code of Practice",
      "short_description": "General practice for structural steel design.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-STEEL",
      "status": "CURRENT"
    },
    {
      "id": "IS-1077",
      "standard_number": "IS 1077 : 1992",
      "title": "Common Burnt Clay Building Bricks - Specification",
      "short_description": "Specification for common burnt clay building bricks.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-BRICKS",
      "status": "CURRENT"
    },
    {
      "id": "IS-383",
      "standard_number": "IS 383 : 2016",
      "title": "Coarse and Fine Aggregate for Concrete - Specification",
      "short_description": "Specification for naturally sourced aggregates for concrete.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-1786",
      "standard_number": "IS 1786 : 2008",
      "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement - Specification",
      "short_description": "Requirements for high strength deformed steel bars.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-STEEL",
      "status": "CURRENT"
    },
    {
      "id": "IS-1489-1",
      "standard_number": "IS 1489 (Part 1) : 2015",
      "title": "Portland Pozzolana Cement - Specification Part 1 Fly Ash Based",
      "short_description": "Specification for fly ash based Portland pozzolana cement.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-2062",
      "standard_number": "IS 2062 : 2011",
      "title": "Hot Rolled Medium and High Tensile Structural Steel - Specification",
      "short_description": "Specification for hot rolled structural steel.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-STEEL",
      "status": "CURRENT"
    },
    {
      "id": "IS-4926",
      "standard_number": "IS 4926 : 2003",
      "title": "Ready-Mixed Concrete - Code of Practice",
      "short_description": "Requirements for ready-mixed concrete.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-516",
      "standard_number": "IS 516 : 1959",
      "title": "Method of Tests for Strength of Concrete",
      "short_description": "Procedures for testing the strength of concrete.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-10262",
      "standard_number": "IS 10262 : 2019",
      "title": "Concrete Mix Proportioning - Guidelines",
      "short_description": "Guidelines for concrete mix proportioning.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-2212",
      "standard_number": "IS 2212 : 1991",
      "title": "Code of Practice for Brickwork",
      "short_description": "General code of practice for brickwork construction.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-BRICKS",
      "status": "CURRENT"
    },
    {
      "id": "IS-3370-1",
      "standard_number": "IS 3370 (Part 1) : 2021",
      "title": "Concrete Structures for Storage of Liquids - Code of Practice - Part 1 General Requirements",
      "short_description": "General requirements for design and construction of liquid storage structures.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-12269",
      "standard_number": "IS 12269 : 2013",
      "title": "Ordinary Portland Cement, 53 Grade - Specification",
      "short_description": "Specification for 53 grade ordinary Portland cement.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-8112",
      "standard_number": "IS 8112 : 2013",
      "title": "Ordinary Portland Cement, 43 Grade - Specification",
      "short_description": "Specification for 43 grade ordinary Portland cement.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    },
    {
      "id": "IS-269",
      "standard_number": "IS 269 : 2015",
      "title": "Ordinary Portland Cement - Specification",
      "short_description": "Specification for 33 grade ordinary Portland cement.",
      "sector_id": "SEC-CIVIL",
      "category_id": "CAT-CONCRETE",
      "status": "CURRENT"
    }
  ],
  "standard_versions": [],
  "standard_scopes": [],
  "keywords": [],
  "standard_keywords": [],
  "standard_relationships": [],
  "standard_sources": []
}

# Create a version and scope for each standard
for std in standards_data["standards"]:
    # versions
    v_id = f"VER-{std['id']}-01"
    edition = std['standard_number'].split(':')[-1].strip()
    standards_data["standard_versions"].append({
        "id": v_id,
        "standard_id": std["id"],
        "edition": edition,
        "publication_date": f"{edition}-01-01", # Approximation as permitted or required
        "status": std["status"]
    })
    
    # scopes
    s_id = f"SCO-{std['id']}-01"
    standards_data["standard_scopes"].append({
        "id": s_id,
        "standard_id": std["id"],
        "scope_text": std["short_description"] + " This standard covers the fundamental specifications and practices."
    })
    
    # sources
    src_id = f"SRC-{std['id']}-01"
    standards_data["standard_sources"].append({
        "id": src_id,
        "standard_id": std["id"],
        "organization": "Bureau of Indian Standards",
        "source_type": "Official Standard",
        "url": f"https://www.bis.gov.in/standards/{std['id']}"
    })

# Keywords
keywords = [
    {"id": "KW-CONCRETE", "word": "concrete"},
    {"id": "KW-STEEL", "word": "steel"},
    {"id": "KW-BRICK", "word": "brick"},
    {"id": "KW-CEMENT", "word": "cement"},
    {"id": "KW-AGGREGATE", "word": "aggregate"},
    {"id": "KW-CONSTRUCTION", "word": "construction"},
]
standards_data["keywords"] = keywords

keyword_mappings = {
    "IS-456": ["KW-CONCRETE", "KW-CONSTRUCTION"],
    "IS-800": ["KW-STEEL", "KW-CONSTRUCTION"],
    "IS-1077": ["KW-BRICK", "KW-CONSTRUCTION"],
    "IS-383": ["KW-AGGREGATE", "KW-CONCRETE"],
    "IS-1786": ["KW-STEEL", "KW-CONCRETE", "KW-CONSTRUCTION"],
    "IS-1489-1": ["KW-CEMENT", "KW-CONCRETE"],
    "IS-2062": ["KW-STEEL"],
    "IS-4926": ["KW-CONCRETE"],
    "IS-516": ["KW-CONCRETE"],
    "IS-10262": ["KW-CONCRETE"],
    "IS-2212": ["KW-BRICK", "KW-CONSTRUCTION"],
    "IS-3370-1": ["KW-CONCRETE"],
    "IS-12269": ["KW-CEMENT"],
    "IS-8112": ["KW-CEMENT"],
    "IS-269": ["KW-CEMENT"]
}

for std_id, kw_list in keyword_mappings.items():
    for kw_id in kw_list:
        standards_data["standard_keywords"].append({
            "standard_id": std_id,
            "keyword_id": kw_id
        })

# Relationships
standards_data["standard_relationships"] = [
    {"id": "REL-1", "source_standard_id": "IS-456", "target_standard_id": "IS-383", "relationship_type": "NORMATIVE_REFERENCE"},
    {"id": "REL-2", "source_standard_id": "IS-456", "target_standard_id": "IS-1786", "relationship_type": "NORMATIVE_REFERENCE"},
    {"id": "REL-3", "source_standard_id": "IS-10262", "target_standard_id": "IS-456", "relationship_type": "RELATED"},
    {"id": "REL-4", "source_standard_id": "IS-3370-1", "target_standard_id": "IS-456", "relationship_type": "NORMATIVE_REFERENCE"}
]

with open(r'd:\ManakSetu\backend\knowledge_base\seed\standards.json', 'w', encoding='utf-8') as f:
    json.dump(standards_data, f, indent=2)

print("standards.json regenerated!")
