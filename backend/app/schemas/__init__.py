"""
Pydantic schemas for the LMS backend.

This package contains all schema definitions for the LMS API.
"""

from . import lesson, exercise, submission, user, course

# Export modules for more readable imports
__all__ = [
    'lesson',
    'exercise',
    'submission',
    'user',
    'course'
]

# Define these directly to avoid circular imports
class SubmissionRequest(BaseModel):
    exercise_id: int
    user_id: int
    answer: str
    
class SubmissionResponse(BaseModel):
    message: str
    score: float

# Lesson schemas
class LessonBase(BaseModel):
    title: str
    description: str
    content: str
    
class LessonCreate(LessonBase):
    pass
    
class Lesson(LessonBase):
    id: int
    
    class Config:
        from_attributes = True
        
class LessonRequest(LessonBase):
    order: Optional[int] = None

# Basic Exercise schemas
class ExerciseBase(BaseModel):
    title: str
    description: Optional[str] = None
    exercise_type: str
    content: Dict[str, Any]
    correct_answer: List[str]
    max_score: int = 1
    grading_type: str = "auto"
    lesson_id: int
    
class ExerciseCreate(ExerciseBase):
    correct_order: Optional[List[str]] = None
    
class Exercise(ExerciseBase):
    id: int
    correct_order: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

# Submission schema
class SubmissionCreate(BaseModel):
    user_id: int
    exercise_id: int
    user_answer: str

# Template schema
class ExerciseRequest(BaseModel):
    title: str
    description: str
    content: Dict[str, Any]
    
class ExerciseTemplate(BaseModel):
    lesson_id: int
    exercises: List[ExerciseRequest]

# Export new schemas
from .exercise_schemas import (
    ExerciseTemplate as DetailedExerciseTemplate,
    ExerciseTemplateCreate,
    ExerciseTemplateUpdate,
    ExerciseContent,
    ExerciseContentCreate,
    ExerciseContentUpdate,
    MediaAsset,
    MediaAssetCreate,
    MediaAssetUpdate,
    UserResponse,
    UserResponseCreate,
    UserResponseUpdate,
    ExerciseWithContent,
    ExerciseContentWithMedia,
    ExerciseSubmission,
    ExerciseSubmissionResponse,
    ExerciseTypeEnum,
    CompletionStatusEnum
) 