#!/usr/bin/env python3
"""
Test helper utilities for the LMS system.
This module provides common fixtures and utility functions for testing.

The utilities in this module simplify common testing tasks such as:
1. Generating test data with random values
2. Managing temporary files and directories
3. Creating sample data structures for tests
4. Making assertions about data structures
5. Working with dates and times
6. Creating mock database connections

These helpers should be used across all test categories (unit, integration, api)
to ensure consistency in test data and behavior.
"""

import pytest
import sys
import os
from pathlib import Path
import random
import string
import json
from datetime import datetime, timedelta
import tempfile

# Add pytest fixtures that can be shared across test types

@pytest.fixture
def random_string():
    """
    Generate a random string for test data.
    
    This fixture returns a function that creates random strings with optional prefix.
    The generated strings can be used for usernames, emails, and other test data
    where unique values are needed.
    
    Returns:
        callable: Function that generates random strings
        
    Example:
        ```
        def test_user_creation(random_string):
            username = random_string(length=8, prefix="user_")
            # username might be "user_a7b3c9d2"
        ```
    """
    def _random_string(length=10, prefix="test_"):
        characters = string.ascii_letters + string.digits
        random_str = ''.join(random.choice(characters) for _ in range(length))
        return f"{prefix}{random_str}"
    return _random_string

@pytest.fixture
def temp_dir():
    """
    Create a temporary directory for file-based tests.
    
    This fixture creates a temporary directory that is automatically deleted
    after the test completes, regardless of whether the test passes or fails.
    
    Yields:
        str: Path to the temporary directory
        
    Example:
        ```
        def test_file_operations(temp_dir):
            file_path = os.path.join(temp_dir, "test.txt")
            with open(file_path, "w") as f:
                f.write("test content")
            # Use the file, then it's automatically cleaned up
        ```
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def temp_file():
    """
    Create a temporary file for file-based tests.
    
    This fixture creates a temporary file that is automatically deleted
    after the test completes, regardless of whether the test passes or fails.
    
    Yields:
        str: Path to the temporary file
        
    Example:
        ```
        def test_file_reading(temp_file):
            with open(temp_file, "w") as f:
                f.write("test content")
            # Test reading from the file
            with open(temp_file, "r") as f:
                content = f.read()
                assert content == "test content"
        ```
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        yield tmp.name
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)

