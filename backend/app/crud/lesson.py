"""
CRUD operations for Lesson models.

This module contains database operations for managing lessons.
"""

from typing import List, Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ..models import Lesson
from ..schemas import lesson as schemas
from ..config import get_logger

# Initialize logger
logger = get_logger("crud.lesson")


async def get_lessons(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    course_id: Optional[int] = None
) -> List[Lesson]:
    """
    Get all lessons, with optional filtering by course.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        course_id: Optional course ID to filter by
        
    Returns:
        List of Lesson objects
    """
    query = select(Lesson)
    
    if course_id is not None:
        query = query.where(Lesson.course_id == course_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_lesson(
    db: AsyncSession, 
    lesson_id: int,
    with_exercises: bool = False
) -> Optional[Lesson]:
    """
    Get a specific lesson by ID.
    
    Args:
        db: Database session
        lesson_id: ID of the lesson to retrieve
        with_exercises: Whether to load related exercises
        
    Returns:
        Lesson object if found, None otherwise
    """
    query = select(Lesson).where(Lesson.id == lesson_id)
    
    if with_exercises:
        query = query.options(selectinload(Lesson.exercises))
    
    result = await db.execute(query)
    return result.scalars().first()


async def create_lesson(
    db: AsyncSession, 
    lesson: schemas.LessonCreate
) -> Lesson:
    """
    Create a new lesson.
    
    Args:
        db: Database session
        lesson: Lesson data to create
        
    Returns:
        Created Lesson object
    """
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    await db.commit()
    await db.refresh(db_lesson)
    logger.info(f"Created lesson: {db_lesson.id} - {db_lesson.title}")
    return db_lesson


async def update_lesson(
    db: AsyncSession, 
    lesson_id: int, 
    lesson_data: schemas.LessonUpdate
) -> Optional[Lesson]:
    """
    Update an existing lesson.
    
    Args:
        db: Database session
        lesson_id: ID of the lesson to update
        lesson_data: Updated lesson data
        
    Returns:
        Updated Lesson object if found, None otherwise
    """
    # First make sure the lesson exists
    db_lesson = await get_lesson(db, lesson_id)
    if not db_lesson:
        logger.warning(f"Attempted to update non-existent lesson: {lesson_id}")
        return None
    
    # Filter out None values
    update_data = {k: v for k, v in lesson_data.dict().items() if v is not None}
    
    # Update the lesson
    query = (
        update(Lesson)
        .where(Lesson.id == lesson_id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    
    # Commit and refresh
    await db.commit()
    
    # Re-fetch the lesson
    db_lesson = await get_lesson(db, lesson_id)
    logger.info(f"Updated lesson: {db_lesson.id} - {db_lesson.title}")
    return db_lesson


async def delete_lesson(
    db: AsyncSession, 
    lesson_id: int
) -> bool:
    """
    Delete a lesson by ID.
    
    Args:
        db: Database session
        lesson_id: ID of the lesson to delete
        
    Returns:
        True if the lesson was deleted, False otherwise
    """
    # Check if the lesson exists
    db_lesson = await get_lesson(db, lesson_id)
    if not db_lesson:
        logger.warning(f"Attempted to delete non-existent lesson: {lesson_id}")
        return False
    
    # Delete the lesson
    query = delete(Lesson).where(Lesson.id == lesson_id)
    await db.execute(query)
    await db.commit()
    
    logger.info(f"Deleted lesson: {lesson_id}")
    return True 