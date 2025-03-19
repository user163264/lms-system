"""
API routes for exercise templates and content.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from app.database import get_db
from app.models.exercise import ExerciseTemplate, ExerciseContent, MediaAsset, UserResponse
from app.models.user import User
from app.schemas.exercise_schemas import (
    ExerciseTemplate as ExerciseTemplateSchema,
    ExerciseTemplateCreate,
    ExerciseTemplateUpdate,
    ExerciseContent as ExerciseContentSchema,
    ExerciseContentCreate,
    ExerciseContentUpdate,
    MediaAsset as MediaAssetSchema,
    MediaAssetCreate,
    UserResponse as UserResponseSchema,
    UserResponseCreate,
    ExerciseSubmission,
    ExerciseSubmissionResponse
)
from app.services.exercise_evaluator import evaluate_exercise_response
from app.services.auth import get_current_active_user, check_teacher_permission, check_admin_permission

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


# Exercise Template Routes
@router.post("/templates/", response_model=ExerciseTemplateSchema, status_code=status.HTTP_201_CREATED)
async def create_exercise_template(
    template: ExerciseTemplateCreate,
    current_user: User = Depends(check_teacher_permission),
    db: AsyncSession = Depends(get_db)
):
    """Create a new exercise template"""
    db_template = ExerciseTemplate(
        name=template.name,
        type=template.type,
        validation_rules=template.validation_rules,
        scoring_mechanism=template.scoring_mechanism,
        display_parameters=template.display_parameters
    )
    
    db.add(db_template)
    await db.commit()
    await db.refresh(db_template)
    return db_template


@router.get("/templates/", response_model=List[ExerciseTemplateSchema])
async def get_exercise_templates(
    skip: int = 0,
    limit: int = 100,
    exercise_type: Optional[str] = Query(None, description="Filter by exercise type"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all exercise templates with optional filtering"""
    query = select(ExerciseTemplate)
    
    if exercise_type:
        query = query.filter(ExerciseTemplate.type == exercise_type)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    templates = result.scalars().all()
    
    return templates


