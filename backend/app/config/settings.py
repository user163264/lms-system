"""
Central configuration module for the LMS application.

This module provides a unified way to access all application configuration settings.
Configuration values are loaded from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, cast

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parents[3]

# Type variable for generic functions
T = TypeVar('T')

# Helper functions for type conversion
def _get_env_bool(name: str, default: bool = False) -> bool:
    """Get a boolean value from an environment variable."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ('true', 'yes', '1', 't', 'y')

def _get_env_int(name: str, default: int) -> int:
    """Get an integer value from an environment variable."""
    value = os.environ.get(name)
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default

def _get_env_float(name: str, default: float) -> float:
    """Get a float value from an environment variable."""
    value = os.environ.get(name)
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default

def _get_env_list(name: str, default: List[str] = None, separator: str = ',') -> List[str]:
    """Get a list of values from an environment variable."""
    value = os.environ.get(name)
    if value is None:
        return default or []
    return [item.strip() for item in value.split(separator)]

def _get_env_str(name: str, default: str = "") -> str:
    """Get a string value from an environment variable."""
    value = os.environ.get(name)
    return value if value is not None else default

def _get_env_path(name: str, default: Path) -> Path:
    """Get a path value from an environment variable."""
    value = os.environ.get(name)
    return Path(value) if value is not None else default

# Database settings
DB_HOST = _get_env_str("LMS_DB_HOST", "localhost")
DB_PORT = _get_env_int("LMS_DB_PORT", 5432)
DB_NAME = _get_env_str("LMS_DB_NAME", "lms_db")
DB_USER = _get_env_str("LMS_DB_USER", "lms_user")
DB_PASSWORD = _get_env_str("LMS_DB_PASSWORD", "lms_password")
DB_ECHO = _get_env_bool("LMS_DB_ECHO", True)

# Construct the database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API Settings
API_PREFIX = _get_env_str("LMS_API_PREFIX", "/api")
API_DEBUG = _get_env_bool("LMS_API_DEBUG", True)
API_TITLE = _get_env_str("LMS_API_TITLE", "LMS API")
API_VERSION = _get_env_str("LMS_API_VERSION", "1.0.0")
API_DESCRIPTION = _get_env_str("LMS_API_DESCRIPTION", 
    "Learning Management System API for exercise generation and evaluation.")
API_HOST = _get_env_str("LMS_API_HOST", "0.0.0.0")
API_PORT = _get_env_int("LMS_API_PORT", 8000)

# Frontend Settings
FRONTEND_HOST = _get_env_str("LMS_FRONTEND_HOST", "localhost")
FRONTEND_PORT = _get_env_int("LMS_FRONTEND_PORT", 3000)
FRONTEND_URL = _get_env_str("LMS_FRONTEND_URL", f"http://{FRONTEND_HOST}:{FRONTEND_PORT}")

# CORS Settings - Updated to use FRONTEND_URL
CORS_ORIGINS = _get_env_list("LMS_CORS_ORIGINS", 
    [f"http://localhost:{FRONTEND_PORT}", "http://13.42.249.90", f"http://13.42.249.90:{FRONTEND_PORT}"])
CORS_ALLOW_CREDENTIALS = _get_env_bool("LMS_CORS_ALLOW_CREDENTIALS", True)
CORS_ALLOW_METHODS = _get_env_list("LMS_CORS_ALLOW_METHODS", 
    ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
CORS_ALLOW_HEADERS = _get_env_list("LMS_CORS_ALLOW_HEADERS", 
    ["*"])

# Auth Settings - JWT signing is security-sensitive but we'll keep defaults for now
# Note: SECRET_KEY should be overridden in production via environment variable
JWT_SECRET_KEY = _get_env_str("LMS_JWT_SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
JWT_ALGORITHM = _get_env_str("LMS_JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = _get_env_int("LMS_JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)

# File storage settings
UPLOAD_DIR = _get_env_path("LMS_UPLOAD_DIR", BASE_DIR / "uploads")
MAX_UPLOAD_SIZE = _get_env_int("LMS_MAX_UPLOAD_SIZE", 5 * 1024 * 1024)  # 5 MB

# Logging settings (reference existing config)
LOG_DIR = _get_env_path("LMS_LOG_DIR", BASE_DIR / "logs")
LOG_LEVEL = _get_env_str("LMS_LOG_LEVEL", "info").lower()
CONSOLE_LOGGING_ENABLED = _get_env_bool("LMS_CONSOLE_LOGGING", True)
FILE_LOGGING_ENABLED = _get_env_bool("LMS_FILE_LOGGING", True)
STRUCTURED_LOGGING_ENABLED = _get_env_bool("LMS_STRUCTURED_LOGGING", False)

# Application settings
APP_NAME = _get_env_str("LMS_APP_NAME", "Learning Management System")
APP_ENVIRONMENT = _get_env_str("LMS_ENVIRONMENT", "development")
TESTING = _get_env_bool("LMS_TESTING", False) 