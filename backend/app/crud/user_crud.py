"""
CRUD operations for user management
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, or_
from sqlalchemy.sql import func
from datetime import datetime

from ..models.user import User
from ..schemas import user_schemas as schemas
from ..services.auth import get_password_hash, verify_password


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Get a user by ID
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User object or None if not found
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    Get a user by username
    
    Args:
        db: Database session
        username: Username to search for
        
    Returns:
        User object or None if not found
    """
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get a user by email
    
    Args:
        db: Database session
        email: Email to search for
        
    Returns:
        User object or None if not found
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_users(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    role: Optional[str] = None
) -> List[User]:
    """
    Get all users with optional filtering
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        search: Optional search term for username, email, or full_name
        role: Optional role filter
        
    Returns:
        List of User objects
    """
    query = select(User)
    
    # Apply filters if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.username.ilike(search_term),
                User.email.ilike(search_term),
                User.full_name.ilike(search_term)
            )
        )
    
    if role:
        query = query.filter(User.role == role)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    return result.scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> User:
    """
    Create a new user
    
    Args:
        db: Database session
        user: User data for creation
        
    Returns:
        Created User object
    """
    # Check if username or email already exists
    username_exists = await get_user_by_username(db, user.username)
    email_exists = await get_user_by_email(db, user.email)
    
    if username_exists:
        raise ValueError(f"Username '{user.username}' already registered")
    
    if email_exists:
        raise ValueError(f"Email '{user.email}' already registered")
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create new user object
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active
    )
    
    # Save to database
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


async def update_user(
    db: AsyncSession, 
    user_id: int, 
    user_update: schemas.UserUpdate
) -> Optional[User]:
    """
    Update a user
    
    Args:
        db: Database session
        user_id: ID of user to update
        user_update: User data for update
        
    Returns:
        Updated User object or None if not found
    """
    # Get current user
    user = await get_user(db, user_id)
    if not user:
        return None
    
    # Prepare update data
    update_data = user_update.dict(exclude_unset=True)
    
    # Hash password if provided
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    # Apply updates
    for key, value in update_data.items():
        setattr(user, key, value)
    
    # Save changes
    await db.commit()
    await db.refresh(user)
    
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    Delete a user
    
    Args:
        db: Database session
        user_id: ID of user to delete
        
    Returns:
        True if deleted, False if not found
    """
    # Check if user exists
    user = await get_user(db, user_id)
    if not user:
        return False
    
    # Delete user
    await db.delete(user)
    await db.commit()
    
    return True


async def authenticate_user(
    db: AsyncSession, 
    username: str, 
    password: str
) -> Optional[User]:
    """
    Authenticate a user by username and password
    
    Args:
        db: Database session
        username: Username
        password: Plain password
        
    Returns:
        User object if authentication succeeds, None otherwise
    """
    user = await get_user_by_username(db, username)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    # Update last login time
    user.last_login = func.now()
    await db.commit()
    
    return user 