from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_recommendation_api():
    # Mock extract_requirement and generate_embedding
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
            assert isinstance(data["recommendations"], list)
            if len(data["recommendations"]) > 0:
                rec = data["recommendations"][0]
                assert "standard_number" in rec
                assert "relevance_score" in rec
                assert "relevance_category" in rec
                assert "why_recommended" in rec
                assert "evidence" in rec
                assert "score_breakdown" in rec
                assert "status" in rec

def test_recommendation_no_match():
    with patch('app.services.recommendation_service.extract_requirement') as mock_extract:
        with patch('app.services.recommendation_service.generate_embedding') as mock_embed:
            
            mock_extract.return_value = MagicMock(
                products=["spaceship engine"],
                applications=["mars travel"],
                keywords=["interstellar"],
                intent_summary="Procure a spaceship engine"
            )
            mock_embed.return_value = [0.0] * 768  # Completely irrelevant vector
            
            response = client.post(
                "/api/recommendations/",
                json={"query": "Need spaceship engine"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "recommendations" in data
            assert data["candidate_count"] >= 0
            if not data["recommendations"]:
                assert "message" in data
