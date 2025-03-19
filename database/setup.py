#!/usr/bin/env python3
"""
Consolidated database setup script for the LMS system.

This script provides multiple methods for setting up and maintaining the database:
1. Direct SQL script execution (for initial setup or reset)
2. Alembic migrations (for schema changes in development and production)
3. Database verification and testing
4. Environment-aware configuration

Usage:
    python setup.py --init         # Initialize the database with schema.sql
    python setup.py --migrate      # Run pending Alembic migrations
    python setup.py --reset        # Reset the database (WARNING: destroys data)
    python setup.py --verify       # Verify the database schema
    python setup.py --debug-init   # Initialize with step-by-step debugging
"""

import argparse
import os
import sys
import time
import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import subprocess
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database_setup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Get the directory of this script
SCRIPT_DIR = Path(__file__).resolve().parent
# Get the root directory of the project
ROOT_DIR = SCRIPT_DIR.parent

# Schema file path
SCHEMA_FILE = SCRIPT_DIR / "schema" / "schema.sql"
# Alembic directory
ALEMBIC_DIR = ROOT_DIR / "backend" / "alembic"

# Database connection parameters from environment or defaults
def get_db_params():
    """Get database connection parameters from environment variables or use defaults."""
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'dbname': os.environ.get('DB_NAME', 'lms_db'),
        'user': os.environ.get('DB_USER', 'lms_user'),
        'password': os.environ.get('DB_PASSWORD', 'lms_password'),
        'port': os.environ.get('DB_PORT', '5432')
    }

def connect_db():
    """Connect to the database and return connection and cursor."""
    try:
        logger.info('Connecting to the PostgreSQL database...')
        params = get_db_params()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        logger.info('Database connection established.')
        return conn, cur
    except Exception as e:
        logger.error(f'Database connection failed: {e}')
        sys.exit(1)

def init_database():
    """Initialize the database with the consolidated schema."""
    conn, cur = connect_db()
    
    try:
        # Check if schema file exists
        if not SCHEMA_FILE.exists():
            logger.error(f"Schema file not found at {SCHEMA_FILE}")
            sys.exit(1)
        
        # Read the SQL file
        with open(SCHEMA_FILE, 'r') as f:
            sql_script = f.read()
        
        # Execute the SQL script
        logger.info('Executing database schema creation script...')
        start_time = time.time()
        
        cur.execute(sql_script)
        
        execution_time = time.time() - start_time
        logger.info(f'Schema creation completed in {execution_time:.2f} seconds.')
        
        # Verify the schema
        verify_schema(cur)
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        logger.info('Database connection closed.')
        
        return True
    except Exception as e:
        logger.error(f'Error initializing database: {e}')
        if conn:
            conn.close()
        return False

def debug_init_database():
    """Initialize the database with step-by-step execution for debugging."""
    conn, cur = connect_db()
    
    try:
        # Check if schema file exists
        if not SCHEMA_FILE.exists():
            logger.error(f"Schema file not found at {SCHEMA_FILE}")
            sys.exit(1)
        
        # Read the SQL file
        with open(SCHEMA_FILE, 'r') as f:
            sql_script = f.read()
        
        # Split the script into individual statements
        # This is a simple approach; it doesn't handle complex SQL perfectly but works for basic debugging
        statements = sql_script.split(';')
        
        logger.info(f'Found {len(statements)} SQL statements to execute.')
        
        for i, statement in enumerate(statements):
            # Skip empty statements
            if statement.strip() == '':
                continue
            
            # Add the semicolon back for execution
            statement = statement.strip() + ';'
            
            logger.info(f'Executing statement {i+1}: {statement[:50]}...')
            
            try:
                start_time = time.time()
                cur.execute(statement)
                execution_time = time.time() - start_time
                logger.info(f'Statement executed successfully in {execution_time:.4f} seconds.')
            except Exception as e:
                logger.error(f'Error executing statement: {e}')
                logger.error(f'Statement was: {statement}')
                if input("Continue with next statement? (y/n): ").lower() != 'y':
                    break
        
        # Verify the schema
        verify_schema(cur)
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        logger.info('Database connection closed.')
        
        return True
    except Exception as e:
        logger.error(f'Error in debug init database: {e}')
        if conn:
            conn.close()
        return False

def reset_database():
    """Reset the database by dropping all tables and reinitializing."""
    logger.warning('RESETTING DATABASE - ALL DATA WILL BE LOST!')
    if input("Are you sure you want to reset the database? This will DELETE ALL DATA. Type 'yes' to confirm: ") != "yes":
        logger.info('Reset cancelled.')
        return False
    
    conn, cur = connect_db()
    
    try:
        # Drop all tables in the correct order to avoid foreign key constraints
        logger.info('Dropping all tables...')
        
        tables_to_drop = [
            "submission_logs", "auth_logs", "error_logs", "query_logs",
            "scores", "submission_answers", "submissions",
            "student_tests", "test_questions", "tests", "students",
            "schema_migrations"
        ]
        
        # Drop view first
        try:
            cur.execute("DROP VIEW IF EXISTS test_completion_status;")
        except Exception as e:
            logger.warning(f'Error dropping view: {e}')
        
        for table in tables_to_drop:
            try:
                cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')
                logger.info(f'Dropped table {table}')
            except Exception as e:
                logger.warning(f'Error dropping table {table}: {e}')
        
        # Close connection
        cur.close()
        conn.close()
        
        # Reinitialize the database
        return init_database()
    except Exception as e:
        logger.error(f'Error resetting database: {e}')
        if conn:
            conn.close()
        return False

