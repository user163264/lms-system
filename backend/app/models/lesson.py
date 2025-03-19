"""
Lesson model definitions for the LMS.

This module defines the Lesson model and related entities.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class Lesson(Base):
    """
    Lesson model representing educational content in the LMS.
    
    A lesson contains educational content and can be part of a course.
    It may have multiple exercises associated with it.
    """
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    description = Column(String(500), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    order_index = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    exercises = relationship("Exercise", back_populates="lesson")
    course = relationship("Course", back_populates="lessons")
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}')>" 