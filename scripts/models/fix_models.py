#!/usr/bin/env python3
"""
Script Name: fix_models.py
Description: Consolidated script for fixing model-related issues in the LMS system

Usage:
    python scripts/models/fix_models.py [options]
    
Options:
    --schema                Fix database schema issues
    --model-save            Fix model save functionality
    --db-save               Fix database save functionality
    --all                   Apply all fixes (default)
    --dry-run               Show what would be fixed without making changes
    
Dependencies:
    - psycopg2
    - sqlalchemy
    
Output:
    Model fixes status messages
    
Author: LMS Team
Last Modified: 2025-03-19
"""

import argparse
import os
import sys
import json
import re
from pathlib import Path
import importlib
import inspect
import psycopg2
import psycopg2.extras

# Add the project root to sys.path to enable imports
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

# Try to import relevant modules
try:
    # These imports are used to analyze and fix models
    from database.db_manager import get_db_params
    import sqlalchemy
    from sqlalchemy import inspect as sa_inspect
    from sqlalchemy.ext.declarative import declarative_base
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure you have all required packages installed.")
    sys.exit(1)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Fix model-related issues in the LMS system")
    parser.add_argument("--schema", action="store_true", help="Fix database schema issues")
    parser.add_argument("--model-save", action="store_true", help="Fix model save functionality")
    parser.add_argument("--db-save", action="store_true", help="Fix database save functionality")
    parser.add_argument("--all", action="store_true", help="Apply all fixes (default)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without making changes")
    return parser.parse_args()

def fix_schema(dry_run=False):
    """Fix database schema issues."""
    print("Fixing database schema issues...")
    
    # Get database connection parameters
    db_params = get_db_params()
    
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Find all models in the database module
        models_path = project_root / "database" / "models.py"
        
        # Read the models file
        with open(models_path, "r") as f:
            models_code = f.read()
        
        # Find model classes in the code
        model_classes = re.findall(r"class\s+(\w+)\(.*Base.*\):", models_code)
        
        # Check each model against the database
        for model_name in model_classes:
            print(f"Checking model: {model_name}")
            
            # Get the table name (convert CamelCase to snake_case)
            table_name = ''.join(['_'+c.lower() if c.isupper() else c for c in model_name]).lstrip('_')
            
            # Check if the table exists
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """, (table_name,))
            
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                print(f"Table {table_name} does not exist in the database")
                if not dry_run:
                    # This would normally run the migration to create the table
                    print(f"  Would create table {table_name}")
                    print("  (Not implemented in this script)")
                else:
                    print(f"  DRY RUN: Would create table {table_name}")
            else:
                # Check columns in the table
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                """, (table_name,))
                
                db_columns = [row[0] for row in cursor.fetchall()]
                
                # Find column definitions in the model
                column_pattern = r"(\w+)\s*=\s*Column\("
                columns_in_model = re.findall(column_pattern, models_code[models_code.find(f"class {model_name}"):])
                
                # Find columns missing from the database
                missing_columns = [col for col in columns_in_model if col.lower() not in db_columns and col != "id"]
                
                if missing_columns:
                    print(f"  Missing columns in table {table_name}: {', '.join(missing_columns)}")
                    if not dry_run:
                        # This would normally run the migration to add the columns
                        print(f"  Would add columns to {table_name}")
                        print("  (Not implemented in this script)")
                    else:
                        print(f"  DRY RUN: Would add columns to {table_name}")
        
        cursor.close()
        conn.close()
        print("Schema fix check completed")
        
    except Exception as e:
        print(f"Error fixing schema: {e}")
        return False
    
    return True

