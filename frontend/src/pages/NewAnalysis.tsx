import { useState } from 'react';
import { FileSearch, AlertCircle, CheckCircle2, Loader2, BookOpen, ChevronDown, ChevronUp, AlertTriangle } from 'lucide-react';
import ErrorBoundary from '../components/ErrorBoundary';
import { SpecificationGenerator } from '../components/SpecificationGenerator';
interface EvidenceSource {
  organization: string;
  source_type: string;
  title?: string;
  url?: string;
  document_name?: string;
  page?: string;
  section?: string;
  retrieved_at?: string;
}

interface EvidenceItem {
  type: string;
  label: string;
  description: string;
  source?: EvidenceSource;
}

interface RecommendedRelationship {
  related_standard: string;
  relationship_type: string;
  description?: string;
  source?: EvidenceSource;
}

interface ExplanationSummary {
  summary: string;
  product_matches: string[];
  application_matches: string[];
  keyword_matches: string[];
  scope_match: boolean;
}

interface ScoreBreakdown {
  semantic: number;
  product: number;
  application: number;
  keyword: number;
  scope: number;
  category_sector: number;
}

interface StandardVersion {
  edition: string;
  status: string;
  publication_date?: string;
  effective_date?: string;
}

interface Recommendation {
  standard_id: string;
  standard_number: string;
  title: string;
  relevance_category: string;
  relevance_score: number;
  status: string;
  version: StandardVersion;
  why_recommended: string[];
  explanation: ExplanationSummary;
  evidence: EvidenceItem[];
  score_breakdown: ScoreBreakdown;
  relationships: RecommendedRelationship[];
  sources: EvidenceSource[];
}

interface RecommendationResponse {
  query: string;
  recommendations: Recommendation[];
  candidate_count: number;
  message: string | null;
}

