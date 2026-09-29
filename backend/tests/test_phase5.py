from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_phase5_evidence_schema():
    with patch('app.services.recommendation_service.extract_requirement') as mock_extract:
        with patch('app.services.recommendation_service.generate_embedding') as mock_embed:
            
            mock_extract.return_value = MagicMock(
                products=["steel bars"],
                applications=["construction"],
                keywords=["reinforcement", "steel"],
                intent_summary="Procure steel bars"
            )
            mock_embed.return_value = [0.1] * 768
            
            response = client.post(
                "/api/recommendations/",
                json={"query": "Need steel bars"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "recommendations" in data
            
            if len(data["recommendations"]) > 0:
                rec = data["recommendations"][0]
                
                # Check new Phase 5 schema fields
                assert "explanation" in rec
                assert "summary" in rec["explanation"]
                assert "product_matches" in rec["explanation"]
                assert "application_matches" in rec["explanation"]
                assert "keyword_matches" in rec["explanation"]
                assert "scope_match" in rec["explanation"]
                
                assert "evidence" in rec
                assert isinstance(rec["evidence"], list)
                for item in rec["evidence"]:
                    assert "type" in item
                    assert "label" in item
                    assert "description" in item
                    assert "source" in item
                
                assert "relationships" in rec
                assert isinstance(rec["relationships"], list)
                
                assert "sources" in rec
                assert isinstance(rec["sources"], list)

def test_phase5_missing_evidence():
    with patch('app.services.recommendation_service.extract_requirement') as mock_extract:
        with patch('app.services.recommendation_service.generate_embedding') as mock_embed:
            
            # Completely mismatching requirement but close semantic distance
            mock_extract.return_value = MagicMock(
                products=["fake product"],
                applications=["fake app"],
                keywords=["fake word"],
                intent_summary="Fake intent"
            )
            mock_embed.return_value = [0.1] * 768 # Force a match to retrieve candidate
            
            response = client.post(
                "/api/recommendations/",
                json={"query": "Fake requirement"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            if len(data["recommendations"]) > 0:
                rec = data["recommendations"][0]
                
                # Because there are no matches, evidence list should be empty (except possibly category/sector)
                # Explanation should reflect no matches
                assert rec["explanation"]["product_matches"] == []
                assert rec["explanation"]["application_matches"] == []
                assert rec["explanation"]["keyword_matches"] == []
                assert rec["explanation"]["scope_match"] == False

                # Assert no fabricated evidence
                # Check for "PRODUCT_MATCH" in evidence list
                product_evidence = [e for e in rec["evidence"] if e["type"] == "PRODUCT_MATCH"]
                assert len(product_evidence) == 0