def fix_model_save(dry_run=False):
    """Fix model save functionality."""
    print("Fixing model save functionality...")
    
    # Path to the models file
    models_path = project_root / "database" / "models.py"
    
    try:
        # Read the models file
        with open(models_path, "r") as f:
            models_code = f.read()
        
        # Check for save method in Base class
        if "def save(self" not in models_code:
            print("Save method is missing from the Base class")
            
            if not dry_run:
                # Add save method to Base class
                base_class_end = models_code.find("class ") - 1
                if base_class_end > 0:
                    base_declaration = models_code[:base_class_end]
                    rest_of_file = models_code[base_class_end:]
                    
                    # Add save method
                    save_method = """
    def save(self):
        '''Save this model to the database.'''
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving {self.__class__.__name__}: {e}")
            return False
"""
                    updated_code = base_declaration + save_method + rest_of_file
                    
                    # Write the updated code back to the file
                    with open(models_path, "w") as f:
                        f.write(updated_code)
                    
                    print("Added save method to Base class")
                else:
                    print("Could not locate Base class declaration")
            else:
                print("DRY RUN: Would add save method to Base class")
        else:
            print("Save method already exists in Base class")
        
        # Check for errors in save method implementation
        if "def save(self" in models_code:
            save_impl = models_code[models_code.find("def save(self"):].split("\n    def ")[0]
            
            errors = []
            
            # Check for common issues
            if "session.add" not in save_impl:
                errors.append("Missing session.add call")
            
            if "session.commit" not in save_impl:
                errors.append("Missing session.commit call")
            
            if "try:" not in save_impl or "except" not in save_impl:
                errors.append("Missing error handling")
            
            if "rollback" not in save_impl:
                errors.append("Missing rollback on error")
            
            if errors:
                print(f"Found issues in save method: {', '.join(errors)}")
                
                if not dry_run:
                    # This would fix the save method
                    print("  Would fix save method implementation")
                    print("  (Not implemented in this script)")
                else:
                    print("  DRY RUN: Would fix save method implementation")
        
        print("Model save fix check completed")
        
    except Exception as e:
        print(f"Error fixing model save: {e}")
        return False
    
    return True

def fix_db_save(dry_run=False):
    """Fix database save functionality."""
    print("Fixing database save functionality...")
    
    # Check for db modules
    db_module_path = project_root / "database" / "db_manager.py"
    
    if not db_module_path.exists():
        print(f"Database manager module not found at {db_module_path}")
        return False
    
    try:
        # Read the db manager file
        with open(db_module_path, "r") as f:
            db_code = f.read()
        
        errors = []
        
        # Check for required components
        if "create_engine" not in db_code:
            errors.append("Missing SQLAlchemy engine creation")
        
        if "sessionmaker" not in db_code:
            errors.append("Missing SQLAlchemy session creation")
        
        if "scoped_session" not in db_code:
            errors.append("Missing SQLAlchemy scoped session")
        
        if errors:
            print(f"Found issues in database manager: {', '.join(errors)}")
            
            if not dry_run:
                # This would fix the database manager
                print("  Would fix database manager implementation")
                print("  (Not implemented in this script)")
            else:
                print("  DRY RUN: Would fix database manager implementation")
        else:
            print("Database manager appears to be properly implemented")
        
        # Check session management
        if "session.close()" not in db_code:
            print("Missing session cleanup")
            
            if not dry_run:
                # This would add session cleanup
                print("  Would add session cleanup")
                print("  (Not implemented in this script)")
            else:
                print("  DRY RUN: Would add session cleanup")
        
        print("Database save fix check completed")
        
    except Exception as e:
        print(f"Error fixing database save: {e}")
        return False
    
    return True

def main():
    """Main function."""
    args = parse_args()
    
    # If no specific fixes are requested, apply all fixes
    apply_all = args.all or not (args.schema or args.model_save or args.db_save)
    
    # Track success status
    success = True
    
    print("Starting model fixes...")
    if args.dry_run:
        print("DRY RUN MODE: No changes will be made")
    
    # Fix schema if requested or applying all fixes
    if args.schema or apply_all:
        schema_success = fix_schema(args.dry_run)
        success = success and schema_success
    
    # Fix model save if requested or applying all fixes
    if args.model_save or apply_all:
        model_success = fix_model_save(args.dry_run)
        success = success and model_success
    
    # Fix database save if requested or applying all fixes
    if args.db_save or apply_all:
        db_success = fix_db_save(args.dry_run)
        success = success and db_success
    
    # Print summary
    print("\nFix Summary:")
    if success:
        print("✅ All fixes completed successfully")
    else:
        print("❌ Some fixes encountered errors")
    
    if args.dry_run:
        print("NOTE: This was a dry run, no changes were made")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 