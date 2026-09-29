from fastapi import APIRouter, HTTPException, Depends
import logging

from app.schemas import SpecificationRequest, SpecificationResponse
from app.services.specification_generator import generate_specification_draft

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/specifications",
    tags=["specifications"],
)

@router.post("/generate", response_model=SpecificationResponse)
async def generate_draft(request: SpecificationRequest):
    """
    Generates a structured procurement specification draft based on user requirements,
    recommendations, evidence, and detected gaps.
    """
    try:
        if not request.requirement or not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Requirement cannot be empty")
            
        if not request.recommendations:
            raise HTTPException(status_code=400, detail="Cannot generate specification without recommended standards")
            
        response = generate_specification_draft(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating specification: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during specification generation")
