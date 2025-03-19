#!/usr/bin/env python3
"""
Script Name: test_database_comprehensive.py
Description: Runs comprehensive tests on the LMS database

Usage:
    python scripts/database/verification/test_database_comprehensive.py [options]
    
Options:
    --basic              Run basic connectivity tests only
    --crud               Run CRUD operation tests
    --relationships      Test table relationships
    --performance        Run performance tests
    --all                Run all tests (default)
    
Dependencies:
    - psycopg2
    
Output:
    Test results for database functionality
    
Author: LMS Team
Last Modified: 2025-03-19
"""

import argparse
import os
import sys
import json
import time
import random
import string
from pathlib import Path
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta

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

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Test LMS database")
    parser.add_argument("--basic", action="store_true", help="Run basic connectivity tests only")
    parser.add_argument("--crud", action="store_true", help="Run CRUD operation tests")
    parser.add_argument("--relationships", action="store_true", help="Test table relationships")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--all", action="store_true", help="Run all tests (default)")
    return parser.parse_args()

def print_result(test_name, passed, details=None):
    """Print test result with appropriate formatting."""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status} - {test_name}")
    if details and not passed:
        print(f"       Details: {details}")
    return passed

def random_string(length=10):
    """Generate a random string for test data."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_connection(db_params):
    """Test basic database connection."""
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return print_result("Database connection", True)
    except Exception as e:
        return print_result("Database connection", False, str(e))

def test_user_crud(db_params):
    """Test CRUD operations on the users table."""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Create a test user
        test_username = f"test_user_{random_string(5)}"
        test_email = f"{test_username}@example.com"
        test_password = "hashed_password_123"
        
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (test_username, test_email, test_password, "student")
        )
        user_id = cursor.fetchone()["id"]
        
        # Read the user
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user or user["username"] != test_username:
            return print_result("User CRUD - Create/Read", False, "User not found or username mismatch")
        
        # Update the user
        new_email = f"updated_{test_username}@example.com"
        cursor.execute(
            """
            UPDATE users
            SET email = %s
            WHERE id = %s
            """,
            (new_email, user_id)
        )
        
        # Verify update
        cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
        updated_email = cursor.fetchone()["email"]
        
        if updated_email != new_email:
            return print_result("User CRUD - Update", False, f"Expected {new_email}, got {updated_email}")
        
        # Delete the user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        # Verify deletion
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone():
            return print_result("User CRUD - Delete", False, "User still exists after deletion")
        
        conn.commit()
        cursor.close()
        return print_result("User CRUD operations", True)
    except Exception as e:
        if conn:
            conn.rollback()
        return print_result("User CRUD operations", False, str(e))
    finally:
        if conn:
            conn.close()

def test_course_lesson_relationship(db_params):
    """Test the relationship between courses and lessons."""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Create a test course
        test_course_title = f"Test Course {random_string(5)}"
        cursor.execute(
            """
            INSERT INTO courses (title, description)
            VALUES (%s, %s)
            RETURNING id
            """,
            (test_course_title, "Test course description")
        )
        course_id = cursor.fetchone()["id"]
        
        # Create test lessons for the course
        lesson_titles = [f"Lesson {i}: {random_string(5)}" for i in range(1, 4)]
        lesson_ids = []
        
        for i, title in enumerate(lesson_titles):
            cursor.execute(
                """
                INSERT INTO lessons (course_id, title, content, sequence)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (course_id, title, f"Content for {title}", i + 1)
            )
            lesson_ids.append(cursor.fetchone()["id"])
        
        # Verify lessons are associated with the course
        cursor.execute(
            """
            SELECT id, title
            FROM lessons
            WHERE course_id = %s
            ORDER BY sequence
            """,
            (course_id,)
        )
        lessons = cursor.fetchall()
        
        if len(lessons) != len(lesson_titles):
            return print_result(
                "Course-Lesson relationship", 
                False, 
                f"Expected {len(lesson_titles)} lessons, got {len(lessons)}"
            )
        
        # Verify cascade delete
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        
        # Check if lessons were deleted (assuming ON DELETE CASCADE)
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE course_id = %s", (course_id,))
        remaining_lessons = cursor.fetchone()[0]
        
        if remaining_lessons > 0:
            return print_result(
                "Course-Lesson cascade delete", 
                False, 
                f"{remaining_lessons} lessons remained after course deletion"
            )
        
        conn.commit()
        cursor.close()
        return print_result("Course-Lesson relationship", True)
    except Exception as e:
        if conn:
            conn.rollback()
        return print_result("Course-Lesson relationship", False, str(e))
    finally:
        if conn:
            conn.close()

