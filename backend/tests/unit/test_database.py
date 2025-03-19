#!/usr/bin/env python3
"""
Consolidated database tests for the LMS system.
This combines functionality from:
- test_database.py
- test_db_layer.py
- backend/app/test_db.py
- backend/app/simple_test_db.py
"""

import pytest
import asyncio
import sys
import os
import time
import random
import json
from datetime import datetime, timedelta
from sqlalchemy import text

# Import SQLAlchemy components
from app.database import engine as app_engine
from app.database import get_db, Base, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

# Import models
from app.models import User, Lesson, Exercise, Submission

# Import database layer components (if using direct psycopg2)
import psycopg2
from psycopg2.extras import RealDictCursor

# Direct database connection parameters
DB_PARAMS = {
    'host': 'localhost',
    'dbname': 'lms_db',
    'user': 'lms_user',
    'password': 'lms_password',
    'port': '5432'
}

# Test database URL for SQLAlchemy tests (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

#
# Direct Database Connection Tests
#

@pytest.mark.direct_db
def test_direct_connection():
    """Test direct database connection using psycopg2."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Simple query to test connection
        cur.execute("SELECT 1")
        result = cur.fetchone()
        
        # Close connection
        cur.close()
        conn.close()
        
        assert result[0] == 1, "Connection test query failed"
        return True
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
        return False

@pytest.mark.direct_db
def test_direct_crud_operations():
    """Test database CRUD operations directly using psycopg2."""
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_PARAMS)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Create: Insert a test student
        test_username = f"test_user_{int(time.time())}"
        test_email = f"test_{int(time.time())}@example.com"
        
        cur.execute("""
            INSERT INTO students (username, email, full_name, password_hash, created_at, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, [
            test_username,
            test_email,
            "Test User",
            "password_hash",
            datetime.now(),
            True
        ])
        
        student_id = cur.fetchone()['id']
        assert student_id is not None, "Failed to insert student"
        
        # Read: Select the student we just created
        cur.execute("SELECT * FROM students WHERE id = %s", [student_id])
        student = cur.fetchone()
        assert student is not None, "Failed to retrieve student"
        assert student['username'] == test_username, "Username mismatch"
        
        # Update: Update the student's name
        new_name = "Updated Test User"
        cur.execute("""
            UPDATE students 
            SET full_name = %s 
            WHERE id = %s
            RETURNING id
        """, [new_name, student_id])
        
        update_result = cur.fetchone()
        assert update_result is not None, "Failed to update student"
        
        # Verify update
        cur.execute("SELECT * FROM students WHERE id = %s", [student_id])
        updated_student = cur.fetchone()
        assert updated_student['full_name'] == new_name, "Update not applied"
        
        # Delete: Remove the test student
        cur.execute("DELETE FROM students WHERE id = %s RETURNING id", [student_id])
        delete_result = cur.fetchone()
        assert delete_result is not None, "Failed to delete student"
        
        # Verify deletion
        cur.execute("SELECT * FROM students WHERE id = %s", [student_id])
        deleted_student = cur.fetchone()
        assert deleted_student is None, "Student not deleted"
        
        # Close connection
        cur.close()
        conn.close()
        
        return True
    except Exception as e:
        pytest.fail(f"Error in direct database operations: {e}")
        return False

#
# SQLAlchemy ORM Tests
#

@pytest.fixture(scope="function")
async def reset_sqlalchemy_db():
    """Reset the SQLAlchemy database for testing."""
    async with app_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.mark.asyncio
async def test_sqlalchemy_connection(reset_sqlalchemy_db):
    """Test SQLAlchemy database connection."""
    async with AsyncSessionLocal() as session:
        # Execute a simple query
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        assert value == 1, "SQLAlchemy connection test failed"

@pytest.mark.asyncio
async def test_sqlalchemy_crud(reset_sqlalchemy_db):
    """Test SQLAlchemy CRUD operations."""
    async with AsyncSessionLocal() as session:
        # Create a user
        user = User(
            username="test_user",
            email="test_user@example.com",
            password_hash="test_password_hash",
            user_type="student"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        assert user.id is not None, "Failed to create user"
        
        # Read the user
        result = await session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user.id})
        user_data = result.mappings().one()
        assert user_data["username"] == "test_user", "Username mismatch"
        
        # Update the user
        await session.execute(
            text("UPDATE users SET email = :email WHERE id = :id"),
            {"email": "updated@example.com", "id": user.id}
        )
        await session.commit()
        
        # Verify update
        result = await session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user.id})
        updated_user = result.mappings().one()
        assert updated_user["email"] == "updated@example.com", "Email update failed"
        
        # Delete the user
        await session.execute(text("DELETE FROM users WHERE id = :id"), {"id": user.id})
        await session.commit()
        
        # Verify deletion
        result = await session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user.id})
        assert result.first() is None, "User was not deleted"

#
# Complex scenarios
#

@pytest.mark.asyncio
async def test_create_lesson_with_exercises(reset_sqlalchemy_db):
    """Test creating a lesson with associated exercises."""
    async with AsyncSessionLocal() as session:
        # Create a teacher
        teacher = User(
            username="teacher",
            email="teacher@example.com",
            password_hash="teacher_hash",
            user_type="teacher"
        )
        session.add(teacher)
        await session.commit()
        
        # Create a lesson
        lesson = Lesson(
            title="Test Lesson",
            description="This is a test lesson",
            owner_id=teacher.id
        )
        session.add(lesson)
        await session.commit()
        
        # Create exercises for the lesson
        exercises = [
            Exercise(
                title=f"Exercise {i}",
                content=f"Content for exercise {i}",
                lesson_id=lesson.id,
                exercise_type="multiple_choice",
                points=10
            )
            for i in range(1, 4)
        ]
        
        session.add_all(exercises)
        await session.commit()
        
        # Query to verify
        result = await session.execute(
            text("SELECT COUNT(*) FROM exercises WHERE lesson_id = :lesson_id"),
            {"lesson_id": lesson.id}
        )
        exercise_count = result.scalar()
        assert exercise_count == 3, "Exercise count doesn't match"
        
        # Query lesson with exercises
        result = await session.execute(
            text("""
                SELECT l.title as lesson_title, e.title as exercise_title
                FROM lessons l
                JOIN exercises e ON l.id = e.lesson_id
                WHERE l.id = :lesson_id
                ORDER BY e.id
            """),
            {"lesson_id": lesson.id}
        )
        
        lesson_exercises = result.mappings().all()
        assert len(lesson_exercises) == 3, "Incorrect number of exercises joined with lesson"
        assert lesson_exercises[0]["lesson_title"] == "Test Lesson", "Lesson title mismatch"
        assert lesson_exercises[0]["exercise_title"] == "Exercise 1", "Exercise title mismatch" 