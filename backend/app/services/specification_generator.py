import logging
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError, ClientError

from app.services.ai_service import get_client, GENERATION_MODEL, _is_retryable_error
from app.schemas import (
    SpecificationRequest,
    SpecificationResponse,
    SpecificationDraft,
    SpecificationMetadata,
    SpecItem,
    SpecStandard,
)
from app.models import Standard
from app.database import SessionLocal

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ServerError, ClientError)),
    reraise=True
)
def generate_specification_draft(request: SpecificationRequest) -> SpecificationResponse:
    """
    Generates a structured procurement specification draft based on user requirements,
    recommended standards, evidence, and detected gaps.
    """
    
    # 1. Build context for the prompt
    recommendation_context = ""
    valid_standard_ids = []
    
    for rec in request.recommendations:
        valid_standard_ids.append(rec.standard_id)
        recommendation_context += f"\n[STANDARD: {rec.standard_number} (ID: {rec.standard_id})]\nTitle: {rec.title}\nEvidence:\n"
        for ev in rec.evidence:
            recommendation_context += f"- {ev.label}: {ev.description}\n"
            
    gap_context = ""
    if request.gaps:
        for gap in request.gaps:
            gap_context += f"- {gap.gap_type} ({gap.severity}): {gap.title} - {gap.description}\n"
            
    prompt = f"""
You are an expert procurement and engineering specification drafter for the Bureau of Indian Standards (BIS).
Your task is to generate a structured procurement specification DRAFT using ONLY the supplied inputs.

--- ORIGINAL PROCUREMENT REQUIREMENT (USER_PROVIDED) ---
{request.requirement}

--- RECOMMENDED STANDARDS & EVIDENCE (KNOWLEDGE_BASE) ---
{recommendation_context}

--- SPECIFICATION GAPS IDENTIFIED ---
{gap_context}

INSTRUCTIONS & STRICT RULES:
1. Generate a structured draft.
2. For each requirement you extract or generate, you MUST classify its source_type as one of:
   - "USER_PROVIDED": Information directly from the user's requirement.
   - "KNOWLEDGE_BASE": Information directly found in the Recommended Standards & Evidence.
   - "AI_DERIVED": Logical deductions based on the inputs (use sparingly).
   - "REQUIRES_VERIFICATION": For any technical requirement or gap that is not fully supported by the knowledge base but needs addressing.
3. DO NOT INVENT: Do not invent IS numbers, clauses, test methods, grades, dimensions, or numerical limits that are not present in the inputs.
4. If a section is not applicable or information is missing, you can return an empty list for that section, or include a "REQUIRES_VERIFICATION" item if appropriate based on the gaps.
5. The output must strictly match the requested JSON schema.
"""

    client = get_client()
    try:
        prompt += """\n\nOUTPUT FORMAT:
Return ONLY a valid JSON object matching the following structure exactly:
{
  "title": "string",
  "procurement_objective": "string",
  "product_description": "string",
  "intended_application": "string",
  "applicable_standards": [{"standard_id": "string", "standard_number": "string", "title": "string", "relevance": "string", "evidence_summary": "string (optional)"}],
  "technical_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "material_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "dimensional_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "performance_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "testing_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "quality_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "packaging_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "documentation_requirements": [{"requirement": "string", "source": "string", "source_type": "string"}],
  "items_requiring_clarification": ["string"]
}"""

        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        
        import json
        try:
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            parsed_json = json.loads(raw_text.strip())
            draft = SpecificationDraft(**parsed_json)
        except Exception as e:
            logger.error(f"Failed to parse AI response: {response.text}")
            raise ValueError(f"AI response format error: {e}")
        
        # 2. Validation / Grounding Check
        # Ensure that applicable standards only contain valid standard IDs.
        db = SessionLocal()
        try:
            validated_standards = []
            for std in draft.applicable_standards:
                # If standard_id is valid, we keep it. If standard_number matches something, we can verify.
                # Simplest check: standard_id must be in our valid_standard_ids from the request.
                if std.standard_id in valid_standard_ids:
                    validated_standards.append(std)
                else:
                    # Alternatively, check DB to be absolutely sure.
                    db_std = db.query(Standard).filter(Standard.id == std.standard_id).first()
                    if db_std:
                        validated_standards.append(std)
                    else:
                        logger.warning(f"AI hallucinated standard ID: {std.standard_id} - removing from draft.")
                        
            draft.applicable_standards = validated_standards
        finally:
            db.close()
            
        # Optional: Add any missing required standards from recommendations if the AI forgot them
        # (For this MVP, we trust the AI subset + validation)
        
        metadata = SpecificationMetadata(
            generated_at=datetime.utcnow().isoformat() + "Z",
            standard_count=len(draft.applicable_standards),
            gap_count=len(request.gaps)
        )
        
        return SpecificationResponse(specification=draft, metadata=metadata)
        
    except Exception as e:
        if _is_retryable_error(e):
            raise
        logger.error(f"Error generating specification draft: {e}", exc_info=True)
        raise