def test_exercise_submission_relationship(db_params):
    """Test the relationship between exercises and submissions."""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Create a test course and lesson
        cursor.execute(
            """
            INSERT INTO courses (title, description)
            VALUES (%s, %s)
            RETURNING id
            """,
            (f"Course for Exercise Test {random_string(5)}", "Test course description")
        )
        course_id = cursor.fetchone()["id"]
        
        cursor.execute(
            """
            INSERT INTO lessons (course_id, title, content, sequence)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (course_id, "Lesson for Exercise Test", "Test lesson content", 1)
        )
        lesson_id = cursor.fetchone()["id"]
        
        # Create a test exercise
        cursor.execute(
            """
            INSERT INTO exercises (lesson_id, exercise_type, question, answers, options)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                lesson_id,
                "multiple_choice",
                "Test question?",
                json.dumps(["Correct answer"]),
                json.dumps({"choices": ["Correct answer", "Wrong answer 1", "Wrong answer 2"]})
            )
        )
        exercise_id = cursor.fetchone()["id"]
        
        # Create a test user
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (f"test_user_{random_string(5)}", "test@example.com", "hashed_password", "student")
        )
        user_id = cursor.fetchone()["id"]
        
        # Create test submissions
        submissions = []
        for i in range(3):
            is_correct = i % 2 == 0  # Alternate between correct and incorrect
            cursor.execute(
                """
                INSERT INTO submissions (user_id, exercise_id, answer, is_correct, score)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    exercise_id,
                    json.dumps(["Correct answer"] if is_correct else ["Wrong answer 1"]),
                    is_correct,
                    100 if is_correct else 0
                )
            )
            submissions.append(cursor.fetchone()["id"])
        
        # Verify submissions are associated with the exercise
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM submissions
            WHERE exercise_id = %s
            """,
            (exercise_id,)
        )
        submission_count = cursor.fetchone()[0]
        
        if submission_count != len(submissions):
            return print_result(
                "Exercise-Submission relationship", 
                False, 
                f"Expected {len(submissions)} submissions, got {submission_count}"
            )
        
        # Clean up
        cursor.execute("DELETE FROM submissions WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        cursor.execute("DELETE FROM exercises WHERE id = %s", (exercise_id,))
        cursor.execute("DELETE FROM lessons WHERE id = %s", (lesson_id,))
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        
        conn.commit()
        cursor.close()
        return print_result("Exercise-Submission relationship", True)
    except Exception as e:
        if conn:
            conn.rollback()
        return print_result("Exercise-Submission relationship", False, str(e))
    finally:
        if conn:
            conn.close()

def test_database_performance(db_params):
    """Test database performance."""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Test simple query performance
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM users")
        query_time = time.time() - start_time
        print(f"Simple query execution time: {query_time:.4f} seconds")
        
        # Test index performance (if users table exists)
        try:
            # Create an index on username if it doesn't exist
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_username ON users (username)
                """
            )
            conn.commit()
            
            # Test queries with and without index
            # Query with index
            start_time = time.time()
            cursor.execute("SELECT * FROM users WHERE username = 'nonexistent_user'")
            indexed_time = time.time() - start_time
            
            # Query without index (using email which might not have an index)
            start_time = time.time()
            cursor.execute("SELECT * FROM users WHERE email = 'nonexistent@example.com'")
            non_indexed_time = time.time() - start_time
            
            print(f"Indexed query time: {indexed_time:.4f} seconds")
            print(f"Non-indexed query time: {non_indexed_time:.4f} seconds")
            
        except Exception as e:
            print(f"Index performance test skipped: {e}")
        
        cursor.close()
        return print_result("Database performance tests", True)
    except Exception as e:
        return print_result("Database performance tests", False, str(e))
    finally:
        if conn:
            conn.close()

def main():
    """Main function."""
    args = parse_args()
    
    # If no specific tests are requested, run all tests
    run_all = args.all or not (args.basic or args.crud or args.relationships or args.performance)
    
    # Get database connection parameters
    db_params = get_db_params()
    
    print("Running database tests...")
    
    # Track test results
    all_tests_passed = True
    
    # Basic connectivity test is always run
    basic_passed = test_connection(db_params)
    all_tests_passed = all_tests_passed and basic_passed
    
    # If basic test failed or only basic tests requested, stop here
    if not basic_passed or args.basic:
        return 0 if all_tests_passed else 1
    
    # CRUD tests
    if args.crud or run_all:
        print("\nRunning CRUD tests:")
        crud_passed = test_user_crud(db_params)
        all_tests_passed = all_tests_passed and crud_passed
    
    # Relationship tests
    if args.relationships or run_all:
        print("\nRunning relationship tests:")
        course_lesson_passed = test_course_lesson_relationship(db_params)
        exercise_submission_passed = test_exercise_submission_relationship(db_params)
        all_tests_passed = all_tests_passed and course_lesson_passed and exercise_submission_passed
    
    # Performance tests
    if args.performance or run_all:
        print("\nRunning performance tests:")
        performance_passed = test_database_performance(db_params)
        all_tests_passed = all_tests_passed and performance_passed
    
    # Print summary
    print("\nTest Summary:")
    print(f"{'✅ All tests passed!' if all_tests_passed else '❌ Some tests failed!'}")
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 