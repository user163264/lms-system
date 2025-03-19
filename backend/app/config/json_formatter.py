"""
JSON formatter for structured logging.

This module provides a JSON formatter for logging that outputs log records as JSON objects,
making them easier to parse and analyze by log management systems.
"""

import json
import logging
import traceback
from datetime import datetime
import socket
import os
from typing import Dict, Any, Optional


class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs log records as JSON objects.
    
    This formatter converts standard Python log records into JSON-formatted strings,
    including all standard fields plus any extra fields provided in the log record.
    """
    
    def __init__(self, include_hostname: bool = True):
        """
        Initialize the formatter.
        
        Args:
            include_hostname: Whether to include the hostname in log records
        """
        super().__init__()
        self.include_hostname = include_hostname
        self.hostname = socket.gethostname() if include_hostname else None
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON string.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON-formatted string
        """
        # Base log data
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread
        }
        
        # Add optional hostname
        if self.include_hostname:
            log_data["hostname"] = self.hostname
        
        # Add environment information
        log_data["environment"] = os.environ.get("LMS_ENVIRONMENT", "development")
            
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields from the record
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Include all extra attributes from the record
        for key, value in record.__dict__.items():
            if key not in log_data and not key.startswith("_") and key not in {
                "args", "exc_info", "exc_text", "stack_info", "created", "msecs",
                "relativeCreated", "funcName", "pathname", "processName", 
                "threadName", "msg", "levelno"
            }:
                # Only include JSON-serializable values
                try:
                    json.dumps({key: value})
                    log_data[key] = value
                except (TypeError, OverflowError):
                    log_data[key] = str(value)
        
        # Convert to JSON string
        return json.dumps(log_data)


def add_extra_to_record(logger: logging.Logger, extra: Dict[str, Any]) -> None:
    """
    Add extra fields to all log records produced by the logger.
    
    Args:
        logger: Logger to modify
        extra: Extra fields to add to all log records
    """
    # Create a filter to add extra fields
    class ExtraFilter(logging.Filter):
        def filter(self, record):
            for key, value in extra.items():
                setattr(record, key, value)
            return True
    
    # Add the filter to the logger
    logger.addFilter(ExtraFilter())


def configure_structured_logging(use_json: bool = True) -> None:
    """
    Configure all loggers to use structured logging.
    
    Args:
        use_json: Whether to use JSON formatting (if False, uses standard formatting)
    """
    if not use_json:
        return
    
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Create a JSON formatter
    json_formatter = JSONFormatter()
    
    # Update all handlers to use the JSON formatter
    for handler in root_logger.handlers:
        handler.setFormatter(json_formatter) 