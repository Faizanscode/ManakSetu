import sys, os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("=== SECTOR COUNTS ===")
r = db.execute(text("""
    SELECT s.name, COUNT(st.id) 
    FROM sectors s 
    LEFT JOIN standards st ON st.sector_id = s.id 
    GROUP BY s.name 
    ORDER BY COUNT(st.id) DESC
"""))
for row in r:
    print(row)

print("\n=== CATEGORY COUNTS ===")
r = db.execute(text("""
    SELECT c.name, c.sector_id, COUNT(st.id) 
    FROM categories c 
    LEFT JOIN standards st ON st.category_id = c.id 
    GROUP BY c.name, c.sector_id 
    ORDER BY COUNT(st.id) DESC
"""))
for row in r:
    print(row)

print("\n=== NULL SECTOR COUNT ===")
r = db.execute(text("SELECT COUNT(*) FROM standards WHERE sector_id IS NULL"))
print(r.fetchone())

print("\n=== NULL CATEGORY COUNT ===")
r = db.execute(text("SELECT COUNT(*) FROM standards WHERE category_id IS NULL"))
print(r.fetchone())

print("\n=== NEW STANDARDS METADATA ===")
r = db.execute(text("""
    SELECT st.standard_number, st.title, st.sector_id, st.category_id, sec.name as sector_name, cat.name as cat_name
    FROM standards st
    LEFT JOIN sectors sec ON sec.id = st.sector_id
    LEFT JOIN categories cat ON cat.id = st.category_id
    WHERE st.standard_number SIMILAR TO 
        'IS 15622%|IS 13630%|IS 504%|IS 13712%|IS 15489%|IS 2932%|IS 4985%|IS 15328%|IS 694%|IS 1554%|IS 1293%|IS 778%|IS 14846%|IS 2925%|IS 13095%|IS 9473%|IS 13920%|IS 1893%|IS 875%|IS 432%|IS 303%|IS 1038%|IS 17546%|IS 5410%|IS 5329%|IS 17650%|IS 1786%'
    ORDER BY st.standard_number
"""))
for row in r:
    print(f"  {row.standard_number}: sector={row.sector_name} | category={row.cat_name} | sector_id={row.sector_id} | cat_id={row.category_id}")

db.close()
