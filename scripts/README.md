# LMS Script Repository

This directory contains all scripts for managing and maintaining the Learning Management System. The scripts are organized by function to make them easier to find and maintain.

## Directory Structure

- **database/** - Database management scripts
  - **setup/** - Scripts for database initialization and migrations
  - **verification/** - Scripts for checking database integrity and schema

- **services/** - Service management scripts
  - **check/** - Scripts to verify service status and health
  - **control/** - Scripts to start, stop, and restart services

- **deployment/** - Scripts related to deploying the application

- **models/** - Scripts for model and schema management

- **tests/** - Test runners and validation scripts

- **import/** - Data import and export scripts

- **frontend/** - Frontend management scripts

- **utils/** - Utility scripts used by other scripts

## Naming Convention

All scripts follow the standard naming convention:
- Use snake_case (underscores between words)
- Begin with a verb indicating the action (setup_, check_, update_, etc.)
- Followed by the domain/subject (database, services, etc.)
- Include specificity if needed (schema, exercises, etc.)
- Use appropriate file extension (.py for Python, .sh for shell scripts)

## Usage

Each script includes documentation on how to use it. Generally, scripts can be run as:

Python scripts:
```bash
python scripts/[directory]/[script_name].py [arguments]
```

Shell scripts:
```bash
bash scripts/[directory]/[script_name].sh [arguments]
```
or
```bash
./scripts/[directory]/[script_name].sh [arguments]
```

## Common Workflows

### Database Setup and Verification
1. Initialize database: `scripts/database/setup/setup_database.py`
2. Verify database: `scripts/database/verification/check_database.py`

### Service Management
1. Check services: `scripts/services/check/check_services.py`
2. Start services: `scripts/services/control/start_backend.sh` and `scripts/services/control/start_frontend.sh`

### Deployment
1. Deploy application: `scripts/deployment/deploy.sh`

## Maintenance

When adding new scripts:
1. Place them in the appropriate directory
2. Follow the naming convention
3. Include proper documentation in the script header
4. Update the relevant README.md file 