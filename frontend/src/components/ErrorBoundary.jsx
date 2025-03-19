import React, { Component } from 'react';
import PropTypes from 'prop-types';
import logger from '../utils/logger';

/**
 * Error Boundary component to catch JavaScript errors in child components
 * and log them to our logging system.
 */
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
    this.logger = logger.getLogger('ErrorBoundary');
  }

  /**
   * Update state when errors are caught
   */
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  /**
   * Log error details when component catches an error
   */
  componentDidCatch(error, errorInfo) {
    // Log error to our backend
    this.logger.error(`React component error: ${error.message}`, {
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack
      },
      componentStack: errorInfo.componentStack
    });
    
    this.setState({ errorInfo });
  }

  /**
   * Reset error state to allow recovery
   */
  resetErrorBoundary = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    this.props.onReset?.();
  };

  render() {
    const { hasError, error, errorInfo } = this.state;
    const { fallback, children } = this.props;

    if (hasError) {
      // If a custom fallback is provided, use it
      if (fallback) {
        return typeof fallback === 'function'
          ? fallback({ error, errorInfo, resetErrorBoundary: this.resetErrorBoundary })
          : fallback;
      }

      // Default error UI
      return (
        <div className="error-boundary">
          <h2>Something went wrong.</h2>
          <p>{error?.message || 'An unexpected error occurred'}</p>
          <button onClick={this.resetErrorBoundary}>Try again</button>
        </div>
      );
    }

    return children;
  }
}

ErrorBoundary.propTypes = {
  /** Custom fallback component or render function */
  fallback: PropTypes.oneOfType([PropTypes.node, PropTypes.func]),
  /** Function to call when resetting the error boundary */
  onReset: PropTypes.func,
  /** Components that this boundary wraps */
  children: PropTypes.node.isRequired
};

export default ErrorBoundary; 