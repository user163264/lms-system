"""
Validation utilities for the LMS backend.

This module provides functions for validating user input such as emails, passwords, etc.
"""

import re
from typing import Tuple, Optional

# Email validation regex pattern - this is a simple pattern, can be adjusted as needed
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Password requirements
MIN_PASSWORD_LENGTH = 8
PASSWORD_REQUIREMENTS = [
    (lambda p: len(p) >= MIN_PASSWORD_LENGTH, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"),
    (lambda p: any(c.isupper() for c in p), "Password must contain at least one uppercase letter"),
    (lambda p: any(c.islower() for c in p), "Password must contain at least one lowercase letter"),
    (lambda p: any(c.isdigit() for c in p), "Password must contain at least one digit"),
    (lambda p: any(not c.isalnum() for c in p), "Password must contain at least one special character")
]


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if the email is valid, False otherwise
        - error_message: Error message if the email is invalid, None otherwise
    """
    if not email:
        return False, "Email cannot be empty"
    
    if len(email) > 255:
        return False, "Email is too long"
        
    if not re.match(EMAIL_PATTERN, email):
        return False, "Invalid email format"
        
    return True, None


def validate_password(password: str, 
                      skip_requirements: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate a password against requirements.
    
    Args:
        password: Password to validate
        skip_requirements: If True, only check that password is not empty
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if the password is valid, False otherwise
        - error_message: Error message if the password is invalid, None otherwise
    """
    if not password:
        return False, "Password cannot be empty"
        
    if skip_requirements:
        return True, None
        
    # Check all password requirements
    for check_func, error_msg in PASSWORD_REQUIREMENTS:
        if not check_func(password):
            return False, error_msg
            
    return True, None


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a username.
    
    Args:
        username: Username to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if the username is valid, False otherwise
        - error_message: Error message if the username is invalid, None otherwise
    """
    if not username:
        return False, "Username cannot be empty"
        
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
        
    if len(username) > 30:
        return False, "Username must be at most 30 characters long"
        
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
        
    return True, None


def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, Optional[str]]:
    """
    Validate a person's name.
    
    Args:
        name: Name to validate
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if the name is valid, False otherwise
        - error_message: Error message if the name is invalid, None otherwise
    """
    if not name:
        return False, f"{field_name} cannot be empty"
        
    if len(name) > 100:
        return False, f"{field_name} is too long"
        
    return True, None 