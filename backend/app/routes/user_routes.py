"""
User management routes for administrators.
"""
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.user import User
from ..schemas.user_schemas import User as UserSchema, UserCreate, UserUpdate
from ..crud import user_crud
from ..services.auth import (
    get_current_active_user,
    check_admin_permission,
    check_teacher_permission
)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    role: Optional[str] = Query(None, description="Filter by user role"),
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve users.
    
    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        search: Optional search term
        role: Optional role filter
        current_user: Current user with admin permissions
        db: Database session
        
    Returns:
        List of users
    """
    users = await user_crud.get_users(db, skip=skip, limit=limit, search=search, role=role)
    return users


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create new user.
    
    Args:
        user_data: User data
        current_user: Current user with admin permissions
        db: Database session
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If username or email already exists
    """
    try:
        user = await user_crud.create_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int,
    current_user: User = Depends(check_teacher_permission),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get a specific user by id.
    
    Args:
        user_id: User ID
        current_user: Current user with teacher or admin permissions
        db: Database session
        
    Returns:
        User data
        
    Raises:
        HTTPException: If user not found
    """
    user = await user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
        
    # Allow teachers to only see student profiles
    if current_user.role != "admin" and user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
        
    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update a user.
    
    Args:
        user_id: User ID
        user_data: User data for update
        current_user: Current user with admin permissions
        db: Database session
        
    Returns:
        Updated user data
        
    Raises:
        HTTPException: If user not found
    """
    user = await user_crud.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
        
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a user.
    
    Args:
        user_id: User ID
        current_user: Current user with admin permissions
        db: Database session
        
    Raises:
        HTTPException: If user not found
    """
    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users cannot delete their own account"
        )
        
    deleted = await user_crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        ) 