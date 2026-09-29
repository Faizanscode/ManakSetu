# Phase 3: Requirement Analysis Engine

## Phase 3 Purpose
Phase 3 establishes the foundation for understanding raw, unstructured procurement requests and preparing them for search. It does this by extracting a structured intent and generating a dense vector embedding of the request.

## Requirement Extraction Flow
1. The user submits a raw procurement query (e.g., "We need standards for electrical transformers").
2. The `POST /api/analyze/` endpoint receives the request.
3. The query is passed to a Gemini LLM (acting as an expert procurement and engineering assistant) with explicit instructions not to invent any Indian Standard numbers.
4. The LLM returns a structured JSON payload using Gemini's `response_schema` feature.

## Structured Output Schema
The output is enforced to follow the `ExtractedRequirement` Pydantic model:
- `products` (List[str]): Extracted materials or products.
- `applications` (List[str]): End-use cases or applications.
- `keywords` (List[str]): Technical terms and keywords.
- `intent_summary` (str): A concise summary of the standard they are looking for.

## Gemini Models Used
- **Generation**: `gemini-2.5-flash`
- **Embedding**: `gemini-embedding-2`

## Embedding Dimensions
The generated embeddings are strictly `768` dimensions to match `gemini-embedding-2` specifications. The `output_dimensionality` parameter is used to enforce this dimension constraint.

## Database Embedding Storage
The `standards` table has been updated to include an `embedding` column of type `Vector(768)` using PostgreSQL's `pgvector` extension. This prepares the standards data to be searchable via cosine/L2 distance in the future. Currently, a deterministic text generation function is available to map standard metadata (title, sector, category, scope, keywords) into embedding text.

## API Endpoint
- **URL**: `POST /api/analyze/`
- **Request Body**: `{"query": "string"}`
- **Response Body**:
  - `extracted`: The `ExtractedRequirement` JSON
  - `embedding_status`: "SUCCESS"
  - `embedding_preview`: First 5 dimensions of the 768-dim vector.

## Test Results
- Database migration tests passed. The `standards.embedding` column exists and the 15 seed standards are preserved intact.
- AI tests are properly configured to skip gracefully if `GEMINI_API_KEY` is not provided in the `.env` file.

## Known Limitations
- The embedding function is implemented but the system does not yet automatically generate embeddings for the 15 seed standards in the database upon startup.
- `GEMINI_API_KEY` is required for the `/api/analyze/` endpoint to function.

**NOTE:** Phase 4 recommendation/search/ranking has NOT been implemented.
