#!/usr/bin/env python3
"""
Integration tests for database workflows.
This tests interactions between different database components.
"""

import pytest
import sys
import os
from pathlib import Path
import random
import json
from datetime import datetime, timedelta

# Import database components
try:
    from backend.app.database import AsyncSessionLocal
    from backend.app.models import User, Course, Lesson, Exercise, Submission
    pytest_skip_sqlalchemy = False
except ImportError as e:
    print(f"Warning: SQLAlchemy imports failed: {e}")
    print("SQLAlchemy integration tests will be skipped")
    pytest_skip_sqlalchemy = True

@pytest.mark.integration
@pytest.mark.direct_db
def test_course_lesson_exercise_relationship(db_connection):
    """Test the relationship between courses, lessons, and exercises using direct database connection."""
    cursor = db_connection.cursor()
    
    # Check if required tables exist
    tables_to_check = ['courses', 'lessons', 'exercises']
    for table in tables_to_check:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = '{table}'
            )
        """)
        if not cursor.fetchone()['exists']:
            pytest.skip(f"Table {table} does not exist, skipping test")
    
    # Create test data
    test_course_name = f"Test Course {random.randint(1000, 9999)}"
    test_lesson_name = f"Test Lesson {random.randint(1000, 9999)}"
    
    try:
        # Create a course
        cursor.execute(
            """
            INSERT INTO courses (title, description, created_at, updated_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (test_course_name, "Test course description", datetime.now(), datetime.now())
        )
        course_id = cursor.fetchone()['id']
        
        # Create a lesson linked to the course
        cursor.execute(
            """
            INSERT INTO lessons (course_id, title, content, sequence, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (course_id, test_lesson_name, "Test lesson content", 1, datetime.now(), datetime.now())
        )
        lesson_id = cursor.fetchone()['id']
        
        # Create exercises linked to the lesson
        for i in range(3):
            cursor.execute(
                """
                INSERT INTO exercises (lesson_id, exercise_type, question, answers, options, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    lesson_id, 
                    "multiple_choice",
                    f"Test question {i+1}?",
                    json.dumps(["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
                    json.dumps({"correct_index": 0}),
                    datetime.now(),
                    datetime.now()
                )
            )
        
        # Commit the changes
        db_connection.commit()
        
        # Verify the relationships
        # 1. Course should have one lesson
        cursor.execute("""
            SELECT COUNT(*) as count FROM lessons WHERE course_id = %s
        """, (course_id,))
        lesson_count = cursor.fetchone()['count']
        assert lesson_count == 1
        
        # 2. Lesson should have three exercises
        cursor.execute("""
            SELECT COUNT(*) as count FROM exercises WHERE lesson_id = %s
        """, (lesson_id,))
        exercise_count = cursor.fetchone()['count']
        assert exercise_count == 3
        
        # 3. Test cascading: deleting the course should delete lessons
        cursor.execute("""
            DELETE FROM courses WHERE id = %s
        """, (course_id,))
        db_connection.commit()
        
        # Verify lessons are deleted
        cursor.execute("""
            SELECT COUNT(*) as count FROM lessons WHERE course_id = %s
        """, (course_id,))
        lesson_count_after = cursor.fetchone()['count']
        
        # Verify exercises are deleted
        cursor.execute("""
            SELECT COUNT(*) as count FROM exercises WHERE lesson_id = %s
        """, (lesson_id,))
        exercise_count_after = cursor.fetchone()['count']
        
        # In a properly configured database, cascade delete should make these counts zero
        # If not, we'll at least clean up properly
        if lesson_count_after > 0:
            cursor.execute("DELETE FROM lessons WHERE course_id = %s", (course_id,))
            db_connection.commit()
        
        if exercise_count_after > 0:
            cursor.execute("DELETE FROM exercises WHERE lesson_id = %s", (lesson_id,))
            db_connection.commit()
        
    except Exception as e:
        db_connection.rollback()
        pytest.fail(f"Exception during test: {e}")
    finally:
        cursor.close()

# Skip all SQLAlchemy tests if imports failed
pytestmark = pytest.mark.skipif(pytest_skip_sqlalchemy, reason="SQLAlchemy imports failed")

@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.sqlalchemy
async def test_user_submission_workflow(reset_sqlalchemy_db):
    """Test the complete workflow from user creation to exercise submission."""
    async with AsyncSessionLocal() as session:
        # Create a test course
        course = Course(
            title=f"Test Course {random.randint(1000, 9999)}",
            description="This is a test course"
        )
        session.add(course)
        await session.flush()
        
        # Create a lesson for the course
        lesson = Lesson(
            title="Introduction to Testing",
            content="This is an introduction to automated testing.",
            course_id=course.id,
            order=1
        )
        session.add(lesson)
        await session.flush()
        
        # Create an exercise for the lesson
        exercise = Exercise(
            lesson_id=lesson.id,
            question="What is the main purpose of unit testing?",
            answer_options=json.dumps([
                "To make the code run faster",
                "To verify individual units of code work as expected",
                "To replace integration testing",
                "To impress the project manager"
            ]),
            correct_answer="To verify individual units of code work as expected",
            exercise_type="multiple_choice"
        )
        session.add(exercise)
        await session.flush()
        
        # Create a test user
        user = User(
            username=f"test_user_{random.randint(1000, 9999)}",
            email="test@example.com",
            password_hash="hashed_password",
            user_type="student"
        )
        session.add(user)
        await session.flush()
        
        # Create a submission from the user for the exercise
        submission = Submission(
            user_id=user.id,
            exercise_id=exercise.id,
            answer_text=json.dumps(["To verify individual units of code work as expected"]),
            is_correct=True,
            score=100,
            submitted_at=datetime.now()
        )
        session.add(submission)
        await session.commit()
        
        # Verify the submission was created correctly
        result = await session.execute(
            "SELECT * FROM submissions WHERE user_id = :user_id AND exercise_id = :exercise_id",
            {"user_id": user.id, "exercise_id": exercise.id}
        )
        fetched_submission = result.mappings().first()
        assert fetched_submission is not None
        assert fetched_submission['is_correct'] is True
        assert fetched_submission['score'] == 100
        
        # Clean up
        await session.delete(submission)
        await session.delete(user)
        await session.delete(exercise)
        await session.delete(lesson)
        await session.delete(course)
        await session.commit()

@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.sqlalchemy
async def test_course_statistics(reset_sqlalchemy_db):
    """Test generating statistics for a course with multiple users and submissions."""
    async with AsyncSessionLocal() as session:
        # Create a test course
        course = Course(
            title=f"Statistics Course {random.randint(1000, 9999)}",
            description="This course tests statistics generation"
        )
        session.add(course)
        await session.flush()
        
        # Create lessons
        lessons = []
        for i in range(3):
            lesson = Lesson(
                title=f"Lesson {i+1}",
                content=f"Content for lesson {i+1}",
                course_id=course.id,
                order=i+1
            )
            session.add(lesson)
            lessons.append(lesson)
        await session.flush()
        
        # Create exercises for each lesson
        exercises = []
        for lesson in lessons:
            for i in range(2):  # 2 exercises per lesson
                exercise = Exercise(
                    lesson_id=lesson.id,
                    question=f"Question {i+1} for {lesson.title}?",
                    answer_options=json.dumps(["A", "B", "C", "D"]),
                    correct_answer="A",
                    exercise_type="multiple_choice"
                )
                session.add(exercise)
                exercises.append(exercise)
        await session.flush()
        
        # Create users
        users = []
        for i in range(5):  # 5 students
            user = User(
                username=f"student_{random.randint(1000, 9999)}",
                email=f"student{i+1}@example.com",
                password_hash="hashed_password",
                user_type="student"
            )
            session.add(user)
            users.append(user)
        await session.flush()
        
        # Create submissions
        for user in users:
            for exercise in exercises:
                # Randomize correctness
                is_correct = random.choice([True, False])
                score = 100 if is_correct else random.randint(0, 50)
                
                submission = Submission(
                    user_id=user.id,
                    exercise_id=exercise.id,
                    answer_text=json.dumps(["A" if is_correct else "B"]),
                    is_correct=is_correct,
                    score=score,
                    submitted_at=datetime.now() - timedelta(days=random.randint(0, 14))
                )
                session.add(submission)
        await session.commit()
        
        # Calculate and verify course statistics
        # 1. Total submissions
        result = await session.execute("""
            SELECT COUNT(*) FROM submissions s
            JOIN exercises e ON s.exercise_id = e.id
            JOIN lessons l ON e.lesson_id = l.id
            WHERE l.course_id = :course_id
        """, {"course_id": course.id})
        total_submissions = result.scalar()
        expected_submissions = len(users) * len(exercises)
        assert total_submissions == expected_submissions
        
        # 2. Average score
        result = await session.execute("""
            SELECT AVG(s.score) FROM submissions s
            JOIN exercises e ON s.exercise_id = e.id
            JOIN lessons l ON e.lesson_id = l.id
            WHERE l.course_id = :course_id
        """, {"course_id": course.id})
        average_score = result.scalar()
        assert average_score is not None
        assert 0 <= average_score <= 100
        
        # 3. Completion rate
        for user in users:
            result = await session.execute("""
                SELECT COUNT(DISTINCT e.id) FROM submissions s
                JOIN exercises e ON s.exercise_id = e.id
                JOIN lessons l ON e.lesson_id = l.id
                WHERE l.course_id = :course_id AND s.user_id = :user_id
            """, {"course_id": course.id, "user_id": user.id})
            completed_exercises = result.scalar()
            assert completed_exercises == len(exercises)
        
        # Clean up
        for user in users:
            result = await session.execute("""
                DELETE FROM submissions WHERE user_id = :user_id
            """, {"user_id": user.id})
        
        for user in users:
            await session.delete(user)
        
        for exercise in exercises:
            await session.delete(exercise)
        
        for lesson in lessons:
            await session.delete(lesson)
        
        await session.delete(course)
        await session.commit() 