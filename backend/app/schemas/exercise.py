"""
Exercise schemas for the LMS API.

This module defines the Pydantic schemas for exercise-related operations.
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field


class ExerciseBase(BaseModel):
    """Base schema for exercise data with common fields."""
    lesson_id: int
    title: Optional[str] = None
    exercise_type: str
    question: str
    instructions: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    correct_answer: Union[str, List[str], Dict[str, str]]
    max_score: Optional[int] = 1
    grading_type: Optional[str] = "auto"
    order_index: Optional[int] = 0
    is_required: Optional[bool] = True


class ExerciseCreate(ExerciseBase):
    """Schema for creating a new exercise."""
    pass


class ExerciseUpdate(BaseModel):
    """Schema for updating an existing exercise."""
    lesson_id: Optional[int] = None
    title: Optional[str] = None
    exercise_type: Optional[str] = None
    question: Optional[str] = None
    instructions: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    correct_answer: Optional[Union[str, List[str], Dict[str, str]]] = None
    max_score: Optional[int] = None
    grading_type: Optional[str] = None
    order_index: Optional[int] = None
    is_required: Optional[bool] = None


class ExerciseInDB(ExerciseBase):
    """Schema for exercise data as stored in the database."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Exercise(ExerciseInDB):
    """Schema for exercise data returned by the API."""
    # Hide correct answer in responses for security
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "lesson_id": 1,
                "title": "Multiple Choice Question",
                "exercise_type": "multiple_choice",
                "question": "What is the capital of France?",
                "options": {
                    "A": "London",
                    "B": "Paris",
                    "C": "Berlin",
                    "D": "Madrid"
                },
                "max_score": 1,
                "grading_type": "auto",
                "order_index": 1,
                "is_required": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }


class ExerciseWithoutAnswer(Exercise):
    """Exercise schema with the correct answer hidden."""
    class Config:
        orm_mode = True

    def __init__(self, **data):
        super().__init__(**data)
        object.__setattr__(self, "correct_answer", None)


class ExerciseTemplateItem(BaseModel):
    """Schema for an individual exercise in a template."""
    title: Optional[str] = None
    exercise_type: str
    question: str
    instructions: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    correct_answer: Union[str, List[str], Dict[str, str]]
    max_score: Optional[int] = 1
    grading_type: Optional[str] = "auto"
    is_required: Optional[bool] = True


class ExerciseTemplate(BaseModel):
    """Schema for creating multiple exercises at once."""
    lesson_id: int
    exercises: List[ExerciseTemplateItem] 