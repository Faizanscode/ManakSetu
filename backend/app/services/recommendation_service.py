import logging
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.models import Standard
from app.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    Recommendation,
    ExplanationSummary,
    ScoreBreakdown,
    RecommendedStandardVersion,
    EvidenceItem,
    EvidenceSource,
    RecommendedRelationship
)
from app.services.ai_service import extract_requirement, generate_embedding
import re

logger = logging.getLogger(__name__)

# Weights
SEMANTIC_WEIGHT = 0.40
PRODUCT_WEIGHT = 0.20
APPLICATION_WEIGHT = 0.15
KEYWORD_WEIGHT = 0.10
SCOPE_WEIGHT = 0.10
CATEGORY_SECTOR_WEIGHT = 0.05

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'[^a-z0-9\s]', ' ', text.lower()).strip()

def text_contains(text: str, search_terms: List[str]) -> List[str]:
    matches = []
    norm_text = normalize_text(text)
    text_tokens = set(norm_text.split())
    for term in search_terms:
        norm_term = normalize_text(term)
        if norm_term in norm_text:
            matches.append(term)
        else:
            term_tokens = set(norm_term.split())
            # If significant overlap (e.g., > 50% of term tokens in text)
            if term_tokens and len(term_tokens.intersection(text_tokens)) / len(term_tokens) >= 0.5:
                matches.append(term)
    return list(set(matches))

