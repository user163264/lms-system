#!/usr/bin/env python3
"""
Shared fixtures and configuration for all LMS tests.
This centralizes test configuration and common fixtures.

This module defines fixtures that are available to all tests in the LMS testing suite.
It handles database connections, test data loading, and provides configuration for pytest.

Usage:
    Import this module's fixtures in your tests:
    ```
    # No import needed, fixtures are automatically available
    def test_something(db_connection, async_db_session):
        # Use fixtures here
    ```

Fixtures:
    - db_connection: PostgreSQL database connection
    - db_cursor: Database cursor with automatic rollback
    - async_db_session: Async SQLAlchemy session
    - reset_sqlalchemy_db: Resets the database for SQLAlchemy tests
    - load_test_data: Function to load test data from fixture files
    - event_loop: Event loop for async tests
"""

import pytest
import os
import sys
import asyncio
from pathlib import Path
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Add parent directory to path to allow importing from the project root
project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root))

# Try to import relevant modules
try:
    from backend.app.database import engine as app_engine
    from backend.app.database import get_db, Base, AsyncSessionLocal
    from backend.app.models import User, Lesson, Exercise, Submission
    from database.db_manager import get_db_params
except ImportError as e:
    print(f"Warning: Some imports failed: {e}")
    print("Some tests may not run correctly.")

# Database connection parameters
DB_PARAMS = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'dbname': os.environ.get('DB_NAME', 'lms_db'),
    'user': os.environ.get('DB_USER', 'lms_user'),
    'password': os.environ.get('DB_PASSWORD', 'lms_password'),
    'port': os.environ.get('DB_PORT', '5432')
}

# Test data paths
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Pytest configuration
def pytest_configure(config):
    """
    Configure pytest with custom markers.
    
    This function registers custom markers that can be used to categorize tests:
    - unit: Basic unit tests
    - integration: Tests between components
    - api: API endpoint tests
    - direct_db: Tests using direct database connection
    - sqlalchemy: Tests using SQLAlchemy ORM
    - asyncio: Async tests
    
    Args:
        config: Pytest configuration object
    """
    config.addinivalue_line("markers", "unit: mark a test as a unit test")
    config.addinivalue_line("markers", "integration: mark a test as an integration test")
    config.addinivalue_line("markers", "api: mark a test as an API test")
    config.addinivalue_line("markers", "direct_db: mark a test as using direct database connection")
    config.addinivalue_line("markers", "sqlalchemy: mark a test as using SQLAlchemy")
    config.addinivalue_line("markers", "asyncio: mark a test as asyncio test")

@pytest.fixture(scope="session")
def event_loop():
    """
    Create an instance of the default event loop for each test session.
    
    This fixture provides a consistent event loop for async tests.
    
    Returns:
        asyncio.EventLoop: Event loop for async tests
        
    Yields:
        asyncio.EventLoop: Event loop that is automatically closed after tests
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_connection():
    """
    Create a database connection for testing.
    
    This fixture establishes a connection to the PostgreSQL database using
    the connection parameters defined in DB_PARAMS.
    
    Returns:
        psycopg2.connection: Database connection object
        
    Yields:
        psycopg2.connection: Connection that is automatically closed after tests
    """
    try:
        conn = psycopg2.connect(**DB_PARAMS, cursor_factory=RealDictCursor)
        conn.autocommit = False
        yield conn
    finally:
        conn.close()

@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """
    Create a database cursor for testing.
    
    This fixture provides a cursor connected to the database, with automatic
    rollback after the test to avoid any test data persistence.
    
    Args:
        db_connection: Database connection fixture
        
    Returns:
        psycopg2.cursor: Database cursor
        
    Yields:
        psycopg2.cursor: Cursor that is automatically rolled back and closed after tests
    """
    cursor = db_connection.cursor()
    yield cursor
    db_connection.rollback()
    cursor.close()

@pytest.fixture(scope="function")
async def async_db_session():
    """
    Create an async database session for testing.
    
    This fixture provides an async SQLAlchemy session that is automatically
    rolled back after the test to avoid any test data persistence.
    
    Returns:
        AsyncSession: Async SQLAlchemy session
        
    Yields:
        AsyncSession: Session that is automatically rolled back after tests
    """
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="function")
async def reset_sqlalchemy_db():
    """
    Reset the database for SQLAlchemy tests.
    
    This fixture drops and recreates all tables before and after each test,
    ensuring a clean database state for each test.
    
    Yields:
        None
    """
    async with app_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with app_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="function")
def load_test_data():
    """
    Load test data from fixtures.
    
    This fixture provides a function to load test data from JSON files
    in the fixtures directory.
    
    Returns:
        callable: Function that loads test data from a file
        
    Example:
        ```
        def test_with_data(load_test_data):
            users = load_test_data('users.json')
            # Test with loaded data
        ```
    """
    def _load_data(filename):
        file_path = FIXTURES_DIR / filename
        if not file_path.exists():
            return None
        with open(file_path, 'r') as f:
            return json.load(f)
    return _load_data 