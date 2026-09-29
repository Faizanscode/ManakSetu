import { Search, Bell, User } from 'lucide-react';
import { useLocation } from 'react-router-dom';

const routeNames: Record<string, { title: string, description: string }> = {
  '/dashboard': { title: 'Dashboard', description: 'Overview of procurement analyses and standards.' },
  '/new-analysis': { title: 'New Analysis', description: 'Analyze procurement requirements.' },
  '/standards': { title: 'Indian Standards', description: 'Explore standards available in the ManakSetu knowledge base.' },
  '/history': { title: 'Analysis History', description: 'Review previous procurement requirement analyses.' },
  '/specification-builder': { title: 'Specification Builder', description: 'Build procurement-ready specifications.' },
  '/settings': { title: 'Settings', description: 'Manage application preferences and system status.' },
};

export default function TopBar() {
  const location = useLocation();
  let currentRoute = routeNames[location.pathname];
  if (!currentRoute) {
    if (location.pathname.startsWith('/analysis/')) {
      currentRoute = { title: 'Analysis Details', description: 'Review the detailed analysis report and generated specifications.' };
    } else if (location.pathname.startsWith('/specification-builder/')) {
      currentRoute = routeNames['/specification-builder'];
    } else {
      currentRoute = { title: 'ManakSetu', description: '' };
    }
  }

  return (
    <header className="h-16 bg-surface border-b border-border flex items-center justify-between px-6 flex-shrink-0">
      <div>
        <h1 className="text-lg font-semibold text-text-primary leading-tight">{currentRoute.title}</h1>
        <p className="text-xs text-text-secondary">{currentRoute.description}</p>
      </div>

      <div className="flex items-center space-x-4">
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" />
          <input 
            type="text" 
            placeholder="Search standards..." 
            className="pl-9 pr-4 py-1.5 text-sm bg-surface-muted border border-border rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary w-64 placeholder:text-text-secondary/70"
          />
        </div>
        
        <button className="p-1.5 text-text-secondary hover:text-text-primary hover:bg-surface-muted rounded-full transition-colors">
          <Bell className="w-5 h-5" />
        </button>
        
        <button className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary">
          <User className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
