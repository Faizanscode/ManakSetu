import { useState, useEffect, useMemo } from 'react';
import { Clock, FileText, Loader2, AlertTriangle, ArrowRight, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';

interface HistoryItem {
  id: string;
  title: string;
  procurement_requirement: string;
  category: string;
  priority: string;
  status: string;
  created_at: string;
  updated_at: string | null;
}

export default function History() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filter states
  const [dateOrder, setDateOrder] = useState<string>('newest');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8002/api/history/');
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }
      const data = await response.json();
      setHistory(data);
    } catch (err: any) {
      setError(err.message || 'Error loading history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this analysis?")) return;
    
    setDeletingId(id);
    try {
      const response = await fetch(`http://127.0.0.1:8002/api/history/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete analysis');
      
      // Update state without refetching
      setHistory(prev => prev.filter(item => item.id !== id));
    } catch (err: any) {
      alert(err.message || "Failed to delete item");
    } finally {
      setDeletingId(null);
    }
  };

  // Derived filter options
  const uniqueCategories = useMemo(() => {
    return Array.from(new Set(history.map(item => item.category).filter(Boolean)));
  }, [history]);
  
  const uniqueStatuses = useMemo(() => {
    return Array.from(new Set(history.map(item => item.status).filter(Boolean)));
  }, [history]);

  // Apply filters
  const filteredHistory = useMemo(() => {
    let result = [...history];
    
    // Apply Category Filter
    if (categoryFilter !== 'all') {
      result = result.filter(item => item.category === categoryFilter);
    }
    
    // Apply Status Filter
    if (statusFilter !== 'all') {
      result = result.filter(item => item.status === statusFilter);
    }
    
    // Apply Date Sort
    result.sort((a, b) => {
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();
      return dateOrder === 'newest' ? dateB - dateA : dateA - dateB;
    });
    
    return result;
  }, [history, categoryFilter, statusFilter, dateOrder]);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
        <h2 className="text-xl font-semibold text-text-primary">Analysis History</h2>
        <p className="text-sm text-text-secondary mt-1">
          Review previous procurement requirement analyses.
        </p>
      </div>

      <div className="flex space-x-3 items-center flex-wrap gap-y-2">
        <select 
          className="px-3 py-1.5 text-xs font-medium border border-border rounded-md bg-surface-muted text-text-primary focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
          value={dateOrder}
          onChange={(e) => setDateOrder(e.target.value)}
        >
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
        </select>
        
        <select 
          className="px-3 py-1.5 text-xs font-medium border border-border rounded-md bg-surface-muted text-text-primary focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer capitalize"
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
        >
          <option value="all">All Categories</option>
          {uniqueCategories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        
        <select 
          className="px-3 py-1.5 text-xs font-medium border border-border rounded-md bg-surface-muted text-text-primary focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer capitalize"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="all">All Statuses</option>
          {uniqueStatuses.map(status => (
            <option key={status} value={status}>{status}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="bg-surface border border-border rounded-xl p-16 flex flex-col items-center justify-center text-center shadow-sm">
          <Loader2 className="w-10 h-10 text-primary animate-spin mb-4" />
          <h3 className="text-lg font-medium text-text-primary mb-2">Loading History</h3>
        </div>
      ) : error ? (
        <div className="bg-surface border border-error/20 rounded-xl p-16 flex flex-col items-center justify-center text-center shadow-sm">
          <AlertTriangle className="w-10 h-10 text-error mb-4" />
          <h3 className="text-lg font-medium text-text-primary mb-2">Error</h3>
          <p className="text-sm text-text-secondary max-w-md">{error}</p>
        </div>
      ) : history.length === 0 ? (
        <div className="bg-surface border border-border rounded-xl p-16 flex flex-col items-center justify-center text-center shadow-sm">
          <Clock className="w-16 h-16 text-text-secondary mb-4 opacity-30" />
          <h3 className="text-lg font-medium text-text-primary mb-2">No analysis history</h3>
          <p className="text-sm text-text-secondary max-w-md">
            Completed analyses will appear here once you save them.
          </p>
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="bg-surface border border-border rounded-xl p-16 flex flex-col items-center justify-center text-center shadow-sm">
          <AlertTriangle className="w-16 h-16 text-text-secondary mb-4 opacity-30" />
          <h3 className="text-lg font-medium text-text-primary mb-2">No matching history</h3>
          <p className="text-sm text-text-secondary max-w-md">
            No analysis matches the selected filters.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredHistory.map((item) => (
            <div key={item.id} className="bg-surface border border-border rounded-xl p-5 shadow-sm hover:border-primary/30 transition-colors">
              <div className="flex flex-col sm:flex-row justify-between sm:items-center">
                <div className="flex-1 pr-4">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="font-semibold text-text-primary text-lg flex items-center">
                      <FileText className="w-4 h-4 text-primary mr-2" />
                      {item.title}
                    </h3>
                    <span className="bg-primary/10 text-primary text-[10px] px-2 py-0.5 rounded-full font-bold uppercase">
                      {item.status}
                    </span>
                  </div>
                  <p className="text-sm text-text-secondary line-clamp-1 max-w-2xl">
                    {item.procurement_requirement}
                  </p>
                  <div className="mt-3 flex items-center text-xs text-text-secondary space-x-4">
                    <span>
                      <span className="font-medium">Date:</span> {new Date(item.created_at).toLocaleDateString()}
                    </span>
                    {item.category && (
                      <span className="capitalize"><span className="font-medium">Category:</span> {item.category}</span>
                    )}
                  </div>
                </div>
                <div className="mt-4 sm:mt-0 flex items-center space-x-2">
                  <Link 
                    to={`/specification-builder/${item.id}`} 
                    className="px-4 py-2 bg-primary/10 text-primary font-medium text-sm rounded border border-primary/20 hover:bg-primary/20 transition-colors flex items-center"
                  >
                    Open in Builder <ArrowRight className="w-3 h-3 ml-2" />
                  </Link>
                  <Link 
                    to={`/analysis/${item.id}`} 
                    className="px-4 py-2 bg-surface-muted text-text-primary font-medium text-sm rounded border border-border hover:bg-border transition-colors flex items-center"
                  >
                    View Details
                  </Link>
                  <button 
                    onClick={() => handleDelete(item.id)}
                    disabled={deletingId === item.id}
                    title="Delete analysis"
                    className="p-2 bg-surface-muted text-error/80 font-medium text-sm rounded border border-border hover:bg-error/10 hover:border-error/30 hover:text-error transition-colors disabled:opacity-50"
                  >
                    {deletingId === item.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
