"""
SQLAlchemy models for the LMS backend.

This package contains all database models for the LMS organized by domain.
"""

from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

# Import all models
from .lesson import Lesson
from .exercise import Exercise
from .submission import Submission
from .user import User
from .course import Course, CourseEnrollment

# For convenience, export all models
__all__ = [
    'Base',
    'Lesson',
    'Exercise',
    'Submission',
    'User',
    'Course',
    'CourseEnrollment'
] 