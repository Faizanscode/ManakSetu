# Explainability & Specification Generation Strategy

## Explainability Design
ManakSetu avoids "black box" AI percentages. When a standard is recommended, the UI will present clear, component-based evidence.

### Evidence Display Structure
**WHY THIS STANDARD?**
- ✓ **Product Match**: The standard explicitly covers "[Product Name]".
- ✓ **Scope Match**: Recommended for "[Specific Application]" as identified in your request.
- ✓ **Current Version**: IS [Number]:[Year] is the active version.
- ✓ **Normative Requirement**: It is a required foundational standard for [Primary Standard].

### Evidence Grounding
- **Factual**: Direct UI links to `standard_sources` data.
- **Derived**: Clear visual indicators denoting AI-inferred relevance vs. hard-coded facts.

## Specification Gap Detection
Before generating a specification, the system compares the user's prompt against the typical requirements found in the recommended standards.
- *Data Flow*: User Input -> LLM analyzes extracted entities -> Compares against `standard_requirements` for the matched category -> Flags missing parameters (e.g., "You requested Industrial Safety Shoes, but did not specify the required toe-impact resistance (Joules).")

## Specification Generator
**Goal**: Assist the procurement officer in drafting a comprehensive tender document.
- **Process**: Uses the validated standards, the user's constraints, and the gap-detection inputs to formulate a structured document.
- **Sections Generated**: Scope, Applicable Standards list (with correct years), Technical Requirements, Testing/Inspection Protocols.
- **Constraint**: The generator is strictly grounded in retrieved context (RAG). It cannot invent testing parameters that do not exist in the referenced standards.
