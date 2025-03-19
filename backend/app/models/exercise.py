"""
Exercise model definitions for the LMS.

This module defines the Exercise model and related entities.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class Exercise(Base):
    """
    Exercise model representing a learning activity or assessment.
    
    An exercise is typically associated with a lesson and can have 
    multiple student submissions.
    """
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(255), nullable=True)
    exercise_type = Column(String(50), nullable=False)
    question = Column(Text, nullable=False)
    instructions = Column(Text, nullable=True)
    options = Column(JSON, nullable=True)
    correct_answer = Column(JSON, nullable=False)
    max_score = Column(Integer, default=1)
    grading_type = Column(String(20), default="auto")
    order_index = Column(Integer, default=0)
    is_required = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lesson = relationship("Lesson", back_populates="exercises")
    submissions = relationship("Submission", back_populates="exercise")
    
    def __repr__(self):
        return f"<Exercise(id={self.id}, type='{self.exercise_type}')>"

# Submission model for user exercise submissions
class Submission(Base):
    """Model for user exercise submissions"""
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    user_answer = Column(String(500), nullable=False)
    score = Column(Float, nullable=False, default=0)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Submission(id={self.id}, user_id={self.user_id}, score={self.score})>"

class ExerciseTemplate(Base):
    """Exercise template model for storing reusable exercise structures"""
    __tablename__ = "exercise_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ExerciseType), nullable=False)
    validation_rules = Column(JSON, nullable=True)
    scoring_mechanism = Column(JSON, nullable=True)
    display_parameters = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with ExerciseContent
    exercises = relationship("ExerciseContent", back_populates="template")
    
    def __repr__(self):
        return f"<ExerciseTemplate(id={self.id}, name='{self.name}', type='{self.type}')>"

class ExerciseContent(Base):
    """Exercise content model for storing specific exercise instances"""
    __tablename__ = "exercise_content"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("exercise_templates.id"), nullable=False)
    title = Column(String(255), nullable=False)
    instructions = Column(Text, nullable=True)
    question_text = Column(Text, nullable=False)
    correct_answers = Column(JSON, nullable=False)  # Store as JSON array
    alternate_answers = Column(JSON, nullable=True)  # Store as JSON array
    difficulty_level = Column(Integer, nullable=False, default=1)
    tags = Column(ARRAY(String), nullable=True)
    subject_area = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    template = relationship("ExerciseTemplate", back_populates="exercises")
    media_assets = relationship("MediaAsset", back_populates="exercise_content")
    user_responses = relationship("UserResponse", back_populates="exercise_content")
    
    def __repr__(self):
        return f"<ExerciseContent(id={self.id}, title='{self.title}', difficulty={self.difficulty_level})>"

class MediaAsset(Base):
    """Media asset model for storing references to media used in exercises"""
    __tablename__ = "media_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    exercise_content_id = Column(Integer, ForeignKey("exercise_content.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    asset_type = Column(String(50), nullable=False)  # image, audio, video
    alt_text = Column(String(255), nullable=True)
    caption = Column(Text, nullable=True)
    license_info = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with ExerciseContent
    exercise_content = relationship("ExerciseContent", back_populates="media_assets")
    
    def __repr__(self):
        return f"<MediaAsset(id={self.id}, type='{self.asset_type}', file='{self.file_path}')>"

class UserResponse(Base):
    """User response model for tracking user interactions with exercises"""
    __tablename__ = "user_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)  # No foreign key for now
    exercise_content_id = Column(Integer, ForeignKey("exercise_content.id"), nullable=False)
    response_data = Column(JSON, nullable=False)  # Store as JSON
    score = Column(Integer, nullable=True)
    completion_status = Column(String(20), nullable=False, default="started")  # started, completed, abandoned
    attempt_number = Column(Integer, nullable=False, default=1)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    exercise_content = relationship("ExerciseContent", back_populates="user_responses")
    
    def __repr__(self):
        return f"<UserResponse(id={self.id}, user_id={self.user_id}, score={self.score}, status='{self.completion_status}')>" 