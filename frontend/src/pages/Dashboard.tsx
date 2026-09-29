import { Link } from 'react-router-dom';
import { ArrowRight, FileSearch, BookOpen, Clock, FileText } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="max-w-5xl mx-auto space-y-8">
      {/* Welcome Section */}
      <section className="bg-surface border border-border rounded-xl p-8 shadow-sm">
        <h2 className="text-2xl font-bold text-text-primary mb-2">Welcome to ManakSetu</h2>
        <p className="text-text-secondary mb-6 max-w-2xl">
          Analyze procurement requirements and identify applicable Indian Standards.
        </p>
        <div className="flex space-x-4">
          <Link
            to="/new-analysis"
            className="inline-flex items-center justify-center px-4 py-2 bg-primary text-white rounded-md font-medium hover:bg-primary-hover transition-colors"
          >
            Start New Analysis
          </Link>
          <Link
            to="/standards"
            className="inline-flex items-center justify-center px-4 py-2 bg-surface-muted text-text-primary border border-border rounded-md font-medium hover:bg-border transition-colors"
          >
            Browse Standards
          </Link>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="bg-surface border border-border rounded-xl p-8 shadow-sm">
        <h3 className="text-lg font-semibold text-text-primary mb-6">Workflow Overview</h3>
        <div className="flex flex-col md:flex-row items-center justify-between text-center space-y-4 md:space-y-0">
          <WorkflowStep icon={FileSearch} title="Requirement Analysis" />
          <ArrowRight className="w-5 h-5 text-text-secondary hidden md:block" />
          <WorkflowStep icon={BookOpen} title="Standards Discovery" />
          <ArrowRight className="w-5 h-5 text-text-secondary hidden md:block" />
          <WorkflowStep icon={FileText} title="Evidence & Explanation" />
          <ArrowRight className="w-5 h-5 text-text-secondary hidden md:block" />
          <WorkflowStep icon={Clock} title="Specification Support" />
        </div>
      </section>

      {/* Recent Analyses */}
      <section>
        <h3 className="text-lg font-semibold text-text-primary mb-4">Recent Analyses</h3>
        <div className="bg-surface border border-border rounded-xl p-12 flex flex-col items-center justify-center text-center shadow-sm">
          <FileSearch className="w-12 h-12 text-text-secondary mb-4 opacity-50" />
          <h4 className="text-base font-medium text-text-primary mb-1">No analyses yet</h4>
          <p className="text-sm text-text-secondary mb-6 max-w-md">
            Your completed procurement analyses will appear here.
          </p>
          <Link
            to="/new-analysis"
            className="inline-flex items-center justify-center px-4 py-2 bg-primary/10 text-primary rounded-md font-medium hover:bg-primary/20 transition-colors"
          >
            Create First Analysis
          </Link>
        </div>
      </section>
    </div>
  );
}

function WorkflowStep({ icon: Icon, title }: { icon: any, title: string }) {
  return (
    <div className="flex flex-col items-center space-y-3 w-40">
      <div className="w-12 h-12 rounded-full bg-surface-muted border border-border flex items-center justify-center text-primary">
        <Icon className="w-6 h-6" />
      </div>
      <span className="text-sm font-medium text-text-primary leading-tight">{title}</span>
    </div>
  );
}
