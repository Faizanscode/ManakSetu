# System Architecture

## Overview
ManakSetu is an AI-Powered Recommendation Engine designed to identify applicable Indian Standards for procurement specifications. The architecture is modular and scalable, strictly separating factual standards data from AI-generated insights.

## Technology Stack
- **Frontend**: React, Vite, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL with `pgvector` extension for embeddings and similarity search
- **AI/RAG Layer**: Hybrid retrieval system combining structured queries, semantic search, and AI-driven reranking

## Architecture Components
### 1. Client Layer (Frontend)
- **Framework**: React (Vite)
- **Role**: Provides the user interface for procurement officials to enter requirements, view recommended standards, and generate technical specifications.
- **Key Features**: Chat/Query interface, Explainability dashboard, Specification export.

### 2. Application Layer (Backend)
- **Framework**: FastAPI (Python)
- **Role**: Exposes REST APIs, orchestrates the retrieval pipeline, and interfaces with the LLM.
- **Key Modules**:
  - `QueryAnalyzer`: Parses raw procurement requests.
  - `RetrievalEngine`: Orchestrates hybrid search across PostgreSQL.
  - `RankingEngine`: Computes multi-dimensional relevance scores.
  - `SpecGenerator`: Grounds generated specifications in retrieved standards.

### 3. Data & AI Layer (PostgreSQL + pgvector)
- **Role**: Stores structured metadata, standard relationships, and high-dimensional vector embeddings.
- **Features**: Hybrid retrieval (SQL filtering + Vector similarity), Relationship traversal (e.g., recursive queries for normative references).

## Proposed Project Directory Structure
```text
manaksetu/
├── frontend/             # React/Vite/TS/Tailwind
├── backend/              # FastAPI Python backend
│   ├── api/              # Route definitions
│   ├── core/             # Config, security, logging
│   ├── services/         # AI, RAG, scoring logic
│   └── models/           # Pydantic schemas, DB models
├── database/             # Alembic migrations, init scripts
├── ai_retrieval/         # Embedding generation, reranking
├── ingestion/            # Scripts to populate the KB
├── tests/                # Pytest and frontend tests
└── docs/                 # Project documentation
```

## Security and Data Integrity
- **Secrets Management**: All DB credentials, API keys, and environment variables stored securely (.env, Secrets Manager).
- **Provenance**: Strict lineage tracking for all standards data to ensure AI recommendations are grounded in reality.
- **Sanitization**: API input validation via Pydantic; prevention of prompt injection and SQL injection.
- **Auditability**: Logging of all procurement queries and resulting recommendations for continuous improvement.
