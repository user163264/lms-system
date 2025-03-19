"""
CRUD operations for Exercise models.

This module contains database operations for managing exercises.
"""

import logging
from typing import List, Optional, Dict, Any, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ..models import Exercise, Lesson
from ..schemas import exercise as schemas
from ..utils.logging import get_app_logger

# Initialize logger
logger = get_app_logger("crud.exercise")


async def get_exercises(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    lesson_id: Optional[int] = None,
    exercise_type: Optional[str] = None
) -> List[Exercise]:
    """
    Get all exercises, with optional filtering.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        lesson_id: Optional lesson ID to filter by
        exercise_type: Optional exercise type to filter by
        
    Returns:
        List of Exercise objects
    """
    query = select(Exercise)
    
    if lesson_id is not None:
        query = query.where(Exercise.lesson_id == lesson_id)
    
    if exercise_type is not None:
        query = query.where(Exercise.exercise_type == exercise_type)
    
    query = query.offset(skip).limit(limit).order_by(Exercise.order_index)
    result = await db.execute(query)
    exercises = result.scalars().all()
    
    logger.info(f"Fetched {len(exercises)} exercises")
    return exercises


async def get_exercise(
    db: AsyncSession, 
    exercise_id: int,
    with_submissions: bool = False
) -> Optional[Exercise]:
    """
    Get a specific exercise by ID.
    
    Args:
        db: Database session
        exercise_id: ID of the exercise to retrieve
        with_submissions: Whether to load related submissions
        
    Returns:
        Exercise object if found, None otherwise
    """
    query = select(Exercise).where(Exercise.id == exercise_id)
    
    if with_submissions:
        query = query.options(selectinload(Exercise.submissions))
    
    result = await db.execute(query)
    return result.scalars().first()


async def create_exercise(
    db: AsyncSession, 
    exercise: schemas.ExerciseCreate
) -> Exercise:
    """
    Create a new exercise.
    
    Args:
        db: Database session
        exercise: Exercise data to create
        
    Returns:
        Created Exercise object
    """
    # Validate that the lesson exists
    result = await db.execute(select(Lesson).where(Lesson.id == exercise.lesson_id))
    lesson = result.scalars().first()
    
    if not lesson:
        logger.error(f"Cannot create exercise: lesson with ID {exercise.lesson_id} does not exist")
        raise ValueError(f"Lesson with ID {exercise.lesson_id} does not exist")
    
    # Create the exercise
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    await db.commit()
    await db.refresh(db_exercise)
    
    logger.info(f"Created exercise: {db_exercise.id} for lesson {db_exercise.lesson_id}")
    return db_exercise


async def create_exercises_from_template(
    db: AsyncSession, 
    template: schemas.ExerciseTemplate
) -> List[Exercise]:
    """
    Create multiple exercises from a template.
    
    Args:
        db: Database session
        template: Template containing multiple exercises to create
        
    Returns:
        List of created Exercise objects
    """
    # Validate that the lesson exists
    result = await db.execute(select(Lesson).where(Lesson.id == template.lesson_id))
    lesson = result.scalars().first()
    
    if not lesson:
        logger.error(f"Cannot create exercises: lesson with ID {template.lesson_id} does not exist")
        raise ValueError(f"Lesson with ID {template.lesson_id} does not exist")
    
    # Create exercises
    exercises = []
    for idx, exercise_data in enumerate(template.exercises):
        exercise_dict = exercise_data.dict()
        exercise_dict["lesson_id"] = template.lesson_id
        exercise_dict["order_index"] = idx
        
        db_exercise = Exercise(**exercise_dict)
        db.add(db_exercise)
        exercises.append(db_exercise)
    
    # Commit all exercises at once
    await db.commit()
    
    # Refresh all exercises
    for exercise in exercises:
        await db.refresh(exercise)
    
    logger.info(f"Created {len(exercises)} exercises for lesson {template.lesson_id}")
    return exercises


async def update_exercise(
    db: AsyncSession, 
    exercise_id: int, 
    exercise_data: schemas.ExerciseUpdate
) -> Optional[Exercise]:
    """
    Update an existing exercise.
    
    Args:
        db: Database session
        exercise_id: ID of the exercise to update
        exercise_data: Updated exercise data
        
    Returns:
        Updated Exercise object if found, None otherwise
    """
    # First make sure the exercise exists
    db_exercise = await get_exercise(db, exercise_id)
    if not db_exercise:
        logger.warning(f"Attempted to update non-existent exercise: {exercise_id}")
        return None
    
    # Filter out None values
    update_data = {k: v for k, v in exercise_data.dict().items() if v is not None}
    
    # Update the exercise
    query = (
        update(Exercise)
        .where(Exercise.id == exercise_id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    
    # Commit and refresh
    await db.commit()
    
    # Re-fetch the exercise
    db_exercise = await get_exercise(db, exercise_id)
    logger.info(f"Updated exercise: {db_exercise.id}")
    return db_exercise


async def delete_exercise(
    db: AsyncSession, 
    exercise_id: int
) -> bool:
    """
    Delete an exercise by ID.
    
    Args:
        db: Database session
        exercise_id: ID of the exercise to delete
        
    Returns:
        True if the exercise was deleted, False otherwise
    """
    # Check if the exercise exists
    db_exercise = await get_exercise(db, exercise_id)
    if not db_exercise:
        logger.warning(f"Attempted to delete non-existent exercise: {exercise_id}")
        return False
    
    # Delete the exercise
    query = delete(Exercise).where(Exercise.id == exercise_id)
    await db.execute(query)
    await db.commit()
    
    logger.info(f"Deleted exercise: {exercise_id}")
    return True 