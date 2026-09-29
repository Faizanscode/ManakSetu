import { Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import NewAnalysis from './pages/NewAnalysis';
import Standards from './pages/Standards';
import History from './pages/History';
import AnalysisDetail from './pages/AnalysisDetail';
import SpecificationBuilder from './pages/SpecificationBuilder';
import Settings from './pages/Settings';
import { useTheme } from './hooks/useTheme';

function App() {
  useTheme(); // Initialize theme

  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="new-analysis" element={<NewAnalysis />} />
        <Route path="standards" element={<Standards />} />
        <Route path="history" element={<History />} />
        <Route path="analysis/:id" element={<AnalysisDetail />} />
        <Route path="specification-builder" element={<SpecificationBuilder />} />
        <Route path="specification-builder/:id" element={<SpecificationBuilder />} />
        <Route path="settings" element={<Settings />} />

      </Route>
    </Routes>
  );
}

export default App;
