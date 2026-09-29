import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';

class ErrorBoundary extends Component<{children: ReactNode}, {hasError: boolean, error: Error | null}> {
  constructor(props: {children: ReactNode}) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 bg-red-50 text-red-700 border border-red-200 rounded-lg m-4">
          <h2 className="text-lg font-bold mb-2">Something went wrong rendering this component.</h2>
          <p className="text-sm mb-4">{this.state.error?.toString()}</p>
          <button onClick={() => this.setState({hasError: false, error: null})} className="px-4 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700">Try Again</button>
        </div>
      );
    }
 return this.props.children;
 }
}

export default ErrorBoundary;