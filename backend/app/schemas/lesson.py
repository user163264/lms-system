"""
Lesson schemas for the LMS API.

This module defines the Pydantic schemas for lesson-related operations.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class LessonBase(BaseModel):
    """Base schema for lesson data with common fields."""
    title: str
    content: str
    description: Optional[str] = None
    course_id: Optional[int] = None
    order_index: Optional[int] = 0
    is_published: Optional[bool] = False


class LessonCreate(LessonBase):
    """Schema for creating a new lesson."""
    pass


class LessonUpdate(BaseModel):
    """Schema for updating an existing lesson."""
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None
    order_index: Optional[int] = None
    is_published: Optional[bool] = None


class LessonInDB(LessonBase):
    """Schema for lesson data as stored in the database."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Lesson(LessonInDB):
    """Schema for lesson data returned by the API."""
    # Additional computed fields or relationships could be added here
    pass


class LessonWithExercises(Lesson):
    """Schema for lesson data with related exercises."""
    from .exercise import Exercise  # Import here to avoid circular imports
    exercises: List[Exercise] = [] 