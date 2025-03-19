# Database Management Scripts

This directory contains scripts for database management in the LMS system.

## Subdirectories

### setup

Scripts in this directory are used for database setup, initialization, and migration:

- `setup_database.py` - Main script for setting up the database
- `create_migration.py` - Creates migration scripts for database schema changes
- `setup_exercise_tables.py` - Sets up the exercise-related tables

### verification

Scripts in this directory are used for verifying database structure and content:

- `check_database.py` - Checks database schema and connectivity
- `test_database_comprehensive.py` - Runs comprehensive tests on database functionality

## Usage

Most database scripts require database connection parameters. These can be provided as command-line arguments or environment variables.

Example:
```bash
python scripts/database/setup/setup_database.py --host localhost --dbname lms_db --user lms_user --password lms_password
```

or using environment variables:

```bash
export DB_HOST=localhost
export DB_NAME=lms_db
export DB_USER=lms_user
export DB_PASSWORD=lms_password
python scripts/database/setup/setup_database.py
``` 