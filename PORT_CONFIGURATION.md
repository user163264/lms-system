# LMS Port Configuration

This document defines the standard port configuration for the LMS application.

## Standard Ports

| Service | Port | Environment Variable | Description |
|---------|------|---------------------|-------------|
| Frontend (Next.js) | 3002 | `LMS_FRONTEND_PORT` | The Next.js frontend server |
| Backend (FastAPI) | 8000 | `LMS_BACKEND_PORT` | The FastAPI backend server |
| Database (PostgreSQL) | 5432 | `LMS_DB_PORT` | PostgreSQL database server |

## Port Usage Guidelines

1. **Development Environment:**
   - Frontend should consistently use port 3002
   - API calls from frontend to backend should target port 3002/api
   - Backend should use port 8000

2. **Production Environment:**
   - Use Nginx to proxy requests to the appropriate services
   - Configure Nginx to route /api/* to backend on port 8000
   - Configure Nginx to route all other traffic to frontend on port 3002

## Configuration Files That Reference Ports

The following files contain port configurations and should be kept in sync:

- `frontend/package.json` - Dev script uses port 3002
- `restart-frontend.sh` - Uses port 3002 for both API URL and server
- `start-frontend.sh` - Default port is 3002
- `frontend/app/services/api.ts` - API URL defaults to port 3002
- `nginx/lms.conf` - Should be updated to use port 3002 for frontend

## How to Change Ports

If you need to change the standard ports:

1. Update this document
2. Update all referenced configuration files
3. Update any documentation that references specific port numbers
4. Update environment variables in deployment configurations 