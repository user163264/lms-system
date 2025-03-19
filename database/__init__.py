#!/usr/bin/env python3

"""
Test submission system database package.

This package provides the data access layer for the test submission system.
It includes model classes, database management, and utility functions.
"""

from .db_manager import DBManager, get_db_params
from .models import (Model, ValidationError, Student, Exercise, Test, TestQuestion, 
                   StudentTest, Submission, SubmissionAnswer, Score)
from .services import TestService, SubmissionService
from .utils import (validate_email, validate_username, generate_secure_token,
                  create_session, validate_session, end_session,
                  generate_test_data, clean_test_data)

__all__ = [
    # DB Manager
    'DBManager', 'get_db_params',
    
    # Models
    'Model', 'ValidationError', 'Student', 'Exercise', 'Test', 'TestQuestion',
    'StudentTest', 'Submission', 'SubmissionAnswer', 'Score',
    
    # Services
    'TestService', 'SubmissionService',
    
    # Utilities
    'validate_email', 'validate_username', 'generate_secure_token',
    'create_session', 'validate_session', 'end_session',
    'generate_test_data', 'clean_test_data'
] 