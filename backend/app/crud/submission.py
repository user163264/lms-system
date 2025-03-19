"""
CRUD operations for Submission models.

This module contains database operations for managing exercise submissions.
"""

import logging
from typing import List, Optional, Dict, Any, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException

from ..models import Submission, Exercise, User
from ..schemas import submission as schemas
from ..utils.logging import get_app_logger

# Initialize logger
logger = get_app_logger("crud.submission")


async def get_submissions(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    user_id: Optional[int] = None,
    exercise_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[Submission]:
    """
    Get all submissions, with optional filtering.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        user_id: Optional user ID to filter by
        exercise_id: Optional exercise ID to filter by
        status: Optional status to filter by
        
    Returns:
        List of Submission objects
    """
    query = select(Submission)
    
    if user_id is not None:
        query = query.where(Submission.user_id == user_id)
    
    if exercise_id is not None:
        query = query.where(Submission.exercise_id == exercise_id)
    
    if status is not None:
        query = query.where(Submission.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Submission.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


async def get_submission(
    db: AsyncSession, 
    submission_id: int,
    with_exercise: bool = False,
    with_user: bool = False
) -> Optional[Submission]:
    """
    Get a specific submission by ID.
    
    Args:
        db: Database session
        submission_id: ID of the submission to retrieve
        with_exercise: Whether to load related exercise
        with_user: Whether to load related user
        
    Returns:
        Submission object if found, None otherwise
    """
    query = select(Submission).where(Submission.id == submission_id)
    
    if with_exercise:
        query = query.options(joinedload(Submission.exercise))
    
    if with_user:
        query = query.options(joinedload(Submission.user))
    
    result = await db.execute(query)
    return result.scalars().first()


async def create_submission(
    db: AsyncSession, 
    submission: schemas.SubmissionCreate
) -> Submission:
    """
    Create a new submission and grade it.
    
    Args:
        db: Database session
        submission: Submission data to create
        
    Returns:
        Created Submission object
    """
    # Check if the exercise exists
    result = await db.execute(
        select(Exercise).where(Exercise.id == submission.exercise_id)
    )
    exercise = result.scalars().first()
    
    if not exercise:
        logger.error(f"Cannot create submission: exercise with ID {submission.exercise_id} does not exist")
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Check if the user exists
    result = await db.execute(
        select(User).where(User.id == submission.user_id)
    )
    user = result.scalars().first()
    
    if not user:
        logger.error(f"Cannot create submission: user with ID {submission.user_id} does not exist")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Grade the submission
    score = await grade_submission(exercise, submission.user_answer)
    
    # Create the submission
    db_submission = Submission(
        user_id=submission.user_id,
        exercise_id=submission.exercise_id,
        user_answer=submission.user_answer,
        score=score,
        status="graded" if exercise.grading_type == "auto" else "pending",
        graded_by="auto" if exercise.grading_type == "auto" else None,
        attempt_number=submission.attempt_number
    )
    
    db.add(db_submission)
    await db.commit()
    await db.refresh(db_submission)
    
    logger.info(f"Created submission: {db_submission.id} for exercise {db_submission.exercise_id}")
    return db_submission


async def grade_submission(
    exercise: Exercise, 
    user_answer: Union[str, Dict, List]
) -> float:
    """
    Grade a submission based on exercise type.
    
    Args:
        exercise: Exercise object to grade against
        user_answer: User's answer to grade
        
    Returns:
        Score for the submission
    """
    if exercise.grading_type != "auto":
        logger.info(f"Exercise {exercise.id} requires manual grading")
        return 0.0
    
    logger.info(f"Grading submission for exercise {exercise.id} of type {exercise.exercise_type}")
    
    # Different grading logic based on exercise type
    if exercise.exercise_type in ["multiple_choice", "true_false"]:
        if str(user_answer).strip().lower() == str(exercise.correct_answer).strip().lower():
            logger.info(f"Correct answer for exercise {exercise.id}")
            return float(exercise.max_score)
    
    elif exercise.exercise_type in ["fill_blank", "short_answer"]:
        if isinstance(exercise.correct_answer, list):
            # Check if user answer matches any of the correct answers
            for answer in exercise.correct_answer:
                if str(user_answer).strip().lower() == str(answer).strip().lower():
                    logger.info(f"Correct answer for exercise {exercise.id}")
                    return float(exercise.max_score)
        else:
            # Single correct answer
            if str(user_answer).strip().lower() == str(exercise.correct_answer).strip().lower():
                logger.info(f"Correct answer for exercise {exercise.id}")
                return float(exercise.max_score)
    
    elif exercise.exercise_type == "matching_words":
        # For matching exercises, check all pairs
        correct_count = 0
        total_count = len(exercise.correct_answer)
        
        if isinstance(user_answer, dict) and isinstance(exercise.correct_answer, dict):
            for key, value in exercise.correct_answer.items():
                if key in user_answer and str(user_answer[key]).strip().lower() == str(value).strip().lower():
                    correct_count += 1
            
            if total_count > 0:
                score = (correct_count / total_count) * exercise.max_score
                logger.info(f"Partial score for exercise {exercise.id}: {score}")
                return float(score)
    
    logger.info(f"Incorrect answer for exercise {exercise.id}")
    return 0.0 