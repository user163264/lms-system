"""
Routes for client-side logging.

This module defines routes for receiving and processing log messages
from client-side applications like the frontend.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

from ..config import get_logger, get_error_logger

# Create router
router = APIRouter()

# Get loggers
logger = get_logger("routes.logs")
client_logger = get_logger("client")
client_error_logger = get_error_logger()


class ClientLogEntry(BaseModel):
    """Model for client-side log entries."""
    timestamp: Optional[str] = Field(None, description="Log timestamp")
    level: str = Field(..., description="Log level")
    module: Optional[str] = Field(None, description="Source module")
    message: str = Field(..., description="Log message")
    browser: Optional[Dict[str, Any]] = Field(None, description="Browser information")


@router.post("/logs", status_code=200)
async def receive_client_logs(log_entry: ClientLogEntry, request: Request):
    """
    Receive and process log messages from client-side applications.
    
    Args:
        log_entry: Log entry from client
        request: HTTP request
        
    Returns:
        Acknowledgement message
    """
    # Add client IP address to the log entry
    client_ip = request.client.host if request.client else "unknown"
    
    # Determine log level and route to appropriate logger
    log_level = log_entry.level.upper()
    
    # Prepare extra data for structured logging
    extra_data = {
        "client_ip": client_ip,
        "module": log_entry.module or "client",
        "browser": log_entry.browser
    }
    
    # Log according to level
    if log_level in ("ERROR", "CRITICAL"):
        client_error_logger.error(log_entry.message, extra=extra_data)
    elif log_level == "WARNING":
        client_logger.warning(log_entry.message, extra=extra_data)
    elif log_level == "INFO":
        client_logger.info(log_entry.message, extra=extra_data)
    elif log_level == "DEBUG":
        client_logger.debug(log_entry.message, extra=extra_data)
    else:
        # Default to info level
        client_logger.info(log_entry.message, extra=extra_data)
    
    return {"status": "received"} 