@pytest.fixture
def sample_course_data(random_string):
    """
    Generate sample course data for tests.
    
    This fixture creates a dictionary with realistic test data for a course.
    It uses the random_string fixture to ensure unique values.
    
    Args:
        random_string: Fixture that generates random strings
        
    Returns:
        dict: Sample course data
        
    Example:
        ```
        def test_course_creation(sample_course_data):
            # Create a course with the sample data
            course = Course(**sample_course_data)
            assert course.title == sample_course_data["title"]
        ```
    """
    return {
        "title": random_string(prefix="Course_"),
        "description": "This is a test course",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

@pytest.fixture
def sample_user_data(random_string):
    """
    Generate sample user data for tests.
    
    This fixture creates a dictionary with realistic test data for a user.
    It uses the random_string fixture to ensure unique values for username and email.
    
    Args:
        random_string: Fixture that generates random strings
        
    Returns:
        dict: Sample user data with username, email, password, and user_type
        
    Example:
        ```
        def test_user_registration(sample_user_data):
            # Register a user with the sample data
            response = client.post("/api/auth/register", json=sample_user_data)
            assert response.status_code == 201
        ```
    """
    return {
        "username": random_string(prefix="user_"),
        "email": f"{random_string(prefix='email_')}@example.com",
        "password": random_string(length=12),
        "user_type": random.choice(["student", "teacher", "admin"])
    }

@pytest.fixture
def sample_lesson_data(random_string, sample_course_data):
    """
    Generate sample lesson data for tests.
    
    This fixture creates a dictionary with realistic test data for a lesson.
    The course_id field is intentionally set to None and should be populated
    by the test that uses this fixture.
    
    Args:
        random_string: Fixture that generates random strings
        sample_course_data: Fixture that generates sample course data
        
    Returns:
        dict: Sample lesson data
        
    Example:
        ```
        def test_lesson_creation(sample_lesson_data, db_session):
            # Create a course first
            course = Course(**sample_course_data)
            db_session.add(course)
            db_session.commit()
            
            # Set the course_id in the lesson data
            sample_lesson_data["course_id"] = course.id
            
            # Create a lesson with the sample data
            lesson = Lesson(**sample_lesson_data)
            assert lesson.title == sample_lesson_data["title"]
        ```
    """
    return {
        "title": random_string(prefix="Lesson_"),
        "content": "This is test lesson content.",
        "course_id": None,  # This should be set by the test
        "order": random.randint(1, 10)
    }

@pytest.fixture
def sample_exercise_data(random_string, sample_lesson_data):
    """
    Generate sample exercise data for tests.
    
    This fixture creates a dictionary with realistic test data for an exercise.
    It randomly selects an exercise type and populates the appropriate fields.
    The lesson_id field is intentionally set to None and should be populated
    by the test that uses this fixture.
    
    Args:
        random_string: Fixture that generates random strings
        sample_lesson_data: Fixture that generates sample lesson data
        
    Returns:
        dict: Sample exercise data
        
    Example:
        ```
        def test_exercise_creation(sample_exercise_data, db_session):
            # Create a lesson first
            lesson = Lesson(**sample_lesson_data)
            db_session.add(lesson)
            db_session.commit()
            
            # Set the lesson_id in the exercise data
            sample_exercise_data["lesson_id"] = lesson.id
            
            # Create an exercise with the sample data
            exercise = Exercise(**sample_exercise_data)
            assert exercise.question == sample_exercise_data["question"]
        ```
    """
    exercise_types = ["multiple_choice", "text_input", "code", "essay"]
    exercise_type = random.choice(exercise_types)
    
    data = {
        "lesson_id": None,  # This should be set by the test
        "question": f"Test question: {random_string(prefix='Q_')}?",
        "exercise_type": exercise_type
    }
    
    if exercise_type == "multiple_choice":
        options = [f"Option {i}" for i in range(1, 5)]
        data["answer_options"] = json.dumps(options)
        data["correct_answer"] = options[0]
    elif exercise_type == "text_input":
        data["correct_answer"] = random_string(prefix="Answer_")
    
    return data

# Test utility functions

def assert_dict_contains_subset(subset, full_dict):
    """
    Assert that full_dict contains all key-value pairs from subset.
    
    This utility function checks that all key-value pairs in the subset dictionary
    are present in the full dictionary. It raises an AssertionError if any key
    is missing or if any value doesn't match.
    
    Args:
        subset (dict): Dictionary with key-value pairs to check for
        full_dict (dict): Dictionary to check against
        
    Raises:
        AssertionError: If any key is missing or any value doesn't match
        
    Example:
        ```
        user_data = {"username": "john", "email": "john@example.com", "id": 123}
        assert_dict_contains_subset({"username": "john"}, user_data)  # Passes
        assert_dict_contains_subset({"username": "jane"}, user_data)  # Fails
        ```
    """
    for key, value in subset.items():
        assert key in full_dict, f"Key '{key}' not found in dictionary"
        assert full_dict[key] == value, f"Value mismatch for key '{key}': expected {value}, got {full_dict[key]}"

def generate_date_range(days=30):
    """
    Generate a list of dates for time-based tests.
    
    This utility function creates a list of datetime objects representing
    a range of dates from the current day backwards.
    
    Args:
        days (int): Number of days to generate, default is 30
        
    Returns:
        list: List of datetime objects in descending order
        
    Example:
        ```
        dates = generate_date_range(7)  # Get the last 7 days
        # Use dates for testing time-based queries
        ```
    """
    base = datetime.now()
    return [base - timedelta(days=i) for i in range(days)]

def create_mock_database():
    """
    Create a mock in-memory database for testing.
    
    This utility function creates an in-memory SQLite database using SQLAlchemy,
    which can be used for testing without affecting a real database.
    
    Returns:
        tuple: Engine and Session objects for SQLAlchemy
        
    Example:
        ```
        engine, Session = create_mock_database()
        Base.metadata.create_all(engine)
        session = Session()
        # Use session for database operations
        ```
    """
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Create in-memory SQLite database
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        return engine, Session
    except ImportError:
        pytest.skip("SQLAlchemy not available")
        return None, None 