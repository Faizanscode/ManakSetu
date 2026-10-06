import React, { useState } from 'react';
import { 
  FileText, 
  CheckCircle2, 
  AlertTriangle,
  RefreshCw,
  ExternalLink,
  Edit2,
  Save,
  BookOpen
} from 'lucide-react';
import { API_BASE_URL } from '../config';

interface SpecificationGeneratorProps {
  requirement: string;
  analysisData: any;
  recData: any;
  gapData: any;
  existingHistoryId?: string;
  initialSpecDraft?: any;
}

export const SpecificationGenerator: React.FC<SpecificationGeneratorProps> = ({
  requirement,
  analysisData,
  recData,
  gapData,
  existingHistoryId,
  initialSpecDraft
}) => {
  const [specDraft, setSpecDraft] = useState<any | null>(initialSpecDraft || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editingMode, setEditingMode] = useState(false);
  const [editedDraft, setEditedDraft] = useState<any | null>(null);
  
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  const generateDraft = async () => {
    setLoading(true);
    setError(null);
    setSaveSuccess(false);
    try {
      const response = await fetch(`${API_BASE_URL}/specifications/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          requirement,
          analysis: analysisData,
          recommendations: recData?.recommendations || (Array.isArray(recData) ? recData : (recData?.recommendations?.recommendations || [])),
          gaps: gapData?.gaps || (Array.isArray(gapData) ? gapData : (gapData?.gaps?.gaps || []))
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status: ${response.status}`);
      }

      const data = await response.json();
      setSpecDraft(data.specification);
      setEditedDraft(data.specification);
      setEditingMode(false);
    } catch (err: any) {
      setError(err.message || 'Failed to generate specification draft');
    } finally {
      setLoading(false);
    }
  };

  const saveAnalysis = async () => {
    if (!specDraft) return;
    setSaving(true);
    setSaveError(null);
    try {
      const url = existingHistoryId ? `${API_BASE_URL}/history/${existingHistoryId}` : `${API_BASE_URL}/history/`;
      const method = existingHistoryId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: specDraft.title || 'Procurement Analysis',
          procurement_requirement: requirement,
          category: 'other', // Will be enhanced if NewAnalysis passes it
          priority: 'routine',
          extracted_requirement: analysisData?.extracted || analysisData,
          recommendations: recData?.recommendations ? { recommendations: recData.recommendations } : recData,
          gaps: gapData?.gaps ? { gaps: gapData.gaps } : gapData,
          specification: specDraft,
          status: 'COMPLETED'
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status: ${response.status}`);
      }

      await response.json();
      setSaveSuccess(true);
    } catch (err: any) {
      setSaveError(err.message || 'Failed to save analysis');
    } finally {
      setSaving(false);
    }
  };

  const handleExport = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow || !specDraft) return;

    const html = `
      <html>
        <head>
          <title>Analysis Report - ${specDraft.title || 'Report'}</title>
          <style>
            body { font-family: 'Inter', system-ui, sans-serif; line-height: 1.5; color: #333; max-width: 800px; margin: 0 auto; padding: 40px; }
            h1 { color: #1e3a8a; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
            h2 { color: #1e40af; margin-top: 30px; }
            h3 { color: #3b82f6; }
            .section { margin-bottom: 30px; }
            .box { background: #f3f4f6; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { text-align: left; padding: 8px; border-bottom: 1px solid #e5e7eb; }
            .gap-high { color: #dc2626; font-weight: bold; }
            .gap-medium { color: #d97706; font-weight: bold; }
            .footer { margin-top: 50px; font-size: 12px; text-align: center; color: #6b7280; border-top: 1px solid #e5e7eb; padding-top: 20px; }
          </style>
        </head>
        <body>
          <h1>MANAKSETU - Indian Standards Procurement Analysis</h1>
          <p><strong>Analysis Title:</strong> ${specDraft.title}</p>
          <p><strong>Date:</strong> ${new Date().toLocaleString()}</p>
          
          <div class="section">
            <h2>1. Original Procurement Requirement</h2>
            <div class="box">${requirement.replace(/\n/g, '<br/>')}</div>
          </div>

          <div class="section">
            <h2>2. Structured Requirement</h2>
            <div class="box">
              <p><strong>Intent Summary:</strong> ${analysisData?.extracted?.intent_summary}</p>
              <p><strong>Products:</strong> ${(analysisData?.extracted?.products || []).join(', ')}</p>
              <p><strong>Applications:</strong> ${(analysisData?.extracted?.applications || []).join(', ')}</p>
            </div>
          </div>

          <div class="section">
            <h2>3. Recommended Indian Standards</h2>
            ${recData?.recommendations?.map((r: any) => `
              <div class="box">
                <h3>${r.standard_number} - ${r.title}</h3>
                <p><strong>Relevance:</strong> ${r.relevance_category}</p>
                <p><strong>Why Recommended:</strong></p>
                <ul>
                  ${r.why_recommended?.map((w: string) => `<li>${w}</li>`).join('') || ''}
                </ul>
              </div>
            `).join('') || '<p>No standards recommended.</p>'}
          </div>

          <div class="section">
            <h2>4. Specification Gap Analysis</h2>
            ${gapData?.gaps?.map((g: any) => `
              <div class="box">
                <p><span class="gap-${g.severity.toLowerCase()}">[${g.severity}]</span> <strong>${g.title}</strong></p>
                <p>${g.description}</p>
                <p><em>Suggested Action:</em> ${g.suggested_information}</p>
              </div>
            `).join('') || '<p>No gaps detected.</p>'}
          </div>

          <div class="section">
            <h2>5. Generated Procurement Specification</h2>
            <div class="box">
              <h3>${specDraft.title}</h3>
              <p><strong>Objective:</strong> ${specDraft.procurement_objective}</p>
              <p><strong>Description:</strong> ${specDraft.product_description}</p>
              
              <h4>Technical Requirements</h4>
              <ul>
                ${specDraft.technical_requirements?.map((req: any) => `<li>${req.requirement}</li>`).join('') || '<li>None</li>'}
              </ul>
              
              <h4>Testing & Inspection</h4>
              <ul>
                ${specDraft.testing_requirements?.map((req: any) => `<li>${req.requirement}</li>`).join('') || '<li>None</li>'}
              </ul>
              
              <h4>Quality & Certification</h4>
              <ul>
                ${specDraft.quality_requirements?.map((req: any) => `<li>${req.requirement}</li>`).join('') || '<li>None</li>'}
              </ul>
            </div>
          </div>

          <div class="footer">
            Generated by ManakSetu — AI-assisted procurement standards analysis.
          </div>
          <script>
            window.onload = () => { window.print(); }
          </script>
        </body>
      </html>
    `;
    printWindow.document.write(html);
    printWindow.document.close();
  };

  const handleEditChange = (field: string, value: string) => {
    if (editedDraft) {
      setEditedDraft({
        ...editedDraft,
        [field]: value
      });
    }
  };

  const saveEdits = () => {
    setSpecDraft(editedDraft);
    setEditingMode(false);
    setSaveSuccess(false); // require re-saving if edits are made
  };

  const renderSourceBadge = (sourceType: string) => {
    switch (sourceType) {
      case 'USER_PROVIDED':
        return <span className="bg-primary/10 text-primary text-[10px] px-1.5 py-0.5 rounded font-medium ml-2 uppercase">User Provided</span>;
      case 'KNOWLEDGE_BASE':
        return <span className="bg-success/10 text-success text-[10px] px-1.5 py-0.5 rounded font-medium ml-2 uppercase">Knowledge Base</span>;
      case 'AI_DERIVED':
        return <span className="bg-secondary/10 text-secondary text-[10px] px-1.5 py-0.5 rounded font-medium ml-2 uppercase">AI Derived</span>;
      case 'REQUIRES_VERIFICATION':
        return <span className="bg-warning/10 text-warning-dark text-[10px] px-1.5 py-0.5 rounded font-medium ml-2 flex items-center uppercase"><AlertTriangle className="w-3 h-3 mr-1" /> Needs Verification</span>;
      default:
        return <span className="bg-surface-muted text-text-secondary text-[10px] px-1.5 py-0.5 rounded font-medium ml-2 uppercase">{sourceType}</span>;
    }
  };

  const renderRequirementsList = (title: string, items: any[]) => {
    if (!items || items.length === 0) return null;
    return (
      <div className="mb-4">
        <h4 className="text-sm font-semibold text-text-primary mb-2 uppercase tracking-wider">{title}</h4>
        <ul className="space-y-2">
          {items.map((item, idx) => (
            <li key={idx} className="flex items-start text-sm">
              <CheckCircle2 className="w-4 h-4 text-primary mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <span className="text-text-primary">{item.requirement}</span>
                <div className="mt-1 flex items-center">
                  <span className="text-xs text-text-secondary mr-1">Source:</span>
                  <span className="text-xs font-medium text-text-primary">{item.source}</span>
                  {renderSourceBadge(item.source_type)}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  if (!specDraft && !loading && !error) {
    const hasHighGaps = gapData?.gaps?.some((g: any) => g.severity === 'HIGH');
    
    return (
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 flex flex-col items-center justify-center text-center">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
          <FileText className="w-8 h-8 text-primary" />
        </div>
        <h3 className="text-xl font-bold text-text-primary mb-2">Specification Generator</h3>
        <p className="text-text-secondary max-w-md mx-auto mb-6">
          Convert your requirement, recommended standards, and gap analysis into a structured procurement specification draft.
        </p>
        
        {hasHighGaps && (
          <div className="bg-warning/10 border border-warning/30 rounded-md p-3 mb-6 max-w-md flex items-start text-left">
            <AlertTriangle className="w-5 h-5 text-warning-dark mt-0.5 mr-2 flex-shrink-0" />
            <p className="text-sm text-warning-dark">
              <strong>Note:</strong> You have HIGH severity gaps. Some specification details may require clarification before finalizing this draft.
            </p>
          </div>
        )}
        
        <button
          onClick={generateDraft}
          className="bg-primary text-white font-medium py-2.5 px-6 rounded-md hover:bg-primary-dark transition-colors flex items-center shadow-sm"
        >
          <FileText className="w-4 h-4 mr-2" />
          Generate Specification Draft
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-border p-10 flex flex-col items-center justify-center text-center">
        <RefreshCw className="w-10 h-10 text-primary animate-spin mb-4" />
        <h3 className="text-lg font-bold text-text-primary mb-1">Generating Specification Draft</h3>
        <p className="text-text-secondary text-sm">Structuring requirements and grounding with evidence...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-error/30 p-6 flex flex-col items-center justify-center text-center">
        <AlertTriangle className="w-10 h-10 text-error mb-4" />
        <h3 className="text-lg font-bold text-text-primary mb-1">Generation Failed</h3>
        <p className="text-error text-sm mb-4">{error}</p>
        <button
          onClick={generateDraft}
          className="bg-primary text-white font-medium py-2 px-4 rounded-md hover:bg-primary-dark transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  const currentDraft = editingMode ? editedDraft : specDraft;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-border overflow-hidden">
      <div className="bg-surface-muted border-b border-border p-4 flex justify-between items-center">
        <div className="flex items-center">
          <FileText className="w-5 h-5 text-primary mr-2" />
          <h3 className="font-bold text-text-primary text-lg">Procurement Specification Draft</h3>
        </div>
        <div className="flex space-x-2">
          {!editingMode ? (
            <button 
              onClick={() => setEditingMode(true)}
              className="px-3 py-1.5 text-sm font-medium text-text-primary border border-border bg-white hover:bg-surface-muted rounded flex items-center transition-colors"
            >
              <Edit2 className="w-3.5 h-3.5 mr-1.5" /> Edit
            </button>
          ) : (
            <button 
              onClick={saveEdits}
              className="px-3 py-1.5 text-sm font-medium text-white bg-primary hover:bg-primary-dark rounded flex items-center transition-colors"
            >
              <Save className="w-3.5 h-3.5 mr-1.5" /> Save Edits
            </button>
          )}
          <button 
            onClick={generateDraft}
            className="px-3 py-1.5 text-sm font-medium text-primary hover:text-primary-dark flex items-center transition-colors"
            title="Regenerate"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
      
      <div className="p-6">
        <div className="max-w-4xl mx-auto space-y-6">
          
          {/* Title */}
          <div>
            <h4 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Title</h4>
            {editingMode ? (
              <input 
                type="text" 
                className="w-full border border-border rounded px-3 py-2 text-text-primary font-medium focus:ring-1 focus:ring-primary focus:border-primary outline-none"
                value={currentDraft?.title || ''}
                onChange={(e) => handleEditChange('title', e.target.value)}
              />
            ) : (
              <h1 className="text-2xl font-bold text-text-primary border-b border-border pb-2">{currentDraft?.title}</h1>
            )}
          </div>

          {/* Objective & Description */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Procurement Objective</h4>
              {editingMode ? (
                <textarea 
                  className="w-full border border-border rounded px-3 py-2 text-sm text-text-primary min-h-[100px] focus:ring-1 focus:ring-primary focus:border-primary outline-none"
                  value={currentDraft?.procurement_objective || ''}
                  onChange={(e) => handleEditChange('procurement_objective', e.target.value)}
                />
              ) : (
                <p className="text-sm text-text-primary bg-surface-muted/30 p-3 rounded">{currentDraft?.procurement_objective || 'Not specified'}</p>
              )}
            </div>
            <div>
              <h4 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Product Description</h4>
              {editingMode ? (
                <textarea 
                  className="w-full border border-border rounded px-3 py-2 text-sm text-text-primary min-h-[100px] focus:ring-1 focus:ring-primary focus:border-primary outline-none"
                  value={currentDraft?.product_description || ''}
                  onChange={(e) => handleEditChange('product_description', e.target.value)}
                />
              ) : (
                <p className="text-sm text-text-primary bg-surface-muted/30 p-3 rounded">{currentDraft?.product_description || 'Not specified'}</p>
              )}
            </div>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Intended Application</h4>
            {editingMode ? (
              <input 
                type="text" 
                className="w-full border border-border rounded px-3 py-2 text-sm text-text-primary focus:ring-1 focus:ring-primary focus:border-primary outline-none"
                value={currentDraft?.intended_application || ''}
                onChange={(e) => handleEditChange('intended_application', e.target.value)}
              />
            ) : (
              <p className="text-sm text-text-primary">{currentDraft?.intended_application || 'Not specified'}</p>
            )}
          </div>

          {/* Applicable Standards */}
          <div>
            <h4 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-3 pb-2 border-b border-border">Applicable Standards</h4>
            {currentDraft?.applicable_standards?.length > 0 ? (
              <div className="space-y-3">
                {currentDraft.applicable_standards.map((std: any, idx: number) => (
                  <div key={idx} className="flex flex-col sm:flex-row sm:items-center justify-between bg-surface-muted/50 border border-border rounded p-3">
                    <div>
                      <span className="font-bold text-text-primary">{std.standard_number}</span>
                      <p className="text-sm text-text-secondary">{std.title}</p>
                    </div>
                    <div className="mt-2 sm:mt-0 flex flex-col items-start sm:items-end">
                      <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-primary/10 text-primary">
                        {std.relevance}
                      </span>
                      {std.evidence_summary && (
                         <span className="text-xs text-text-secondary mt-1 flex items-center">
                           <BookOpen className="w-3 h-3 mr-1" /> 
                           Source: {std.evidence_summary}
                         </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-text-secondary italic">No standards applied.</p>
            )}
          </div>

          {/* Technical Sections */}
          <div className="bg-white border border-border rounded shadow-sm p-5">
            {renderRequirementsList("Technical Requirements", currentDraft?.technical_requirements)}
            {renderRequirementsList("Material Requirements", currentDraft?.material_requirements)}
            {renderRequirementsList("Dimensional & Grade Requirements", currentDraft?.dimensional_requirements)}
            {renderRequirementsList("Performance Requirements", currentDraft?.performance_requirements)}
          </div>

          <div className="bg-white border border-border rounded shadow-sm p-5">
            {renderRequirementsList("Testing & Inspection", currentDraft?.testing_requirements)}
            {renderRequirementsList("Quality & Certification", currentDraft?.quality_requirements)}
          </div>

          <div className="bg-white border border-border rounded shadow-sm p-5">
            {renderRequirementsList("Packaging & Delivery", currentDraft?.packaging_requirements)}
            {renderRequirementsList("Documentation Required", currentDraft?.documentation_requirements)}
          </div>

          {/* Clarifications */}
          {currentDraft?.items_requiring_clarification?.length > 0 && (
            <div className="bg-warning/5 border border-warning/30 rounded p-5">
              <h4 className="text-sm font-semibold text-warning-dark uppercase tracking-wider mb-3 flex items-center">
                <AlertTriangle className="w-4 h-4 mr-2" />
                Items Requiring Clarification
              </h4>
              <ul className="list-disc pl-5 space-y-1">
                {currentDraft.items_requiring_clarification.map((item: string, idx: number) => (
                  <li key={idx} className="text-sm text-warning-dark">{item}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Action Buttons */}
          <div className="mt-8 pt-6 border-t border-border flex flex-col sm:flex-row justify-between items-center gap-4">
            {saveError && (
              <div className="text-sm text-error mb-2 sm:mb-0 w-full sm:w-auto text-center sm:text-left">
                {saveError}
              </div>
            )}
            {!saveSuccess ? (
              <button 
                onClick={saveAnalysis}
                disabled={saving || editingMode}
                className="w-full sm:w-auto px-6 py-2.5 bg-primary text-white font-medium rounded hover:bg-primary-dark transition-colors disabled:opacity-50 flex items-center justify-center"
              >
                {saving ? (
                  <>Saving...</>
                ) : (
                  <><Save className="w-4 h-4 mr-2" /> Save Analysis</>
                )}
              </button>
            ) : (
              <div className="w-full sm:w-auto flex flex-col sm:flex-row items-center gap-3">
                <span className="text-sm font-medium text-success flex items-center">
                  <CheckCircle2 className="w-4 h-4 mr-1.5" /> Saved successfully
                </span>
                <div className="flex gap-2">
                  <a href="/history" className="px-4 py-2 border border-border bg-white text-text-primary text-sm font-medium rounded hover:bg-surface-muted transition-colors flex items-center">
                    View in History
                  </a>
                  <button onClick={handleExport} className="px-4 py-2 bg-primary text-white text-sm font-medium rounded hover:bg-primary-dark transition-colors flex items-center">
                    <ExternalLink className="w-4 h-4 mr-2" /> Export Report
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

