import os
import sys
import json
from datetime import datetime
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
import app.models as models

SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'seed', 'standards.json')

def seed_data(db: Session):
    print("Starting data seeding process...")
    
    if not os.path.exists(SEED_DATA_PATH):
        print(f"Seed file not found at {SEED_DATA_PATH}")
        return

    with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        # Counters
        counts = {
            "sectors": 0, "categories": 0, "standards": 0, "versions": 0,
            "scopes": 0, "keywords": 0, "standard_keywords": 0,
            "relationships": 0, "sources": 0
        }

        # 1. Insert sectors
        for sector_data in data.get("sectors", []):
            sector = models.Sector(**sector_data)
            db.merge(sector)
            counts["sectors"] += 1
        
        # 2. Insert categories
        for cat_data in data.get("categories", []):
            cat = models.Category(**cat_data)
            db.merge(cat)
            counts["categories"] += 1

        # 3. Insert standards
        for std_data in data.get("standards", []):
            std = models.Standard(
                id=std_data["id"],
                standard_number=std_data["standard_number"],
                title=std_data["title"],
                short_description=std_data.get("short_description"),
                issuing_body=std_data.get("issuing_body", "Bureau of Indian Standards"),
                sector_id=std_data.get("sector_id"),
                category_id=std_data.get("category_id"),
                status=std_data.get("status", "CURRENT")
            )
            db.merge(std)
            counts["standards"] += 1

        # 4. Insert standard_versions
        for ver_data in data.get("standard_versions", []):
            ver = models.StandardVersion(**ver_data)
            db.merge(ver)
            counts["versions"] += 1

        # 5. Insert standard_scopes
        for scope_data in data.get("standard_scopes", []):
            scope = models.StandardScope(**scope_data)
            db.merge(scope)
            counts["scopes"] += 1

        # 6. Insert keywords
        for kw_data in data.get("keywords", []):
            kw = models.Keyword(**kw_data)
            db.merge(kw)
            counts["keywords"] += 1

        # 7. Insert standard_keywords
        for sk_data in data.get("standard_keywords", []):
            sk = models.StandardKeyword(
                standard_id=sk_data["standard_id"],
                keyword_id=sk_data["keyword_id"]
            )
            db.merge(sk)
            counts["standard_keywords"] += 1

        # 8. Insert standard_relationships
        for rel_data in data.get("standard_relationships", []):
            rel = models.StandardRelationship(**rel_data)
            db.merge(rel)
            counts["relationships"] += 1

        # 9. Insert standard_sources
        for src_data in data.get("standard_sources", []):
            src = models.StandardSource(**src_data)
            db.merge(src)
            counts["sources"] += 1

        db.commit()
        print("\nSeeding completed successfully.\n")
        print(f"Sectors: {counts['sectors']}")
        print(f"Categories: {counts['categories']}")
        print(f"Standards: {counts['standards']}")
        print(f"Versions: {counts['versions']}")
        print(f"Scopes: {counts['scopes']}")
        print(f"Keywords: {counts['keywords']}")
        print(f"Standard-keyword mappings: {counts['standard_keywords']}")
        print(f"Relationships: {counts['relationships']}")
        print(f"Sources: {counts['sources']}")
        
    except Exception as e:
        db.rollback()
        print(f"\nFailed to seed database. Transaction rolled back.\nError: {e}")
        raise e

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