@router.get("/templates/{template_id}", response_model=ExerciseTemplateSchema)
async def get_exercise_template(
    template_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific exercise template by ID"""
    query = select(ExerciseTemplate).filter(ExerciseTemplate.id == template_id)
    result = await db.execute(query)
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise template with ID {template_id} not found"
        )
    
    return template


@router.put("/templates/{template_id}", response_model=ExerciseTemplateSchema)
async def update_exercise_template(
    template_id: int,
    template_update: ExerciseTemplateUpdate,
    current_user: User = Depends(check_teacher_permission),
    db: AsyncSession = Depends(get_db)
):
    """Update an exercise template"""
    # Check if template exists
    query = select(ExerciseTemplate).filter(ExerciseTemplate.id == template_id)
    result = await db.execute(query)
    db_template = result.scalars().first()
    
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise template with ID {template_id} not found"
        )
    
    # Update template fields
    update_data = template_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_template, key, value)
    
    await db.commit()
    await db.refresh(db_template)
    return db_template


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise_template(
    template_id: int,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """Delete an exercise template"""
    # Check if template exists
    query = select(ExerciseTemplate).filter(ExerciseTemplate.id == template_id)
    result = await db.execute(query)
    db_template = result.scalars().first()
    
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise template with ID {template_id} not found"
        )
    
    # Delete template
    await db.delete(db_template)
    await db.commit()
    return None


# Exercise Content Routes
@router.post("/content/", response_model=ExerciseContentSchema, status_code=status.HTTP_201_CREATED)
async def create_exercise_content(
    content: ExerciseContentCreate,
    current_user: User = Depends(check_teacher_permission),
    db: AsyncSession = Depends(get_db)
):
    """Create new exercise content based on a template"""
    # Check if template exists
    query = select(ExerciseTemplate).filter(ExerciseTemplate.id == content.template_id)
    result = await db.execute(query)
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise template with ID {content.template_id} not found"
        )
    
    # Create exercise content
    db_content = ExerciseContent(**content.dict())
    db.add(db_content)
    await db.commit()
    await db.refresh(db_content)
    
    return db_content


@router.get("/content/", response_model=List[ExerciseContentSchema])
async def get_exercise_contents(
    skip: int = 0,
    limit: int = 100,
    template_id: Optional[int] = Query(None, description="Filter by template ID"),
    subject_area: Optional[str] = Query(None, description="Filter by subject area"),
    difficulty: Optional[int] = Query(None, ge=1, le=5, description="Filter by difficulty level"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all exercise content with optional filtering"""
    query = select(ExerciseContent).options(selectinload(ExerciseContent.template))
    
    # Apply filters
    if template_id:
        query = query.filter(ExerciseContent.template_id == template_id)
    
    if subject_area:
        query = query.filter(ExerciseContent.subject_area == subject_area)
    
    if difficulty:
        query = query.filter(ExerciseContent.difficulty_level == difficulty)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    contents = result.scalars().all()
    
    return contents


@router.get("/content/{content_id}", response_model=ExerciseContentSchema)
async def get_exercise_content(
    content_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific exercise content by ID"""
    query = select(ExerciseContent).options(
        selectinload(ExerciseContent.template),
        selectinload(ExerciseContent.media_assets)
    ).filter(ExerciseContent.id == content_id)
    
    result = await db.execute(query)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise content with ID {content_id} not found"
        )
    
    return content


@router.put("/content/{content_id}", response_model=ExerciseContentSchema)
async def update_exercise_content(
    content_id: int,
    content_update: ExerciseContentUpdate,
    current_user: User = Depends(check_teacher_permission),
    db: AsyncSession = Depends(get_db)
):
    """Update exercise content"""
    # Check if content exists
    query = select(ExerciseContent).filter(ExerciseContent.id == content_id)
    result = await db.execute(query)
    db_content = result.scalars().first()
    
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise content with ID {content_id} not found"
        )
    
    # Update content fields
    update_data = content_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_content, key, value)
    
    await db.commit()
    await db.refresh(db_content)
    return db_content


@router.delete("/content/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise_content(
    content_id: int,
    current_user: User = Depends(check_teacher_permission),
    db: AsyncSession = Depends(get_db)
):
    """Delete exercise content"""
    # Check if content exists
    query = select(ExerciseContent).filter(ExerciseContent.id == content_id)
    result = await db.execute(query)
    db_content = result.scalars().first()
    
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise content with ID {content_id} not found"
        )
    
    # Delete content
    await db.delete(db_content)
    await db.commit()
    return None


# Media Asset Routes
@router.post("/media/", response_model=MediaAssetSchema, status_code=status.HTTP_201_CREATED)
async def create_media_asset(
    media: MediaAssetCreate,
    current_user: User = Depends(check_teacher_permission),
    db: AsyncSession = Depends(get_db)
):
    """Create a new media asset for an exercise"""
    # Check if exercise content exists
    query = select(ExerciseContent).filter(ExerciseContent.id == media.exercise_content_id)
    result = await db.execute(query)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise content with ID {media.exercise_content_id} not found"
        )
    
    # Create media asset
    db_media = MediaAsset(**media.dict())
    db.add(db_media)
    await db.commit()
    await db.refresh(db_media)
    
    return db_media


# Exercise Submission Routes
@router.post("/submit/", response_model=ExerciseSubmissionResponse)
async def submit_exercise_response(
    submission: ExerciseSubmission,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit a response to an exercise and get evaluation"""
    # Get exercise content
    query = select(ExerciseContent).options(
        selectinload(ExerciseContent.template)
    ).filter(ExerciseContent.id == submission.exercise_content_id)
    
    result = await db.execute(query)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise content with ID {submission.exercise_content_id} not found"
        )
    
    # Get existing attempts count
    attempt_query = select(UserResponse).filter(
        UserResponse.user_id == current_user.id,
        UserResponse.exercise_content_id == submission.exercise_content_id
    )
    attempt_result = await db.execute(attempt_query)
    existing_attempts = attempt_result.scalars().all()
    attempt_number = len(existing_attempts) + 1
    
    # Evaluate response
    evaluation = await evaluate_exercise_response(
        content.template.type.value,
        submission.response_data,
        content.correct_answers,
        content.alternate_answers,
        content.template.validation_rules,
        content.template.scoring_mechanism
    )
    
    # Create user response record
    user_response = UserResponse(
        user_id=current_user.id,
        exercise_content_id=submission.exercise_content_id,
        response_data=submission.response_data,
        score=evaluation.score,
        completion_status="completed",
        attempt_number=attempt_number,
        completed_at=func.now()
    )
    
    db.add(user_response)
    await db.commit()
    await db.refresh(user_response)
    
    # Return evaluation and response ID
    return ExerciseSubmissionResponse(
        response_id=user_response.id,
        is_correct=evaluation.is_correct,
        score=evaluation.score,
        feedback=evaluation.feedback,
        detailed_results=evaluation.detailed_results
    )


# User Response History
@router.get("/responses/user/{user_id}", response_model=List[UserResponseSchema])
async def get_user_exercise_responses(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get exercise response history for a specific user"""
    # Check permissions - users can only see their own responses unless admin/teacher
    if current_user.id != user_id and current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's responses"
        )
        
    query = select(UserResponse).filter(UserResponse.user_id == user_id)
    query = query.options(selectinload(UserResponse.exercise_content))
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    responses = result.scalars().all()
    
    return responses 