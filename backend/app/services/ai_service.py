import os
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError
from pydantic import BaseModel
from typing import List
from app.schemas import ExtractedRequirement
from app.models import Standard
import math
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

# Get models from environment or use defaults per instructions
GENERATION_MODEL = os.environ.get("GEMINI_GENERATION_MODEL", "gemini-3.8-flash")
EMBEDDING_MODEL = os.environ.get("GEMINI_EMBEDDING_MODEL", "gemini-embedding-2")

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY must be provided in the backend process environment")
    return genai.Client(api_key=api_key)

def _is_retryable_error(exception):
    # Retry on ServerError (e.g. 503) or specific ClientError (e.g. 429 Rate Limit)
    if isinstance(exception, ServerError) and exception.code in [503, 500, 502, 504]:
        logger.warning(f"Retrying after transient ServerError: {exception.code}")
        return True
    if isinstance(exception, ClientError) and exception.code == 429:
        logger.warning("Retrying after 429 Rate Limit")
        return True
    return False

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ServerError, ClientError)),
    reraise=True
)
def extract_requirement(query: str) -> ExtractedRequirement:
    """
    Extracts structured technical intent from a raw procurement query.
    """
    prompt = f"""
    You are an expert procurement and engineering assistant for the Bureau of Indian Standards.
    Analyze the following procurement request and extract the key information.
    
    IMPORTANT RULES:
    - Do NOT invent or hallucinate any Indian Standard (IS) numbers.
    - Only structure the user's procurement requirement based exactly on what they provided.
    - Do not recommend standards in your summary.

    Request: "{query}"

    OUTPUT FORMAT - Return ONLY valid JSON matching this exact structure:
    {{
      "products": ["list of specific product names or items being procured"],
      "applications": ["list of intended applications or use cases"],
      "keywords": ["list of key technical terms, material types, properties"],
      "intent_summary": "A concise 1-2 sentence summary of what is being procured and why"
    }}
    """
    
    client = get_client()
    try:
        print(f"Using model: {GENERATION_MODEL}")
        chat = client.chats.create(model=GENERATION_MODEL)
        response = chat.send_message(
            prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        import json as json_mod
        try:
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            parsed_json = json_mod.loads(raw_text.strip())
            return ExtractedRequirement(**parsed_json)
        except Exception as parse_err:
            logger.error(f"extract_requirement JSON parse error: {parse_err}. Response: {response.text[:300]}")
            raise ValueError(f"AI response format error during requirement extraction: {parse_err}")
    except Exception as e:
        if _is_retryable_error(e):
            raise
        # Re-raise non-retryable immediately
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ServerError, ClientError)),
    reraise=True
)
def generate_embedding(text: str) -> List[float]:
    """
    Generates a dense vector embedding for the given text using gemini-embedding-2.
    """
    try:
        client = get_client()
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )
        
        embedding = response.embeddings[0].values
        
        # Validation
        if len(embedding) != 768:
            raise ValueError(f"Expected 768 dimensions, got {len(embedding)}")
            
        for val in embedding:
            if not isinstance(val, (int, float)):
                raise ValueError("Embedding contains non-numeric values")
            if math.isnan(val) or math.isinf(val):
                raise ValueError("Embedding contains NaN or infinite values")
                
        # Ensure it's not silently returning a zero vector
        if all(v == 0.0 for v in embedding):
            raise ValueError("Embedding is a zero vector")
            
        return embedding
    except Exception as e:
        if _is_retryable_error(e):
            raise
        if isinstance(e, (ValueError, TypeError)):
            raise
        # Wrap other errors
        raise Exception(f"Embedding API request failed: {str(e)}")


def build_standard_embedding_text(standard: Standard) -> str:
    """
    Builds a deterministic string representation of a Standard for embedding generation.
    Relies ONLY on structured metadata already stored in the database.
    """
    lines = []
    lines.append(f"Standard: {standard.standard_number}")
    lines.append(f"Title: {standard.title}")
    
    if standard.short_description:
        lines.append(f"Description: {standard.short_description}")
        
    if standard.sector and standard.sector.name:
        lines.append(f"Sector: {standard.sector.name}")
        
    if standard.category and standard.category.name:
        lines.append(f"Category: {standard.category.name}")
        
    scopes_text = " ".join([s.scope_text for s in standard.scopes if s.scope_text])
    if scopes_text:
        lines.append(f"Scope: {scopes_text}")
        
    keywords_text = ", ".join([k.keyword.word for k in standard.keywords if k.keyword])
    if keywords_text:
        lines.append(f"Keywords: {keywords_text}")
        
    return "\n".join(lines)
