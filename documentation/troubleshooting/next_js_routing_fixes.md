# Next.js App Router Implementation and Fixes

## Overview

This document outlines the implementation and troubleshooting of the Next.js App Router in the LMS Spotvogel frontend. The App Router is a newer routing system in Next.js that uses file-system based routing with directory structures.

## Recent Fixes (March 2025)

### Routing Structure Fix

The main issue with the routing system was an incorrect implementation of the App Router structure. We identified and fixed the following issues:

1. **Empty Route Directories**: The `/app/exercise-gallery/` directory existed but was empty, causing 404 errors.
2. **Incorrect File Paths**: Some components were created with tilde paths (`~/lms/frontend/app/...`) which weren't properly recognized by Next.js.
3. **Missing page.tsx Files**: Routes were not properly defined due to missing `page.tsx` files within route directories.

### External Access Configuration

To make the application accessible from outside:

1. **Server Binding**: Updated the server to bind to all interfaces (`0.0.0.0`) instead of just localhost.
2. **Port Configuration**: Standardized on port 3002 for the frontend service.
3. **Firewall Rules**: Added UFW rules to allow external access on port 3002.
4. **Start Script**: Modified `start-frontend.sh` to include proper host and port settings.

## Proper App Router Structure

The Next.js App Router requires specific conventions:

```
app/
├── layout.tsx      # Global layout
├── page.tsx        # Home page (/)
├── favicon.ico     # Favicon
├── globals.css     # Global styles
├── route-name/     # Route: /route-name
│   └── page.tsx    # Required file defining the route
└── nested-route/   # Route: /nested-route
    ├── page.tsx    # Required file for /nested-route
    └── [param]/    # Dynamic route: /nested-route/[param]
        └── page.tsx
```

Key requirements:
- Each route must have a `page.tsx` (or `page.js`) file
- The file must export a default component
- Directory names define the URL path

## Troubleshooting Steps

When routes aren't working properly, follow these steps:

1. **Verify Directory Structure**:
   ```bash
   ls -la ~/lms/frontend/app/your-route-name
   ```

2. **Check for Required Files**:
   - Ensure `page.tsx` exists in the route directory
   - Verify it exports a default component

3. **Restart the Next.js Server**:
   ```bash
   cd ~/lms
   pkill -f "next-server" && pkill -f "next dev" 
   ./start-frontend.sh
   ```

4. **Verify External Access**:
   - Check UFW settings: `sudo ufw status`
   - Verify the server is listening on all interfaces: `sudo netstat -tulpn | grep 3002`
   - Test local access: `curl -I http://localhost:3002/your-route`
   - Test external access: `curl -I http://13.42.249.90:3002/your-route`

## Common Routing Errors

### 404 Not Found

Causes:
- Missing `page.tsx` file in the route directory
- Next.js build cache issues
- Route not included in the build

Solution:
- Add the required `page.tsx` file
- Clear the `.next` directory: `rm -rf ~/lms/frontend/.next`
- Restart the Next.js server

### Route Conflicts

Causes:
- Multiple definitions of the same route
- Conflicting static and dynamic routes

Solution:
- Remove duplicate route definitions
- Follow Next.js priority order for routes

### API Connection Errors

When routes load but API data fails to load:
- Check the API URL in `.env.local`: `NEXT_PUBLIC_API_URL=http://13.42.249.90/api`
- Verify the backend API is running
- Look for CORS issues in the browser console

## Best Practices

1. **Always use the App Router structure**:
   - One `page.tsx` per route directory
   - Default exports for page components

2. **External Access Configuration**:
   ```javascript
   // In next.config.js or start script
   {
     hostname: '0.0.0.0',  // Bind to all interfaces
     port: 3002            // Use consistent port
   }
   ```

3. **Port Management**:
   - Ensure port 3002 is open in the firewall
   - Check for port conflicts before starting services
   - Document port assignments in configuration files 