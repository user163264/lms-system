#!/usr/bin/env python3
"""
Consolidated API tests for the LMS system.
This combines functionality from:
- test_api.py
- test_exercise_api.py
"""

import pytest
import asyncio
import httpx
import json
import time
from typing import Dict, List, Any, Optional, Tuple

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"
TIMEOUT = 5  # seconds

# Common fixture for httpx client
@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=TIMEOUT) as client:
        yield client

class TestGeneralAPI:
    """Tests for general API endpoints"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, async_client):
        """Test API health check endpoint"""
        response = await async_client.get(f"{API_PREFIX}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "LMS API Running!"
    
    @pytest.mark.asyncio
    async def test_swagger_docs(self, async_client):
        """Test Swagger documentation is accessible"""
        response = await async_client.get("/docs")
        assert response.status_code == 200
        # This is HTML content, so we check for swagger-ui
        assert "swagger-ui" in response.text.lower()

class TestLessonAPI:
    """Tests for lesson-related API endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_lessons(self, async_client):
        """Test retrieving all lessons"""
        response = await async_client.get(f"{API_PREFIX}/lessons/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Response should be a list of lessons"

class TestExerciseAPI:
    """Tests for exercise-related API endpoints"""
    
    # Test data for exercise template
    template_data = {
        "name": "Word Scramble Test Template",
        "type": "word_scramble",
        "validation_rules": {
            "case_sensitive": False
        },
        "scoring_mechanism": {
            "points_per_correct": 1
        },
        "display_parameters": {
            "time_limit": 60,
            "show_hints": True
        }
    }
    
    # Test data for exercise content
    content_data = {
        "template_id": 1,  # Will be updated with actual template ID
        "title": "Basic Word Scramble Exercise",
        "instructions": "Unscramble the letters to form a valid word.",
        "question_text": "nrdgea",
        "correct_answers": ["garden"],
        "alternate_answers": ["danger"],
        "difficulty_level": 2,
        "tags": ["vocabulary", "english"],
        "subject_area": "English"
    }
    
    # Test data for submission
    submission_data = {
        "user_id": 1,  # Mock user ID
        "exercise_content_id": 1,  # Will be updated with actual content ID
        "response_data": {
            "answer": "garden"
        },
        "completion_status": "completed"
    }
    
    @pytest.mark.asyncio
    async def test_get_exercises(self, async_client):
        """Test retrieving all exercises (original style)"""
        response = await async_client.get(f"{API_PREFIX}/exercises/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Response should be a list of exercises"
    
    @pytest.mark.asyncio
    async def test_get_exercise_templates(self, async_client):
        """Test retrieving exercise templates"""
        response = await async_client.get(f"{API_PREFIX}/exercises/templates/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Response should be a list of templates"
    
    @pytest.mark.asyncio
    async def test_exercise_template_lifecycle(self, async_client):
        """Test the complete lifecycle of an exercise template - create, retrieve, update, delete"""
        # 1. Create a template
        response = await async_client.post(
            f"{API_PREFIX}/exercises/templates/",
            json=self.template_data
        )
        assert response.status_code == 201, f"Failed to create template: {response.text}"
        template = response.json()
        template_id = template["id"]
        assert template_id is not None, "Template should have an ID"
        
        # 2. Retrieve the template
        response = await async_client.get(f"{API_PREFIX}/exercises/templates/{template_id}")
        assert response.status_code == 200
        retrieved_template = response.json()
        assert retrieved_template["name"] == self.template_data["name"]
        
        # 3. Update the template
        update_data = {"name": "Updated Template Name"}
        response = await async_client.patch(
            f"{API_PREFIX}/exercises/templates/{template_id}",
            json=update_data
        )
        assert response.status_code == 200
        updated_template = response.json()
        assert updated_template["name"] == update_data["name"]
        
        # 4. Delete the template
        response = await async_client.delete(f"{API_PREFIX}/exercises/templates/{template_id}")
        assert response.status_code == 204
        
        # 5. Verify deletion
        response = await async_client.get(f"{API_PREFIX}/exercises/templates/{template_id}")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_exercise_content_creation(self, async_client):
        """Test creating exercise content based on a template"""
        # First create a template to use
        response = await async_client.post(
            f"{API_PREFIX}/exercises/templates/",
            json=self.template_data
        )
        template_id = response.json()["id"]
        
        # Update content data with the template ID
        content_data = self.content_data.copy()
        content_data["template_id"] = template_id
        
        # Create exercise content
        response = await async_client.post(
            f"{API_PREFIX}/exercises/content/",
            json=content_data
        )
        assert response.status_code == 201
        content = response.json()
        content_id = content["id"]
        
        # Retrieve the content
        response = await async_client.get(f"{API_PREFIX}/exercises/content/{content_id}")
        assert response.status_code == 200
        retrieved_content = response.json()
        assert retrieved_content["title"] == content_data["title"]
        
        # Clean up - delete content and template
        await async_client.delete(f"{API_PREFIX}/exercises/content/{content_id}")
        await async_client.delete(f"{API_PREFIX}/exercises/templates/{template_id}")
    
    @pytest.mark.asyncio
    async def test_exercise_submission(self, async_client):
        """Test submitting a response to an exercise"""
        # Create template and content first
        response = await async_client.post(
            f"{API_PREFIX}/exercises/templates/",
            json=self.template_data
        )
        template_id = response.json()["id"]
        
        content_data = self.content_data.copy()
        content_data["template_id"] = template_id
        
        response = await async_client.post(
            f"{API_PREFIX}/exercises/content/",
            json=content_data
        )
        content_id = response.json()["id"]
        
        # Update submission data with content ID
        submission_data = self.submission_data.copy()
        submission_data["exercise_content_id"] = content_id
        
        # Submit a response
        response = await async_client.post(
            f"{API_PREFIX}/exercises/submissions/",
            json=submission_data
        )
        assert response.status_code == 201
        submission = response.json()
        assert submission["user_id"] == submission_data["user_id"]
        assert submission["exercise_content_id"] == content_id
        
        # Clean up
        await async_client.delete(f"{API_PREFIX}/exercises/content/{content_id}")
        await async_client.delete(f"{API_PREFIX}/exercises/templates/{template_id}") 