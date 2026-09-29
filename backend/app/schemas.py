from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SectorBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class CategoryBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    sector_id: str

class KeywordBase(BaseModel):
    id: str
    word: str

class StandardSourceBase(BaseModel):
    id: str
    organization: str
    source_type: str
    title: Optional[str] = None
    url: Optional[str] = None
    document_name: Optional[str] = None
    page: Optional[str] = None
    section: Optional[str] = None
    retrieved_at: Optional[datetime] = None
    notes: Optional[str] = None

class StandardVersionBase(BaseModel):
    id: str
    edition: str
    publication_date: Optional[str] = None
    effective_date: Optional[str] = None
    status: str
    amendment_information: Optional[str] = None
    supersedes_version_id: Optional[str] = None

class StandardScopeBase(BaseModel):
    id: str
    scope_text: str
    included_products: Optional[str] = None
    excluded_products: Optional[str] = None
    applications: Optional[str] = None

class StandardRelationshipBase(BaseModel):
    id: str
    source_standard_id: str
    target_standard_id: str
    relationship_type: str
    description: Optional[str] = None

class StandardBase(BaseModel):
    id: str
    standard_number: str
    title: str
    short_description: Optional[str] = None
    issuing_body: str
    status: str
    sector_id: Optional[str] = None
    category_id: Optional[str] = None

class StandardDetail(StandardBase):
    sector: Optional[SectorBase] = None
    category: Optional[CategoryBase] = None
    versions: List[StandardVersionBase] = []
    scopes: List[StandardScopeBase] = []
    keywords: List[KeywordBase] = []
    sources: List[StandardSourceBase] = []

    class Config:
        from_attributes = True

class StandardList(StandardBase):
    sector: Optional[SectorBase] = None
    category: Optional[CategoryBase] = None

    class Config:
        from_attributes = True

class RequirementAnalysisRequest(BaseModel):
    query: str

class ExtractedRequirement(BaseModel):
    products: List[str]
    applications: List[str]
    keywords: List[str]
    intent_summary: str

class RequirementAnalysisResponse(BaseModel):
    extracted: ExtractedRequirement
    embedding_status: str
    embedding_preview: Optional[List[float]] = None

class RecommendedStandardVersion(BaseModel):
    edition: str
    status: str
    publication_date: Optional[str] = None
    effective_date: Optional[str] = None

class ExplanationSummary(BaseModel):
    summary: str
    product_matches: List[str]
    application_matches: List[str]
    keyword_matches: List[str]
    scope_match: bool

class EvidenceSource(BaseModel):
    organization: str
    source_type: str
    title: Optional[str] = None
    url: Optional[str] = None
    document_name: Optional[str] = None
    page: Optional[str] = None
    section: Optional[str] = None
    retrieved_at: Optional[datetime] = None

class EvidenceItem(BaseModel):
    type: str
    label: str
    description: str
    source: Optional[EvidenceSource] = None

class RecommendedRelationship(BaseModel):
    related_standard: str
    relationship_type: str
    description: Optional[str] = None
    source: Optional[EvidenceSource] = None

class ScoreBreakdown(BaseModel):
    semantic: float
    product: float
    application: float
    keyword: float
    scope: float
    category_sector: float

class Recommendation(BaseModel):
    standard_id: str
    standard_number: str
    title: str
    relevance_category: str
    relevance_score: float
    status: str
    version: Optional[RecommendedStandardVersion] = None
    why_recommended: List[str]
    explanation: ExplanationSummary
    evidence: List[EvidenceItem]
    score_breakdown: ScoreBreakdown
    relationships: List[RecommendedRelationship] = []
    sources: List[EvidenceSource] = []

class RecommendationRequest(BaseModel):
    query: str

class RecommendationResponse(BaseModel):
    query: str
    recommendations: List[Recommendation]
    candidate_count: int
    message: Optional[str] = None

class GapEvidenceBase(BaseModel):
    source_type: str
    description: str
    reference_id: Optional[str] = None

class SpecificationGap(BaseModel):
    gap_id: str
    standard_id: str
    gap_type: str
    title: str
    description: str
    severity: str
    reason: str
    suggested_information: str
    evidence: List[GapEvidenceBase] = []

class GapSummary(BaseModel):
    total_gaps: int
    high: int
    medium: int
    low: int
    info: int

class GapDetectionRequest(BaseModel):
    requirement: str
    recommendations: List[Recommendation]

class GapDetectionResponse(BaseModel):
    gaps: List[SpecificationGap]
    summary: GapSummary


class SpecItem(BaseModel):
    requirement: str
    source: str
    source_type: str # USER_PROVIDED, KNOWLEDGE_BASE, AI_DERIVED, REQUIRES_VERIFICATION

class SpecStandard(BaseModel):
    standard_id: str
    standard_number: str
    title: str
    relevance: str
    evidence_summary: Optional[str] = None

class SpecificationDraft(BaseModel):
    title: str
    procurement_objective: str
    product_description: str
    intended_application: str
    applicable_standards: List[SpecStandard] = []
    technical_requirements: List[SpecItem] = []
    material_requirements: List[SpecItem] = []
    dimensional_requirements: List[SpecItem] = []
    performance_requirements: List[SpecItem] = []
    testing_requirements: List[SpecItem] = []
    quality_requirements: List[SpecItem] = []
    packaging_requirements: List[SpecItem] = []
    documentation_requirements: List[SpecItem] = []
    items_requiring_clarification: List[str] = []

class SpecificationMetadata(BaseModel):
    generated_at: str
    standard_count: int
    gap_count: int

class SpecificationRequest(BaseModel):
    requirement: str
    analysis: RequirementAnalysisResponse
    recommendations: List[Recommendation]
    gaps: List[SpecificationGap]

class SpecificationResponse(BaseModel):
    specification: SpecificationDraft
    metadata: SpecificationMetadata

class AnalysisHistoryBase(BaseModel):
    title: str
    procurement_requirement: str
    category: Optional[str] = None
    priority: Optional[str] = None
    
    extracted_requirement: Optional[dict] = None
    recommendations: Optional[dict] = None
    gaps: Optional[dict] = None
    specification: Optional[dict] = None
    
    status: Optional[str] = "COMPLETED"

class AnalysisHistoryCreate(AnalysisHistoryBase):
    pass

class AnalysisHistoryUpdate(BaseModel):
    title: Optional[str] = None
    procurement_requirement: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    extracted_requirement: Optional[dict] = None
    recommendations: Optional[dict] = None
    gaps: Optional[dict] = None
    specification: Optional[dict] = None
    status: Optional[str] = None

class AnalysisHistoryResponse(AnalysisHistoryBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AnalysisHistoryList(BaseModel):
    id: str
    title: str
    procurement_requirement: str
    category: Optional[str] = None
    priority: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

