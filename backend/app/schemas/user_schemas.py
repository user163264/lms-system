"""
User schemas for authentication and user management.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enum for role-based access control"""
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class UserBase(BaseModel):
    """Base schema for user data"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.STUDENT
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """Schema for retrieved user data"""
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for login credentials"""
    username: str
    password: str


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"
    

class TokenPayload(BaseModel):
    """Schema for token payload data"""
    sub: str  # User ID as string
    exp: datetime
    role: str
    username: str


class TokenData(BaseModel):
    """Schema for token data decoded from JWT"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None 