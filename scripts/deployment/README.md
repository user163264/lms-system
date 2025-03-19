# Deployment Scripts

This directory contains scripts for deploying the LMS system.

## Scripts

- `deploy.sh` - Main script for deploying the entire LMS application

## Usage

### Deploying the Application

To deploy the LMS application:

```bash
./scripts/deployment/deploy.sh [environment]
```

Where `[environment]` can be:
- `dev` for development environment
- `staging` for staging environment
- `prod` for production environment

If no environment is specified, it defaults to `dev`.

## Pre-requisites

Before running the deployment script, ensure:

1. You have appropriate permissions for the target environment
2. The database connection parameters are properly configured
3. All required services (database, etc.) are running
4. You have committed any local changes

## Post-deployment

After deployment, you should:

1. Run health checks to verify the deployment
2. Check logs for any errors
3. Run basic functionality tests 