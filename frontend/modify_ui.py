import sys

def modify_frontend():
    path = r"D:\ManakSetu\frontend\src\pages\NewAnalysis.tsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Imports
    if "AlertTriangle" not in content:
        content = content.replace(
            "CheckCircle2, Loader2, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';",
            "CheckCircle2, Loader2, BookOpen, ChevronDown, ChevronUp, AlertTriangle } from 'lucide-react';"
        )

    # 2. State variables
    state_vars = """
  const [gapLoading, setGapLoading] = useState(false);
  const [gapError, setGapError] = useState<string | null>(null);
  const [gapData, setGapData] = useState<any>(null);
"""
    if "gapLoading" not in content:
        content = content.replace(
            "const [expandedEvidence, setExpandedEvidence] = useState<Record<string, boolean>>({});",
            "const [expandedEvidence, setExpandedEvidence] = useState<Record<string, boolean>>({});\n" + state_vars
        )

    # 3. handleClear updates
    clear_updates = """
    setGapError(null);
    setGapData(null);
"""
    if "setGapData(null)" not in content:
        content = content.replace(
            "setExpandedEvidence({});",
            "setExpandedEvidence({});\n" + clear_updates
        )

    # 4. handleCheckGaps function
    handle_check_gaps = """
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
"""
    if "handleCheckGaps" not in content:
        content = content.replace(
            "const toggleEvidence = (id: string) => {",
            handle_check_gaps + "\n  const toggleEvidence = (id: string) => {"
        )

    # 5. UI elements
    # I need to insert it right before the last </div> in the return block.
    # We look for the end of the recData block: `      )}`
    
    gap_ui = """
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
          </div>
        </div>
      )}
"""

    if "Specification Completeness Check" not in content:
        # We replace `      )}` which ends the recData block
        # The end of the file looks like this:
        #           </div>
        #         </div>
        #       )}
        #     </div>
        #     </ErrorBoundary>
        #   );
        # }
        
        # Safe replacement logic:
        # We replace exactly the last `      )}` before `    </div>`
        parts = content.rsplit("      )}\n    </div>", 1)
        if len(parts) == 2:
            content = parts[0] + "      )}\n" + gap_ui + "\n    </div>" + parts[1]
        else:
            print("Failed to find injection point for UI")
            sys.exit(1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully updated NewAnalysis.tsx")

if __name__ == "__main__":
    modify_frontend()
