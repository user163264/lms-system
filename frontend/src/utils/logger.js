/**
 * Client-side logging module for the LMS frontend.
 * 
 * This module provides logging functions that send logs to the backend API
 * while also logging to the console for development.
 */

const API_URL = process.env.REACT_APP_API_URL || '/api';
const LOG_ENDPOINT = `${API_URL}/logs`;
const LOG_TO_CONSOLE = process.env.NODE_ENV === 'development';
const SEND_TO_SERVER = process.env.REACT_APP_ENABLE_REMOTE_LOGGING !== 'false';

// Log levels
const LOG_LEVELS = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARNING: 'WARNING',
  ERROR: 'ERROR',
  CRITICAL: 'CRITICAL'
};

/**
 * Get browser information for diagnostics
 * @returns {Object} Object containing browser information
 */
const getBrowserInfo = () => {
  return {
    userAgent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    screenSize: {
      width: window.screen.width,
      height: window.screen.height
    },
    viewportSize: {
      width: window.innerWidth,
      height: window.innerHeight
    }
  };
};

/**
 * Send a log entry to the backend server
 * @param {Object} logEntry Log entry to send
 */
const sendLogToServer = async (logEntry) => {
  if (!SEND_TO_SERVER) return;
  
  try {
    const response = await fetch(LOG_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
      },
      body: JSON.stringify(logEntry)
    });
    
    if (!response.ok) {
      // Log failure to console but don't create an infinite loop by calling logger again
      console.error(`Failed to send log to server: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    // Log failure to console but don't create an infinite loop
    console.error(`Error sending log to server: ${error.message}`);
  }
};

/**
 * Log a message with the specified level
 * @param {string} level Log level
 * @param {string} message Log message
 * @param {string} module Source module name
 * @param {Object} extra Additional data to include in the log
 */
const log = (level, message, module = 'app', extra = {}) => {
  const timestamp = new Date().toISOString();
  
  // Create log entry
  const logEntry = {
    timestamp,
    level,
    module,
    message,
    browser: getBrowserInfo(),
    ...extra
  };
  
  // Log to console in development
  if (LOG_TO_CONSOLE) {
    const consoleMethod = level === LOG_LEVELS.DEBUG ? 'debug'
      : level === LOG_LEVELS.INFO ? 'info'
      : level === LOG_LEVELS.WARNING ? 'warn'
      : 'error';
      
    console[consoleMethod](`[${timestamp}] [${level}] [${module}] ${message}`, extra);
  }
  
  // Send to server
  sendLogToServer(logEntry);
};

// Export public API
const logger = {
  debug: (message, module, extra) => log(LOG_LEVELS.DEBUG, message, module, extra),
  info: (message, module, extra) => log(LOG_LEVELS.INFO, message, module, extra),
  warning: (message, module, extra) => log(LOG_LEVELS.WARNING, message, module, extra),
  warn: (message, module, extra) => log(LOG_LEVELS.WARNING, message, module, extra), // Alias for warning
  error: (message, module, extra) => log(LOG_LEVELS.ERROR, message, module, extra),
  critical: (message, module, extra) => log(LOG_LEVELS.CRITICAL, message, module, extra),
  
  // Utility method to create a logger for a specific module
  getLogger: (moduleName) => ({
    debug: (message, extra) => log(LOG_LEVELS.DEBUG, message, moduleName, extra),
    info: (message, extra) => log(LOG_LEVELS.INFO, message, moduleName, extra),
    warning: (message, extra) => log(LOG_LEVELS.WARNING, message, moduleName, extra),
    warn: (message, extra) => log(LOG_LEVELS.WARNING, message, moduleName, extra),
    error: (message, extra) => log(LOG_LEVELS.ERROR, message, moduleName, extra),
    critical: (message, extra) => log(LOG_LEVELS.CRITICAL, message, moduleName, extra),
  })
};

export default logger; 