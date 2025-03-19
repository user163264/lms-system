#!/usr/bin/env python3
"""
Script Name: data_purge.py
Description: Utility for purging sensitive data from the LMS database

Usage:
    python scripts/database/admin/data_purge.py [options]
    
Options:
    --student-personal-data  Purge student personal information
    --grades                 Purge grade data 
    --all                    Purge all sensitive data
    --backup                 Create a backup before purging
    --dry-run                Show what would be purged without making changes
    --confirm                Skip confirmation prompt
    
Dependencies:
    - psycopg2
    
Output:
    Status messages about purged data
    
Author: LMS Team
Last Modified: 2025-03-19
"""

import argparse
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import psycopg2
import psycopg2.extras
import getpass

# Add the project root to sys.path to enable imports
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

# Try to import relevant modules
try:
    from database.db_manager import get_db_params
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure you have all required packages installed.")
    sys.exit(1)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Purge sensitive data from the LMS database")
    
    # Purge options
    group = parser.add_argument_group("Purge options")
    group.add_argument("--student-personal-data", action="store_true", help="Purge student personal information")
    group.add_argument("--grades", action="store_true", help="Purge grade data")
    group.add_argument("--all", action="store_true", help="Purge all sensitive data")
    
    # Additional options
    parser.add_argument("--backup", action="store_true", help="Create a backup before purging")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be purged without making changes")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation prompt")
    
    return parser.parse_args()

def create_backup():
    """Create a database backup."""
    print("Creating database backup...")
    
    try:
        # Get database connection parameters
        db_params = get_db_params()
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"lms_backup_{timestamp}.sql"
        backup_path = project_root / "backups" / backup_file
        
        # Create backups directory if it doesn't exist
        backup_dir = project_root / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        # Construct pg_dump command
        cmd = [
            "pg_dump",
            f"--host={db_params['host']}",
            f"--port={db_params['port']}",
            f"--username={db_params['user']}",
            f"--dbname={db_params['dbname']}",
            f"--file={backup_path}"
        ]
        
        # Execute pg_dump command
        import subprocess
        env = os.environ.copy()
        env["PGPASSWORD"] = db_params["password"]
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error creating backup: {result.stderr}")
            return False
        
        print(f"Backup created: {backup_path}")
        return True
    
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def confirm_purge(dry_run=False):
    """Confirm with the user before proceeding with purge."""
    if dry_run:
        print("DRY RUN MODE: No data will be deleted")
        return True
    
    print("WARNING: This operation will permanently delete data from the database.")
    print("It is recommended to create a backup before proceeding.")
    
    while True:
        confirm = input("Are you sure you want to proceed? (yes/no): ").lower()
        if confirm in ["yes", "y"]:
            # For sensitive operations, require admin password
            admin_password = getpass.getpass("Enter admin password to confirm: ")
            # This is a simple check - in a real system, this would validate against stored credentials
            if admin_password == "admin":  # In a real system, NEVER hardcode passwords
                return True
            else:
                print("Invalid admin password")
                return False
        elif confirm in ["no", "n"]:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def purge_student_personal_data(conn, dry_run=False):
    """Purge student personal information."""
    print("Purging student personal information...")
    
    try:
        cursor = conn.cursor()
        
        # Define the update queries to anonymize personal data
        queries = [
            """
            UPDATE student
            SET 
                email = CONCAT('student', id, '@example.com'),
                phone = NULL,
                address = NULL,
                date_of_birth = NULL,
                emergency_contact = NULL
            """,
            
            """
            UPDATE user_account
            SET
                email = CONCAT('user', id, '@example.com'),
                recovery_email = NULL,
                phone = NULL
            WHERE user_type = 'student'
            """
        ]
        
        # Execute or print the queries
        for query in queries:
            if dry_run:
                print(f"Would execute: {query}")
            else:
                cursor.execute(query)
                print(f"Affected rows: {cursor.rowcount}")
        
        if not dry_run:
            conn.commit()
            print("Student personal data purged successfully")
        
        cursor.close()
        return True
    
    except Exception as e:
        conn.rollback()
        print(f"Error purging student personal data: {e}")
        return False

def purge_grade_data(conn, dry_run=False):
    """Purge grade data."""
    print("Purging grade data...")
    
    try:
        cursor = conn.cursor()
        
        # Define the update queries to remove grade data
        queries = [
            """
            UPDATE student_assignment
            SET 
                score = NULL,
                feedback = NULL
            """,
            
            """
            UPDATE grade
            SET
                value = NULL,
                notes = NULL
            """
        ]
        
        # Execute or print the queries
        for query in queries:
            if dry_run:
                print(f"Would execute: {query}")
            else:
                cursor.execute(query)
                print(f"Affected rows: {cursor.rowcount}")
        
        if not dry_run:
            conn.commit()
            print("Grade data purged successfully")
        
        cursor.close()
        return True
    
    except Exception as e:
        conn.rollback()
        print(f"Error purging grade data: {e}")
        return False

def main():
    """Main function."""
    args = parse_args()
    
    # Check if any purge option was selected
    if not (args.student_personal_data or args.grades or args.all):
        print("No purge option selected. Use --student-personal-data, --grades, or --all")
        return 1
    
    # Create backup if requested
    if args.backup:
        backup_success = create_backup()
        if not backup_success and not args.dry_run:
            print("Backup failed. Aborting operation for safety.")
            return 1
    
    # Get confirmation unless --confirm flag is set
    if not args.confirm and not confirm_purge(args.dry_run):
        print("Operation cancelled by user")
        return 0
    
    try:
        # Get database connection parameters
        db_params = get_db_params()
        
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        
        # Track overall success
        success = True
        
        # Purge student personal data if requested or all
        if args.student_personal_data or args.all:
            success = purge_student_personal_data(conn, args.dry_run) and success
        
        # Purge grade data if requested or all
        if args.grades or args.all:
            success = purge_grade_data(conn, args.dry_run) and success
        
        # Close the database connection
        conn.close()
        
        # Print summary
        print("\nPurge Summary:")
        if success:
            print("✅ All purge operations completed successfully")
        else:
            print("❌ Some purge operations encountered errors")
        
        if args.dry_run:
            print("NOTE: This was a dry run, no data was actually purged")
        
        return 0 if success else 1
    
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 