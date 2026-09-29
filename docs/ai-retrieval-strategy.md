# AI & Hybrid Retrieval Strategy

## Overview
The retrieval system uses a Hybrid Search architecture to bridge the gap between unstructured procurement language and strictly structured standards data.

## Pipeline Architecture
1. **Requirement Understanding**: The LLM extracts intent, entities, and technical specifications from the raw procurement request.
2. **Hybrid Search execution**:
   - **Structured Search**: Filters by extracted categories, sectors, status (e.g., `is_current = True`), and keywords.
   - **Semantic Search**: `pgvector` computes cosine/L2 distance between the procurement requirement embedding and `standard_embeddings`.
3. **Filtering**: Standards outside the required scope or marked as "superseded" (unless specifically requested) are heavily penalized or removed.
4. **Relationship Expansion**: The system fetches normative references linked to the top candidate standards to ensure completeness.
5. **Reranking**: An AI or cross-encoder model evaluates the candidate list against the original query to assign a final relevance score.

## Recommendation Score Design
The final recommendation score is a weighted composite of distinct signals, enabling explainability:
- **Semantic Similarity** (30%): Vector distance match.
- **Category/Product Match** (20%): Exact or hierarchical taxonomy match.
- **Scope Match** (20%): Alignment with included/excluded applications.
- **Requirement Match** (15%): Satisfaction of specific technical parameters.
- **Status/Relationship** (15%): Current version status and normative relevance.

(Weights are illustrative and will be tuned during implementation).