def run_alembic_migrations():
    """Run Alembic migrations to bring the database schema up to date."""
    try:
        logger.info('Running Alembic migrations...')
        
        # Change to the backend directory where alembic.ini is located
        os.chdir(ROOT_DIR / "backend")
        
        # Run the Alembic migration command
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info('Alembic migrations completed successfully.')
            logger.info(result.stdout)
            return True
        else:
            logger.error('Error running Alembic migrations.')
            logger.error(f'Exit code: {result.returncode}')
            logger.error(f'Output: {result.stdout}')
            logger.error(f'Error: {result.stderr}')
            return False
    except Exception as e:
        logger.error(f'Error running Alembic migrations: {e}')
        return False

def verify_schema(cur):
    """Verify the database schema is correctly set up."""
    logger.info('Verifying database schema...')
    
    # Get all tables in the database
    cur.execute("""
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname = 'public'
    """)
    
    tables = [row['tablename'] for row in cur.fetchall()]
    
    # Define the expected tables
    expected_tables = [
        "students", "tests", "test_questions", "student_tests",
        "submissions", "submission_answers", "scores",
        "query_logs", "error_logs", "auth_logs", "submission_logs",
        "schema_migrations"
    ]
    
    # Check if all expected tables exist
    missing_tables = [table for table in expected_tables if table not in tables]
    
    if missing_tables:
        logger.error(f'Missing tables: {", ".join(missing_tables)}')
        return False
    
    # Check if view exists
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.views WHERE table_name = 'test_completion_status');")
    view_exists = cur.fetchone()['exists']
    
    if not view_exists:
        logger.warning('The "test_completion_status" view does not exist.')
    
    # Check for latest migration
    cur.execute("SELECT version FROM schema_migrations ORDER BY id DESC LIMIT 1;")
    version = cur.fetchone()
    
    if version:
        logger.info(f'Latest schema version: {version["version"]}')
    else:
        logger.warning('No schema migration records found.')
    
    # Schema verification passed
    logger.info('Schema verification completed successfully.')
    return True

def list_tables(detailed=False):
    """List all tables in the database with optional detailed information."""
    conn, cur = connect_db()
    
    try:
        # Get all tables
        cur.execute("""
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        
        tables = [row['tablename'] for row in cur.fetchall()]
        
        logger.info(f"Found {len(tables)} tables in the database:")
        
        if not detailed:
            # Simple listing
            for table in tables:
                logger.info(f"- {table}")
        else:
            # Detailed listing with record counts
            for table in tables:
                cur.execute(f"SELECT COUNT(*) AS count FROM {table}")
                count = cur.fetchone()['count']
                
                # Get column information
                cur.execute(f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position
                """, (table,))
                
                columns = cur.fetchall()
                
                logger.info(f"\nTable: {table} ({count} records)")
                logger.info("Columns:")
                for col in columns:
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    logger.info(f"  - {col['column_name']} ({col['data_type']}, {nullable})")
        
        # Get all views
        cur.execute("""
            SELECT viewname
            FROM pg_catalog.pg_views
            WHERE schemaname = 'public'
            ORDER BY viewname
        """)
        
        views = [row['viewname'] for row in cur.fetchall()]
        
        logger.info(f"\nFound {len(views)} views in the database:")
        for view in views:
            logger.info(f"- {view}")
        
        # Close connection
        cur.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f'Error listing tables: {e}')
        if conn:
            conn.close()
        return False

def main():
    """Main function for the script."""
    parser = argparse.ArgumentParser(description='LMS Database Setup Tool')
    
    # Define command-line arguments
    parser.add_argument('--init', action='store_true', help='Initialize the database with schema.sql')
    parser.add_argument('--migrate', action='store_true', help='Run pending Alembic migrations')
    parser.add_argument('--reset', action='store_true', help='Reset the database (destroys data)')
    parser.add_argument('--verify', action='store_true', help='Verify the database schema')
    parser.add_argument('--debug-init', action='store_true', help='Initialize with step-by-step debugging')
    parser.add_argument('--list-tables', action='store_true', help='List all tables in the database')
    parser.add_argument('--detailed', action='store_true', help='Show detailed table information')
    
    args = parser.parse_args()
    
    # If no arguments are provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Execute the requested action
    if args.init:
        init_database()
    elif args.debug_init:
        debug_init_database()
    elif args.reset:
        reset_database()
    elif args.migrate:
        run_alembic_migrations()
    elif args.verify:
        conn, cur = connect_db()
        verify_schema(cur)
        cur.close()
        conn.close()
    elif args.list_tables:
        list_tables(detailed=args.detailed)

if __name__ == "__main__":
    main() 