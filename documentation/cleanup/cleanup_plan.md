# LMS Codebase Cleanup Plan

## 1. Codebase Cleanup Plan

### 1.1 Test Files Consolidation

- Merge redundant test files (`test_database.py`, `test_db.py`, `test_db_layer.py`, `simple_test_db.py`) into a structured test suite
- Organize backend tests into categories (unit, integration, API)
- Remove duplicate test exercises (`test_exercises.py` exists in multiple locations)
- Standardize test naming conventions and practices

### 1.2 Database Script Consolidation

- Combine database setup scripts (`setup_database.py`, `setup_database_fixed.py`, `setup_database_debug.py`)
- Merge database schema files (`database_schema.sql`, `database_schema_fixed.sql`)
- Create a single migration system using Alembic (already present but underutilized)
- Remove redundant table check scripts (`check_tables.py`, `check_all_tables.py`)

### 1.3 Backend Structure Improvement

- Move utility files from root to appropriate subdirectories
- Reorganize models into domain-specific modules
- Standardize backend API structure using consistent route patterns
- Migrate legacy code in root directory to modular structure in `/app`
- Consolidate CRUD operations that are duplicated across files

### 1.4 Logging Standardization

- Implement proper logging configuration (replace ad-hoc log files)
- Move logs to dedicated directory with rotation policy
- Clean up existing log files in git repository

### 1.5 Documentation Reorganization

- Convert RTF documents to Markdown format
- Organize documentation by categories (setup, development, API, troubleshooting)
- Remove outdated documentation files
- Create standardized README files for each major component

### 1.6 Frontend Cleanup

- Remove redundant configuration files (multiple next.config files)
- Organize frontend structure into feature-based directories
- Clean up large log files from version control
- Standardize component naming and organization

### 1.7 Script Management

- Move all scripts to the scripts directory
- Standardize script naming conventions
- Add proper documentation for each script
- Remove redundant check scripts

### 1.8 Dependency Management

- Update and clean requirements.txt files
- Remove unused dependencies
- Standardize dependency versions across environments
- Create separate development and production dependency lists

### 1.9 Configuration Management

- Implement environment-based configuration
- Remove hardcoded paths and credentials
- Create example configuration files
- Standardize configuration access patterns

### 1.10 Git Repository Cleanup

- Remove large files from git history
- Set up proper gitignore for logs and temporary files
- Create .gitattributes for proper line ending handling
- Organize branches and tags for better version management

### Implementation Approach

1. Start with test files consolidation to ensure functionality remains intact
2. Move to database scripts to standardize data access
3. Proceed with backend and frontend structural improvements
4. Complete with documentation and configuration updates

## 2. Port Configuration Analysis

Based on the examination of the codebase, here's an analysis of the port configurations used by various services in the LMS system:

### 2.1 Database Service
- **PostgreSQL** runs on standard port **5432**
- This is configured in multiple database connection scripts
- All database scripts use hardcoded connection parameters instead of environment variables

### 2.2 Backend API Service
- **FastAPI backend** runs on port **8000**
- The `check_services.py` script confirms this port is used for backend API checks
- The FastAPI app is served using Uvicorn as shown in process checks

### 2.3 Frontend Service
- **Next.js frontend** runs on port **3000**
- This is explicitly set in `start-frontend.sh` script with `npm run dev -- -p 3000`
- The port is also checked in `check_services.py`

### 2.4 Web Server Configuration
- **CORS settings** in backend are configured to allow origins:
  - `http://13.42.249.90` (production server without port)
  - `http://13.42.249.90:3000` (production server with frontend port)
- The Nginx configuration file exists but appears to be empty

### 2.5 Environment Configuration Issues
- Frontend has an `.env.local` file with `NEXT_PUBLIC_API_URL=http://13.42.249.90/api`
- No proper backend `.env` file for configuration
- Hard-coded IP addresses and ports throughout the codebase
- No consistent environment variable usage for service configuration

### 2.6 Port Conflict Risk Areas
- Documentation mentions "Port conflicts during development requiring fallback to alternate ports"
- No proper port management or configuration system in place
- Multiple scripts contain hardcoded port values instead of using environment variables
- No explicit port configuration in Nginx to manage routing between services

### 2.7 Port Configuration Recommendations

To address the port configuration issues, we recommend:

1. **Implement consistent environment variable usage** for all service configurations
2. **Create standard .env files** for both development and production environments
3. **Configure Nginx properly** to handle routing between services
4. **Remove hardcoded IP addresses and ports** from the codebase
5. **Document standard ports** for all services in a central configuration guide
6. **Implement port conflict detection** in development startup scripts



-------




Based on my thorough analysis of dependency version standardization, here are my findings:
Current State:
Main requirements.txt uses the >= version specifier for production dependencies
Test dependencies in requirements-test.txt use exact pinning with ==
Development dependencies in requirements-dev.txt also use exact pinning
Proper hierarchy via -r requirements.txt and -r requirements-test.txt references
No Docker configuration found, but deployment scripts use the requirements files
Cross-Environment Standardization Issues:
No environment-specific requirements file (no requirements-prod.txt)
No consistent version specifier strategy across environments
Production using flexible constraints (>=) while test/dev use exact pins (==)
No lock files to ensure exact dependency resolution
No mechanism to ensure test and production environments match exactly
Dependency Resolution Risks:
Production could use newer dependency versions than what was tested
Different developers may get different package versions in development
Deployment may install different versions on different servers
CI/CD environments might use different versions than production
Recommended Standardization Approach:
Create environment-specific requirements files with consistent pinning strategy
Use a dependency lock file system (pip-compile, poetry, pipenv)
Implement a version matrix test strategy for critical dependencies
Consider containerization to ensure environment consistency
Implement a centralized versioning strategy with a single source of truth
Specific Areas for Improvement:
The main requirements file should either use exact pins or constrained ranges consistently
Development environments should mirror production exactly, with additional dev tools
A clear process for upgrading dependencies needs documentation
Version conflicts between environments need proactive detection
This analysis shows that while the current dependency management system has a good structure, it lacks standardization across environments, which could lead to inconsistent behavior between development, testing, and production.