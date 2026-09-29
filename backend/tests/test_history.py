import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_history_flow():
    # 1. Create/save analysis
    payload = {
        "title": "Test History Analysis",
        "procurement_requirement": "Procurement of safety helmets",
        "category": "safety",
        "priority": "urgent",
        "extracted_requirement": {"intent_summary": "Test"},
        "recommendations": {"recommendations": []},
        "gaps": {"gaps": []},
        "specification": {"title": "Spec"},
        "status": "COMPLETED"
    }

    response = client.post("/api/history/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test History Analysis"
    history_id = data["id"]

    # 2. List history
    response = client.get("/api/history/")
    assert response.status_code == 200
    history_list = response.json()
    assert isinstance(history_list, list)
    assert any(h["id"] == history_id for h in history_list)

    # 3. Retrieve analysis
    response = client.get(f"/api/history/{history_id}")
    assert response.status_code == 200
    history_detail = response.json()
    assert history_detail["id"] == history_id
    assert history_detail["procurement_requirement"] == "Procurement of safety helmets"
    assert history_detail["specification"]["title"] == "Spec"

    # 4. Invalid analysis ID
    response = client.get("/api/history/invalid-id")
    assert response.status_code == 404

    # 5. Delete analysis to cleanup (Optional, assuming tests use real DB for now)
    response = client.delete(f"/api/history/{history_id}")
    assert response.status_code == 204
