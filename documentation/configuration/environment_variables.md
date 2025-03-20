# Environment Variables

This document outlines all environment variables used in the LMS Spotvogel system.

## Overview

Environment variables are used to configure various aspects of the LMS system without modifying code. They should be defined in the `.env` file in the project root directory.

## Server Information

- `LMS_SERVER_IP`: The server's public IP address (13.42.249.90)
- `LMS_ENVIRONMENT`: The environment name (development, staging, production)

## Port Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LMS_FRONTEND_PORT` | 3002 | The port for the Next.js frontend |
| `LMS_FRONTEND_HOST` | 0.0.0.0 | The host address for the frontend |
| `LMS_BACKEND_PORT` | 8000 | The port for the FastAPI backend |
| `LMS_BACKEND_HOST` | 0.0.0.0 | The host address for the backend |
| `LMS_DB_PORT` | 5432 | The port for the PostgreSQL database |
| `LMS_DB_HOST` | localhost | The host address for the database |

## Database Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LMS_DB_NAME` | lms | The name of the database |
| `LMS_DB_USER` | postgres | The database user |
| `LMS_DB_PASSWORD` | | The database password (no default) |
| `LMS_DB_MAX_CONNECTIONS` | 10 | Maximum database connections |

## API Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LMS_API_PREFIX` | /api | The prefix for all API routes |
| `LMS_API_TIMEOUT` | 60 | Timeout for API requests in seconds |
| `LMS_CORS_ORIGINS` | http://localhost:3002 | Allowed CORS origins (comma-separated) |

## Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `LMS_JWT_SECRET` | | The secret key for JWT tokens (no default) |
| `LMS_JWT_ALGORITHM` | HS256 | The algorithm for JWT tokens |
| `LMS_JWT_EXPIRATION` | 86400 | JWT token expiration in seconds (24 hours) |

## Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `LMS_LOG_LEVEL` | INFO | The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `LMS_LOG_FORMAT` | json | The log format (text, json) |
| `LMS_LOG_DIR` | /home/ubuntu/lms/logs | Directory for log files |

## Frontend Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | http://localhost:3002/api | The URL for API requests from the frontend |
| `NEXT_PUBLIC_USE_MOCK_DATA` | false | Whether to use mock data in the frontend |

## Using Environment Variables

### In Scripts

Bash scripts should load environment variables from the `.env` file:

```bash
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi
```

### In Python

Python code should use the `os` module or a dedicated configuration module:

```python
import os

# Get variable with default
port = os.getenv("LMS_BACKEND_PORT", "8000")
```

### In Next.js (Frontend)

Frontend code should use variables with the `NEXT_PUBLIC_` prefix:

```javascript
// This is accessible in the browser
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

## Example .env File

```
# Server Information
LMS_SERVER_IP=13.42.249.90
LMS_ENVIRONMENT=production

# Port Configuration
LMS_FRONTEND_PORT=3002
LMS_BACKEND_PORT=8000
LMS_DB_PORT=5432

# Database Configuration
LMS_DB_NAME=lms
LMS_DB_USER=postgres
LMS_DB_PASSWORD=secure_password_here

# API Configuration
LMS_CORS_ORIGINS=http://13.42.249.90,http://localhost:3002

# Authentication
LMS_JWT_SECRET=very_secure_and_random_secret_key_here

# Logging
LMS_LOG_LEVEL=INFO
``` 