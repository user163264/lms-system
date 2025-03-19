"""
Submission schemas for the LMS API.

This module defines the Pydantic schemas for submission-related operations.
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field


class SubmissionBase(BaseModel):
    """Base schema for submission data with common fields."""
    user_id: int
    exercise_id: int
    user_answer: Union[str, Dict, List]
    attempt_number: Optional[int] = 1


class SubmissionCreate(SubmissionBase):
    """Schema for creating a new submission."""
    pass


class SubmissionUpdate(BaseModel):
    """Schema for updating an existing submission."""
    score: Optional[float] = None
    feedback: Optional[str] = None
    graded_by: Optional[str] = None
    status: Optional[str] = None


class SubmissionInDB(SubmissionBase):
    """Schema for submission data as stored in the database."""
    id: int
    score: Optional[float] = None
    feedback: Optional[str] = None
    graded_by: Optional[str] = "auto"
    status: str = "submitted"
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Submission(SubmissionInDB):
    """Schema for submission data returned by the API."""
    pass


class SubmissionWithExercise(Submission):
    """Schema for submission data with related exercise."""
    from .exercise import ExerciseWithoutAnswer  # Import here to avoid circular imports
    exercise: Optional[ExerciseWithoutAnswer] = None


class SubmissionFeedback(BaseModel):
    """Schema for providing feedback on a submission."""
    feedback: str
    score: float
    graded_by: str = "instructor" 