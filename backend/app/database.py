# /home/ubuntu/lms/backend/app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Import config settings
from .config import DATABASE_URL, DB_ECHO

# Create base class for declarative models
Base = declarative_base()

# Database configuration using settings from config
engine = create_async_engine(DATABASE_URL, echo=DB_ECHO)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency for database session
async def get_db():
    async with SessionLocal() as session:
        yield session