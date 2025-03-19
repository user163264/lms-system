"""
Common test fixtures for pytest
"""
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Dict, Generator, AsyncGenerator

from app.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole
from app.services.auth import get_password_hash, create_access_token

# Test database URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine
engine = create_async_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_test_db():
    """Initialize the test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_test_db():
    """Get a test database session"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()


# Override get_db dependency
app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def initialize_db():
    """Initialize the test database for the entire test session"""
    await init_test_db()
    yield
    # Clean up


@pytest.fixture(scope="session")
async def test_users() -> Dict[str, User]:
    """Create test users with different roles"""
    users = {}
    
    async with TestingSessionLocal() as db:
        # Student user
        student = User(
            username="teststudent",
            email="student@example.com",
            hashed_password=get_password_hash("student123"),
            full_name="Test Student",
            role=UserRole.STUDENT
        )
        db.add(student)
        
        # Teacher user
        teacher = User(
            username="testteacher",
            email="teacher@example.com",
            hashed_password=get_password_hash("teacher123"),
            full_name="Test Teacher",
            role=UserRole.TEACHER
        )
        db.add(teacher)
        
        # Admin user
        admin = User(
            username="testadmin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Test Admin",
            role=UserRole.ADMIN
        )
        db.add(admin)
        
        await db.commit()
        
        # Refresh to get IDs
        await db.refresh(student)
        await db.refresh(teacher)
        await db.refresh(admin)
        
        users["student"] = student
        users["teacher"] = teacher
        users["admin"] = admin
        
    return users


@pytest.fixture(scope="session")
def user_tokens(test_users) -> Dict[str, str]:
    """Create tokens for test users"""
    tokens = {}
    
    for role, user in test_users.items():
        tokens[role] = create_access_token(
            data={"sub": str(user.id), "username": user.username, "role": user.role}
        )
        
    return tokens 