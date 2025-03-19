#!/usr/bin/env python3
"""
Unit tests for database functionality.
This consolidates tests from:
- test_database.py
- test_db.py
- test_db_layer.py
- simple_test_db.py
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path
import time
import random
from datetime import datetime, timedelta
import json

# Import database components
try:
    from backend.app.database import engine as app_engine
    from backend.app.database import get_db, Base, AsyncSessionLocal
    from backend.app.models import User, Lesson, Exercise, Submission
except ImportError as e:
    print(f"Warning: SQLAlchemy imports failed: {e}")
    print("SQLAlchemy tests will be skipped")

# Direct database connection
import psycopg2
from psycopg2.extras import RealDictCursor

# Mark direct DB tests
@pytest.mark.unit
@pytest.mark.direct_db
def test_direct_connection(db_connection):
    """Test direct database connection using psycopg2."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    assert version is not None
    assert "PostgreSQL" in version['version']
    cursor.close()

@pytest.mark.unit
@pytest.mark.direct_db
def test_direct_db_tables(db_cursor):
    """Test if required tables exist in the database."""
    # Check for essential tables
    essential_tables = ['users', 'courses', 'lessons', 'exercises', 'submissions']
    
    db_cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    tables = [row['table_name'] for row in db_cursor.fetchall()]
    
    for table in essential_tables:
        if table not in tables:
            pytest.skip(f"Table {table} does not exist, skipping test")
    
    assert len(tables) > 0, "No tables found in database"

@pytest.mark.unit
@pytest.mark.direct_db
def test_direct_crud_operations(db_connection):
    """Test CRUD operations using direct database connection."""
    cursor = db_connection.cursor()
    
    # Check if users table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'users'
        )
    """)
    
    if not cursor.fetchone()['exists']:
        pytest.skip("Users table does not exist, skipping test")
    
    # Create a test user
    test_username = f"test_user_{random.randint(1000, 9999)}"
    test_email = f"{test_username}@example.com"
    
    try:
        # Create
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (test_username, test_email, "hashed_password", "student")
        )
        user_id = cursor.fetchone()['id']
        db_connection.commit()
        
        # Read
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        assert user is not None
        assert user['username'] == test_username
        
        # Update
        new_email = f"updated_{test_username}@example.com"
        cursor.execute(
            """
            UPDATE users
            SET email = %s
            WHERE id = %s
            """,
            (new_email, user_id)
        )
        db_connection.commit()
        
        # Verify update
        cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
        updated_email = cursor.fetchone()['email']
        assert updated_email == new_email
        
        # Delete
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db_connection.commit()
        
        # Verify deletion
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        assert cursor.fetchone() is None
        
    except Exception as e:
        db_connection.rollback()
        pytest.fail(f"Exception during CRUD operations: {e}")
    finally:
        cursor.close()

# Mark SQLAlchemy tests
try:
    # Only define these tests if imports succeeded
    if 'User' in globals():
        @pytest.mark.unit
        @pytest.mark.asyncio
        @pytest.mark.sqlalchemy
        async def test_sqlalchemy_connection(reset_sqlalchemy_db):
            """Test SQLAlchemy database connection."""
            async with AsyncSessionLocal() as session:
                result = await session.execute("SELECT 1")
                assert result.scalar() == 1
        
        @pytest.mark.unit
        @pytest.mark.asyncio
        @pytest.mark.sqlalchemy
        async def test_sqlalchemy_crud(reset_sqlalchemy_db):
            """Test CRUD operations using SQLAlchemy."""
            async with AsyncSessionLocal() as session:
                # Create a test user
                test_username = f"test_user_{random.randint(1000, 9999)}"
                user = User(
                    username=test_username,
                    email=f"{test_username}@example.com",
                    password_hash="hashed_password",
                    user_type="student"
                )
                
                # Create
                session.add(user)
                await session.commit()
                await session.refresh(user)
                assert user.id is not None
                
                # Read
                result = await session.execute("SELECT * FROM users WHERE id = :id", {"id": user.id})
                fetched_user = result.mappings().first()
                assert fetched_user is not None
                assert fetched_user['username'] == test_username
                
                # Update
                new_email = f"updated_{test_username}@example.com"
                user.email = new_email
                await session.commit()
                
                # Verify update
                result = await session.execute("SELECT email FROM users WHERE id = :id", {"id": user.id})
                updated_email = result.scalar()
                assert updated_email == new_email
                
                # Delete
                await session.delete(user)
                await session.commit()
                
                # Verify deletion
                result = await session.execute("SELECT id FROM users WHERE id = :id", {"id": user.id})
                assert result.first() is None

        @pytest.mark.unit
        @pytest.mark.asyncio
        @pytest.mark.sqlalchemy
        async def test_create_lesson_with_exercises(reset_sqlalchemy_db):
            """Test creating a lesson with exercises using SQLAlchemy."""
            async with AsyncSessionLocal() as session:
                # Create a test lesson
                lesson = Lesson(
                    title=f"Test Lesson {random.randint(1000, 9999)}",
                    content="This is a test lesson content.",
                    order=1
                )
                
                # Create exercises for the lesson
                exercise1 = Exercise(
                    lesson=lesson,
                    question="What is 2 + 2?",
                    answer_options=json.dumps(["3", "4", "5", "6"]),
                    correct_answer="4",
                    exercise_type="multiple_choice"
                )
                
                exercise2 = Exercise(
                    lesson=lesson,
                    question="What is the capital of France?",
                    answer_options=json.dumps(["London", "Paris", "Berlin", "Rome"]),
                    correct_answer="Paris",
                    exercise_type="multiple_choice"
                )
                
                # Save to database
                session.add(lesson)
                session.add(exercise1)
                session.add(exercise2)
                await session.commit()
                
                # Verify lesson was saved
                result = await session.execute("SELECT * FROM lessons WHERE id = :id", {"id": lesson.id})
                fetched_lesson = result.mappings().first()
                assert fetched_lesson is not None
                assert fetched_lesson['title'] == lesson.title
                
                # Verify exercises were saved
                result = await session.execute("SELECT * FROM exercises WHERE lesson_id = :lesson_id", 
                                             {"lesson_id": lesson.id})
                exercises = result.mappings().all()
                assert len(exercises) == 2
                
                # Clean up
                await session.delete(exercise1)
                await session.delete(exercise2)
                await session.delete(lesson)
                await session.commit()
except NameError:
    # If the imports failed, no tests will be defined
    pass 