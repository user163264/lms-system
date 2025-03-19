# LMS Backend Dependency Management

This document explains how dependencies are managed in the LMS backend.

## Requirements Files

The backend uses three different requirements files for different environments:

1. **requirements.txt** - Core production dependencies
   - Contains all packages needed to run the application in production
   - Uses version constraints with `>=` to allow compatible updates

2. **requirements-test.txt** - Testing dependencies
   - Includes only test-specific packages
   - References the main requirements.txt file
   - Uses exact version pinning with `==` for reproducible tests

3. **requirements-dev.txt** - Development dependencies
   - Additional tools for development (linters, formatters, etc.)
   - References requirements-test.txt (which includes production dependencies)
   - Uses exact version pinning with `==` for consistent developer environments

## Installation

For production:
```bash
pip install -r requirements.txt
```

For testing:
```bash
pip install -r requirements-test.txt
```

For development:
```bash
pip install -r requirements-dev.txt
```

## Updating Dependencies

When updating dependencies:

1. Update the appropriate file based on the type of dependency
2. Use consistent version constraint formats
3. Maintain the categorization of dependencies
4. Test thoroughly after updating any dependency

## Dependency Categories

Dependencies are organized into these categories:

- Web Framework: FastAPI, Uvicorn
- Database: SQLAlchemy, Alembic, AsyncPG, Psycopg2
- Authentication: python-jose, passlib, python-multipart
- Validation: email-validator, pydantic
- Testing: pytest and related packages
- Development: linting and formatting tools 