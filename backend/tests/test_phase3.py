import os
import pytest
import math
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.main import app
from app.services.ai_service import extract_requirement, generate_embedding, GENERATION_MODEL, EMBEDDING_MODEL
from app.database import Base
from dotenv import load_dotenv

# Ensure dotenv is loaded so GEMINI_API_KEY is available
load_dotenv()

client = TestClient(app)

# A. Requirement extraction
@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="No Gemini API Key")
def test_requirement_extraction():
    test_query = "We need standards for manufacturing prestressed concrete pipes."
    extracted = extract_requirement(test_query)
    
    # Verify structured output
    assert isinstance(extracted.products, list)
    assert isinstance(extracted.applications, list)
    assert isinstance(extracted.keywords, list)
    assert isinstance(extracted.intent_summary, str)

# B. Embedding generation
@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="No Gemini API Key")
def test_embedding_generation():
    test_text = "Standard: IS 456\nTitle: Plain and Reinforced Concrete"
    embedding = generate_embedding(test_text)
    
    assert EMBEDDING_MODEL == "gemini-embedding-2"
    assert len(embedding) == 768
    
    for val in embedding:
        assert isinstance(val, (int, float))
        assert not math.isnan(val)
        assert not math.isinf(val)

# C. Database
def test_database_schema_and_data():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("No DATABASE_URL configured")
        
    engine = create_engine(database_url.replace("%", "%%"))
    
    with engine.connect() as conn:
        # Check standard_versions exists and check standards.embedding
        result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'standards' AND column_name = 'embedding'"))
        col = result.fetchone()
        assert col is not None, "embedding column is missing"
        assert col[1] == 'USER-DEFINED', "embedding column should be of type USER-DEFINED (vector)"
        
        # Check the 15 standards exist
        result = conn.execute(text("SELECT COUNT(*) FROM standards"))
        count = result.scalar()
        assert count == 15, f"Expected 15 standards, found {count}"

# D. API
@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="No Gemini API Key")
def test_api_analyze():
    response = client.post(
        "/api/analyze/",
        json={"query": "We need standards for electrical transformers"}
    )
    
    if response.status_code != 200:
        print("ERROR DETAIL:", response.text)
    assert response.status_code == 200
    data = response.json()
    
    assert "extracted" in data
    assert "embedding_status" in data
    assert data["embedding_status"] == "SUCCESS"
    assert "embedding_preview" in data
    assert isinstance(data["embedding_preview"], list)
    assert len(data["embedding_preview"]) == 5