def get_recommendations(db: Session, request: RecommendationRequest) -> RecommendationResponse:
    # 1. Requirement extraction
    extracted = extract_requirement(request.query)

    # 2. Requirement embedding
    embed_input = (
        f"Intent: {extracted.intent_summary}\n"
        f"Products: {', '.join(extracted.products)}\n"
        f"Applications: {', '.join(extracted.applications)}\n"
        f"Keywords: {', '.join(extracted.keywords)}"
    )
    req_embedding = generate_embedding(embed_input)

    # 3. pgvector candidate retrieval
    candidates = db.execute(
        select(Standard, Standard.embedding.cosine_distance(req_embedding).label("distance"))
        .filter(Standard.embedding != None)
        .order_by("distance")
        .limit(10)
    ).all()

    if not candidates:
        return RecommendationResponse(
            query=request.query,
            recommendations=[],
            candidate_count=0,
            message="No sufficiently relevant Indian Standard was identified in the current ManakSetu knowledge base."
        )

    recommendations = []

    for row in candidates:
        std = row.Standard
        distance = row.distance
        
        # Status filtering
        if std.status in ["WITHDRAWN", "SUPERSEDED"]:
            continue
        
        # Calculate scores
        # A. Semantic Score (cosine distance to similarity)
        semantic_sim = 1.0 - (distance if distance is not None else 1.0)
        semantic_score = max(0.0, min(1.0, semantic_sim))

        # Collect text fields
        std_title = std.title or ""
        std_desc = std.short_description or ""
        std_scope_text = " ".join([s.scope_text for s in std.scopes if s.scope_text])
        std_included_products = " ".join([s.included_products for s in std.scopes if s.included_products])
        std_excluded_products = " ".join([s.excluded_products for s in std.scopes if s.excluded_products])
        std_applications = " ".join([s.applications for s in std.scopes if s.applications])
        std_keywords = [k.keyword.word for k in std.keywords if k.keyword]
        std_sector = std.sector.name if std.sector else ""
        std_category = std.category.name if std.category else ""

        full_text = " ".join([std_title, std_desc, std_scope_text, std_included_products, std_applications] + std_keywords)

        # B. Product Match Score
        matched_products = text_contains(full_text, extracted.products)
        product_score = len(matched_products) / max(1, len(extracted.products)) if extracted.products else 0.0

        # C. Application Match Score
        matched_applications = text_contains(full_text, extracted.applications)
        application_score = len(matched_applications) / max(1, len(extracted.applications)) if extracted.applications else 0.0

        # D. Keyword Match Score
        matched_keywords = text_contains(full_text, extracted.keywords)
        keyword_score = len(matched_keywords) / max(1, len(extracted.keywords)) if extracted.keywords else 0.0

        # E. Scope Match Score
        scope_score = 0.0
        if len(matched_products) > 0 or len(matched_applications) > 0:
            scope_score = 1.0
        
        excluded = text_contains(std_excluded_products, extracted.products)
        if excluded:
            scope_score = 0.0
            product_score = 0.0 # Penalty

        # F. Category/Sector Match
        category_match = False
        sector_match = False
        cat_sec_text = std_sector + " " + std_category
        cat_matches = text_contains(cat_sec_text, extracted.keywords + extracted.products)
        cat_sec_score = 0.0
        if cat_matches:
            cat_sec_score = 1.0
            category_match = True
            sector_match = True

        # G. Weighted Ranking
        final_score = (
            semantic_score * SEMANTIC_WEIGHT +
            product_score * PRODUCT_WEIGHT +
            application_score * APPLICATION_WEIGHT +
            keyword_score * KEYWORD_WEIGHT +
            scope_score * SCOPE_WEIGHT +
            cat_sec_score * CATEGORY_SECTOR_WEIGHT
        )

        if final_score < 0.2:
            continue

        if final_score >= 0.7:
            rel_cat = "HIGH RELEVANCE"
        elif final_score >= 0.4:
            rel_cat = "MODERATE RELEVANCE"
        else:
            rel_cat = "LOW RELEVANCE"

        why = []
        if product_score > 0:
            why.append(f"Product matches the standard scope")
        if application_score > 0:
            why.append("Application is covered by the standard")
        if keyword_score > 0:
            why.append("Multiple procurement keywords match")
        
        if not why:
            why.append("Semantic similarity suggests relevance")

        # Get latest version
        current_version = None
        versions = [v for v in std.versions]
        if versions:
            for v in versions:
                if v.status == "CURRENT":
                    current_version = RecommendedStandardVersion(edition=v.edition, status=v.status)
                    break
            if not current_version:
                v = versions[0]
                current_version = RecommendedStandardVersion(edition=v.edition, status=v.status)

        # Construct Explanation Summary
        explanation = ExplanationSummary(
            summary="Recommended based on the available knowledge-base evidence.",
            product_matches=matched_products,
            application_matches=matched_applications,
            keyword_matches=matched_keywords,
            scope_match=(scope_score > 0)
        )

        evidence_items = []
        if matched_products:
            evidence_items.append(EvidenceItem(
                type="PRODUCT_MATCH",
                label="Product Match",
                description=f"Requirement product(s) '{', '.join(matched_products)}' found in standard scope."
            ))
        if matched_applications:
            evidence_items.append(EvidenceItem(
                type="APPLICATION_MATCH",
                label="Application Match",
                description=f"Requirement application(s) '{', '.join(matched_applications)}' found in standard scope."
            ))
        if matched_keywords:
            evidence_items.append(EvidenceItem(
                type="KEYWORD_MATCH",
                label="Keyword Match",
                description=f"Requirement keyword(s) '{', '.join(matched_keywords)}' match standard terms."
            ))
        if scope_score > 0:
            evidence_items.append(EvidenceItem(
                type="SCOPE_MATCH",
                label="Scope Match",
                description="The procurement requirement's product and/or application match the standard's stored scope."
            ))
        if category_match:
            evidence_items.append(EvidenceItem(
                type="CATEGORY_MATCH",
                label="Category Match",
                description=f"Matches category '{std_category}'."
            ))
        if sector_match:
            evidence_items.append(EvidenceItem(
                type="SECTOR_MATCH",
                label="Sector Match",
                description=f"Matches sector '{std_sector}'."
            ))

        # Sources and versions mapping
        sources = []
        for src in std.sources:
            sources.append(EvidenceSource(
                organization=src.organization,
                source_type=src.source_type,
                title=src.title,
                url=src.url,
                document_name=src.document_name,
                page=src.page,
                section=src.section,
                retrieved_at=src.retrieved_at
            ))

        # Attach sources to scope evidence if available
        if scope_score > 0 and sources:
            for item in evidence_items:
                if item.type == "SCOPE_MATCH":
                    item.source = sources[0]

        relationships = []
        for r in std.relationships_as_source:
            # We don't have target standard title easily without querying, but we have target_standard_id.
            # In Phase 2 schemas, relationship doesn't fetch target_standard deeply unless eager loaded. 
            # We will use relationship_type.
            relationships.append(RecommendedRelationship(
                related_standard=r.target_standard_id,
                relationship_type=r.relationship_type,
                description=r.description
            ))

        rec = Recommendation(
            standard_id=std.id,
            standard_number=std.standard_number,
            title=std.title,
            relevance_category=rel_cat,
            relevance_score=round(final_score, 4),
            status=std.status,
            version=current_version,
            why_recommended=why,
            explanation=explanation,
            evidence=evidence_items,
            score_breakdown=ScoreBreakdown(
                semantic=round(semantic_score, 4),
                product=round(product_score, 4),
                application=round(application_score, 4),
                keyword=round(keyword_score, 4),
                scope=round(scope_score, 4),
                category_sector=round(cat_sec_score, 4)
            ),
            relationships=relationships,
            sources=sources
        )
        recommendations.append(rec)

    # Sort descending
    recommendations.sort(key=lambda x: x.relevance_score, reverse=True)

    if not recommendations:
        return RecommendationResponse(
            query=request.query,
            recommendations=[],
            candidate_count=len(candidates),
            message="No sufficiently relevant Indian Standard was identified in the current ManakSetu knowledge base."
        )

    return RecommendationResponse(
        query=request.query,
        recommendations=recommendations,
        candidate_count=len(candidates)
    )
