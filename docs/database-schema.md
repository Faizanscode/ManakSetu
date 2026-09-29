# Logical Database Schema Design

The following tables define the relational and vector data structures required for ManakSetu.

## Core Taxonomy Tables
- **`sectors`**: High-level industry sectors (e.g., Civil, Electrical).
- **`categories`**: Sub-categories under sectors.
- **`keywords`**: Global dictionary of technical keywords.

## Standards Knowledge Base (MVP Essential)
- **`standards`**: 
  - *Fields*: id, standard_number, title, description, scope, sector_id, category_id, issuing_organization, status.
- **`standard_versions`**:
  - *Fields*: id, standard_id, edition_year, publication_date, effective_date, is_current.
- **`standard_keywords`**: Mapping table between standards and keywords.
- **`standard_relationships`**:
  - *Fields*: source_standard_id, target_standard_id, relationship_type (normative, related, supersedes, superseded_by, amendment).
- **`standard_sources`**:
  - *Fields*: id, standard_id, source_organization, source_type, source_url, document_name, retrieval_date.

## Detailed Standard Data
- **`standard_scope`**:
  - *Fields*: id, standard_id, included_products, excluded_products, applications, scope_text.
- **`standard_requirements`**:
  - *Fields*: id, standard_id, requirement_type, requirement_name, description, is_mandatory, unit, value_type.

## Vector Storage (pgvector)
- **`standard_embeddings`** (MVP Essential):
  - *Fields*: id, standard_id, chunk_type (title, scope, requirement), chunk_content, embedding (vector), metadata (JSONB).

## Transactional / Workflow Tables
- **`procurement_requests`**: 
  - *Fields*: id, user_id, raw_query, timestamp.
- **`extracted_requirements`**:
  - *Fields*: id, request_id, inferred_category, inferred_requirements (JSONB).
- **`recommendations`**:
  - *Fields*: id, request_id, standard_id, final_score, ranking_position.
- **`recommendation_evidence`**:
  - *Fields*: id, recommendation_id, evidence_type (semantic, scope, normative), description, factual_source_id.
- **`specification_gaps`**:
  - *Fields*: id, request_id, missing_requirement_type, description.
- **`procurement_specifications`**:
  - *Fields*: id, request_id, generated_text, status (draft, finalized).
- **`specification_standards`**: Mapping between final specifications and adopted standards.
