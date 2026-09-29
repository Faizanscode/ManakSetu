# Knowledge Base & Data Strategy

## MVP Target
For the SIH screening round, the prototype will target **200–300 well-structured standards** to demonstrate the system's depth and accuracy without requiring the entire national catalogue. 

## Domain Distribution
The initial dataset will cover high-value and frequently procured domains:
1. Electrical & Electronics
2. Civil & Construction Materials
3. Mechanical & Industrial Equipment
4. Safety & Personal Protective Equipment (PPE)
5. Water, Sanitation & Health
6. Information Technology

## Data Acquisition Strategy
We will strictly adhere to legal and ethical data acquisition practices:
- **Primary Sources**: Publicly available metadata from authoritative sources (e.g., BIS catalogues, public procurement portals).
- **Curation**: For the MVP, a curated set of prototype data representing real-world standard structures will be manually or semi-automatically ingested.
- **No Illegal Scraping**: The system will not scrape paywalled PDFs or violate BIS copyrights.
- **Provenance**: Every record will include a `source_url` and `retrieval_date` to maintain auditability.

## Knowledge Graph / Relationship Strategy
Relationships (Normative, Supersedes, Related) will be modeled natively in PostgreSQL using relational tables (`standard_relationships`). 
- **Recursive CTEs**: We will use SQL Recursive Common Table Expressions to traverse relationships (e.g., finding all normative references of a normative reference).
- No external Graph Database is necessary for the MVP scale.

## Official vs. AI-Generated Data
The UI and Data Layer will strictly separate:
- **Source Information**: Factual standard metadata, versions, and explicit scope directly from official sources.
- **AI Analysis**: Extracted intent, semantic matching scores, and inferred applicability.
*Rule: AI must never fabricate an IS number, title, or clause.*
