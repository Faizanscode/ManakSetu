import os
import sys
import json
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app.services.recommendation_service import get_recommendations
from app.schemas import RecommendationRequest, RequirementAnalysisResponse, ExtractedRequirement

def test_query(db, name, text):
    print(f"\n{'='*50}\nTEST: {name}\n{'='*50}")
    print(f"Query: {text}\n")
    
    extracted = ExtractedRequirement(
        procurement_objective=text,
        product_description=text,
        products=["test"],
        applications=["test"],
        intent_summary="test",
        keywords=["test"]
    )
    analysis_result = RequirementAnalysisResponse(
        extracted=extracted,
        embedding_status="SUCCESS",
        embedding_preview=[]
    )
    request = RecommendationRequest(
        query=text,
        analysis=analysis_result
    )
    
    try:
        recommendations = get_recommendations(db, request)
        
        if not recommendations.recommendations:
            print("No recommendations found.")
            
        for r in recommendations.recommendations:
            print(f"- {r.standard_number}: {r.title} (Score: {r.overall_score:.2f})")
            # print(f"  {r.explanation.match_reason[:150]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    db = SessionLocal()
    
    test_query(db, "TEST 1 - FLOOR TILES", "We need 2,500 square meters of durable floor tiles for a newly constructed government administrative building. The tiles should be suitable for high foot-traffic areas and should have adequate breaking strength, abrasion resistance, low water absorption, dimensional consistency, and slip resistance. Tiles should be available in standard sizes and finishes and should comply with applicable BIS standards. The supplier should provide samples and product test certificates before bulk delivery.")
    
    test_query(db, "TEST 2 - REINFORCEMENT STEEL", "We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard.")
    
    test_query(db, "TEST 3 - CONCRETE", "We need concrete for construction of structural members of a government building. The concrete should achieve the required characteristic strength and workability, and the supplier should provide appropriate testing and quality documentation.")
    
    test_query(db, "TEST 4 - BRICKS", "We need burnt clay building bricks for construction of internal and external masonry walls for a government building.")
    
    test_query(db, "TEST 5 - ELECTRICAL", "We need PVC insulated electrical cables for domestic wiring in a commercial building. The cables should operate safely up to 1,100 volts and have heavy duty insulation. Electrical sockets and switches are also needed.")
    
    test_query(db, "TEST 6 - WATER / PLUMBING", "We need PVC-U pipes for an underground drainage and potable water supply system. Valves and fittings should be durable and comply with the latest standards for sanitary plumbing.")
    
    db.close()
