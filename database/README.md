# LMS Database Management

This directory contains the database management tools and structure for the LMS system.

## Directory Structure

- `schema/` - Contains the database schema files
  - `schema.sql` - Consolidated schema file for initial database setup
  
- `migrations/` - Alembic migration scripts
- `create_migration.py` - Helper script for creating Alembic migrations
- `setup.py` - Main database setup and management script
- `db_manager.py` - Database connection and transaction management
- `models.py` - Data models for accessing database records
- `services.py` - Service layer for business logic around database operations
- `utils.py` - Utility functions for database operations

## Database Schema Management

The LMS system uses two complementary approaches to manage the database schema:

1. **Direct SQL (schema.sql)** - Used for initial database setup and reference
2. **Alembic Migrations** - Used for making schema changes in development and production

## Setup and Management Commands

### Initial Setup

To initialize the database with the base schema:

```bash
python database/setup.py --init
```

### Running Migrations

To apply all pending Alembic migrations:

```bash
python database/setup.py --migrate
```

### Verifying Schema

To verify the database schema is correctly set up:

```bash
python database/setup.py --verify
```

### Debugging

For step-by-step initialization of the database (debugging):

```bash
python database/setup.py --debug-init
```

### Listing Tables

To list all tables in the database:

```bash
python database/setup.py --list-tables
python database/setup.py --list-tables --detailed  # For detailed information
```

### Database Reset (Caution!)

To reset the database (will delete all data!):

```bash
python database/setup.py --reset
```

## Creating Migrations

To create new Alembic migrations, use the `create_migration.py` script:

### Interactive Mode

```bash
python database/create_migration.py
```

This will guide you through the process of creating a migration.

### Command-line Mode

For a standard migration:

```bash
python database/create_migration.py --message "Add user roles"
```

For a migration with a template:

```bash
# Create a table
python database/create_migration.py --message "Add roles table" --template table --table-name roles

# Add a column
python database/create_migration.py --message "Add email verified" --template column --table-name users --column-name email_verified --column-type Boolean --nullable
```

## Best Practices

1. **Always use migrations** for schema changes in development and production
2. **Don't edit the schema.sql file** directly after initial setup - use migrations
3. **Include both up and down migrations** to enable rollbacks
4. **Test migrations** thoroughly before applying to production
5. **Back up the database** before applying migrations
6. **Use environment variables** for database connection parameters
7. **Keep migrations small and focused** - one logical change per migration

## Migration Workflow

1. Create a new branch for your feature
2. Make schema changes via a migration
3. Test the migration locally
4. Submit a pull request
5. After approval, apply the migration to production

## Database Connection

The system uses environment variables for database connection. You can override these with:

```bash
export DB_HOST=localhost
export DB_NAME=lms_db
export DB_USER=lms_user
export DB_PASSWORD=lms_password
export DB_PORT=5432
```

These will be used by all database scripts and applications.

## Related Documentation

For more information about the database, refer to:
- [Database Schema](../documentation/architecture/database_schema.md)
- [Database Troubleshooting](../documentation/troubleshooting/database_troubleshooting.md) 