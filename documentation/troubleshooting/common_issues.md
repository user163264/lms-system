# Common Issues and Solutions

This document provides solutions for common issues encountered during development and deployment of the LMS system.

## Backend Issues

### Database Connection Errors

**Issue**: Unable to connect to the database with errors like "Connection refused" or "Authentication failed".

**Solutions**:
1. Check that PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify database credentials in your `.env` file
3. Ensure the database exists: `psql -U postgres -c "\l"`
4. Check PostgreSQL logs: `sudo tail -n 50 /var/log/postgresql/postgresql-15-main.log`
5. Test connection manually: `psql -U yourusername -d yourdatabasename -h localhost`

### Alembic Migration Errors

**Issue**: Alembic migrations fail with errors like "Target database is not up to date" or "Can't locate revision".

**Solutions**:
1. Check current migration state: `python database/setup.py --check-migrations`
2. For merge conflicts, create a merge migration: `alembic merge heads -m "merge multiple heads"`
3. For specific revision issues, use `alembic stamp <revision>` to mark a specific migration as complete
4. For database sync issues: `alembic current` to check current state

### FastAPI Startup Errors

**Issue**: FastAPI fails to start with import errors or configuration issues.

**Solutions**:
1. Check for Python dependency issues: `pip install -r requirements.txt --force-reinstall`
2. Verify all required environment variables are set
3. Check log files for specific errors: `tail -n 100 logs/error.log`
4. Restart the ASGI server: `systemctl restart uvicorn`

## Frontend Issues

### NPM Installation Errors

**Issue**: NPM dependencies fail to install with errors like "Failed to compile" or "Module not found".

**Solutions**:
1. Delete `node_modules` folder and reinstall: `rm -rf node_modules && npm install`
2. Clear NPM cache: `npm cache clean --force`
3. Check for Node.js version compatibility: `node -v` (should be v18+)
4. Check for conflicting dependencies in `package.json`

### Hydration Errors

**Issue**: Next.js hydration errors in the console, with warnings about content mismatch between server and client.

**Solutions**:
1. See the [Hydration Error Solutions](./hydration_error_solution.md) document for detailed fixes
2. Wrap dynamic content in a client-side component
3. Use the `useEffect` hook for browser-only code
4. Add `suppressHydrationWarning` to elements with dynamic content

### API Connection Issues

**Issue**: Frontend fails to connect to the backend API.

**Solutions**:
1. Check that the API URL is correctly set in `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
2. Verify CORS settings in the backend are configured to allow your frontend origin
3. Check browser console for specific error messages
4. Ensure the backend server is running and accessible

## Deployment Issues

### Production Build Failures

**Issue**: Production build fails with errors during `npm run build`.

**Solutions**:
1. Check for TypeScript errors: `npm run type-check`
2. Verify all imports are working correctly
3. Run development server first to catch runtime errors: `npm run dev`
4. Increase Node.js memory limit: `NODE_OPTIONS=--max_old_space_size=4096 npm run build`

### Nginx Configuration Issues

**Issue**: Web server returns 502 Bad Gateway or other server errors.

**Solutions**:
1. Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`
2. Verify Nginx configuration: `sudo nginx -t`
3. Ensure the upstream service (Uvicorn/FastAPI) is running
4. Check firewall settings: `sudo ufw status`
5. Restart Nginx: `sudo systemctl restart nginx`

### SSL Certificate Issues

**Issue**: SSL certificates are invalid or expired.

**Solutions**:
1. Check certificate expiration: `openssl x509 -in /etc/ssl/certs/your-cert.crt -text -noout | grep "Not After"`
2. Renew Let's Encrypt certificates: `certbot renew`
3. Verify certificate paths in Nginx configuration
4. Restart Nginx after certificate updates: `sudo systemctl restart nginx`

## Environment Issues

### Environment Variable Problems

**Issue**: Application can't access environment variables or has incorrect values.

**Solutions**:
1. Check that `.env` file exists in the correct location
2. Verify variable names match what the application expects
3. Restart the application after changing environment variables
4. For Next.js, remember that environment variables must be prefixed with `NEXT_PUBLIC_` to be accessible in the browser

### Port Conflicts

**Issue**: Services fail to start because ports are already in use.

**Solutions**:
1. Check what's using a specific port: `sudo lsof -i :8000`
2. Kill the process using the port: `sudo kill -9 <PID>`
3. Change the port in the configuration if needed
4. For testing, use a different port: `uvicorn app.main:app --port 8001`

## Testing Issues

### Test Failures

**Issue**: Unit or integration tests fail unexpectedly.

**Solutions**:
1. Run tests with verbose output: `pytest -v tests/`
2. Check test database configuration
3. Verify test fixtures are working correctly
4. Isolate failing tests and run them individually: `pytest tests/test_file.py::test_function`

### Authentication Issues in Tests

**Issue**: Tests fail with authentication errors.

**Solutions**:
1. Verify test JWT token generation
2. Check that authentication bypass is correctly configured for tests
3. Ensure test user accounts exist in the test database
4. Review authentication middleware behavior in test environment

## Monitoring Issues

### Missing Logs

**Issue**: Application events are not being logged as expected.

**Solutions**:
1. Check log configuration in `config/logging_config.py`
2. Verify log directory exists and has proper permissions
3. Check log rotation settings
4. Set more verbose log level for debugging: `export LMS_LOG_LEVEL=debug`

### Performance Problems

**Issue**: Application responds slowly or times out.

**Solutions**:
1. Check database query performance
2. Look for blocking operations in asynchronous code
3. Review server resource usage: `htop`
4. Check for memory leaks or high CPU usage
5. Implement performance monitoring with tools like Prometheus and Grafana 