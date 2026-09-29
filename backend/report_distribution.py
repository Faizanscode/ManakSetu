import sys, os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app.models import Standard, Category, Sector
from sqlalchemy import func

db = SessionLocal()

print("="*50)
print("SECTOR DISTRIBUTION")
print("="*50)
sectors = db.query(Sector.name, func.count(Standard.id)).outerjoin(Standard).group_by(Sector.name).order_by(func.count(Standard.id).desc()).all()
for s in sectors:
    print(f"{s[0]}: {s[1]}")

print("\n" + "="*50)
print("CATEGORY DISTRIBUTION")
print("="*50)
cats = db.query(Category.name, func.count(Standard.id)).outerjoin(Standard).group_by(Category.name).order_by(func.count(Standard.id).desc()).all()
for c in cats:
    print(f"{c[0]}: {c[1]}")
