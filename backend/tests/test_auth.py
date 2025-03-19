import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from typing import Dict, Generator, AsyncGenerator

from app.main import app
from app.database import get_db, Base
from app.models.user import User, UserRole
from app.services.auth import create_access_token, get_password_hash

# Test database URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine
engine = create_async_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()


# Override get_db dependency
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def test_db():
    await init_test_db()
    yield
    # Clean up after tests


@pytest.fixture(scope="module")
async def test_user(test_db) -> User:
    """Create a test user and return it"""
    async with TestingSessionLocal() as db:
        # Create test user
        hashed_password = get_password_hash("testpassword123")
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hashed_password,
            full_name="Test User",
            role=UserRole.STUDENT,
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


@pytest.fixture(scope="module")
async def test_admin(test_db) -> User:
    """Create a test admin user and return it"""
    async with TestingSessionLocal() as db:
        # Create admin user
        hashed_password = get_password_hash("adminpassword123")
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        return admin


@pytest.fixture(scope="module")
def user_token(test_user) -> str:
    """Create a token for test user"""
    return create_access_token(
        data={"sub": str(test_user.id), "username": test_user.username, "role": test_user.role}
    )


@pytest.fixture(scope="module")
def admin_token(test_admin) -> str:
    """Create a token for admin user"""
    return create_access_token(
        data={"sub": str(test_admin.id), "username": test_admin.username, "role": test_admin.role}
    )


@pytest.mark.asyncio
async def test_register_user(test_db):
    """Test user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
            "full_name": "New User",
            "role": "student"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_login_for_access_token():
    """Test OAuth2 login endpoint"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_simple():
    """Test simple login endpoint"""
    response = client.post(
        "/api/auth/login/simple",
        json={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_me(user_token):
    """Test getting current user data"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_unauthorized_access():
    """Test unauthorized access to protected endpoint"""
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_invalid_login():
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login/simple",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_get_users_admin_only(user_token, admin_token):
    """Test that only admins can list all users"""
    # Try with regular user token
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]
    
    # Try with admin token
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # at least test user and admin 