export default function NewAnalysis() {
  const [requirement, setRequirement] = useState('');
  const [category, setCategory] = useState('');
  const [priority, setPriority] = useState('routine');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  const [recLoading, setRecLoading] = useState(false);
  const [recError, setRecError] = useState<string | null>(null);
  const [recData, setRecData] = useState<RecommendationResponse | null>(null);
  const [expandedEvidence, setExpandedEvidence] = useState<Record<string, boolean>>({});

  const [gapLoading, setGapLoading] = useState(false);
  const [gapError, setGapError] = useState<string | null>(null);
  const [gapData, setGapData] = useState<any>(null);


  const handleClear = () => {
    setRequirement('');
    setCategory('');
    setPriority('routine');
    setError(null);
    setResult(null);
    setRecError(null);
    setRecData(null);
    setExpandedEvidence({});

    setGapError(null);
    setGapData(null);

  };

  const handleAnalyze = async () => {
    if (!requirement.trim()) {
      setError('Please enter a procurement requirement.');
      return;
    }
    
    setLoading(true);
    setError(null);
    setResult(null);
    setRecError(null);
    setRecData(null);
    setExpandedEvidence({});

    setGapError(null);
    setGapData(null);

    
    try {
      const response = await fetch('http://127.0.0.1:8002/api/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: requirement })
      });
      
      if (!response.ok) {
        if (response.status === 503) {
          throw new Error('AI service is temporarily unavailable. Please try again.');
        } else if (response.status === 429) {
          throw new Error('AI service request limit reached. Please try again shortly.');
        } else if (response.status >= 500) {
          throw new Error('An unexpected server error occurred.');
        } else {
          try {
            const errData = await response.json();
            throw new Error(errData.detail || `Analysis failed with status: ${response.status}`);
          } catch {
            throw new Error(`Analysis failed with status: ${response.status}`);
          }
        }
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  const handleFindStandards = async () => {
    if (!requirement.trim()) return;

    setRecLoading(true);
    setRecError(null);
    setRecData(null);

    try {
      const response = await fetch('http://127.0.0.1:8002/api/recommendations/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: requirement })
      });

      if (!response.ok) {
        if (response.status === 503) {
          throw new Error('The AI service is temporarily unavailable. Please retry.');
        } else if (response.status === 429) {
          throw new Error('The AI service is temporarily rate limited. Please try again.');
        } else if (response.status >= 500) {
          throw new Error('Unable to generate recommendations. Please try again.');
        } else {
          try {
            const errData = await response.json();
            throw new Error(errData.detail || `Request failed with status: ${response.status}`);
          } catch {
            throw new Error(`Request failed with status: ${response.status}`);
          }
        }
      }

      const data = await response.json();
      console.log("PHASE4/5 RECOMMENDATION RESPONSE:", data);
      console.log("RECOMMENDATIONS ARRAY:", data?.recommendations);
      setRecData(data);
    } catch (err: any) {
      setRecError(err.message || 'Failed to fetch recommendations.');
    } finally {
      setRecLoading(false);
    }
  };

  
  const handleCheckGaps = async () => {
    if (!requirement.trim() || !recData || !recData.recommendations) return;

    setGapLoading(true);
    setGapError(null);
    setGapData(null);

    try {
      const response = await fetch('http://127.0.0.1:8002/api/gaps/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          requirement: requirement,
          recommendations: recData.recommendations
        })
      });

      if (!response.ok) {
        throw new Error(`Request failed with status: ${response.status}`);
      }

      const data = await response.json();
      setGapData(data);
    } catch (err: any) {
      setGapError(err.message || 'Failed to fetch specification gaps.');
    } finally {
      setGapLoading(false);
    }
  };

  const toggleEvidence = (id: string) => {
    setExpandedEvidence((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <ErrorBoundary>
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-surface border border-border rounded-xl shadow-sm">
        <div className="p-6 border-b border-border">
          <h2 className="text-xl font-semibold text-text-primary flex items-center">
            <FileSearch className="w-5 h-5 mr-2 text-primary" />
            New Procurement Analysis
          </h2>
          <p className="text-sm text-text-secondary mt-1">
            Describe the product, service, or procurement requirement you want to analyze.
          </p>
        </div>
        
        <div className="p-6 space-y-6">
          <div className="space-y-2">
            <label htmlFor="requirement" className="block text-sm font-medium text-text-primary">
              Procurement Requirement
            </label>
            <textarea
              id="requirement"
              rows={8}
              value={requirement}
              onChange={(e) => {
                setRequirement(e.target.value);
                setRecData(null);
                setRecError(null);
              }}
              className="w-full bg-surface-muted border border-border rounded-md px-4 py-3 text-sm text-text-primary focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent placeholder:text-text-secondary/70 resize-y"
              placeholder="Enter the technical requirements, product description, intended use, or procurement specification..."
            ></textarea>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label htmlFor="category" className="block text-sm font-medium text-text-primary">
                Category
              </label>
              <select
                id="category"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-surface-muted border border-border rounded-md px-4 py-2.5 text-sm text-text-primary focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent appearance-none"
              >
                <option value="" disabled>Select category</option>
                <option value="electrical">Electrical</option>
                <option value="civil">Civil & Construction</option>
                <option value="mechanical">Mechanical</option>
                <option value="safety">Safety & PPE</option>
                <option value="water">Water & Sanitation</option>
                <option value="electronics">Electronics & IT</option>
                <option value="industrial">Industrial Equipment</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-text-primary">
                Priority
              </label>
              <div className="flex items-center space-x-4 h-10">
                <label className="flex items-center space-x-2">
                  <input type="radio" name="priority" value="routine" checked={priority === 'routine'} onChange={() => setPriority('routine')} className="text-primary focus:ring-primary" />
                  <span className="text-sm text-text-primary">Routine</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input type="radio" name="priority" value="important" checked={priority === 'important'} onChange={() => setPriority('important')} className="text-primary focus:ring-primary" />
                  <span className="text-sm text-text-primary">Important</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input type="radio" name="priority" value="urgent" checked={priority === 'urgent'} onChange={() => setPriority('urgent')} className="text-primary focus:ring-primary" />
                  <span className="text-sm text-text-primary">Urgent</span>
                </label>
              </div>
            </div>
          </div>
          
          {error && (
            <div className="p-4 rounded-md bg-error/10 border border-error/20 flex items-start">
              <AlertCircle className="w-5 h-5 text-error mt-0.5 mr-3 flex-shrink-0" />
              <div className="text-sm text-error">{error}</div>
            </div>
          )}
        </div>

        <div className="p-6 border-t border-border bg-surface-muted rounded-b-xl flex justify-between items-center">
          <span className="text-xs text-text-secondary flex items-center">
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin text-primary" />
                Analyzing requirement...
              </>
            ) : result ? (
              <>
                <CheckCircle2 className="w-4 h-4 mr-2 text-success" />
                Analysis completed successfully
              </>
            ) : (
              <>
                <span className="w-1.5 h-1.5 rounded-full bg-primary mr-2"></span>
                Ready to analyze
              </>
            )}
          </span>
          <div className="flex space-x-3">
            <button onClick={handleClear} disabled={loading} className="px-4 py-2 text-sm font-medium text-text-secondary hover:text-text-primary hover:bg-border rounded-md transition-colors disabled:opacity-50">
              Clear
            </button>
            <button onClick={handleAnalyze} disabled={loading} className="px-4 py-2 text-sm font-medium bg-primary text-white rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 flex items-center">
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                'Analyze Requirement'
              )}
            </button>
          </div>
        </div>
      </div>
      
      {result && result.extracted && (
        <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border bg-surface-muted">
            <h3 className="text-lg font-semibold text-text-primary">Structured Requirement</h3>
          </div>
          <div className="p-6 space-y-6">
            <div>
              <h4 className="text-sm font-medium text-text-secondary mb-2 uppercase tracking-wider">Intent Summary</h4>
              <p className="text-text-primary text-sm bg-surface-muted p-4 rounded-md border border-border">
                {result.extracted.intent_summary}
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-sm font-medium text-text-secondary mb-2 uppercase tracking-wider">Products</h4>
                {result.extracted.products && result.extracted.products.length > 0 ? (
                  <ul className="list-disc list-inside text-sm text-text-primary space-y-1">
                    {result.extracted.products.map((item: string, i: number) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-text-secondary italic">None identified</p>
                )}
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-text-secondary mb-2 uppercase tracking-wider">Applications</h4>
                {result.extracted.applications && result.extracted.applications.length > 0 ? (
                  <ul className="list-disc list-inside text-sm text-text-primary space-y-1">
                    {result.extracted.applications.map((item: string, i: number) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-text-secondary italic">None identified</p>
                )}
              </div>
            </div>
            
            <div>
              <h4 className="text-sm font-medium text-text-secondary mb-2 uppercase tracking-wider">Keywords</h4>
              <div className="flex flex-wrap gap-2">
                {result.extracted.keywords && result.extracted.keywords.length > 0 ? (
                  result.extracted.keywords.map((kw: string, i: number) => (
                    <span key={i} className="px-2.5 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full border border-primary/20">
                      {kw}
                    </span>
                  ))
                ) : (
                  <p className="text-sm text-text-secondary italic">None identified</p>
                )}
              </div>
            </div>
            
            {result.embedding_status && (
              <div className="pt-4 border-t border-border mt-4">
                <h4 className="text-sm font-medium text-text-secondary mb-2 uppercase tracking-wider">System Metadata</h4>
                <div className="flex items-center space-x-6 text-sm">
                  <div className="flex items-center text-text-primary">
                    <span className="text-text-secondary mr-2">Embedding generated:</span>
                    <CheckCircle2 className="w-4 h-4 text-success mr-1" /> Yes
                  </div>
                  <div className="flex items-center text-text-primary">
                    <span className="text-text-secondary mr-2">Embedding dimensions:</span>
                    768
                  </div>
                </div>
              </div>
            )}
            
            <div className="pt-6 mt-4 flex flex-col space-y-4">
              <button
                onClick={handleFindStandards}
                disabled={recLoading}
                className="w-full py-3 px-4 flex justify-center items-center bg-primary text-white rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 text-sm font-medium"
              >
                {recLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Finding applicable Indian Standards...
                  </>
                ) : (
                  <>
                    <BookOpen className="w-5 h-5 mr-2" />
                    Find Applicable Standards
                  </>
                )}
              </button>
              
              {recError && (
                <div className="p-4 rounded-md bg-error/10 border border-error/20 flex items-start">
                  <AlertCircle className="w-5 h-5 text-error mt-0.5 mr-3 flex-shrink-0" />
                  <div className="text-sm text-error">{recError}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {recData && (
        <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border bg-surface-muted flex items-center">
            <BookOpen className="w-5 h-5 mr-2 text-primary" />
            <h3 className="text-lg font-semibold text-text-primary">Recommended Indian Standards</h3>
          </div>
          <div className="p-6 space-y-6">
            {(!recData.recommendations || recData.recommendations.length === 0) ? (
              <div className="text-center py-8">
                <p className="text-text-primary font-medium mb-2">No sufficiently relevant Indian Standard was identified in the current ManakSetu knowledge base.</p>
                <p className="text-text-secondary text-sm">The current knowledge base is a curated prototype dataset and does not represent the complete BIS catalogue.</p>
              </div>
            ) : (
              <ErrorBoundary>
                <div className="space-y-6">
                {(recData.recommendations || []).map((rec) => {
                  const version = rec.version || { edition: 'Unknown', status: 'Unknown' };
                  const explanation = rec.explanation || {
                    summary: rec.why_recommended?.[0] || "Semantic similarity suggests relevance",
                    product_matches: Array.isArray(rec.evidence) ? [] : (rec.evidence as any)?.matched_products || [],
                    application_matches: Array.isArray(rec.evidence) ? [] : (rec.evidence as any)?.matched_applications || [],
                    keyword_matches: Array.isArray(rec.evidence) ? [] : (rec.evidence as any)?.matched_keywords || [],
                    scope_match: Array.isArray(rec.evidence) ? false : (rec.evidence as any)?.scope_match || false
                  };
                  const evidenceList = Array.isArray(rec.evidence) ? rec.evidence : [];
                  const sources = Array.isArray(rec.sources) ? rec.sources : [];
                  const relationships = Array.isArray(rec.relationships) ? rec.relationships : [];
                  
                  return (
                  <div key={rec.standard_id} className="border border-border rounded-lg overflow-hidden">
                    <div className="p-5 bg-surface-muted border-b border-border">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="text-lg font-bold text-text-primary">{rec.standard_number}</h4>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          rec.relevance_category === 'HIGH RELEVANCE' ? 'bg-success/20 text-success' :
                          rec.relevance_category === 'MODERATE RELEVANCE' ? 'bg-warning/20 text-warning-dark' :
                          'bg-surface border border-border text-text-secondary'
                        }`}>
                          {rec.relevance_category}
                        </span>
                      </div>
                      <p className="text-sm text-text-primary mb-4">{rec.title}</p>
                      <div className="flex flex-wrap gap-4 text-xs">
                        <div className="bg-surface px-3 py-1.5 rounded-md border border-border">
                          <span className="text-text-secondary mr-1">Relevance Score:</span>
                          <span className="font-semibold text-primary">{rec.relevance_score.toFixed(4)}</span>
                        </div>
                        <div className="bg-surface px-3 py-1.5 rounded-md border border-border">
                          <span className="text-text-secondary mr-1">Status:</span>
                          <span className="font-semibold text-text-primary">{rec.status}</span>
                        </div>
                        <div className="bg-surface px-3 py-1.5 rounded-md border border-border">
                          <span className="text-text-secondary mr-1">Edition:</span>
                          <span className="font-semibold text-text-primary">{version.edition}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="p-5 space-y-4">
                      <div>
                        <h5 className="text-sm font-semibold text-text-secondary mb-2 uppercase">Why recommended:</h5>
                        <ul className="space-y-1">
                          <li className="text-sm text-text-primary flex items-start">
                            <CheckCircle2 className="w-4 h-4 text-success mr-2 mt-0.5 flex-shrink-0" />
                            <span>{explanation.summary}</span>
                          </li>
                        </ul>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {(explanation?.product_matches || []).length > 0 && (
                          <div>
                            <h5 className="text-sm font-semibold text-text-secondary mb-1">Matched Products:</h5>
                            <ul className="list-disc list-inside text-sm text-text-primary">
                              {(explanation?.product_matches || []).map((p, idx) => <li key={idx}>{p}</li>)}
                            </ul>
                          </div>
                        )}
                        {(explanation?.application_matches || []).length > 0 && (
                          <div>
                            <h5 className="text-sm font-semibold text-text-secondary mb-1">Matched Applications:</h5>
                            <ul className="list-disc list-inside text-sm text-text-primary">
                              {(explanation?.application_matches || []).map((a, idx) => <li key={idx}>{a}</li>)}
                            </ul>
                          </div>
                        )}
                        {(explanation?.keyword_matches || []).length > 0 && (
                          <div>
                            <h5 className="text-sm font-semibold text-text-secondary mb-1">Matched Keywords:</h5>
                            <ul className="list-disc list-inside text-sm text-text-primary">
                              {(explanation?.keyword_matches || []).map((k, idx) => <li key={idx}>{k}</li>)}
                            </ul>
                          </div>
                        )}
                      </div>

                      <div className="pt-2 border-t border-border">
                        <button
                          onClick={() => toggleEvidence(rec.standard_id)}
                          className="flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors"
                        >
                          {expandedEvidence[rec.standard_id] ? (
                            <><ChevronUp className="w-4 h-4 mr-1" /> Hide Recommendation Evidence</>
                          ) : (
                            <><ChevronDown className="w-4 h-4 mr-1" /> View Recommendation Evidence</>
                          )}
                        </button>
                        
                        {expandedEvidence[rec.standard_id] && (
                          <div className="mt-3 bg-surface-muted p-4 rounded-md border border-border space-y-6">
                            
                            {/* Evidence coverage/items */}
                            <div>
                              <h5 className="text-xs font-semibold text-text-secondary mb-3 uppercase tracking-wider">Why This Standard</h5>
                              {evidenceList.length === 0 ? (
                                <p className="text-sm text-text-secondary italic">Limited evidence available in the current knowledge base.</p>
                              ) : (
                                <ul className="space-y-3">
                                  {evidenceList.map((ev, idx) => (
                                    <li key={idx} className="text-sm">
                                      <div className="flex items-start">
                                        <CheckCircle2 className="w-4 h-4 text-success mr-2 mt-0.5 flex-shrink-0" />
                                        <div>
                                          <span className="font-medium text-text-primary">{ev.label}</span>
                                          <p className="text-text-secondary mt-0.5">{ev.description}</p>
                                          {ev.source && ev.source.url && (
                                            <a href={ev.source.url} target="_blank" rel="noreferrer" className="text-xs text-primary hover:underline mt-1 inline-block">
                                              View Source
                                            </a>
                                          )}
                                        </div>
                                      </div>
                                    </li>
                                  ))}
                                </ul>
                              )}
                            </div>

                            {/* Score Breakdown */}
                            <div>
                              <h5 className="text-xs font-semibold text-text-secondary mb-3 uppercase tracking-wider">Score Breakdown</h5>
                              <div className="grid grid-cols-2 sm:grid-cols-3 gap-y-3 gap-x-4 text-sm">
                                <div className="flex flex-col">
                                  <span className="text-text-secondary text-xs">Semantic Match</span>
                                  <span className="font-medium text-text-primary">{rec.score_breakdown?.semantic?.toFixed(4) || '0.0000'}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-text-secondary text-xs">Product Match</span>
                                  <span className="font-medium text-text-primary">{rec.score_breakdown?.product?.toFixed(4) || '0.0000'}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-text-secondary text-xs">Application Match</span>
                                  <span className="font-medium text-text-primary">{rec.score_breakdown?.application?.toFixed(4) || '0.0000'}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-text-secondary text-xs">Keyword Match</span>
                                  <span className="font-medium text-text-primary">{rec.score_breakdown?.keyword?.toFixed(4) || '0.0000'}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-text-secondary text-xs">Scope Match</span>
                                  <span className="font-medium text-text-primary">{rec.score_breakdown?.scope?.toFixed(4) || '0.0000'}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-text-secondary text-xs">Category/Sector Match</span>
                                  <span className="font-medium text-text-primary">{rec.score_breakdown?.category_sector?.toFixed(4) || '0.0000'}</span>
                                </div>
                              </div>
                            </div>

                            {/* Standard Information */}
                            <div>
                               <h5 className="text-xs font-semibold text-text-secondary mb-3 uppercase tracking-wider">Standard Information</h5>
                               <div className="grid grid-cols-2 sm:grid-cols-4 gap-y-3 gap-x-4 text-sm">
                                  <div className="flex flex-col">
                                    <span className="text-text-secondary text-xs">Status</span>
                                    <span className="font-medium text-text-primary">{version.status}</span>
                                  </div>
                                  <div className="flex flex-col">
                                    <span className="text-text-secondary text-xs">Edition</span>
                                    <span className="font-medium text-text-primary">{version.edition}</span>
                                  </div>
                                  {version.publication_date && (
                                    <div className="flex flex-col">
                                      <span className="text-text-secondary text-xs">Publication Date</span>
                                      <span className="font-medium text-text-primary">{version.publication_date}</span>
                                    </div>
                                  )}
                                  {version.effective_date && (
                                    <div className="flex flex-col">
                                      <span className="text-text-secondary text-xs">Effective Date</span>
                                      <span className="font-medium text-text-primary">{version.effective_date}</span>
                                    </div>
                                  )}
                               </div>
                            </div>

                            {/* Relationships */}
                            {relationships.length > 0 && (
                               <div>
                                  <h5 className="text-xs font-semibold text-text-secondary mb-3 uppercase tracking-wider">Relationships</h5>
                                  <ul className="space-y-2">
                                     {relationships.map((rel, idx) => {
                                        if (typeof rel === 'string') {
                                          return (
                                            <li key={idx} className="text-sm text-text-primary">
                                               <span className="font-medium">Relationship:</span> {rel}
                                            </li>
                                          );
                                        }
                                        return (
                                          <li key={idx} className="text-sm text-text-primary">
                                             <span className="font-medium">{rel.relationship_type}:</span> {rel.related_standard}
                                          </li>
                                        );
                                     })}
                                  </ul>
                               </div>
                            )}

                            {/* Sources */}
                            <div>
                              <h5 className="text-xs font-semibold text-text-secondary mb-3 uppercase tracking-wider">Sources</h5>
                              {sources.length > 0 ? (
                                <div className="space-y-4">
                                  {sources.map((src, idx) => (
                                    <div key={idx} className="bg-surface border border-border rounded-md p-3 text-sm">
                                      <div className="grid grid-cols-2 gap-2">
                                        <div><span className="text-text-secondary text-xs">Organization:</span> <div className="font-medium text-text-primary">{src.organization}</div></div>
                                        <div><span className="text-text-secondary text-xs">Source Type:</span> <div className="text-text-primary">{src.source_type}</div></div>
                                        {src.title && <div className="col-span-2"><span className="text-text-secondary text-xs">Title:</span> <div className="text-text-primary">{src.title}</div></div>}
                                      </div>
                                      {src.url ? (
                                        <div className="mt-2 pt-2 border-t border-border">
                                          <a href={src.url} target="_blank" rel="noreferrer" className="text-primary hover:underline text-xs font-medium">View Source</a>
                                        </div>
                                      ) : (
                                        <div className="mt-2 pt-2 border-t border-border text-xs text-text-secondary italic">
                                          Source metadata available; direct URL not available.
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                  <p className="text-xs text-text-secondary italic mt-2">
                                    Source information is provided from the ManakSetu knowledge base. Verify the applicable edition and official documentation before use in procurement decisions.
                                  </p>
                                </div>
                              ) : (
                                <p className="text-sm text-text-secondary italic">Not available in current knowledge base.</p>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )})}
              </div>
              </ErrorBoundary>
            )}
          </div>
        </div>
      )}

      {/* Gap Detection Section */}
      {recData && recData.recommendations && recData.recommendations.length > 0 && (
        <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden mt-6">
          <div className="p-6 border-b border-border bg-surface-muted flex items-center justify-between">
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-warning" />
              <h3 className="text-lg font-semibold text-text-primary">Specification Completeness Check</h3>
            </div>
          </div>
          
          <div className="p-6">
            {!gapData ? (
              <div className="flex flex-col items-center py-8">
                <p className="text-text-primary font-medium text-center mb-4">
                  Check if your procurement requirement is missing important details based on the recommended standards.
                </p>
                <button
                  onClick={handleCheckGaps}
                  disabled={gapLoading}
                  className="px-6 py-3 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 flex items-center font-medium"
                >
                  {gapLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Checking Specification Gaps...
                    </>
                  ) : (
                    'Check Specification Gaps'
                  )}
                </button>
                {gapError && (
                  <div className="mt-4 p-4 rounded-md bg-error/10 border border-error/20 flex items-start w-full">
                    <AlertCircle className="w-5 h-5 text-error mt-0.5 mr-3 flex-shrink-0" />
                    <div className="text-sm text-error">{gapError}</div>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold text-text-primary">Potential Gaps Identified: {gapData.summary?.total_gaps || 0}</h4>
                  <div className="flex space-x-3 text-sm">
                    {gapData.summary?.high > 0 && <span className="text-error font-medium">● {gapData.summary.high} High</span>}
                    {gapData.summary?.medium > 0 && <span className="text-warning font-medium">● {gapData.summary.medium} Medium</span>}
                    {gapData.summary?.low > 0 && <span className="text-success font-medium">● {gapData.summary.low} Low</span>}
                  </div>
                </div>
                
                {(!gapData.gaps || gapData.gaps.length === 0) ? (
                  <div className="bg-success/10 border border-success/20 p-6 rounded-md text-center">
                    <CheckCircle2 className="w-8 h-8 text-success mx-auto mb-2" />
                    <h5 className="font-medium text-success mb-1">No significant gaps detected</h5>
                    <p className="text-sm text-success/80">Your procurement requirement appears comprehensive based on the knowledge base.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {gapData.gaps.map((gap: any) => (
                      <div key={gap.gap_id} className={`border rounded-md overflow-hidden ${
                        gap.severity === 'HIGH' ? 'border-error/30' : 
                        gap.severity === 'MEDIUM' ? 'border-warning/30' : 
                        'border-border'
                      }`}>
                        <div className={`p-4 border-b flex items-start justify-between ${
                          gap.severity === 'HIGH' ? 'bg-error/5 border-error/20' : 
                          gap.severity === 'MEDIUM' ? 'bg-warning/5 border-warning/20' : 
                          'bg-surface-muted/50 border-border'
                        }`}>
                          <div>
                            <div className="flex items-center gap-2 mb-1">
                              <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${
                                gap.severity === 'HIGH' ? 'bg-error text-white' : 
                                gap.severity === 'MEDIUM' ? 'bg-warning text-white' : 
                                'bg-success text-white'
                              }`}>
                                {gap.severity}
                              </span>
                              <span className="text-xs font-medium text-text-secondary">{gap.gap_type}</span>
                            </div>
                            <h5 className="font-semibold text-text-primary text-base">{gap.title}</h5>
                          </div>
                        </div>
                        <div className="p-4 space-y-4">
                          <p className="text-sm text-text-primary">{gap.description}</p>
                          
                          <div className="bg-surface-muted p-3 rounded text-sm border border-border">
                            <span className="font-semibold block mb-1 text-xs text-text-secondary uppercase">Why this matters</span>
                            <p className="text-text-primary">{gap.reason}</p>
                          </div>
                          
                          <div className="bg-primary/5 p-3 rounded text-sm border border-primary/10">
                            <span className="font-semibold block mb-1 text-xs text-primary uppercase">Suggested Action</span>
                            <p className="text-text-primary">{gap.suggested_information}</p>
                          </div>
                          
                          {gap.evidence && gap.evidence.length > 0 && (
                            <div className="mt-3">
                              <span className="font-semibold block mb-2 text-xs text-text-secondary uppercase">Supporting Evidence</span>
                              <ul className="space-y-2">
                                {gap.evidence.map((ev: any, i: number) => (
                                  <li key={i} className="text-xs text-text-secondary flex items-start">
                                    <BookOpen className="w-3.5 h-3.5 mr-1.5 mt-0.5 flex-shrink-0" />
                                    <span><span className="font-medium text-text-primary">{ev.source_type}:</span> {ev.description}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                <div className="flex justify-center mt-6 pt-4 border-t border-border">
                  <button
                    onClick={handleCheckGaps}
                    disabled={gapLoading}
                    className="text-primary hover:underline text-sm font-medium flex items-center"
                  >
                    {gapLoading ? 'Re-checking...' : 'Refresh Specification Check'}
                  </button>
                </div>
              </div>
            )}
            
            {/* Step 4: Generate Specification Draft */}
            {gapData && !gapLoading && (
              <div className="mt-8 animate-fade-in-up" style={{ animationDelay: '300ms' }}>
                <div className="flex items-center mb-6">
                  <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-bold mr-3 shadow-sm">
                    4
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-text-primary">Draft Specification</h2>
                    <p className="text-text-secondary text-sm">Review and edit your drafted requirements.</p>
                  </div>
                </div>
                
                <SpecificationGenerator 
                  requirement={requirement}
                  analysisData={result}
                  recData={recData}
                  gapData={gapData}
                />
              </div>
            )}
            
          </div>
        </div>
      )}

    </div>
    </ErrorBoundary>
  );
}
