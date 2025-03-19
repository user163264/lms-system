/**
 * Client-side logging utility for the LMS frontend.
 * 
 * This module provides logging functions that can send logs to the backend 
 * for centralized logging and monitoring.
 */

// Log levels with numeric values
const LOG_LEVELS = {
  DEBUG: 10,
  INFO: 20,
  WARNING: 30,
  ERROR: 40,
  CRITICAL: 50
};

// Configuration from environment
const LOG_LEVEL = process.env.NEXT_PUBLIC_LOG_LEVEL || 'INFO';
const LOG_TO_CONSOLE = process.env.NEXT_PUBLIC_LOG_TO_CONSOLE !== 'false';
const LOG_TO_SERVER = process.env.NEXT_PUBLIC_LOG_TO_SERVER !== 'false';
const LOG_ENDPOINT = process.env.NEXT_PUBLIC_LOG_ENDPOINT || '/api/logs';

// Get the numeric value for the configured log level
const CONFIGURED_LEVEL = LOG_LEVELS[LOG_LEVEL] || LOG_LEVELS.INFO;

/**
 * Logger class for client-side logging
 */
class Logger {
  /**
   * Create a new logger instance
   * @param {string} module - The module/component name
   */
  constructor(module) {
    this.module = module;
    this.browserInfo = this.getBrowserInfo();
  }

  /**
   * Get browser and environment information
   * @returns {Object} Browser information
   */
  getBrowserInfo() {
    if (typeof window === 'undefined') {
      return { environment: 'server' };
    }

    return {
      environment: 'browser',
      userAgent: navigator.userAgent,
      language: navigator.language,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      },
      url: window.location.href
    };
  }

  /**
   * Send a log message to the server
   * @param {string} level - Log level
   * @param {string} message - Log message
   * @param {Object} data - Additional data to log
   */
  async sendToServer(level, message, data = {}) {
    if (!LOG_TO_SERVER) return;

    try {
      // Build log entry
      const logEntry = {
        timestamp: new Date().toISOString(),
        level,
        module: this.module,
        message,
        browser: this.browserInfo,
        ...data
      };

      // Send log to server using fetch
      const response = await fetch(LOG_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(logEntry),
        credentials: 'include',
        // Don't wait for response to avoid blocking UI
        keepalive: true
      });

      // Check if the request was successful
      if (!response.ok) {
        // Only log to console if enabled
        if (LOG_TO_CONSOLE) {
          console.warn('Failed to send log to server:', response.status);
        }
      }
    } catch (error) {
      // Only log to console if enabled
      if (LOG_TO_CONSOLE) {
        console.warn('Error sending log to server:', error);
      }
    }
  }

  /**
   * Log a message at the specified level
   * @param {string} level - Log level
   * @param {string} message - Log message
   * @param {Object} data - Additional data to log
   */
  log(level, message, data = {}) {
    // Check if we should log at this level
    if (LOG_LEVELS[level] < CONFIGURED_LEVEL) {
      return;
    }

    // Log to console if enabled
    if (LOG_TO_CONSOLE) {
      const consoleData = { module: this.module, ...data };
      switch (level) {
        case 'DEBUG':
          console.debug(message, consoleData);
          break;
        case 'INFO':
          console.info(message, consoleData);
          break;
        case 'WARNING':
          console.warn(message, consoleData);
          break;
        case 'ERROR':
        case 'CRITICAL':
          console.error(message, consoleData);
          break;
        default:
          console.log(message, consoleData);
      }
    }

    // Send to server
    this.sendToServer(level, message, data);
  }

  /**
   * Log a debug message
   * @param {string} message - Log message
   * @param {Object} data - Additional data to log
   */
  debug(message, data = {}) {
    this.log('DEBUG', message, data);
  }

  /**
   * Log an info message
   * @param {string} message - Log message
   * @param {Object} data - Additional data to log
   */
  info(message, data = {}) {
    this.log('INFO', message, data);
  }

  /**
   * Log a warning message
   * @param {string} message - Log message
   * @param {Object} data - Additional data to log
   */
  warn(message, data = {}) {
    this.log('WARNING', message, data);
  }

  /**
   * Log an error message
   * @param {string} message - Log message
   * @param {Object} data - Additional data to log
   */
  error(message, data = {}) {
    this.log('ERROR', message, data);
  }

  /**
   * Log a critical message
   * @param {string} message - Log message
   * @param {Object} data - Additional data to log
   */
  critical(message, data = {}) {
    this.log('CRITICAL', message, data);
  }

  /**
   * Create a logger with a specific name
   * @param {string} module - Module name
   * @returns {Logger} Logger instance
   */
  static getLogger(module) {
    return new Logger(module);
  }
}

// Export the Logger class and a default instance
export { Logger };
export default Logger.getLogger('app'); 