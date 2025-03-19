"""
Logging configuration for the LMS backend.

This module provides a centralized configuration for logging across the application,
including log formatting, handlers, and level configurations.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Base directory for all logs
LOG_DIR = Path(__file__).resolve().parents[3] / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log levels mapping from string to int
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

# Default log format
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Default log level from environment or fallback to INFO
DEFAULT_LOG_LEVEL = LOG_LEVELS.get(
    os.environ.get("LMS_LOG_LEVEL", "info").lower(),
    logging.INFO
)

# Enable console logging by default
CONSOLE_LOGGING_ENABLED = os.environ.get("LMS_CONSOLE_LOGGING", "true").lower() == "true"

# Maximum size of log files before rotation
MAX_LOG_SIZE = int(os.environ.get("LMS_MAX_LOG_SIZE", 10 * 1024 * 1024))  # 10 MB

# Maximum number of backup log files
MAX_LOG_BACKUPS = int(os.environ.get("LMS_MAX_LOG_BACKUPS", 5))

# File logging settings
FILE_LOGGING_CONFIG = {
    "enabled": os.environ.get("LMS_FILE_LOGGING", "true").lower() == "true",
    "rotation": os.environ.get("LMS_LOG_ROTATION", "size").lower(),  # 'size' or 'time'
    "when": os.environ.get("LMS_LOG_ROTATION_WHEN", "midnight").lower(),  # for time-based rotation
    "interval": int(os.environ.get("LMS_LOG_ROTATION_INTERVAL", 1)),  # for time-based rotation
}

# Structured logging settings
STRUCTURED_LOGGING_CONFIG = {
    "enabled": os.environ.get("LMS_STRUCTURED_LOGGING", "false").lower() == "true",
    "format": os.environ.get("LMS_STRUCTURED_LOG_FORMAT", "json").lower(),  # 'json' or 'text'
}

# Import JSON formatter if structured logging is enabled
if STRUCTURED_LOGGING_CONFIG["enabled"] and STRUCTURED_LOGGING_CONFIG["format"] == "json":
    try:
        from .json_formatter import JSONFormatter, configure_structured_logging
        json_formatter = JSONFormatter()
    except ImportError:
        print("WARNING: JSON formatter not available. Using text formatter instead.")
        STRUCTURED_LOGGING_CONFIG["enabled"] = False


def configure_logger(
    name: str,
    log_level: Optional[int] = None,
    log_format: str = DEFAULT_LOG_FORMAT,
    log_file: Optional[Union[str, Path]] = None,
    rotation_type: str = "size",  # 'size' or 'time'
    console: bool = CONSOLE_LOGGING_ENABLED,
    structured: Optional[bool] = None,  # Use STRUCTURED_LOGGING_CONFIG if None
) -> logging.Logger:
    """
    Configure a logger with the specified settings.
    
    Args:
        name: Name of the logger
        log_level: Log level (if None, uses DEFAULT_LOG_LEVEL)
        log_format: Format string for log messages
        log_file: Path to log file (if None, uses name parameter to generate filename)
        rotation_type: Type of log rotation ('size' or 'time')
        console: Whether to log to console
        structured: Whether to use structured logging (if None, uses STRUCTURED_LOGGING_CONFIG)
        
    Returns:
        Configured logger instance
    """
    # Use default log level if none specified
    if log_level is None:
        log_level = DEFAULT_LOG_LEVEL
    
    # Determine whether to use structured logging
    use_structured = STRUCTURED_LOGGING_CONFIG["enabled"] if structured is None else structured
    
    # Get or create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Clear existing handlers
    if logger.handlers:
        logger.handlers = []
    
    # Create formatter
    if use_structured and STRUCTURED_LOGGING_CONFIG["format"] == "json":
        formatter = json_formatter
    else:
        formatter = logging.Formatter(log_format)
    
    # Add file handler if file logging is enabled
    if FILE_LOGGING_CONFIG["enabled"]:
        # Create log file path if not provided
        if log_file is None:
            log_file = LOG_DIR / f"{name.replace('.', '_')}.log"
        
        # Ensure path is a Path object
        if isinstance(log_file, str):
            log_file = Path(log_file)
        
        # Ensure directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create appropriate handler based on rotation type
        if rotation_type == "size" or FILE_LOGGING_CONFIG["rotation"] == "size":
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=MAX_LOG_SIZE,
                backupCount=MAX_LOG_BACKUPS
            )
        else:  # time-based rotation
            file_handler = TimedRotatingFileHandler(
                log_file,
                when=FILE_LOGGING_CONFIG["when"],
                interval=FILE_LOGGING_CONFIG["interval"],
                backupCount=MAX_LOG_BACKUPS
            )
        
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Add console handler if enabled
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_logger(module_name: str) -> logging.Logger:
    """
    Get a configured logger for a module.
    
    Args:
        module_name: Name of the module
        
    Returns:
        Configured logger instance
    """
    # Use 'lms' prefix for all loggers for consistency
    if not module_name.startswith("lms."):
        logger_name = f"lms.{module_name}"
    else:
        logger_name = module_name
    
    # Configure based on the module name
    return configure_logger(
        name=logger_name,
        log_file=LOG_DIR / f"{logger_name.replace('.', '_')}.log"
    )


# Configure the root logger
def configure_root_logger():
    """Configure the root logger with basic settings."""
    root_logger = logging.getLogger()
    root_logger.setLevel(DEFAULT_LOG_LEVEL)
    
    # Determine whether to use structured logging
    use_structured = STRUCTURED_LOGGING_CONFIG["enabled"]
    
    # Create formatter
    if use_structured and STRUCTURED_LOGGING_CONFIG["format"] == "json":
        formatter = json_formatter
    else:
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
    
    # Root logger console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(DEFAULT_LOG_LEVEL)
    console_handler.setFormatter(formatter)
    
    # Add and configure file handler for the root logger
    file_handler = RotatingFileHandler(
        LOG_DIR / "lms.log",
        maxBytes=MAX_LOG_SIZE,
        backupCount=MAX_LOG_BACKUPS
    )
    file_handler.setLevel(DEFAULT_LOG_LEVEL)
    file_handler.setFormatter(formatter)
    
    # Clear existing handlers
    if root_logger.handlers:
        root_logger.handlers = []
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger


# Special loggers
def get_request_logger() -> logging.Logger:
    """Get logger specifically for HTTP requests."""
    return configure_logger(
        name="lms.api.requests",
        log_format="%(asctime)s - %(levelname)s - %(message)s",
        log_file=LOG_DIR / "requests.log",
        structured=True  # Always use structured logging for requests
    )


def get_error_logger() -> logging.Logger:
    """Get logger specifically for errors."""
    return configure_logger(
        name="lms.error",
        log_level=logging.ERROR,
        log_file=LOG_DIR / "error.log",
        structured=True  # Always use structured logging for errors
    )


def get_db_logger() -> logging.Logger:
    """Get logger specifically for database operations."""
    return configure_logger(
        name="lms.db",
        log_file=LOG_DIR / "database.log"
    )


# Enable structured logging if configured
if STRUCTURED_LOGGING_CONFIG["enabled"] and STRUCTURED_LOGGING_CONFIG["format"] == "json":
    try:
        from .json_formatter import configure_structured_logging
        configure_structured_logging()
    except ImportError:
        pass


# Initialize root logger
root_logger = configure_root_logger()


# Export commonly used loggers
__all__ = [
    "get_logger",
    "configure_logger",
    "get_request_logger",
    "get_error_logger",
    "get_db_logger",
    "LOG_DIR",
    "DEFAULT_LOG_LEVEL",
    "LOG_LEVELS",
    "STRUCTURED_LOGGING_CONFIG"
] 