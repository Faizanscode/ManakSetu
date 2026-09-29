import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import select, text

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app.models import Standard
from app.services.ai_service import generate_embedding

def test_vector_search(db: Session, name: str, query: str):
    print(f"\n{'='*50}\nTEST: {name}\n{'='*50}")
    print(f"Query: {query}\n")
    
    # 1. Generate embedding
    req_embedding = generate_embedding(query)
    
    # 2. Vector search
    # Using L2 distance or cosine distance
    stmt = (
        select(Standard, Standard.embedding.cosine_distance(req_embedding).label("distance"))
        .filter(Standard.embedding != None)
        .order_by(text("distance ASC"))
        .limit(5)
    )
    
    results = db.execute(stmt).all()
    
    for std, distance in results:
        # Convert distance to a similarity score (0-100)
        similarity = (1 - float(distance)) * 100
        print(f"- {std.standard_number}: {std.title} (Similarity: {similarity:.1f}%)")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        test_vector_search(db, "TEST 1 - FLOOR TILES", "We need 2,500 square meters of durable floor tiles for a newly constructed government administrative building. The tiles should be suitable for high foot-traffic areas and should have adequate breaking strength, abrasion resistance, low water absorption, dimensional consistency, and slip resistance. Tiles should be available in standard sizes and finishes and should comply with applicable BIS standards. The supplier should provide samples and product test certificates before bulk delivery.")
        
        test_vector_search(db, "TEST 2 - REINFORCEMENT STEEL", "We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard.")
        
        test_vector_search(db, "TEST 3 - CONCRETE", "We need concrete for construction of structural members of a government building. The concrete should achieve the required characteristic strength and workability, and the supplier should provide appropriate testing and quality documentation.")
        
        test_vector_search(db, "TEST 4 - BRICKS", "We need burnt clay building bricks for construction of internal and external masonry walls for a government building.")
        
        test_vector_search(db, "TEST 5 - ELECTRICAL", "We need PVC insulated electrical cables for domestic wiring in a commercial building. The cables should operate safely up to 1,100 volts and have heavy duty insulation. Electrical sockets and switches are also needed.")
        
        test_vector_search(db, "TEST 6 - WATER / PLUMBING", "We need PVC-U pipes for an underground drainage and potable water supply system. Valves and fittings should be durable and comply with the latest standards for sanitary plumbing.")
    finally:
        db.close()
