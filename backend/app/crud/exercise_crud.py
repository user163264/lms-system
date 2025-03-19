"""
CRUD operations for exercise-related models
"""
from typing import List, Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from ..models.exercise import ExerciseTemplate, ExerciseContent, MediaAsset, UserResponse
from ..schemas import exercise_schemas as schemas


# Exercise Template CRUD operations

async def create_exercise_template(
    db: AsyncSession, 
    template: schemas.ExerciseTemplateCreate
) -> ExerciseTemplate:
    """Create a new exercise template"""
    db_template = ExerciseTemplate(**template.dict())
    db.add(db_template)
    await db.commit()
    await db.refresh(db_template)
    return db_template


async def get_exercise_template(
    db: AsyncSession, 
    template_id: int
) -> Optional[ExerciseTemplate]:
    """Get an exercise template by ID"""
    result = await db.execute(
        select(ExerciseTemplate).where(ExerciseTemplate.id == template_id)
    )
    return result.scalars().first()


async def get_exercise_templates(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[ExerciseTemplate]:
    """Get a list of exercise templates"""
    result = await db.execute(
        select(ExerciseTemplate).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_exercise_templates_by_type(
    db: AsyncSession, 
    exercise_type: str
) -> List[ExerciseTemplate]:
    """Get a list of exercise templates by type"""
    result = await db.execute(
        select(ExerciseTemplate).where(ExerciseTemplate.type == exercise_type)
    )
    return result.scalars().all()


async def update_exercise_template(
    db: AsyncSession, 
    template_id: int, 
    template_update: schemas.ExerciseTemplateUpdate
) -> Optional[ExerciseTemplate]:
    """Update an exercise template"""
    update_data = template_update.dict(exclude_unset=True)
    if not update_data:
        # No fields to update
        return await get_exercise_template(db, template_id)
    
    await db.execute(
        update(ExerciseTemplate)
        .where(ExerciseTemplate.id == template_id)
        .values(**update_data)
    )
    await db.commit()
    
    return await get_exercise_template(db, template_id)


async def delete_exercise_template(
    db: AsyncSession, 
    template_id: int
) -> bool:
    """Delete an exercise template"""
    # Check if template exists
    template = await get_exercise_template(db, template_id)
    if not template:
        return False
    
    await db.execute(
        delete(ExerciseTemplate).where(ExerciseTemplate.id == template_id)
    )
    await db.commit()
    
    return True


# Exercise Content CRUD operations

async def create_exercise_content(
    db: AsyncSession, 
    content: schemas.ExerciseContentCreate
) -> ExerciseContent:
    """Create a new exercise content"""
    db_content = ExerciseContent(**content.dict())
    db.add(db_content)
    await db.commit()
    await db.refresh(db_content)
    return db_content


async def get_exercise_content(
    db: AsyncSession, 
    content_id: int
) -> Optional[ExerciseContent]:
    """Get an exercise content by ID"""
    result = await db.execute(
        select(ExerciseContent).where(ExerciseContent.id == content_id)
    )
    return result.scalars().first()


async def get_exercise_contents(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[ExerciseContent]:
    """Get a list of exercise contents"""
    result = await db.execute(
        select(ExerciseContent).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_exercise_contents_by_template(
    db: AsyncSession, 
    template_id: int
) -> List[ExerciseContent]:
    """Get a list of exercise contents by template ID"""
    result = await db.execute(
        select(ExerciseContent).where(ExerciseContent.template_id == template_id)
    )
    return result.scalars().all()


async def get_exercise_contents_by_difficulty(
    db: AsyncSession, 
    difficulty_level: int
) -> List[ExerciseContent]:
    """Get a list of exercise contents by difficulty level"""
    result = await db.execute(
        select(ExerciseContent).where(ExerciseContent.difficulty_level == difficulty_level)
    )
    return result.scalars().all()


async def get_exercise_contents_by_tags(
    db: AsyncSession, 
    tags: List[str]
) -> List[ExerciseContent]:
    """Get a list of exercise contents by tags"""
    result = await db.execute(
        select(ExerciseContent).where(ExerciseContent.tags.overlap(tags))
    )
    return result.scalars().all()


async def update_exercise_content(
    db: AsyncSession, 
    content_id: int, 
    content_update: schemas.ExerciseContentUpdate
) -> Optional[ExerciseContent]:
    """Update an exercise content"""
    update_data = content_update.dict(exclude_unset=True)
    if not update_data:
        # No fields to update
        return await get_exercise_content(db, content_id)
    
    await db.execute(
        update(ExerciseContent)
        .where(ExerciseContent.id == content_id)
        .values(**update_data)
    )
    await db.commit()
    
    return await get_exercise_content(db, content_id)


async def delete_exercise_content(
    db: AsyncSession, 
    content_id: int
) -> bool:
    """Delete an exercise content"""
    # Check if content exists
    content = await get_exercise_content(db, content_id)
    if not content:
        return False
    
    await db.execute(
        delete(ExerciseContent).where(ExerciseContent.id == content_id)
    )
    await db.commit()
    
    return True


# Media Asset CRUD operations

async def create_media_asset(
    db: AsyncSession, 
    asset: schemas.MediaAssetCreate
) -> MediaAsset:
    """Create a new media asset"""
    db_asset = MediaAsset(**asset.dict())
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    return db_asset


async def get_media_asset(
    db: AsyncSession, 
    asset_id: int
) -> Optional[MediaAsset]:
    """Get a media asset by ID"""
    result = await db.execute(
        select(MediaAsset).where(MediaAsset.id == asset_id)
    )
    return result.scalars().first()


async def get_media_assets_by_exercise(
    db: AsyncSession, 
    exercise_content_id: int
) -> List[MediaAsset]:
    """Get media assets by exercise content ID"""
    result = await db.execute(
        select(MediaAsset).where(MediaAsset.exercise_content_id == exercise_content_id)
    )
    return result.scalars().all()


async def update_media_asset(
    db: AsyncSession, 
    asset_id: int, 
    asset_update: schemas.MediaAssetUpdate
) -> Optional[MediaAsset]:
    """Update a media asset"""
    update_data = asset_update.dict(exclude_unset=True)
    if not update_data:
        # No fields to update
        return await get_media_asset(db, asset_id)
    
    await db.execute(
        update(MediaAsset)
        .where(MediaAsset.id == asset_id)
        .values(**update_data)
    )
    await db.commit()
    
    return await get_media_asset(db, asset_id)


async def delete_media_asset(
    db: AsyncSession, 
    asset_id: int
) -> bool:
    """Delete a media asset"""
    # Check if asset exists
    asset = await get_media_asset(db, asset_id)
    if not asset:
        return False
    
    await db.execute(
        delete(MediaAsset).where(MediaAsset.id == asset_id)
    )
    await db.commit()
    
    return True


# User Response CRUD operations

async def create_user_response(
    db: AsyncSession, 
    response: schemas.UserResponseCreate
) -> UserResponse:
    """Create a new user response"""
    db_response = UserResponse(**response.dict())
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response


async def get_user_response(
    db: AsyncSession, 
    response_id: int
) -> Optional[UserResponse]:
    """Get a user response by ID"""
    result = await db.execute(
        select(UserResponse).where(UserResponse.id == response_id)
    )
    return result.scalars().first()


async def get_user_responses_by_user(
    db: AsyncSession, 
    user_id: int
) -> List[UserResponse]:
    """Get user responses by user ID"""
    result = await db.execute(
        select(UserResponse).where(UserResponse.user_id == user_id)
    )
    return result.scalars().all()


async def get_user_responses_by_exercise(
    db: AsyncSession, 
    exercise_content_id: int
) -> List[UserResponse]:
    """Get user responses by exercise content ID"""
    result = await db.execute(
        select(UserResponse).where(UserResponse.exercise_content_id == exercise_content_id)
    )
    return result.scalars().all()


async def get_latest_user_response(
    db: AsyncSession, 
    user_id: int, 
    exercise_content_id: int
) -> Optional[UserResponse]:
    """Get the latest user response for a specific exercise"""
    result = await db.execute(
        select(UserResponse)
        .where(
            UserResponse.user_id == user_id,
            UserResponse.exercise_content_id == exercise_content_id
        )
        .order_by(UserResponse.started_at.desc())
    )
    return result.scalars().first()


async def update_user_response(
    db: AsyncSession, 
    response_id: int, 
    response_update: schemas.UserResponseUpdate
) -> Optional[UserResponse]:
    """Update a user response"""
    update_data = response_update.dict(exclude_unset=True)
    if not update_data:
        # No fields to update
        return await get_user_response(db, response_id)
    
    await db.execute(
        update(UserResponse)
        .where(UserResponse.id == response_id)
        .values(**update_data)
    )
    await db.commit()
    
    return await get_user_response(db, response_id)


async def delete_user_response(
    db: AsyncSession, 
    response_id: int
) -> bool:
    """Delete a user response"""
    # Check if response exists
    response = await get_user_response(db, response_id)
    if not response:
        return False
    
    await db.execute(
        delete(UserResponse).where(UserResponse.id == response_id)
    )
    await db.commit()
    
    return True


# Composite operations

async def get_exercise_with_content(
    db: AsyncSession, 
    template_id: int
) -> Optional[Dict[str, Any]]:
    """Get exercise template with all its content"""
    template = await get_exercise_template(db, template_id)
    if not template:
        return None
    
    contents = await get_exercise_contents_by_template(db, template_id)
    
    return {
        "template": template,
        "contents": contents
    }


async def get_exercise_content_with_media(
    db: AsyncSession, 
    content_id: int
) -> Optional[Dict[str, Any]]:
    """Get exercise content with all its media assets"""
    content = await get_exercise_content(db, content_id)
    if not content:
        return None
    
    assets = await get_media_assets_by_exercise(db, content_id)
    
    return {
        "content": content,
        "media_assets": assets
    } 