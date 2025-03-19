# /home/ubuntu/lms/backend/app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.get("/")
async def get_users():
    """Placeholder for user management (to be implemented)"""
    return {"message": "User management not yet implemented"}