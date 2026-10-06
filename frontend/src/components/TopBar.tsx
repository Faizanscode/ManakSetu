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

    </header>
  );
}
