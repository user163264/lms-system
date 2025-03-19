"""
Middleware package for the LMS backend.

This package contains middleware components for the FastAPI application.
"""

from .logging_middleware import RequestLoggingMiddleware

__all__ = ["RequestLoggingMiddleware"] 