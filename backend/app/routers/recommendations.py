from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import get_recommendations
import logging
from google.genai.errors import ServerError, ClientError

router = APIRouter(
    prefix="/api",
    tags=["Recommendations"]
)

logger = logging.getLogger(__name__)

@router.post("/recommendations/", response_model=RecommendationResponse)
def get_standard_recommendations(request: RecommendationRequest, db: Session = Depends(get_db)):
    try:
        return get_recommendations(db, request)
    except ServerError as e:
        logger.error(f"Gemini ServerError during recommendation: {e}")
        raise HTTPException(status_code=503, detail="AI service is currently unavailable. Please try again later.")
    except ClientError as e:
        logger.error(f"Gemini ClientError during recommendation: {e}")
        if e.code == 429:
            raise HTTPException(status_code=429, detail="Too many requests to AI service.")
        raise HTTPException(status_code=400, detail="Configuration or model error.")
    except Exception as e:
        logger.error(f"Error during recommendation: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating recommendations.")
