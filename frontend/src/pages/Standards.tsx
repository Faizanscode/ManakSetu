import { useState, useEffect, useMemo } from 'react';
import { BookOpen, AlertCircle, RefreshCw, Search, X } from 'lucide-react';
import { API_BASE_URL } from '../config';

interface Sector {
  id: string;
  name: string;
  description?: string;
}

interface Category {
  id: string;
  name: string;
  sector_id: string;
}

interface Standard {
  id: string;
  standard_number: string;
  title: string;
  short_description?: string;
  status: string;
  sector_id?: string;
  category_id?: string;
  sector?: Sector;
  category?: Category;
}

const STATUS_COLORS: Record<string, string> = {
  CURRENT: 'bg-success/10 text-success',
  WITHDRAWN: 'bg-error/10 text-error',
  UNDER_REVISION: 'bg-warning/10 text-warning',
};

export default function Standards() {
  const [standards, setStandards] = useState<Standard[]>([]);
  const [sectors, setSectors] = useState<Sector[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filter state
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSector, setSelectedSector] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [totalCount, setTotalCount] = useState<number>(0);

  const fetchStandards = async () => {
    setLoading(true);
    setError(null);
    try {
      const [standardsRes, sectorsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/standards?limit=1000`),
        fetch(`${API_BASE_URL}/standards/sectors`),
      ]);
      if (!standardsRes.ok) throw new Error(`Failed to fetch standards: ${standardsRes.statusText}`);
      if (!sectorsRes.ok) throw new Error(`Failed to fetch sectors: ${sectorsRes.statusText}`);

      const totalHeader = standardsRes.headers.get('X-Total-Count');
      const standardsData = await standardsRes.json();
      const sectorsData = await sectorsRes.json();
      setStandards(standardsData);
      setSectors(sectorsData);
      setTotalCount(totalHeader ? parseInt(totalHeader, 10) : standardsData.length);
    } catch (err: any) {
      setError(err.message || 'Unable to connect to the backend API.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStandards();
  }, []);

  // Filtered standards (client-side)
  const filteredStandards = useMemo(() => {
    return standards.filter((std) => {
      const matchesSearch =
        !searchQuery ||
        std.standard_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
        std.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (std.short_description || '').toLowerCase().includes(searchQuery.toLowerCase());

      const matchesSector = !selectedSector || std.sector_id === selectedSector;
      const matchesStatus = !selectedStatus || std.status === selectedStatus;

      return matchesSearch && matchesSector && matchesStatus;
    });
  }, [standards, searchQuery, selectedSector, selectedStatus]);

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedSector('');
    setSelectedStatus('');
  };

  const hasActiveFilters = searchQuery || selectedSector || selectedStatus;

  // Sector counts for display
  const sectorCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    standards.forEach((s) => {
      if (s.sector_id) counts[s.sector_id] = (counts[s.sector_id] || 0) + 1;
    });
    return counts;
  }, [standards]);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold text-text-primary">Indian Standards Knowledge Base</h2>
            <p className="text-sm text-text-secondary mt-1">
              {loading 
                ? 'Loading...' 
                : hasActiveFilters 
                  ? `Showing ${filteredStandards.length} matching standards out of ${totalCount}` 
                  : `Total Standards: ${totalCount}`
              }
            </p>
          </div>
          <button
            onClick={fetchStandards}
            disabled={loading}
            className="flex items-center gap-2 bg-surface border border-border rounded-md px-3 py-2 text-sm text-text-secondary hover:text-text-primary hover:border-primary/50 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Sector Summary Chips */}
      {!loading && sectors.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {sectors.map((sector) => (
            <button
              key={sector.id}
              onClick={() => setSelectedSector(selectedSector === sector.id ? '' : sector.id)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                selectedSector === sector.id
                  ? 'bg-primary text-white border-primary'
                  : 'bg-surface border-border text-text-secondary hover:border-primary/50 hover:text-text-primary'
              }`}
            >
              {sector.name}
              <span className="ml-1.5 opacity-70">({sectorCounts[sector.id] || 0})</span>
            </button>
          ))}
        </div>
      )}

      {/* Filter Bar */}
      <div className="flex flex-col md:flex-row gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by IS number or title..."
            className="w-full pl-9 pr-3 bg-surface border border-border rounded-md px-3 py-2 text-sm text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        {/* Sector Filter */}
        <select
          value={selectedSector}
          onChange={(e) => setSelectedSector(e.target.value)}
          className="bg-surface border border-border rounded-md px-3 py-2 text-sm text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="">All Sectors</option>
          {sectors.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>

        {/* Status Filter */}
        <select
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
          className="bg-surface border border-border rounded-md px-3 py-2 text-sm text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="">All Statuses</option>
          <option value="CURRENT">Current</option>
          <option value="WITHDRAWN">Withdrawn</option>
          <option value="UNDER_REVISION">Under Revision</option>
        </select>

        {/* Clear Filters */}
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="flex items-center gap-1.5 px-3 py-2 text-sm text-text-secondary hover:text-text-primary border border-border rounded-md hover:border-primary/50 transition-colors"
          >
            <X className="w-4 h-4" />
            Clear
          </button>
        )}
      </div>

      {/* Content */}
      {loading ? (
        <div className="bg-surface border border-border rounded-xl p-16 flex flex-col items-center justify-center text-center shadow-sm">
          <RefreshCw className="w-12 h-12 text-primary animate-spin mb-4" />
          <p className="text-sm text-text-secondary">Loading standards knowledge base...</p>
        </div>
      ) : error ? (
        <div className="bg-error/10 border border-error/20 rounded-xl p-8 flex flex-col items-center justify-center text-center shadow-sm">
          <AlertCircle className="w-12 h-12 text-error mb-4" />
          <h3 className="text-lg font-medium text-error mb-2">Connection Error</h3>
          <p className="text-sm text-error/80 max-w-md mb-4">{error}</p>
          <button
            onClick={fetchStandards}
            className="bg-error text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-error/90 transition-colors"
          >
            Retry Connection
          </button>
        </div>
      ) : filteredStandards.length === 0 ? (
        <div className="bg-surface border border-border rounded-xl p-16 flex flex-col items-center justify-center text-center shadow-sm">
          <BookOpen className="w-16 h-16 text-text-secondary mb-4 opacity-30" />
          <h3 className="text-lg font-medium text-text-primary mb-2">
            {hasActiveFilters ? 'No Matching Standards' : 'No Standards Found'}
          </h3>
          <p className="text-sm text-text-secondary max-w-md">
            {hasActiveFilters
              ? 'Try adjusting your search or filters.'
              : 'The knowledge base is currently empty. Run the seed script to populate data.'}
          </p>
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="mt-4 text-primary text-sm hover:underline"
            >
              Clear all filters
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredStandards.map((std) => (
            <div
              key={std.id}
              className="bg-surface border border-border rounded-xl p-5 shadow-sm hover:border-primary/50 transition-colors cursor-pointer"
            >
              <div className="flex justify-between items-start mb-2">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary">
                  {std.standard_number}
                </span>
                <span
                  className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                    STATUS_COLORS[std.status] || 'bg-surface border border-border text-text-secondary'
                  }`}
                >
                  {std.status}
                </span>
              </div>
              <h3 className="text-base font-medium text-text-primary mb-2 line-clamp-2">{std.title}</h3>
              <p className="text-sm text-text-secondary line-clamp-3 mb-4">
                {std.short_description || 'No description available.'}
              </p>
              {(std.sector || std.category) && (
                <div className="text-xs text-text-muted mt-auto pt-4 border-t border-border flex flex-wrap gap-4">
                  {std.sector && (
                    <span className="flex items-center gap-1">
                      <span className="font-medium text-text-secondary">Sector:</span> {std.sector.name}
                    </span>
                  )}
                  {std.category && (
                    <span className="flex items-center gap-1">
                      <span className="font-medium text-text-secondary">Category:</span> {std.category.name}
                    </span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
