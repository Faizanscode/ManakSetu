import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from app.database import SessionLocal
from app.models import Standard
from app.services.ai_service import build_standard_embedding_text, generate_embedding
import time

def seed_embeddings():
    db = SessionLocal()
    standards = db.query(Standard).filter(Standard.embedding == None).all()
    print(f"Found {len(standards)} standards without embeddings.")
    
    for std in standards:
        text = build_standard_embedding_text(std)
        print(f"Generating embedding for {std.standard_number}...")
        try:
            embedding = generate_embedding(text)
            std.embedding = embedding
            db.commit()
            print("Success")
        except Exception as e:
            print(f"Failed: {e}")
            db.rollback()
        time.sleep(1)
        
    print("Done")

if __name__ == "__main__":
    seed_embeddings()
