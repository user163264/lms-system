#!/usr/bin/env python3
"""
Script Name: sql_reporter.py
Description: Generates SQL reports from the LMS database

Usage:
    python scripts/database/reports/sql_reporter.py [options]
    
Options:
    --student-progress       Generate student progress report
    --assignment-stats       Generate assignment statistics
    --course-overview        Generate course overview
    --custom QUERY           Run a custom SQL query
    --format FORMAT          Output format (csv, json, table) [default: table]
    --output FILE            Save output to file instead of stdout
    
Dependencies:
    - psycopg2
    - pandas
    - tabulate
    
Output:
    SQL reports in specified format (CSV, JSON, or tabular)
    
Author: LMS Team
Last Modified: 2025-03-19
"""

import argparse
import os
import sys
import json
import csv
from pathlib import Path
from datetime import datetime
import psycopg2
import psycopg2.extras

# Add the project root to sys.path to enable imports
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

# Try to import relevant modules
try:
    from database.db_manager import get_db_params
    import pandas as pd
    from tabulate import tabulate
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure you have all required packages installed.")
    sys.exit(1)

# Predefined SQL queries
QUERIES = {
    "student_progress": """
        SELECT 
            s.id AS student_id,
            s.name AS student_name,
            c.name AS course_name,
            COUNT(a.id) AS total_assignments,
            COUNT(sa.id) AS submitted_assignments,
            AVG(sa.score) AS average_score
        FROM 
            student s
        JOIN 
            enrollment e ON s.id = e.student_id
        JOIN 
            course c ON e.course_id = c.id
        LEFT JOIN 
            assignment a ON c.id = a.course_id
        LEFT JOIN 
            student_assignment sa ON a.id = sa.assignment_id AND s.id = sa.student_id
        GROUP BY 
            s.id, s.name, c.name
        ORDER BY 
            s.name, c.name
    """,
    
    "assignment_stats": """
        SELECT 
            c.name AS course_name,
            a.id AS assignment_id,
            a.title AS assignment_title,
            a.due_date,
            COUNT(sa.id) AS submission_count,
            AVG(sa.score) AS average_score,
            MIN(sa.score) AS min_score,
            MAX(sa.score) AS max_score,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sa.score) AS median_score
        FROM 
            assignment a
        JOIN 
            course c ON a.course_id = c.id
        LEFT JOIN 
            student_assignment sa ON a.id = sa.assignment_id
        GROUP BY 
            c.name, a.id, a.title, a.due_date
        ORDER BY 
            c.name, a.due_date
    """,
    
    "course_overview": """
        SELECT 
            c.id AS course_id,
            c.name AS course_name,
            c.code AS course_code,
            i.name AS instructor,
            COUNT(DISTINCT e.student_id) AS enrolled_students,
            COUNT(DISTINCT a.id) AS assignment_count,
            MIN(a.due_date) AS first_assignment,
            MAX(a.due_date) AS last_assignment
        FROM 
            course c
        LEFT JOIN 
            instructor i ON c.instructor_id = i.id
        LEFT JOIN 
            enrollment e ON c.id = e.course_id
        LEFT JOIN 
            assignment a ON c.id = a.course_id
        GROUP BY 
            c.id, c.name, c.code, i.name
        ORDER BY 
            c.name
    """,
}

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate SQL reports from the LMS database")
    
    # Report type options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--student-progress", action="store_true", help="Generate student progress report")
    group.add_argument("--assignment-stats", action="store_true", help="Generate assignment statistics")
    group.add_argument("--course-overview", action="store_true", help="Generate course overview")
    group.add_argument("--custom", type=str, help="Run a custom SQL query")
    
    # Output options
    parser.add_argument("--format", choices=["csv", "json", "table"], default="table",
                      help="Output format (csv, json, table) [default: table]")
    parser.add_argument("--output", type=str, help="Save output to file instead of stdout")
    
    return parser.parse_args()

def get_report_query(args):
    """Get the SQL query based on the requested report type."""
    if args.student_progress:
        return QUERIES["student_progress"]
    elif args.assignment_stats:
        return QUERIES["assignment_stats"]
    elif args.course_overview:
        return QUERIES["course_overview"]
    elif args.custom:
        return args.custom
    else:
        print("No report type specified")
        sys.exit(1)

def run_query(query):
    """Run the SQL query and return the results as a pandas DataFrame."""
    try:
        # Get database connection parameters
        db_params = get_db_params()
        
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        
        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Close the database connection
        conn.close()
        
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        sys.exit(1)

def format_output(df, format_type):
    """Format the DataFrame according to the specified format type."""
    if format_type == "csv":
        return df.to_csv(index=False)
    elif format_type == "json":
        return df.to_json(orient="records", indent=2)
    elif format_type == "table":
        return tabulate(df, headers="keys", tablefmt="psql")
    else:
        print(f"Unsupported format: {format_type}")
        sys.exit(1)

def save_output(output, filename):
    """Save the output to a file."""
    try:
        with open(filename, "w") as f:
            f.write(output)
        print(f"Output saved to {filename}")
    except Exception as e:
        print(f"Error saving output to file: {e}")
        sys.exit(1)

def main():
    """Main function."""
    args = parse_args()
    
    # Get the query
    query = get_report_query(args)
    
    # Run the query
    df = run_query(query)
    
    # Format the output
    output = format_output(df, args.format)
    
    # Save or print the output
    if args.output:
        save_output(output, args.output)
    else:
        print(output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 