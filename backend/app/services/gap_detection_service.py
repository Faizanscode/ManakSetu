import logging
import uuid
from typing import List
from google.genai import types
from pydantic import BaseModel
from app.services.ai_service import get_client, GENERATION_MODEL, _is_retryable_error
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError, ClientError
from app.schemas import GapDetectionRequest, GapDetectionResponse, SpecificationGap, GapSummary, GapEvidenceBase

logger = logging.getLogger(__name__)

class RawGapOutput(BaseModel):
    gap_type: str
    title: str
    description: str
    severity: str
    reason: str
    suggested_information: str
    evidence_source_type: str
    evidence_description: str

class RawGapDetectionResponse(BaseModel):
    gaps: List[RawGapOutput]

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ServerError, ClientError)),
    reraise=True
)
def detect_specification_gaps(request: GapDetectionRequest) -> GapDetectionResponse:
    """
    Detects gaps in the procurement requirement against the recommended standards.
    Uses structured output from the LLM.
    """
    if not request.recommendations:
        return GapDetectionResponse(gaps=[], summary=GapSummary(total_gaps=0, high=0, medium=0, low=0, info=0))

    # Limit to top 5 most-relevant recommendations to keep the prompt manageable
    top_recs = sorted(request.recommendations, key=lambda r: r.relevance_score, reverse=True)[:5]

    # Build context for the LLM based on the recommended standards
    standards_context = ""
    for rec in top_recs:
        standards_context += f"\n--- STANDARD: {rec.standard_number} ({rec.title}) ---\n"
        if rec.explanation:
            standards_context += f"Scope Match: {rec.explanation.scope_match}\n"
        standards_context += "Evidence Extracted from DB:\n"
        for ev in rec.evidence[:4]:  # Limit to 4 evidence items per standard
            standards_context += f"- {ev.label}: {ev.description} (Source: {ev.source.source_type if ev.source else 'Unknown'})\n"

            
    prompt = f"""
You are an expert procurement and engineering analyst for the Bureau of Indian Standards (BIS).
Your task is to analyze a user's procurement requirement against the provided recommended Indian Standards and identify important specification gaps.
A gap is defined as information that is missing, ambiguous, incomplete, or potentially insufficient for a proper procurement specification.

USER PROCUREMENT REQUIREMENT:
"{request.requirement}"

RECOMMENDED STANDARDS (BASED ON OUR DB):
{standards_context}

INSTRUCTIONS:
1. Identify gaps where the user's requirement lacks specifics that the recommended standards expect (e.g., missing grade, size, material property, test certificate requirement).
2. Do NOT invent technical requirements that are not supported by the provided RECOMMENDED STANDARDS context.
3. If the provided context does not contain enough information to determine a specific gap, DO NOT invent it.
4. Do NOT claim that a specification is legally compliant/non-compliant.
5. Do NOT invent IS numbers, clauses, technical limits, or source URLs.
6. The severity must be exactly one of: "HIGH", "MEDIUM", "LOW", "INFO".
7. Be exhaustive but strict: Only extract gaps strongly supported by the evidence. If the requirement lacks dimensions, grade, testing methods, or material properties mentioned in the evidence, you MUST flag it as a gap.
8. Do not return different results for the same input. Consistently report all missing criteria based ONLY on the evidence provided.

OUTPUT FORMAT - Return ONLY valid JSON matching this exact structure:
{{
  "gaps": [
    {{
      "gap_type": "string (e.g. MISSING_SPECIFICATION, AMBIGUOUS_REQUIREMENT, INCOMPLETE_STANDARD_REFERENCE)",
      "title": "string",
      "description": "string",
      "severity": "HIGH or MEDIUM or LOW or INFO",
      "reason": "string",
      "suggested_information": "string",
      "evidence_source_type": "string",
      "evidence_description": "string"
    }}
  ]
}}
"""
    
    client = get_client()
    try:
        import json as json_mod
        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0,
            ),
        )
        
        # Parse the response manually
        try:
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            parsed_json = json_mod.loads(raw_text.strip())
            raw_response = RawGapDetectionResponse(**parsed_json)
        except Exception as parse_err:
            logger.error(f"Gap detection JSON parse error: {parse_err}. Response: {response.text[:500]}")
            return GapDetectionResponse(gaps=[], summary=GapSummary(total_gaps=0, high=0, medium=0, low=0, info=0))
        
        gaps = []
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        
        # Currently, the prompt analyzes across all recommended standards. 
        # To strictly map a gap to a standard, we'll assign it to the top recommendation or loop logic.
        # Since the LLM might combine insights, we will assign standard_id of the first recommendation 
        # as a general fallback unless specifically parseable. We can just use the first standard id.
        default_standard_id = request.recommendations[0].standard_id if request.recommendations else "unknown"
        
        if raw_response and raw_response.gaps:
            for raw_gap in raw_response.gaps:
                severity_upper = raw_gap.severity.upper()
                if severity_upper not in counts:
                    severity_upper = "INFO"
                    
                counts[severity_upper] += 1
                
                evidence = []
                if raw_gap.evidence_description and raw_gap.evidence_description.upper() != "INSUFFICIENT_EVIDENCE":
                    evidence.append(GapEvidenceBase(
                        source_type=raw_gap.evidence_source_type or "Analysis",
                        description=raw_gap.evidence_description
                    ))
                    
                gaps.append(SpecificationGap(
                    gap_id=str(uuid.uuid4()),
                    standard_id=default_standard_id,
                    gap_type=raw_gap.gap_type,
                    title=raw_gap.title,
                    description=raw_gap.description,
                    severity=severity_upper,
                    reason=raw_gap.reason,
                    suggested_information=raw_gap.suggested_information,
                    evidence=evidence
                ))
                
        summary = GapSummary(
            total_gaps=len(gaps),
            high=counts["HIGH"],
            medium=counts["MEDIUM"],
            low=counts["LOW"],
            info=counts["INFO"]
        )
        
        return GapDetectionResponse(gaps=gaps, summary=summary)
        
    except Exception as e:
        if _is_retryable_error(e):
            raise
        logger.error(f"Error generating gaps: {e}")
        # On failure like malformed response, just return empty gracefully
        return GapDetectionResponse(gaps=[], summary=GapSummary(total_gaps=0, high=0, medium=0, low=0, info=0))
