"""
Logging middleware for the FastAPI application.

This middleware logs HTTP requests and responses to provide insight into API usage and performance.
"""

import time
import json
from typing import Callable, Dict, Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from ..config import get_request_logger, get_error_logger

# Get loggers
request_logger = get_request_logger()
error_logger = get_error_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    
    This middleware logs the following information for each request:
    - HTTP method
    - URL
    - Status code
    - Response time
    - Client IP
    - User agent
    - Request headers (optional)
    - Response size
    """
    
    def __init__(self, app: ASGIApp, log_headers: bool = False):
        """
        Initialize the middleware.
        
        Args:
            app: ASGI application
            log_headers: Whether to log request headers (defaults to False for privacy)
        """
        super().__init__(app)
        self.log_headers = log_headers
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log information about it.
        
        Args:
            request: HTTP request
            call_next: Next middleware/route handler
            
        Returns:
            HTTP response
        """
        # Record start time
        start_time = time.time()
        
        # Extract request details
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Include request headers if enabled
        headers = dict(request.headers) if self.log_headers else {}
        
        # Initial log entry
        request_info = {
            "method": method,
            "url": url,
            "client_ip": client_ip,
            "user_agent": user_agent
        }
        
        # Log the request
        request_logger.info(f"Request started: {method} {url}", extra=request_info)
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Extract response details
            status_code = response.status_code
            response_size = int(response.headers.get("content-length", 0))
            
            # Create response log entry
            response_info = {
                **request_info,
                "status_code": status_code,
                "process_time_ms": round(process_time * 1000, 2),
                "response_size": response_size
            }
            
            # Log based on status code
            if 200 <= status_code < 300:
                request_logger.info(
                    f"Request completed: {method} {url} - {status_code} - {process_time:.2f}s",
                    extra=response_info
                )
            elif 400 <= status_code < 500:
                request_logger.warning(
                    f"Client error: {method} {url} - {status_code} - {process_time:.2f}s",
                    extra=response_info
                )
            elif status_code >= 500:
                error_logger.error(
                    f"Server error: {method} {url} - {status_code} - {process_time:.2f}s",
                    extra=response_info
                )
            else:
                request_logger.info(
                    f"Request completed: {method} {url} - {status_code} - {process_time:.2f}s",
                    extra=response_info
                )
            
            return response
            
        except Exception as e:
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log the exception
            error_info = {
                **request_info,
                "error": str(e),
                "process_time_ms": round(process_time * 1000, 2)
            }
            
            error_logger.exception(
                f"Request failed: {method} {url} - {str(e)} - {process_time:.2f}s",
                extra=error_info
            )
            
            # Re-raise the exception
            raise 