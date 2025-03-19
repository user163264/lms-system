"""
Pydantic schemas for exercise-related models
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Enum for exercise types
class ExerciseTypeEnum(str, Enum):
    WORD_SCRAMBLE = "word_scramble"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    TRUE_FALSE = "true_false"
    LONG_ANSWER = "long_answer"
    SYN_ANT = "syn_ant"
    SENTENCE_REORDERING = "sentence_reordering"
    MATCHING_WORDS = "matching_words" 
    SHORT_ANSWER = "short_answer"
    CLOZE_TEST = "cloze_test"
    COMPREHENSION = "comprehension"
    IMAGE_LABELING = "image_labeling"

# Exercise Template Schemas
class ExerciseTemplateBase(BaseModel):
    """Base schema for exercise template"""
    name: str
    type: ExerciseTypeEnum
    validation_rules: Optional[Dict[str, Any]] = None
    scoring_mechanism: Optional[Dict[str, Any]] = None
    display_parameters: Optional[Dict[str, Any]] = None

class ExerciseTemplateCreate(ExerciseTemplateBase):
    """Schema for creating an exercise template"""
    pass

class ExerciseTemplateUpdate(BaseModel):
    """Schema for updating an exercise template"""
    name: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None
    scoring_mechanism: Optional[Dict[str, Any]] = None
    display_parameters: Optional[Dict[str, Any]] = None

class ExerciseTemplate(ExerciseTemplateBase):
    """Schema for retrieved exercise template"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Exercise Content Schemas
class ExerciseContentBase(BaseModel):
    """Base schema for exercise content"""
    template_id: int
    title: str
    instructions: Optional[str] = None
    question_text: str
    correct_answers: List[Union[str, Dict[str, Any]]]
    alternate_answers: Optional[List[Union[str, Dict[str, Any]]]] = None
    difficulty_level: int = Field(1, ge=1, le=5)
    tags: Optional[List[str]] = None
    subject_area: Optional[str] = None

class ExerciseContentCreate(ExerciseContentBase):
    """Schema for creating exercise content"""
    pass

class ExerciseContentUpdate(BaseModel):
    """Schema for updating exercise content"""
    title: Optional[str] = None
    instructions: Optional[str] = None
    question_text: Optional[str] = None
    correct_answers: Optional[List[Union[str, Dict[str, Any]]]] = None
    alternate_answers: Optional[List[Union[str, Dict[str, Any]]]] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    tags: Optional[List[str]] = None
    subject_area: Optional[str] = None

class ExerciseContent(ExerciseContentBase):
    """Schema for retrieved exercise content"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Media Asset Schemas
class MediaAssetBase(BaseModel):
    """Base schema for media asset"""
    exercise_content_id: int
    file_path: str
    asset_type: str
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    license_info: Optional[str] = None

class MediaAssetCreate(MediaAssetBase):
    """Schema for creating a media asset"""
    pass

class MediaAssetUpdate(BaseModel):
    """Schema for updating a media asset"""
    file_path: Optional[str] = None
    asset_type: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    license_info: Optional[str] = None

class MediaAsset(MediaAssetBase):
    """Schema for retrieved media asset"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# User Response Schemas
class CompletionStatusEnum(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class UserResponseBase(BaseModel):
    """Base schema for user response"""
    user_id: int
    exercise_content_id: int
    response_data: Dict[str, Any]
    score: Optional[int] = None
    completion_status: CompletionStatusEnum = CompletionStatusEnum.STARTED
    attempt_number: int = 1

class UserResponseCreate(UserResponseBase):
    """Schema for creating a user response"""
    pass

class UserResponseUpdate(BaseModel):
    """Schema for updating a user response"""
    response_data: Optional[Dict[str, Any]] = None
    score: Optional[int] = None
    completion_status: Optional[CompletionStatusEnum] = None
    completed_at: Optional[datetime] = None

class UserResponse(UserResponseBase):
    """Schema for retrieved user response"""
    id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Full Exercise with Content and Media
class ExerciseWithContent(ExerciseTemplate):
    """Schema for exercise template with its content"""
    exercises: List[ExerciseContent] = []
    
    class Config:
        orm_mode = True

class ExerciseContentWithMedia(ExerciseContent):
    """Schema for exercise content with its media"""
    media_assets: List[MediaAsset] = []
    
    class Config:
        orm_mode = True

# Exercise submission schema
class ExerciseSubmission(BaseModel):
    """Schema for submitting an exercise response"""
    user_id: int
    exercise_content_id: int
    response_data: Dict[str, Any]
    completion_status: CompletionStatusEnum = CompletionStatusEnum.COMPLETED

class ExerciseSubmissionResponse(BaseModel):
    """Schema for exercise submission response"""
    message: str
    score: Optional[int] = None
    is_correct: bool
    feedback: Optional[str] = None 