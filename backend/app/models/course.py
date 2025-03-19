"""
Course model definitions for the LMS.

This module defines the Course model and related entities for course management.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


# Association table for course tags
course_tags = Table(
    'course_tags',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Course(Base):
    """
    Course model representing a collection of lessons in the LMS.
    
    A course contains multiple lessons and can have multiple enrolled students.
    """
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=False)
    cover_image = Column(String(255), nullable=True)
    difficulty_level = Column(String(20), default="beginner")
    estimated_duration = Column(Integer, nullable=True)  # in minutes
    prerequisites = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("CourseEnrollment", back_populates="course")
    instructor = relationship("User")
    tags = relationship("Tag", secondary=course_tags, back_populates="courses")
    
    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}')>"


class CourseEnrollment(Base):
    """
    CourseEnrollment model tracking student enrollment in courses.
    
    This model links users to courses they are enrolled in and tracks their progress.
    """
    __tablename__ = "course_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    progress = Column(Integer, default=0)  # percentage complete
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    def __repr__(self):
        return f"<CourseEnrollment(user_id={self.user_id}, course_id={self.course_id})>"


class Tag(Base):
    """
    Tag model for categorizing courses.
    
    Tags can be used to organize and filter courses by topic.
    """
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationships
    courses = relationship("Course", secondary=course_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>" 