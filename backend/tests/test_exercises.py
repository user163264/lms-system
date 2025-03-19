import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from typing import Dict, List

from app.main import app
from app.database import get_db, Base
from app.models.exercise import ExerciseTemplate, ExerciseContent, MediaAsset, UserResponse
from app.models.user import User, UserRole
from app.schemas.exercise_schemas import ExerciseTypeEnum
from app.services.auth import create_access_token, get_password_hash

# Test database URL - same as in test_auth.py
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
async def test_users(test_db) -> Dict[str, User]:
    """Create test users with different roles"""
    users = {}
    async with TestingSessionLocal() as db:
        # Student user
        student = User(
            username="student",
            email="student@example.com",
            hashed_password=get_password_hash("student123"),
            full_name="Student User",
            role=UserRole.STUDENT
        )
        db.add(student)
        
        # Teacher user
        teacher = User(
            username="teacher",
            email="teacher@example.com",
            hashed_password=get_password_hash("teacher123"),
            full_name="Teacher User",
            role=UserRole.TEACHER
        )
        db.add(teacher)
        
        # Admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
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


@pytest.fixture(scope="module")
def user_tokens(test_users) -> Dict[str, str]:
    """Create tokens for test users"""
    tokens = {}
    
    for role, user in test_users.items():
        tokens[role] = create_access_token(
            data={"sub": str(user.id), "username": user.username, "role": user.role}
        )
        
    return tokens


@pytest.fixture(scope="module")
async def test_template(test_users) -> ExerciseTemplate:
    """Create a test exercise template"""
    async with TestingSessionLocal() as db:
        template = ExerciseTemplate(
            name="Test Multiple Choice",
            type=ExerciseTypeEnum.MULTIPLE_CHOICE,
            validation_rules={"allow_multiple": False},
            scoring_mechanism={"correct_points": 2, "incorrect_points": 0},
            display_parameters={"shuffle_options": True}
        )
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return template


@pytest.fixture(scope="module")
async def test_content(test_template) -> ExerciseContent:
    """Create test exercise content"""
    async with TestingSessionLocal() as db:
        content = ExerciseContent(
            template_id=test_template.id,
            title="Sample Question",
            instructions="Select the correct answer",
            question_text="What is the capital of France?",
            correct_answers=["Paris"],
            alternate_answers=["paris", "PARIS"],
            difficulty_level=2,
            tags=["geography", "europe", "capitals"],
            subject_area="Geography"
        )
        db.add(content)
        await db.commit()
        await db.refresh(content)
        return content


@pytest.mark.asyncio
async def test_create_template(user_tokens):
    """Test creating an exercise template (teacher only)"""
    template_data = {
        "name": "Word Scramble Template",
        "type": "word_scramble",
        "validation_rules": {"case_sensitive": False},
        "scoring_mechanism": {"partial_credit": True},
        "display_parameters": {"time_limit": 60}
    }
    
    # Student should not be able to create template
    response = client.post(
        "/api/exercises/templates/",
        json=template_data,
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 403
    
    # Teacher should be able to create template
    response = client.post(
        "/api/exercises/templates/",
        json=template_data,
        headers={"Authorization": f"Bearer {user_tokens['teacher']}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Word Scramble Template"
    assert data["type"] == "word_scramble"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_templates(user_tokens, test_template):
    """Test getting exercise templates"""
    # Any authenticated user should be able to get templates
    response = client.get(
        "/api/exercises/templates/",
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Get specific template
    response = client.get(
        f"/api/exercises/templates/{test_template.id}",
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_template.id
    assert data["name"] == test_template.name


@pytest.mark.asyncio
async def test_create_exercise_content(user_tokens, test_template):
    """Test creating exercise content"""
    content_data = {
        "template_id": test_template.id,
        "title": "Math Question",
        "instructions": "Solve the equation",
        "question_text": "What is 2+2?",
        "correct_answers": ["4"],
        "difficulty_level": 1,
        "tags": ["math", "addition"],
        "subject_area": "Mathematics"
    }
    
    # Student should not be able to create content
    response = client.post(
        "/api/exercises/content/",
        json=content_data,
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 403
    
    # Teacher should be able to create content
    response = client.post(
        "/api/exercises/content/",
        json=content_data,
        headers={"Authorization": f"Bearer {user_tokens['teacher']}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Math Question"
    assert data["template_id"] == test_template.id
    assert "id" in data


@pytest.mark.asyncio
async def test_get_exercise_content(user_tokens, test_content):
    """Test getting exercise content"""
    # Any authenticated user should be able to get content
    response = client.get(
        f"/api/exercises/content/{test_content.id}",
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_content.id
    assert data["title"] == test_content.title


@pytest.mark.asyncio
async def test_submit_exercise_response(user_tokens, test_content, test_users):
    """Test submitting a response to an exercise"""
    submission_data = {
        "exercise_content_id": test_content.id,
        "response_data": {
            "answer": "Paris"
        }
    }
    
    # Submit correct answer
    response = client.post(
        "/api/exercises/submit/",
        json=submission_data,
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["score"] > 0
    
    # Submit incorrect answer
    submission_data["response_data"]["answer"] = "London"
    response = client.post(
        "/api/exercises/submit/",
        json=submission_data,
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    
    # Check user can see their own responses
    response = client.get(
        f"/api/exercises/responses/user/{test_users['student'].id}",
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Should have at least 2 responses


@pytest.mark.asyncio
async def test_unauthorized_response_access(user_tokens, test_users):
    """Test that users can't access other users' responses"""
    # Student shouldn't be able to access teacher's responses
    response = client.get(
        f"/api/exercises/responses/user/{test_users['teacher'].id}",
        headers={"Authorization": f"Bearer {user_tokens['student']}"}
    )
    assert response.status_code == 403
    
    # Teacher should be able to access student's responses
    response = client.get(
        f"/api/exercises/responses/user/{test_users['student'].id}",
        headers={"Authorization": f"Bearer {user_tokens['teacher']}"}
    )
    assert response.status_code == 200 