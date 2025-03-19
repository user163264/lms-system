"""
Logging utilities for the LMS backend.

This module provides functions for working with logs in the application.
It serves as a backwards compatibility layer for existing code that uses this module.
"""

from ..config.logging_config import (
    get_logger as get_config_logger,
    get_request_logger as get_config_request_logger,
    get_error_logger,
    get_db_logger,
    LOG_DIR
)

# Re-export the functions from config.logging_config for backward compatibility
def setup_logger(name, log_level=None, log_file=None, console=True, log_format=None):
    """
    Backwards compatibility wrapper for configure_logger.
    
    This function exists for backward compatibility with existing code.
    New code should use get_logger() directly.
    
    Args:
        name: Name of the logger
        log_level: Log level
        log_file: Path to log file
        console: Whether to log to console
        log_format: Format string for log messages
        
    Returns:
        Configured logger instance
    """
    from ..config.logging_config import configure_logger
    
    return configure_logger(
        name=name,
        log_level=log_level,
        log_file=log_file,
        console=console,
        log_format=log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def get_app_logger(module_name):
    """
    Get a logger for an application module.
    
    This function exists for backward compatibility with existing code.
    New code should use get_logger() directly.
    
    Args:
        module_name: Name of the module
        
    Returns:
        Configured logger instance
    """
    return get_config_logger(module_name)


def get_request_logger():
    """
    Get a logger for HTTP requests.
    
    This function exists for backward compatibility with existing code.
    New code should use get_request_logger() from config.logging_config directly.
    
    Returns:
        Configured logger instance for HTTP requests
    """
    return get_config_request_logger()


# Constants for backward compatibility
LOGS_DIR = LOG_DIR


__all__ = [
    'setup_logger',
    'get_app_logger',
    'get_request_logger',
    'LOGS_DIR'
] 