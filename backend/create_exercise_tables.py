#!/usr/bin/env python3
"""
Script to create exercise-related tables directly using SQLAlchemy
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine

# Import our models
from app.models.exercise import Base

# Database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://lms_user:lms_password@localhost/lms_db")

async def create_tables():
    """Create all the tables defined in our models"""
    # Create an async engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Create tables
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
    
    # Close the engine
    await engine.dispose()
    
    print("Tables created successfully")

if __name__ == "__main__":
    asyncio.run(create_tables()) 