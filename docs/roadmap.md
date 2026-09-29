# Master Implementation Roadmap

## Phase 0: Architecture & Data Strategy (Current)
- Finalize system design, logical schemas, and knowledge base strategy.
- Establish project rules, boundaries, and AI retrieval architecture.

## Phase 1: Project Setup & UI Shell
- Initialize Git repository.
- Setup React/Vite/Tailwind frontend shell.
- Setup FastAPI backend and PostgreSQL database.
- Configure environment variables and basic routing.

## Phase 2: Standards Knowledge Base
- Implement DB migrations.
- Ingest 200–300 curated, well-structured standards (metadata, versions, scopes).
- Build basic search/filter APIs.

## Phase 3: Requirement Analysis Engine
- Implement LLM prompt chains to extract structured intent from raw procurement requests.
- Integrate embedding generation for the query.

## Phase 4: Recommendation Engine
- Implement `pgvector` hybrid search.
- Build the multi-signal scoring model (semantic + structured + relational).
- Tune retrieval weights.

## Phase 5: Explainability & Evidence
- Map recommendation scores to human-readable evidence.
- Build the "Why this standard?" UI component.
- Surface version status and normative relationship graphs.

## Phase 6: Specification Gap Detection
- Implement the logic to compare user requests against standard requirements.
- Build the UI to prompt users for missing critical parameters.

## Phase 7: Specification Generator
- Implement the RAG-based specification drafting tool.
- Ground generation strictly in retrieved standard data.
- Add export functionality (PDF/Word).

## Phase 8: History, Reports, & Export
- Implement user session history and query logs.
- Add dashboard analytics for procurement trends.

## Phase 9: Demo Polish & SIH Presentation Flow
- Final UI/UX polish.
- Pre-cache demo queries.
- Rehearse the standard SIH presentation flow (Query -> Extract -> Recommend -> Explain -> Gap Detect -> Generate).
