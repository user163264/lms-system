#!/usr/bin/env python3
"""
Script Name: check_database.py
Description: Comprehensive database verification script for the LMS system

Usage:
    python scripts/database/verification/check_database.py [options]
    
Options:
    --connection-only    Only check database connection
    --schema             Check database schema
    --tables             Check tables and their structures
    --quiet              Suppress output except for errors
    --verbose            Show detailed information
    
Dependencies:
    - psycopg2
    
Output:
    Database verification results
    
Author: LMS Team
Last Modified: 2025-03-19
"""

import argparse
import os
import sys
import json
from pathlib import Path
import psycopg2
import psycopg2.extras

# Add the project root to sys.path to enable imports
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

# Try to import database connection details from the project
try:
    from database.db_manager import get_db_params
except ImportError:
    # Fall back to default parameters if import fails
    def get_db_params():
        return {
            "host": "localhost",
            "dbname": "lms_db",
            "user": "lms_user", 
            "password": "lms_password"
        }

# Expected table structure for verification
EXPECTED_TABLES = {
    "users": [
        "id", "username", "email", "password_hash", "role", "created_at", "updated_at"
    ],
    "courses": [
        "id", "title", "description", "created_at", "updated_at"
    ],
    "lessons": [
        "id", "course_id", "title", "content", "sequence", "created_at", "updated_at"
    ],
    "exercises": [
        "id", "lesson_id", "exercise_type", "question", "answers", "options", "created_at", "updated_at"
    ],
    "submissions": [
        "id", "user_id", "exercise_id", "answer", "is_correct", "score", "submitted_at"
    ]
}

# Expected exercise types
EXERCISE_TYPES = [
    "multiple_choice",
    "true_false",
    "short_answer",
    "long_answer", 
    "fill_blanks",
    "matching",
    "cloze_test",
    "image_labeling",
    "audio_transcription"
]

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Check LMS database")
    parser.add_argument("--connection-only", action="store_true", help="Only check database connection")
    parser.add_argument("--schema", action="store_true", help="Check database schema")
    parser.add_argument("--tables", action="store_true", help="Check tables and their structures")
    parser.add_argument("--quiet", action="store_true", help="Suppress output except for errors")
    parser.add_argument("--verbose", action="store_true", help="Show detailed information")
    return parser.parse_args()

def print_message(message, level="info", quiet=False):
    """Print a message with the appropriate formatting."""
    if quiet and level == "info":
        return
    
    prefixes = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    prefix = prefixes.get(level, "")
    print(f"{prefix} {message}")

def check_connection(db_params, quiet=False, verbose=False):
    """Check if the database connection is working."""
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print_message(f"Successfully connected to the database", "success", quiet)
        if verbose:
            print_message(f"PostgreSQL version: {version}", "info", quiet)
        return True
    except Exception as e:
        print_message(f"Failed to connect to the database: {e}", "error", quiet)
        return False

def check_schema(db_params, quiet=False, verbose=False):
    """Check the database schema."""
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Check if the expected tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = [table for table in EXPECTED_TABLES.keys() if table not in tables]
        
        if missing_tables:
            print_message(f"Missing tables: {', '.join(missing_tables)}", "error", quiet)
        else:
            print_message("All expected tables exist", "success", quiet)
        
        if verbose:
            print_message(f"Found tables: {', '.join(tables)}", "info", quiet)
        
        cursor.close()
        conn.close()
        return not missing_tables
    except Exception as e:
        print_message(f"Error checking schema: {e}", "error", quiet)
        return False

def check_table_structure(db_params, quiet=False, verbose=False):
    """Check the structure of database tables."""
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        all_good = True
        
        for table_name, expected_columns in EXPECTED_TABLES.items():
            if verbose:
                print_message(f"Checking table: {table_name}", "info", quiet)
            
            # Check if the table exists
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """, (table_name,))
            if not cursor.fetchone()[0]:
                print_message(f"Table {table_name} does not exist", "error", quiet)
                all_good = False
                continue
            
            # Check table columns
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = %s
            """, (table_name,))
            columns = [row[0] for row in cursor.fetchall()]
            
            missing_columns = [col for col in expected_columns if col not in columns]
            
            if missing_columns:
                print_message(f"Table {table_name} is missing columns: {', '.join(missing_columns)}", "error", quiet)
                all_good = False
            elif verbose:
                print_message(f"Table {table_name} has all expected columns", "success", quiet)
        
        cursor.close()
        conn.close()
        
        if all_good:
            print_message("All tables have the expected structure", "success", quiet)
        
        return all_good
    except Exception as e:
        print_message(f"Error checking table structure: {e}", "error", quiet)
        return False

def check_exercise_types(db_params, quiet=False, verbose=False):
    """Check exercise types in the database."""
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Check if exercises table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'exercises'
            )
        """)
        if not cursor.fetchone()[0]:
            print_message("Exercises table does not exist, skipping exercise types check", "warning", quiet)
            cursor.close()
            conn.close()
            return True
        
        # Get unique exercise types from the database
        cursor.execute("""
            SELECT DISTINCT exercise_type 
            FROM exercises
        """)
        db_exercise_types = [row[0] for row in cursor.fetchall()]
        
        unknown_types = [t for t in db_exercise_types if t not in EXERCISE_TYPES]
        
        if unknown_types:
            print_message(f"Unknown exercise types found: {', '.join(unknown_types)}", "warning", quiet)
        elif db_exercise_types:
            print_message("All exercise types are valid", "success", quiet)
        else:
            print_message("No exercise types found in the database", "info", quiet)
        
        if verbose:
            print_message(f"Exercise types in database: {', '.join(db_exercise_types) if db_exercise_types else 'None'}", "info", quiet)
            print_message(f"Expected exercise types: {', '.join(EXERCISE_TYPES)}", "info", quiet)
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print_message(f"Error checking exercise types: {e}", "error", quiet)
        return False

def main():
    """Main function."""
    args = parse_args()
    
    # If no specific checks are requested, do all checks
    run_all = not (args.connection_only or args.schema or args.tables)
    
    # Get database connection parameters
    db_params = get_db_params()
    
    # Track success status
    success = True
    
    # Always check connection
    connection_ok = check_connection(db_params, args.quiet, args.verbose)
    success = success and connection_ok
    
    # If connection failed or only checking connection, stop here
    if not connection_ok or args.connection_only:
        return 0 if success else 1
    
    # Check schema if requested or running all checks
    if args.schema or run_all:
        schema_ok = check_schema(db_params, args.quiet, args.verbose)
        success = success and schema_ok
    
    # Check table structure if requested or running all checks
    if args.tables or run_all:
        tables_ok = check_table_structure(db_params, args.quiet, args.verbose)
        success = success and tables_ok
    
    # Check exercise types if checking tables or running all checks
    if args.tables or run_all:
        exercise_types_ok = check_exercise_types(db_params, args.quiet, args.verbose)
        success = success and exercise_types_ok
    
    # Final status message
    if success:
        print_message("Database check completed successfully", "success", args.quiet)
    else:
        print_message("Database check completed with issues", "error", args.quiet)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 