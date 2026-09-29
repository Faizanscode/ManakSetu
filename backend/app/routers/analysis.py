from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RequirementAnalysisRequest, RequirementAnalysisResponse
from app.services.ai_service import extract_requirement, generate_embedding
import os
import logging
from google.genai.errors import ServerError, ClientError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

@router.post("/", response_model=RequirementAnalysisResponse)
def analyze_requirement(request: RequirementAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyzes a raw procurement requirement.
    Extracts structured data and generates an embedding.
    """
    # Check if GEMINI_API_KEY is available
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY must be provided in the backend process environment")
    
    try:
        # Step 1: LLM Extraction
        extracted = extract_requirement(request.query)
        
        # Step 2: Generate Embedding
        embedding = generate_embedding(request.query)
        
        return RequirementAnalysisResponse(
            extracted=extracted,
            embedding_status="SUCCESS",
            embedding_preview=embedding[:5]  # Preview first 5 dimensions
        )
    except ServerError as e:
        logger.error(f"Gemini API Server Error: {e.code}")
        if e.code == 503:
            raise HTTPException(status_code=503, detail="AI service is temporarily unavailable. Please retry.")
        raise HTTPException(status_code=503, detail=f"AI service returned server error {e.code}. Please retry.")
    except ClientError as e:
        logger.error(f"Gemini API Client Error: {e.code}")
        if e.code == 429:
            raise HTTPException(status_code=429, detail="AI service request limit reached. Please try again shortly.")
        raise HTTPException(status_code=400, detail=f"AI service client error: {e.code}")
    except ValueError as e:
        logger.error(f"Validation Error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected Analysis Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

