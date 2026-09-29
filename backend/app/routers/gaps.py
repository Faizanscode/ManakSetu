from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging

from app.schemas import GapDetectionRequest, GapDetectionResponse
from app.services.gap_detection_service import detect_specification_gaps

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/gaps",
    tags=["gaps"],
)

@router.post("/", response_model=GapDetectionResponse)
async def check_gaps(request: GapDetectionRequest):
    """
    Analyzes the procurement requirement against the recommended standards
    to detect missing, ambiguous, or incomplete specification details.
    """
    try:
        if not request.requirement or not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Requirement cannot be empty")
            
        if not request.recommendations:
            # If no recommendations are passed, we just return empty gaps
            return detect_specification_gaps(request)
            
        response = detect_specification_gaps(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in gap detection: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during gap detection")
