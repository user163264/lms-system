# /home/ubuntu/lms/backend/app/routes/exercises.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..database import get_db
from ..schemas import Exercise, ExerciseCreate, ExerciseRequest, ExerciseTemplate
from .. import crud

router = APIRouter(
    prefix="/api/exercises",
    tags=["Exercises"]
)

@router.get("/", response_model=List[Exercise])
async def get_exercises(
    lesson_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all exercises.
    If lesson_id is provided, filters exercises by that lesson_id.
    """
    return await crud.get_exercises(db, lesson_id)

@router.get("/{exercise_id}", response_model=Exercise)
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific exercise by ID"""
    exercise = await crud.get_exercise(db, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/", response_model=Exercise)
async def create_exercise(exercise: ExerciseRequest, db: AsyncSession = Depends(get_db)):
    """Create a new exercise"""
    return await crud.create_exercise(db, exercise)

@router.post("/batch/", response_model=List[Exercise])
async def create_exercises_batch(template: ExerciseTemplate, db: AsyncSession = Depends(get_db)):
    """Create multiple exercises at once using a template"""
    return await crud.create_exercises_from_template(db, template)