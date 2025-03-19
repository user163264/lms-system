"""
Submission model definitions for the LMS.

This module defines the Submission model for tracking student responses to exercises.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class Submission(Base):
    """
    Submission model representing a student's response to an exercise.
    
    A submission tracks the student's answer, score, and feedback for an exercise.
    """
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    user_answer = Column(JSON, nullable=False)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    graded_by = Column(String(50), default="auto")
    attempt_number = Column(Integer, default=1)
    status = Column(String(20), default="submitted")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    exercise = relationship("Exercise", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
    
    def __repr__(self):
        return f"<Submission(id={self.id}, user_id={self.user_id}, exercise_id={self.exercise_id})>" 