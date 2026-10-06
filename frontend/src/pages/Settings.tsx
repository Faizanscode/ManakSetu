import { useEffect, useState } from 'react';
import { useTheme } from '../hooks/useTheme';
import { API_BASE_URL } from '../config';

export default function Settings() {
  const { theme, setTheme } = useTheme();
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'unavailable'>('checking');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/health`);
        if (res.ok) {
          setApiStatus('connected');
        } else {
          setApiStatus('unavailable');
        }
      } catch (err) {
        setApiStatus('unavailable');
      }
    };
    checkHealth();
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
        <h2 className="text-xl font-semibold text-text-primary mb-6">Settings</h2>
        
        <div className="space-y-8">
          <section>
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">Appearance</h3>
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-2">
                <input 
                  type="radio" 
                  name="theme" 
                  value="light" 
                  checked={theme === 'light'} 
                  onChange={() => setTheme('light')}
                  className="text-primary focus:ring-primary" 
                />
                <span className="text-sm text-text-primary">Light</span>
              </label>
              <label className="flex items-center space-x-2">
                <input 
                  type="radio" 
                  name="theme" 
                  value="dark" 
                  checked={theme === 'dark'} 
                  onChange={() => setTheme('dark')}
                  className="text-primary focus:ring-primary" 
                />
                <span className="text-sm text-text-primary">Dark</span>
              </label>
              <label className="flex items-center space-x-2">
                <input 
                  type="radio" 
                  name="theme" 
                  value="system" 
                  checked={theme === 'system'} 
                  onChange={() => setTheme('system')}
                  className="text-primary focus:ring-primary" 
                />
                <span className="text-sm text-text-primary">System Default</span>
              </label>
            </div>
          </section>

          <section>
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">Application</h3>
            <div className="bg-surface-muted rounded-md p-4 space-y-2 border border-border">
              <div className="flex justify-between">
                <span className="text-sm text-text-secondary">Product</span>
                <span className="text-sm font-medium text-text-primary">ManakSetu</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-text-secondary">Version</span>
                <span className="text-sm font-medium text-text-primary">0.1.0</span>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">System Status</h3>
            <div className="bg-surface-muted rounded-md p-4 border border-border">
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Backend API Connection</span>
                <div className="flex items-center">
                  {apiStatus === 'checking' && <span className="text-sm text-text-secondary">Checking...</span>}
                  {apiStatus === 'connected' && (
                    <>
                      <div className="w-2 h-2 rounded-full bg-success mr-2"></div>
                      <span className="text-sm font-medium text-success">Backend Connected</span>
                    </>
                  )}
                  {apiStatus === 'unavailable' && (
                    <>
                      <div className="w-2 h-2 rounded-full bg-danger mr-2"></div>
                      <span className="text-sm font-medium text-danger">Backend Unavailable</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
