#!/usr/bin/env python3
"""
API tests for the LMS system.
This tests the REST API endpoints.
"""

import pytest
import sys
import os
from pathlib import Path
import json
import random
from datetime import datetime

# Try to import FastAPI testing components
try:
    from fastapi.testclient import TestClient
    from backend.app.main import app
    import backend.app.models as models
    import backend.app.database as database
    pytest_skip_api = False
except ImportError as e:
    print(f"Warning: FastAPI imports failed: {e}")
    print("API tests will be skipped")
    pytest_skip_api = True

# Skip all API tests if imports failed
pytestmark = pytest.mark.skipif(pytest_skip_api, reason="FastAPI imports failed")

# Test client
client = None if pytest_skip_api else TestClient(app)

# Test data
test_user_data = {
    "username": f"test_user_{random.randint(1000, 9999)}",
    "email": "test_api@example.com",
    "password": "securepassword123",
    "user_type": "student"
}

test_course_data = {
    "title": f"API Test Course {random.randint(1000, 9999)}",
    "description": "This is a course created through the API"
}

# Setup and teardown
@pytest.fixture(scope="module")
def auth_headers():
    """Create a test user and get authentication headers."""
    if pytest_skip_api:
        return {}
    
    # Register a test user
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Return headers with token
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def test_course(auth_headers):
    """Create a test course."""
    if pytest_skip_api:
        return None
    
    # Create a course
    response = client.post("/api/courses/", json=test_course_data, headers=auth_headers)
    assert response.status_code == 201
    course_id = response.json()["id"]
    
    # Return the course ID
    yield course_id
    
    # Clean up
    client.delete(f"/api/courses/{course_id}", headers=auth_headers)

# Tests
@pytest.mark.api
def test_health_endpoint():
    """Test the health check endpoint."""
    if pytest_skip_api:
        pytest.skip("FastAPI imports failed")
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.api
def test_auth_endpoints():
    """Test authentication endpoints."""
    if pytest_skip_api:
        pytest.skip("FastAPI imports failed")
    
    # Test login with valid credentials
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    # Test login with invalid credentials
    invalid_login = {
        "username": test_user_data["username"],
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", data=invalid_login)
    assert response.status_code == 401

@pytest.mark.api
def test_course_endpoints(auth_headers):
    """Test course-related endpoints."""
    if pytest_skip_api:
        pytest.skip("FastAPI imports failed")
    
    # Create a new course
    response = client.post("/api/courses/", json=test_course_data, headers=auth_headers)
    assert response.status_code == 201
    course_id = response.json()["id"]
    
    # Get course details
    response = client.get(f"/api/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["title"] == test_course_data["title"]
    
    # Update course
    update_data = {
        "title": f"Updated Course {random.randint(1000, 9999)}",
        "description": "This course has been updated"
    }
    response = client.put(f"/api/courses/{course_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    # Verify update
    response = client.get(f"/api/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    
    # Get all courses
    response = client.get("/api/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Delete course
    response = client.delete(f"/api/courses/{course_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/api/courses/{course_id}")
    assert response.status_code == 404

@pytest.mark.api
def test_lesson_endpoints(auth_headers, test_course):
    """Test lesson-related endpoints."""
    if pytest_skip_api:
        pytest.skip("FastAPI imports failed")
    
    # Create test lesson data
    lesson_data = {
        "title": f"API Test Lesson {random.randint(1000, 9999)}",
        "content": "This is lesson content created through the API",
        "course_id": test_course,
        "order": 1
    }
    
    # Create a new lesson
    response = client.post("/api/lessons/", json=lesson_data, headers=auth_headers)
    assert response.status_code == 201
    lesson_id = response.json()["id"]
    
    # Get lesson details
    response = client.get(f"/api/lessons/{lesson_id}")
    assert response.status_code == 200
    assert response.json()["title"] == lesson_data["title"]
    
    # Update lesson
    update_data = {
        "title": f"Updated Lesson {random.randint(1000, 9999)}",
        "content": "This lesson has been updated"
    }
    response = client.patch(f"/api/lessons/{lesson_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    # Verify update
    response = client.get(f"/api/lessons/{lesson_id}")
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    
    # Get lessons by course
    response = client.get(f"/api/courses/{test_course}/lessons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
    
    # Delete lesson
    response = client.delete(f"/api/lessons/{lesson_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/api/lessons/{lesson_id}")
    assert response.status_code == 404

@pytest.mark.api
def test_exercise_and_submission_flow(auth_headers, test_course):
    """Test the complete flow of exercises and submissions."""
    if pytest_skip_api:
        pytest.skip("FastAPI imports failed")
    
    # Create a lesson
    lesson_data = {
        "title": "Exercise Flow Lesson",
        "content": "This lesson tests the exercise submission flow",
        "course_id": test_course,
        "order": 1
    }
    response = client.post("/api/lessons/", json=lesson_data, headers=auth_headers)
    assert response.status_code == 201
    lesson_id = response.json()["id"]
    
    # Create an exercise
    exercise_data = {
        "lesson_id": lesson_id,
        "question": "What is the capital of France?",
        "answer_options": json.dumps(["London", "Paris", "Berlin", "Rome"]),
        "correct_answer": "Paris",
        "exercise_type": "multiple_choice"
    }
    response = client.post("/api/exercises/", json=exercise_data, headers=auth_headers)
    assert response.status_code == 201
    exercise_id = response.json()["id"]
    
    # Get exercise details
    response = client.get(f"/api/exercises/{exercise_id}")
    assert response.status_code == 200
    assert response.json()["question"] == exercise_data["question"]
    
    # Submit correct answer
    submission_data = {
        "exercise_id": exercise_id,
        "answer_text": json.dumps(["Paris"])
    }
    response = client.post("/api/submissions/", json=submission_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["is_correct"] is True
    
    # Submit incorrect answer
    wrong_submission = {
        "exercise_id": exercise_id,
        "answer_text": json.dumps(["London"])
    }
    response = client.post("/api/submissions/", json=wrong_submission, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["is_correct"] is False
    
    # Get user submissions
    response = client.get("/api/submissions/my", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2
    
    # Clean up
    # Delete exercise (submissions should be deleted automatically)
    response = client.delete(f"/api/exercises/{exercise_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Delete lesson
    response = client.delete(f"/api/lessons/{lesson_id}", headers=auth_headers)
    assert response.status_code == 204 