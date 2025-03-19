"""
Configuration package for the LMS backend.

This package contains configuration modules for various aspects of the application,
including database settings, logging, and other application-wide configurations.
"""

# Import settings
from .settings import (
    # Database settings
    DATABASE_URL, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_ECHO,
    
    # API settings
    API_PREFIX, API_DEBUG, API_TITLE, API_VERSION, API_DESCRIPTION, API_HOST, API_PORT,
    
    # Frontend settings
    FRONTEND_HOST, FRONTEND_PORT, FRONTEND_URL,
    
    # CORS settings
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS,
    
    # Auth settings
    JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    
    # File storage settings
    UPLOAD_DIR, MAX_UPLOAD_SIZE,
    
    # Application settings
    APP_NAME, APP_ENVIRONMENT, TESTING,
    
    # Base directory
    BASE_DIR
)

# Import logging configuration
from .logging_config import (
    get_logger,
    get_request_logger,
    get_error_logger,
    get_db_logger,
    configure_logger,
    LOG_DIR,
    DEFAULT_LOG_LEVEL,
    STRUCTURED_LOGGING_CONFIG
)

# Import JSON formatter if available
try:
    from .json_formatter import (
        JSONFormatter,
        configure_structured_logging,
        add_extra_to_record
    )
    
    __all__ = [
        # Settings
        "DATABASE_URL", "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_ECHO",
        "API_PREFIX", "API_DEBUG", "API_TITLE", "API_VERSION", "API_DESCRIPTION", "API_HOST", "API_PORT",
        "FRONTEND_HOST", "FRONTEND_PORT", "FRONTEND_URL",
        "CORS_ORIGINS", "CORS_ALLOW_CREDENTIALS", "CORS_ALLOW_METHODS", "CORS_ALLOW_HEADERS",
        "JWT_SECRET_KEY", "JWT_ALGORITHM", "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "UPLOAD_DIR", "MAX_UPLOAD_SIZE",
        "APP_NAME", "APP_ENVIRONMENT", "TESTING",
        "BASE_DIR",
        
        # Logging
        "get_logger",
        "get_request_logger", 
        "get_error_logger",
        "get_db_logger",
        "configure_logger",
        "LOG_DIR",
        "DEFAULT_LOG_LEVEL",
        "STRUCTURED_LOGGING_CONFIG",
        "JSONFormatter",
        "configure_structured_logging",
        "add_extra_to_record"
    ]
except ImportError:
    # JSON formatter not available
    __all__ = [
        # Settings
        "DATABASE_URL", "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_ECHO",
        "API_PREFIX", "API_DEBUG", "API_TITLE", "API_VERSION", "API_DESCRIPTION", "API_HOST", "API_PORT",
        "FRONTEND_HOST", "FRONTEND_PORT", "FRONTEND_URL",
        "CORS_ORIGINS", "CORS_ALLOW_CREDENTIALS", "CORS_ALLOW_METHODS", "CORS_ALLOW_HEADERS",
        "JWT_SECRET_KEY", "JWT_ALGORITHM", "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "UPLOAD_DIR", "MAX_UPLOAD_SIZE",
        "APP_NAME", "APP_ENVIRONMENT", "TESTING",
        "BASE_DIR",
        
        # Logging
        "get_logger",
        "get_request_logger", 
        "get_error_logger",
        "get_db_logger",
        "configure_logger",
        "LOG_DIR",
        "DEFAULT_LOG_LEVEL",
        "STRUCTURED_LOGGING_CONFIG"
    ] 