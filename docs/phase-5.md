# Phase 5: Explainability & Evidence Engine

## Overview
Phase 5 implements the Explainability and Evidence layer for ManakSetu, allowing users to understand exactly *why* a particular Indian Standard was recommended for their procurement requirement. By linking the recommendation logic directly to database-backed evidence, the system ensures transparency, traceability, and confidence without fabricating or hallucinating data.

## Explainability Architecture
The architecture is structured to map the backend evidence (provenance) to frontend representations seamlessly:

1. **Extraction & Similarity**: The system extracts structured parameters (Products, Applications, Keywords) and intent from the user query using Gemini.
2. **Metadata Matching**: The Recommendation Engine scores each standard against the extracted requirement.
3. **Evidence Construction**:
   - Instead of simply passing abstract scores to the frontend, the system populates structured `EvidenceItem` objects.
   - It captures the matching parameters across semantics, products, applications, keywords, and scope.
   - For every point of evidence (e.g., standard category, specific keyword match, scope alignment), the system links an `EvidenceSource` (organization, source type, URL, retrieved timestamp) from the `standard_sources` table.
4. **Structured Delivery**: The recommendation payload sent to the frontend includes:
   - `explanation`: High-level summary of matching criteria.
   - `evidence`: Detailed list of `EvidenceItem` with source data.
   - `score_breakdown`: Detailed point-by-point breakdown.
   - `relationships`: Linked standard data from `standard_relationships`.
   - `sources`: Aggregated `EvidenceSource` metadata for tracking.

## Limitations
- **Prototype Scope**: This is a prototype knowledge base with 15 standards. It does not reflect the entire BIS catalogue.
- **Evidence URL Availability**: Some evidence may have metadata (organization, source type) but lack a direct web URL (`url` is optional/nullable). 
- **Not a Legal Substitute**: The explainability engine assists in identifying relevance based on text and parameters, but it is not a certification or legal guarantee of compliance.
- **Static Corpus**: The evidence is grounded to the data ingested during Phase 2. Updates to standards from BIS require a new data ingestion cycle.

## How to Read the Evidence UI
- **Why recommended**: Provides a quick summary of what matched.
- **Why This Standard**: Expands to show individual `EvidenceItem` objects, pointing out exactly which keyword, product, application, or semantic scope triggered the match, along with the specific source if available.
- **Score Breakdown**: A numerical visualization of the recommendation logic, highlighting which factor (Semantic, Product, Keyword, Application, Scope, Category/Sector) contributed the most to the relevance score.
- **Sources**: Explicit references backing the standard information. It clearly separates *Source Data* from *AI Analysis*, and users should refer to these sources to verify the standard edition and status.
