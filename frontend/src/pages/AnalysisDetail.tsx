import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Loader2, AlertTriangle, Download, FileText } from 'lucide-react';
import ErrorBoundary from '../components/ErrorBoundary';
import { API_BASE_URL } from '../config';

export default function AnalysisDetail() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/history/${id}`);
        if (!response.ok) {
          throw new Error('Failed to load analysis details');
        }
        const result = await response.json();
        setData(result);
      } catch (err: any) {
        setError(err.message || 'Error loading analysis');
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [id]);

  const handleExport = () => {
    // Generate an HTML report and open it in a new window to print/save as PDF
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;

    const html = `
      <html>
        <head>
          <title>Analysis Report - ${data?.title || 'Report'}</title>
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
          <p><strong>Analysis Title:</strong> ${data?.title}</p>
          <p><strong>Date:</strong> ${new Date(data?.created_at).toLocaleString()}</p>
          <p><strong>Status:</strong> ${data?.status}</p>
          
          <div class="section">
            <h2>1. Original Procurement Requirement</h2>
            <div class="box">${data?.procurement_requirement.replace(/\n/g, '<br/>')}</div>
          </div>

          <div class="section">
            <h2>2. Structured Requirement</h2>
            <div class="box">
              <p><strong>Intent Summary:</strong> ${data?.extracted_requirement?.intent_summary}</p>
              <p><strong>Products:</strong> ${(data?.extracted_requirement?.products || []).join(', ')}</p>
              <p><strong>Applications:</strong> ${(data?.extracted_requirement?.applications || []).join(', ')}</p>
            </div>
          </div>

          <div class="section">
            <h2>3. Recommended Indian Standards</h2>
            ${data?.recommendations?.recommendations?.map((r: any) => `
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
            ${data?.gaps?.gaps?.map((g: any) => `
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
              <h3>${data?.specification?.title}</h3>
              <p><strong>Objective:</strong> ${data?.specification?.procurement_objective}</p>
              <p><strong>Description:</strong> ${data?.specification?.product_description}</p>
              
              <h4>Technical Requirements</h4>
              <ul>
                ${data?.specification?.technical_requirements?.map((req: any) => `<li>${req.requirement}</li>`).join('') || '<li>None</li>'}
              </ul>
              
              <h4>Testing & Inspection</h4>
              <ul>
                ${data?.specification?.testing_requirements?.map((req: any) => `<li>${req.requirement}</li>`).join('') || '<li>None</li>'}
              </ul>
              
              <h4>Quality & Certification</h4>
              <ul>
                ${data?.specification?.quality_requirements?.map((req: any) => `<li>${req.requirement}</li>`).join('') || '<li>None</li>'}
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

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center p-20">
        <Loader2 className="w-10 h-10 text-primary animate-spin mb-4" />
        <h3 className="text-lg font-medium text-text-primary">Loading analysis...</h3>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex flex-col items-center justify-center p-20 bg-surface border border-error/20 rounded-xl">
        <AlertTriangle className="w-10 h-10 text-error mb-4" />
        <h3 className="text-lg font-medium text-text-primary mb-2">Error Loading Analysis</h3>
        <p className="text-sm text-text-secondary mb-6">{error}</p>
        <Link to="/history" className="px-4 py-2 bg-primary text-white rounded-md">Back to History</Link>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex justify-between items-center bg-surface border border-border rounded-xl p-4 shadow-sm">
          <Link to="/history" className="flex items-center text-sm font-medium text-text-secondary hover:text-text-primary transition-colors">
            <ArrowLeft className="w-4 h-4 mr-2" /> Back to History
          </Link>
          <div className="flex space-x-3">
            <Link to={`/specification-builder/${id}`} className="flex items-center px-4 py-2 bg-white border border-border text-text-primary text-sm font-medium rounded hover:bg-surface-muted transition-colors">
              <FileText className="w-4 h-4 mr-2" /> Open in Specification Builder
            </Link>
            <button onClick={handleExport} className="flex items-center px-4 py-2 bg-primary text-white text-sm font-medium rounded hover:bg-primary-dark transition-colors">
              <Download className="w-4 h-4 mr-2" /> Export Report
            </button>
          </div>
        </div>

        <div className="bg-surface border border-border rounded-xl shadow-sm p-6">
          <div className="border-b border-border pb-4 mb-6">
            <h1 className="text-2xl font-bold text-text-primary">{data.title}</h1>
            <div className="mt-2 flex space-x-4 text-sm text-text-secondary">
              <span>Date: {new Date(data.created_at).toLocaleString()}</span>
              <span>Status: <span className="uppercase text-primary font-bold">{data.status}</span></span>
            </div>
          </div>

          <div className="space-y-8">
            <section>
              <h2 className="text-lg font-semibold text-text-primary mb-3">1. Original Requirement</h2>
              <div className="bg-surface-muted p-4 rounded-lg border border-border">
                <p className="whitespace-pre-wrap text-sm text-text-primary">{data.procurement_requirement}</p>
              </div>
            </section>

            {data.extracted_requirement && (
              <section>
                <h2 className="text-lg font-semibold text-text-primary mb-3">2. Structured Requirement</h2>
                <div className="bg-surface-muted p-4 rounded-lg border border-border space-y-3 text-sm">
                  <p><strong>Intent Summary:</strong> {data.extracted_requirement.intent_summary}</p>
                  <p><strong>Products:</strong> {(data.extracted_requirement.products || []).join(', ')}</p>
                  <p><strong>Applications:</strong> {(data.extracted_requirement.applications || []).join(', ')}</p>
                </div>
              </section>
            )}

            {data.recommendations?.recommendations && (
              <section>
                <h2 className="text-lg font-semibold text-text-primary mb-3">3. Recommended Standards</h2>
                <div className="space-y-3">
                  {data.recommendations.recommendations.map((r: any, idx: number) => (
                    <div key={idx} className="bg-surface-muted p-4 rounded-lg border border-border">
                      <h3 className="font-bold text-text-primary">{r.standard_number} - {r.title}</h3>
                      <span className="inline-block mt-1 px-2 py-0.5 text-[10px] font-bold uppercase rounded-full bg-primary/10 text-primary">{r.relevance_category}</span>
                      <div className="mt-3">
                        <p className="text-xs font-semibold uppercase text-text-secondary mb-1">Why Recommended:</p>
                        <ul className="list-disc pl-4 space-y-1 text-sm text-text-primary">
                          {r.why_recommended?.map((w: string, i: number) => <li key={i}>{w}</li>)}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {data.gaps?.gaps && (
              <section>
                <h2 className="text-lg font-semibold text-text-primary mb-3">4. Specification Gaps</h2>
                <div className="space-y-3">
                  {data.gaps.gaps.map((g: any, idx: number) => (
                    <div key={idx} className="bg-surface-muted p-4 rounded-lg border border-border flex items-start">
                      <AlertTriangle className={`w-5 h-5 mt-0.5 mr-3 ${g.severity === 'HIGH' ? 'text-error' : g.severity === 'MEDIUM' ? 'text-warning' : 'text-success'}`} />
                      <div>
                        <h3 className="font-bold text-text-primary">{g.title} <span className="text-xs uppercase ml-2 opacity-70">[{g.severity}]</span></h3>
                        <p className="text-sm text-text-primary mt-1">{g.description}</p>
                        <p className="text-sm text-primary mt-2"><strong>Action:</strong> {g.suggested_information}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {data.specification && (
              <section>
                <h2 className="text-lg font-semibold text-text-primary mb-3">5. Draft Specification</h2>
                <div className="bg-surface-muted p-4 rounded-lg border border-border space-y-4">
                  <h3 className="text-xl font-bold border-b border-border pb-2">{data.specification.title}</h3>
                  <p className="text-sm"><strong>Objective:</strong> {data.specification.procurement_objective}</p>
                  
                  <h4 className="font-bold text-sm uppercase mt-4">Technical Requirements</h4>
                  <ul className="list-disc pl-5 text-sm space-y-1">
                    {data.specification.technical_requirements?.map((r: any, i: number) => <li key={i}>{r.requirement}</li>)}
                  </ul>
                  
                  <h4 className="font-bold text-sm uppercase mt-4">Quality & Certification</h4>
                  <ul className="list-disc pl-5 text-sm space-y-1">
                    {data.specification.quality_requirements?.map((r: any, i: number) => <li key={i}>{r.requirement}</li>)}
                  </ul>
                </div>
              </section>
            )}
          </div>
        </div>
      </div>
    </ErrorBoundary>
  );
}
