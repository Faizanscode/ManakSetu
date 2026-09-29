import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileSearch, BookOpen, Clock, FileText, Settings, ShieldCheck } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: (string | undefined | null | false)[]) {
  return twMerge(clsx(inputs));
}

const navItems = [
  { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { name: 'New Analysis', to: '/new-analysis', icon: FileSearch },
  { name: 'Standards', to: '/standards', icon: BookOpen },
  { name: 'Analysis History', to: '/history', icon: Clock },
  { name: 'Specification Builder', to: '/specification-builder', icon: FileText },
  { name: 'Settings', to: '/settings', icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-surface border-r border-border flex flex-col h-full flex-shrink-0">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <ShieldCheck className="w-8 h-8 text-primary mr-3" />
        <div className="flex flex-col">
          <span className="font-bold text-lg tracking-tight text-text-primary leading-tight">ManakSetu</span>
          <span className="text-[10px] text-text-secondary uppercase tracking-wider font-semibold">Indian Standards</span>
        </div>
      </div>
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                'flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary/10 text-primary'
                  : 'text-text-secondary hover:bg-surface-muted hover:text-text-primary'
              )
            }
          >
            <item.icon className="w-5 h-5 mr-3 flex-shrink-0" />
            {item.name}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-border">
        <div className="flex items-center text-xs text-text-secondary font-medium">
          <div className="w-2 h-2 rounded-full bg-success mr-2"></div>
          System Ready
        </div>
      </div>
    </aside>
  );
}
