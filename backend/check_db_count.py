import sys, os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app.models import Standard
from sqlalchemy import func

db = SessionLocal()

total = db.query(func.count(Standard.id)).scalar()
dist_num = db.query(func.count(func.distinct(Standard.standard_number))).scalar()
dist_title = db.query(func.count(func.distinct(Standard.title))).scalar()

print(f"Total: {total}")
print(f"Distinct Number: {dist_num}")
print(f"Distinct Title: {dist_title}")
