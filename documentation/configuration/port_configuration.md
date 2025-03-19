# LMS Port Configuration Guide

This document describes the port configuration for the LMS system, including how to customize ports and resolve port conflicts.

## Default Port Configuration

The LMS system uses the following default ports:

| Service | Default Port | Environment Variable | Description |
|---------|--------------|----------------------|-------------|
| PostgreSQL | 5432 | `LMS_DB_PORT` | Database server |
| FastAPI Backend | 8000 | `LMS_API_PORT` | Backend API server |
| Next.js Frontend | 3000 | `LMS_FRONTEND_PORT` | Frontend server |

## Changing Port Configuration

All ports can be customized using environment variables. There are several ways to set these variables:

### 1. Using a .env File

Create a `.env` file in the root or backend directory with your custom port settings:

```bash
# Database port
LMS_DB_PORT=5433

# Backend API port
LMS_API_PORT=8001

# Frontend port
LMS_FRONTEND_PORT=3001
```

### 2. Setting Environment Variables Directly

You can set the environment variables directly before starting the services:

```bash
export LMS_API_PORT=8001
export LMS_FRONTEND_PORT=3001
./scripts/start_backend.sh
./start-frontend.sh
```

### 3. Modifying Service Scripts

Alternatively, you can modify the service startup scripts directly if needed.

## Port Conflict Resolution

The startup scripts for both the backend and frontend include automatic port conflict resolution. If the configured port is already in use:

1. The script will attempt to find the next available port
2. A message will be displayed showing the port change
3. The service will start on the new port
4. The environment variable will be updated for the current session

Example output when a port conflict is detected:
```
Port 8000 is in use, trying the next one
Original port 8000 is in use, using port 8001 instead
Starting LMS backend API service on 0.0.0.0:8001
```

## CORS Configuration

When changing port configurations, especially for the frontend, CORS settings need to be updated accordingly. This happens automatically in the application because:

1. CORS origins are constructed using the `FRONTEND_PORT` setting
2. The application reads environment variables at startup

If you're experiencing CORS issues after changing ports, make sure both services are restarted to pick up the new configuration.

## Nginx Configuration

For production deployments, it's recommended to use Nginx as a reverse proxy. The provided Nginx configuration at `nginx/lms.conf` routes traffic to the appropriate services:

- `/api/*` → Backend API (port 8000)
- `/*` → Frontend (port 3000)

If you change the default ports, update the Nginx configuration accordingly. The comments in the configuration file explain how to use environment variables with Nginx if needed.

## Testing Port Configuration

You can verify your port configuration is working correctly using the service check script:

```bash
python scripts/services/check/check_services.py
```

This script checks if all services are running on their configured ports and reports any issues.

## Troubleshooting

If you encounter port-related issues:

1. **Check for running processes**: Use `lsof -i :port` to check if a port is in use
2. **Verify environment variables**: Run `echo $LMS_API_PORT` to confirm they're set correctly
3. **Check service logs**: Look for startup errors in the service logs
4. **Restart services**: Sometimes restarting services can resolve port binding issues

For persistent issues, consider setting fixed, non-standard ports in your configuration. 