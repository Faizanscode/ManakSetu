import os
import sys

# add backend dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import SessionLocal
from app.models import Standard

db = SessionLocal()
total = db.query(Standard).count()
embedded = db.query(Standard).filter(Standard.embedding != None).count()
print(f"Total standards: {total}")
print(f"Standards with embeddings: {embedded}")
