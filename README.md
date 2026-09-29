# 🇮🇳 ManakSetu

### AI-Powered Recommendation Engine for Identifying Applicable Indian Standards for Procurement Specifications

> **Connecting Procurement Requirements with the Right Indian Standards**

ManakSetu is an AI-assisted procurement intelligence platform designed to help procurement officials identify applicable **Indian Standards (IS)** from natural-language procurement requirements.

Instead of manually searching through large collections of standards, ManakSetu analyzes a procurement specification, understands its technical requirements, retrieves relevant standards from a curated knowledge base, explains why each standard is applicable, detects missing specification details, and helps generate a standards-aligned procurement specification.

---

## 🎯 Problem Statement

### SIH PS26108

**AI-Powered Recommendation Engine for Identifying Applicable Indian Standards for Procurement Specifications**

Government and institutional procurement specifications often contain technical requirements for products, materials, equipment, construction work, electrical systems, safety equipment, and other goods or services.

Identifying the correct Indian Standards manually can be:

- Time-consuming
- Difficult for non-specialist procurement users
- Prone to missing relevant standards
- Difficult when multiple related standards apply
- Challenging when specifications are incomplete

ManakSetu addresses this problem by combining:

- Natural-language requirement analysis
- Semantic search
- Structured database filtering
- Standards relationship analysis
- AI-assisted reasoning
- Evidence-based recommendations
- Specification gap detection
- Procurement specification generation

---

# 🚀 Key Features

## 1. Procurement Requirement Analysis

Users can enter procurement requirements using natural language.

Example:

> We need 2,500 square meters of durable floor tiles for a government administrative building. The tiles should be suitable for high foot-traffic areas with adequate breaking strength, abrasion resistance, low water absorption, dimensional consistency, and slip resistance.

ManakSetu extracts structured information such as:

- Product
- Material
- Application
- Quantity
- Technical characteristics
- Performance requirements
- Intended use
- Relevant keywords
- Sector/category

---

## 2. Indian Standards Knowledge Base

ManakSetu currently uses a curated knowledge base containing:

### **293 verified Indian Standards**

The current prototype covers five major sectors:

- Civil Engineering
- Electrical Engineering
- Mechanical Engineering
- Water & Sanitation
- Industrial Safety

The knowledge base contains structured metadata including:

- IS number
- Standard title
- Description
- Sector
- Category
- Scope
- Keywords
- Version/status information
- Relationships
- Source information
- Semantic embeddings

> **Note:** The 293-standard knowledge base is a curated prototype dataset and does not represent the complete BIS catalogue.

---

## 3. Semantic Standard Retrieval

ManakSetu converts procurement requirements and standards into vector representations and uses semantic similarity to identify relevant candidates.

Technology:

- PostgreSQL
- pgvector
- Gemini Embeddings
- Semantic similarity search

This allows the system to recognize related concepts even when the wording used by the procurement officer differs from the wording in the standard metadata.

---

## 4. Multi-Signal Recommendation Engine

ManakSetu does not depend only on semantic similarity.

Recommendations combine multiple signals:

```text
Semantic Similarity
        +
Product Match
        +
Application Match
        +
Keyword Match
        +
Scope Match
        +
Category / Sector Match
        +
Version / Status
        +
Standard Relationships
        ↓
Recommendation
