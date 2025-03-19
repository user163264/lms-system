# /home/ubuntu/lms/backend/app/routes/lessons.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..schemas import Lesson, LessonCreate, LessonRequest
from .. import crud

router = APIRouter(
    prefix="/api/lessons",
    tags=["Lessons"]
)

@router.get("/", response_model=List[Lesson])
async def get_lessons(db: AsyncSession = Depends(get_db)):
    """Get all lessons"""
    return await crud.get_lessons(db)

@router.get("/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific lesson by ID"""
    lesson = await crud.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/", response_model=Lesson)
async def create_lesson(lesson: LessonRequest, db: AsyncSession = Depends(get_db)):
    """Create a new lesson"""
    return await crud.create_lesson(db, lesson)