# LMS Logging System Guide

This guide explains how to use the standardized logging system implemented in the LMS application, covering both backend and frontend logging.

## Backend Logging

### Basic Usage

Import the logger in your Python module:

```python
from app.config import get_logger

# Create a logger specific to your module
logger = get_logger("my_module")

# Log at different levels
logger.debug("Detailed information for debugging")
logger.info("General information about system operation")
logger.warning("Warning about potential issues")
logger.error("Error that doesn't prevent the application from running")
logger.critical("Critical error that may prevent the application from running")
```

### Adding Context Information

You can add additional context to log entries:

```python
# Add extra data to a log message
logger.info("User logged in", extra={"user_id": user.id, "username": user.username})
```

### Specialized Loggers

For specific types of logging, use the specialized loggers:

```python
from app.config import get_request_logger, get_error_logger, get_db_logger

# For HTTP requests
request_logger = get_request_logger()

# For errors
error_logger = get_error_logger()

# For database operations
db_logger = get_db_logger()
```

### Configuration

The logging system can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `LMS_LOG_LEVEL` | Minimum log level to record | `info` |
| `LMS_CONSOLE_LOGGING` | Enable logging to console | `true` |
| `LMS_FILE_LOGGING` | Enable logging to files | `true` |
| `LMS_MAX_LOG_SIZE` | Maximum size of log files | `10485760` (10 MB) |
| `LMS_MAX_LOG_BACKUPS` | Maximum number of backup log files | `5` |
| `LMS_LOG_ROTATION` | Rotation type (`size` or `time`) | `size` |
| `LMS_STRUCTURED_LOGGING` | Enable structured logging | `false` |
| `LMS_STRUCTURED_LOG_FORMAT` | Format for structured logs (`json` or `text`) | `json` |

### Log File Locations

All logs are stored in the `logs/` directory at the root of the project:

- `lms.log`: Root logger
- `lms_api_requests.log`: HTTP request logs
- `lms_error.log`: Error logs
- `lms_database.log`: Database operation logs
- Module-specific logs are named after the module (e.g., `lms_my_module.log`)

## Frontend Logging

### Basic Usage

Import the logger in your JavaScript file:

```javascript
import logger from '../utils/logger';

// Log at different levels
logger.debug('Detailed information for debugging');
logger.info('General information about system operation');
logger.warning('Warning about potential issues');
logger.error('Error that prevents normal operation');
logger.critical('Critical error that requires immediate attention');
```

### Module-Specific Logging

Create a logger for a specific module:

```javascript
import logger from '../utils/logger';

const myLogger = logger.getLogger('MyComponent');

myLogger.info('Component initialized');
```

### Adding Context Information

You can add additional context to log entries:

```javascript
logger.info('User action completed', 'UserActions', {
  userId: user.id,
  action: 'download',
  itemId: item.id
});
```

### Error Boundary

Use the ErrorBoundary component to catch and log React component errors:

```jsx
import ErrorBoundary from '../components/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <YourComponent />
    </ErrorBoundary>
  );
}
```

### Configuration

Frontend logging can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment (`development` enables console logging) | — |
| `REACT_APP_API_URL` | API URL | `/api` |
| `REACT_APP_ENABLE_REMOTE_LOGGING` | Send logs to backend | `true` |

## Log Aggregation in Production

For production environments, we use the ELK Stack (Elasticsearch, Logstash, Kibana) for log aggregation.

See the [Log Aggregation Solution](./log_aggregation.md) document for details on setting up and using the ELK Stack for production logging.

## Best Practices

1. **Use appropriate log levels**:
   - `DEBUG`: Detailed information, useful for troubleshooting
   - `INFO`: Confirmation that things are working as expected
   - `WARNING`: Indication that something unexpected happened, but the application can still work
   - `ERROR`: Due to a more serious problem, the application couldn't perform a function
   - `CRITICAL`: Very serious error that might prevent the program from continuing to run

2. **Be descriptive but concise**: Log messages should be clear about what happened but not excessively long.

3. **Include context**: Add relevant context information using the `extra` parameter.

4. **Avoid sensitive information**: Never log passwords, tokens, or personal information.

5. **Structure logs when possible**: Use structured logging to make logs easier to parse and analyze.

6. **Log actions, not state**: Focus on logging events and actions rather than system state.

7. **Use specialized loggers** for specific types of events (requests, errors, etc.).

## Troubleshooting

If logs are not appearing:

1. Check that the appropriate log level is set (`LMS_LOG_LEVEL` environment variable)
2. Verify that the log directory exists and is writable
3. Check that the logger is being properly initialized
4. For frontend logs, ensure that `REACT_APP_ENABLE_REMOTE_LOGGING` is not set to `false` 