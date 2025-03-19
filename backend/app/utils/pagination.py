"""
Pagination utilities for the LMS backend.

This module provides functions for paginating query results.
"""

from typing import List, Dict, Any, TypeVar, Generic, Optional, Union
from math import ceil

import sqlalchemy
from sqlalchemy.orm import Query
from pydantic import BaseModel
from fastapi import Query as QueryParam

T = TypeVar('T')


class PaginationParams(BaseModel):
    """
    Pagination parameters for API endpoints.
    """
    page: int = 1
    page_size: int = 10
    sort_by: Optional[str] = None
    sort_desc: bool = False


class PageInfo(BaseModel):
    """
    Pagination information to be included in paginated responses.
    """
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard response format for paginated results.
    """
    items: List[T]
    page_info: PageInfo


def paginate_results(
    query: Union[Query, List[Any]],
    params: PaginationParams,
    model_to_dict: Optional[callable] = None
) -> PaginatedResponse:
    """
    Paginate SQLAlchemy query results or a list of items.
    
    Args:
        query: SQLAlchemy query or list of items to paginate
        params: Pagination parameters
        model_to_dict: Optional function to convert each result to a dictionary
        
    Returns:
        Paginated response with items and pagination info
    """
    # Validate pagination parameters
    page = max(1, params.page)
    page_size = max(1, min(100, params.page_size))  # Limit page_size to reasonable values
    
    # Handle different input types
    if isinstance(query, list):
        # For lists, we need to count, sort, and slice manually
        total = len(query)
        
        # Apply sorting if specified and items have the attribute
        if params.sort_by and hasattr(query[0], params.sort_by) if query else False:
            query.sort(
                key=lambda x: getattr(x, params.sort_by),
                reverse=params.sort_desc
            )
        
        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        items = query[start:end]
    else:
        # For SQLAlchemy queries
        total = query.count()
        
        # Apply sorting if specified
        if params.sort_by:
            sort_column = getattr(query.column_descriptions[0]['entity'], params.sort_by, None)
            if sort_column is not None:
                query = query.order_by(sort_column.desc() if params.sort_desc else sort_column)
        
        # Apply pagination
        items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # Calculate pagination info
    total_pages = ceil(total / page_size) if total > 0 else 1
    
    # Convert models to dictionaries if function provided
    if model_to_dict:
        items = [model_to_dict(item) for item in items]
    
    # Create page info
    page_info = PageInfo(
        total=total,
        page=page,
        page_size=page_size,
        pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return PaginatedResponse(items=items, page_info=page_info)


def get_pagination_params(
    page: int = QueryParam(1, ge=1, description="Page number"),
    page_size: int = QueryParam(10, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = QueryParam(None, description="Field to sort by"),
    sort_desc: bool = QueryParam(False, description="Sort in descending order")
) -> PaginationParams:
    """
    FastAPI dependency for pagination parameters.
    
    Args:
        page: Page number (starts at 1)
        page_size: Number of items per page
        sort_by: Field to sort by
        sort_desc: Whether to sort in descending order
        
    Returns:
        PaginationParams object
    """
    return PaginationParams(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_desc=sort_desc
    ) 