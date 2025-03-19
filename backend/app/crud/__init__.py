"""
CRUD operations for the LMS backend.

This package contains all database operations organized by domain.
"""

# Import CRUD modules
from .lesson import get_lessons, get_lesson, create_lesson, update_lesson, delete_lesson
from .exercise import (
    get_exercises, get_exercise, create_exercise, update_exercise, delete_exercise,
    create_exercises_from_template
)
from .submission import create_submission, get_submissions, get_submission, grade_submission
from .user import (
    get_users, get_user, get_user_by_email, get_user_by_username,
    create_user, update_user, delete_user, authenticate_user
)
from .course import (
    get_courses, get_course, create_course, update_course, delete_course,
    enroll_user, get_enrollments, get_enrollment
)

# Export everything
__all__ = [
    # Lesson CRUD
    'get_lessons', 'get_lesson', 'create_lesson', 'update_lesson', 'delete_lesson',
    
    # Exercise CRUD
    'get_exercises', 'get_exercise', 'create_exercise', 'update_exercise', 'delete_exercise',
    'create_exercises_from_template',
    
    # Submission CRUD
    'create_submission', 'get_submissions', 'get_submission', 'grade_submission',
    
    # User CRUD
    'get_users', 'get_user', 'get_user_by_email', 'get_user_by_username',
    'create_user', 'update_user', 'delete_user', 'authenticate_user',
    
    # Course CRUD
    'get_courses', 'get_course', 'create_course', 'update_course', 'delete_course',
    'enroll_user', 'get_enrollments', 'get_enrollment'
] 