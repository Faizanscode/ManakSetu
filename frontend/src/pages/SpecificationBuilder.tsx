import { useState, useEffect } from 'react';
import { FileText, FolderOpen, Loader2, AlertTriangle, FileSearch, BookOpen } from 'lucide-react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { SpecificationGenerator } from '../components/SpecificationGenerator';

export default function SpecificationBuilder() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(!!id);
  const [error, setError] = useState<string | null>(null);
  const [analysisData, setAnalysisData] = useState<any | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      if (!id) return;
      
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://127.0.0.1:8002/api/history/${id}`);
        if (!response.ok) {
          throw new Error('Failed to load analysis data');
        }
        const data = await response.json();
        setAnalysisData(data);
      } catch (err: any) {
        setError(err.message || 'Error fetching analysis details.');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [id]);

  if (!id) {
    return (
      <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
        <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
          <h2 className="text-xl font-semibold text-text-primary">Specification Builder</h2>
          <p className="text-sm text-text-secondary mt-1">
            Build procurement-ready specifications using validated standards and requirement evidence.
          </p>
        </div>

        <div className="bg-surface border border-border rounded-xl p-16 flex flex-col items-center justify-center text-center shadow-sm">
          <FileText className="w-16 h-16 text-text-secondary mb-4 opacity-30" />
          <h3 className="text-lg font-medium text-text-primary mb-2">No procurement analysis selected</h3>
          <p className="text-sm text-text-secondary max-w-md mb-8">
            Start with a new procurement analysis or open a saved analysis to build a standards-aligned specification.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              to="/new-analysis"
              className="inline-flex items-center justify-center px-5 py-2.5 bg-primary text-white rounded-md font-medium hover:bg-primary-hover transition-colors shadow-sm"
            >
              Start New Analysis
            </Link>
            <Link
              to="/history"
              className="inline-flex items-center justify-center px-5 py-2.5 bg-white border border-border text-text-primary rounded-md font-medium hover:bg-surface-muted transition-colors shadow-sm"
            >
              <FolderOpen className="w-4 h-4 mr-2" />
              Open Saved Analysis
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
        <span className="ml-3 text-text-secondary font-medium">Loading analysis...</span>
      </div>
    );
  }

  if (error || !analysisData) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="bg-error/10 border border-error/20 p-6 rounded-xl flex flex-col items-center justify-center text-center">
          <AlertTriangle className="w-10 h-10 text-error mb-3" />
          <h3 className="text-lg font-bold text-error mb-1">Error Loading Analysis</h3>
          <p className="text-error/80 text-sm mb-4">{error || 'Unknown error occurred.'}</p>
          <Link
            to="/history"
            className="px-4 py-2 bg-white border border-error/30 text-error rounded-md text-sm font-medium hover:bg-error/5 transition-colors"
          >
            Back to History
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold text-text-primary mb-1">Specification Builder</h1>
          <p className="text-text-secondary text-sm flex items-center">
            <span className="font-medium text-primary bg-primary/10 px-2 py-0.5 rounded mr-2">Analysis Workspace</span>
            {analysisData.title}
          </p>
        </div>
        <button
          onClick={() => navigate('/history')}
          className="text-sm text-text-secondary hover:text-primary transition-colors flex items-center font-medium"
        >
          <FolderOpen className="w-4 h-4 mr-1.5" />
          Change Analysis
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Context Data */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
            <div className="bg-surface-muted border-b border-border p-4">
              <h3 className="font-semibold text-text-primary flex items-center text-sm">
                <FileSearch className="w-4 h-4 mr-2 text-primary" />
                Requirement Context
              </h3>
            </div>
            <div className="p-4 space-y-4">
              <div>
                <span className="text-[10px] uppercase font-bold tracking-wider text-text-secondary block mb-1">Original Requirement</span>
                <p className="text-sm text-text-primary bg-surface-muted/50 p-2.5 rounded border border-border">
                  {analysisData.procurement_requirement}
                </p>
              </div>
              
              {analysisData.extracted_requirement && (
                <div>
                  <span className="text-[10px] uppercase font-bold tracking-wider text-text-secondary block mb-1">Structured Details</span>
                  <div className="space-y-2">
                    {analysisData.extracted_requirement.intent_summary && (
                      <p className="text-xs text-text-secondary">
                        <span className="font-medium text-text-primary">Intent:</span> {analysisData.extracted_requirement.intent_summary}
                      </p>
                    )}
                    {analysisData.extracted_requirement.products?.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {analysisData.extracted_requirement.products.map((p: string, i: number) => (
                          <span key={i} className="text-[10px] bg-primary/10 text-primary px-1.5 py-0.5 rounded font-medium border border-primary/20">
                            {p}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
            <div className="bg-surface-muted border-b border-border p-4">
              <h3 className="font-semibold text-text-primary flex items-center text-sm">
                <BookOpen className="w-4 h-4 mr-2 text-primary" />
                Applicable Standards
              </h3>
            </div>
            <div className="p-4">
              <div className="space-y-3">
                {analysisData.recommendations?.recommendations?.map((rec: any, idx: number) => (
                  <div key={idx} className="bg-surface-muted/50 border border-border rounded p-2.5">
                    <div className="flex justify-between items-start mb-1">
                      <span className="font-bold text-sm text-text-primary">{rec.standard_number}</span>
                      <span className="text-[9px] uppercase font-bold px-1.5 py-0.5 rounded-full bg-success/10 text-success">
                        {rec.relevance_category}
                      </span>
                    </div>
                    <p className="text-xs text-text-secondary line-clamp-2">{rec.title}</p>
                  </div>
                )) || <p className="text-xs text-text-secondary italic">No standards found.</p>}
              </div>
            </div>
          </div>

          {analysisData.gaps?.gaps?.length > 0 && (
            <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
              <div className="bg-surface-muted border-b border-border p-4">
                <h3 className="font-semibold text-text-primary flex items-center text-sm">
                  <AlertTriangle className="w-4 h-4 mr-2 text-warning" />
                  Identified Gaps
                </h3>
              </div>
              <div className="p-4">
                <div className="space-y-3">
                  {analysisData.gaps.gaps.map((gap: any, idx: number) => (
                    <div key={idx} className={`border rounded p-2.5 ${gap.severity === 'HIGH' ? 'border-error/20 bg-error/5' : gap.severity === 'MEDIUM' ? 'border-warning/20 bg-warning/5' : 'border-border bg-surface-muted/30'}`}>
                      <div className="flex items-center gap-1.5 mb-1">
                        <span className={`text-[9px] uppercase font-bold px-1.5 py-0.5 rounded-sm text-white ${gap.severity === 'HIGH' ? 'bg-error' : gap.severity === 'MEDIUM' ? 'bg-warning' : 'bg-success'}`}>
                          {gap.severity}
                        </span>
                        <span className="text-xs font-semibold text-text-primary truncate">{gap.title}</span>
                      </div>
                      <p className="text-[11px] text-text-secondary line-clamp-2 mt-1">{gap.suggested_information}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Specification Generator */}
        <div className="lg:col-span-2">
          <SpecificationGenerator 
            requirement={analysisData.procurement_requirement}
            analysisData={analysisData.extracted_requirement}
            recData={analysisData.recommendations}
            gapData={analysisData.gaps}
            existingHistoryId={analysisData.id}
            initialSpecDraft={analysisData.specification}
          />
        </div>
      </div>
    </div>
  );
}
