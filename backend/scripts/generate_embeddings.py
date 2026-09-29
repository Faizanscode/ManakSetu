import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import select

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app.models import Standard
from app.services.ai_service import generate_embedding, build_standard_embedding_text

def generate_missing_embeddings(db: Session):
    print("Finding standards without embeddings...")
    # Using python filtering to be safe on the pgvector column or just use SQL IS NULL
    stmt = select(Standard).where(Standard.embedding.is_(None))
    standards_without_embeddings = db.scalars(stmt).all()
    
    print(f"Found {len(standards_without_embeddings)} standards needing embeddings.")
    
    success_count = 0
    for std in standards_without_embeddings:
        try:
            print(f"Generating embedding for {std.standard_number}...")
            text = build_standard_embedding_text(std)
            emb = generate_embedding(text)
            std.embedding = emb
            db.commit()
            success_count += 1
        except Exception as e:
            db.rollback()
            print(f"Failed to generate embedding for {std.standard_number}: {e}")
            
    print(f"Successfully generated {success_count} embeddings.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        generate_missing_embeddings(db)
    finally:
        db.close()
