#!/usr/bin/env python3
"""
Consolidated exercise tests for the LMS system.
This combines functionality from:
- test_exercises.py (root)
- backend/test_exercises.py
- backend/tests/test_exercises.py
"""

import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import text
import os

# Import models and enums
from app.models.exercise import ExerciseTemplate, ExerciseType, ExerciseContent
from app.models import Exercise, User, Base

# Test database URL - using in-memory SQLite for unit tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="function")
async def engine():
    """Create a test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Close engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def session(engine):
    """Create a test database session."""
    # Create session factory
    TestingSessionLocal = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    
    # Create a session
    async with TestingSessionLocal() as session:
        yield session

class TestExerciseModel:
    """Tests for the Exercise model"""
    
    @pytest.mark.asyncio
    async def test_list_exercises(self, session):
        """Test listing all exercises"""
        # Create a test exercise
        exercise = Exercise(
            title="Test Exercise",
            content="Test content",
            exercise_type="multiple_choice",
            points=10
        )
        session.add(exercise)
        await session.commit()
        
        # Query exercises
        result = await session.execute(select(Exercise))
        exercises = result.scalars().all()
        
        # Validate results
        assert len(exercises) >= 1, "Should have at least one exercise"
        assert exercises[0].title == "Test Exercise", "Exercise title mismatch"
        assert exercises[0].exercise_type == "multiple_choice", "Exercise type mismatch"
        assert exercises[0].points == 10, "Exercise points mismatch"
    
    @pytest.mark.asyncio
    async def test_exercise_crud(self, session):
        """Test CRUD operations for Exercise model"""
        # Create
        exercise = Exercise(
            title="CRUD Test Exercise",
            content="Test content for CRUD",
            exercise_type="fill_in_blank",
            points=5
        )
        session.add(exercise)
        await session.commit()
        await session.refresh(exercise)
        
        exercise_id = exercise.id
        assert exercise_id is not None, "Exercise ID should be assigned"
        
        # Read
        result = await session.execute(
            select(Exercise).where(Exercise.id == exercise_id)
        )
        retrieved_exercise = result.scalars().first()
        assert retrieved_exercise is not None, "Should retrieve the exercise"
        assert retrieved_exercise.title == "CRUD Test Exercise", "Retrieved title mismatch"
        
        # Update
        retrieved_exercise.title = "Updated Exercise"
        retrieved_exercise.points = 8
        await session.commit()
        
        # Verify update
        result = await session.execute(
            select(Exercise).where(Exercise.id == exercise_id)
        )
        updated_exercise = result.scalars().first()
        assert updated_exercise.title == "Updated Exercise", "Title not updated"
        assert updated_exercise.points == 8, "Points not updated"
        
        # Delete
        await session.delete(updated_exercise)
        await session.commit()
        
        # Verify deletion
        result = await session.execute(
            select(Exercise).where(Exercise.id == exercise_id)
        )
        deleted_exercise = result.scalars().first()
        assert deleted_exercise is None, "Exercise not deleted"

class TestExerciseTemplates:
    """Tests for the ExerciseTemplate model"""
    
    @pytest.mark.asyncio
    async def test_create_templates(self, session):
        """Test creating exercise templates with different types"""
        # Create a word scramble template
        word_scramble_template = ExerciseTemplate(
            name="Word Scramble Template",
            type=ExerciseType.WORD_SCRAMBLE,
            validation_rules={"case_sensitive": False},
            scoring_mechanism={"points_per_correct": 1},
            display_parameters={"time_limit": 60, "show_hints": True}
        )
        
        # Create a multiple choice template
        multiple_choice_template = ExerciseTemplate(
            name="Multiple Choice Template",
            type=ExerciseType.MULTIPLE_CHOICE,
            validation_rules={"allow_multiple": False},
            scoring_mechanism={"correct_points": 1, "incorrect_points": 0},
            display_parameters={"randomize_options": True, "show_feedback": True}
        )
        
        # Add templates to session
        session.add(word_scramble_template)
        session.add(multiple_choice_template)
        await session.commit()
        
        # Refresh to get IDs
        await session.refresh(word_scramble_template)
        await session.refresh(multiple_choice_template)
        
        # Verify they have IDs
        assert word_scramble_template.id is not None
        assert multiple_choice_template.id is not None
        
        # Retrieve templates to verify creation
        result = await session.execute(
            select(ExerciseTemplate).order_by(ExerciseTemplate.name)
        )
        templates = result.scalars().all()
        
        assert len(templates) >= 2, "Should have at least two templates"
        assert templates[1].name == "Word Scramble Template", "Template name mismatch"
        assert templates[1].type == ExerciseType.WORD_SCRAMBLE, "Template type mismatch"
        assert templates[0].name == "Multiple Choice Template", "Template name mismatch"
        assert templates[0].type == ExerciseType.MULTIPLE_CHOICE, "Template type mismatch"

class TestExerciseContent:
    """Tests for the ExerciseContent model"""
    
    @pytest.mark.asyncio
    async def test_create_content_for_template(self, session):
        """Test creating exercise content based on a template"""
        # First create a template
        template = ExerciseTemplate(
            name="Word Scramble Test",
            type=ExerciseType.WORD_SCRAMBLE,
            validation_rules={"case_sensitive": False},
            scoring_mechanism={"points_per_correct": 1},
            display_parameters={"time_limit": 60}
        )
        session.add(template)
        await session.commit()
        await session.refresh(template)
        
        # Create content using the template
        content = ExerciseContent(
            template_id=template.id,
            title="Word Scramble Exercise",
            instructions="Unscramble the letters to form a valid word.",
            question_text="mputcoer",
            correct_answers=["computer"],
            difficulty_level=2,
            tags=["computer", "technology"],
            subject_area="IT"
        )
        
        session.add(content)
        await session.commit()
        await session.refresh(content)
        
        # Verify content was created with correct template relationship
        assert content.id is not None, "Content should have an ID"
        assert content.template_id == template.id, "Template ID mismatch"
        
        # Retrieve content by template
        result = await session.execute(
            select(ExerciseContent).where(ExerciseContent.template_id == template.id)
        )
        retrieved_content = result.scalars().first()
        
        assert retrieved_content is not None, "Content should be retrievable"
        assert retrieved_content.title == "Word Scramble Exercise", "Content title mismatch"
        assert retrieved_content.question_text == "mputcoer", "Question text mismatch"
        assert "computer" in retrieved_content.correct_answers, "Correct answer mismatch"

    @pytest.mark.asyncio
    async def test_exercise_relationships(self, session):
        """Test relationships between exercises, templates, and content"""
        # Create a user (teacher)
        teacher = User(
            username="teacher",
            email="teacher@example.com",
            password_hash="hash",
            user_type="teacher"
        )
        session.add(teacher)
        await session.commit()
        
        # Create a template
        template = ExerciseTemplate(
            name="Quiz Template",
            type=ExerciseType.QUIZ,
            validation_rules={"pass_threshold": 70},
            scoring_mechanism={"points_per_question": 10},
            created_by=teacher.id
        )
        session.add(template)
        await session.commit()
        
        # Create multiple content items using the template
        contents = []
        for i in range(3):
            content = ExerciseContent(
                template_id=template.id,
                title=f"Quiz Question {i+1}",
                question_text=f"What is {i+1} + {i+1}?",
                correct_answers=[str((i+1)*2)],
                created_by=teacher.id
            )
            contents.append(content)
        
        session.add_all(contents)
        await session.commit()
        
        # Query to verify the relationship
        # Using raw SQL to demonstrate relationships
        result = await session.execute(text("""
            SELECT t.name as template_name, COUNT(c.id) as content_count
            FROM exercise_templates t
            JOIN exercise_contents c ON t.id = c.template_id
            GROUP BY t.name
        """))
        
        data = result.mappings().all()
        assert len(data) > 0, "Should have template data"
        
        # The first template should have content count of at least 3
        assert data[0]['template_name'] == "Quiz Template", "Template name mismatch"
        assert data[0]['content_count'] >= 3, "Should have at least 3 content items" 