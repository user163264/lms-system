#!/usr/bin/env python3
"""
Integration tests for the complete exercise workflow.

This test file verifies that the entire exercise workflow functions correctly:
1. Creating exercise templates
2. Creating exercise content
3. Assigning exercises to students
4. Students submitting responses
5. Grading submissions
6. Reviewing results
"""

import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
import json
import os

# Import models and services
from app.models.exercise import ExerciseTemplate, ExerciseContent, Submission
from app.models.user import User
from app.services.exercise_service import ExerciseService
from app.services.submission_service import SubmissionService
from app.services.grading_service import GradingService

# Import test fixtures
from ..conftest import get_test_db, test_users

@pytest.mark.integration
class TestExerciseWorkflow:
    """Test the complete exercise workflow as an integration test"""
    
    @pytest.mark.asyncio
    async def test_complete_exercise_workflow(self, initialize_db, test_users):
        """Test the complete workflow from exercise creation to grading"""
        # Get services and session
        async for db in get_test_db():
            # Step 1: Get user IDs for test users
            teacher = test_users["teacher"]
            student = test_users["student"]
            
            # Step 2: Create an exercise template (as teacher)
            exercise_service = ExerciseService(db)
            template_data = {
                "name": "Integration Test Template",
                "type": "multiple_choice",
                "validation_rules": {
                    "allow_multiple": False
                },
                "scoring_mechanism": {
                    "correct_points": 10,
                    "incorrect_points": 0
                },
                "display_parameters": {
                    "show_feedback": True
                }
            }
            
            template = await exercise_service.create_template(template_data, teacher.id)
            assert template.id is not None, "Template should be created with ID"
            
            # Step 3: Create exercise content using the template
            content_data = {
                "template_id": template.id,
                "title": "Integration Test Exercise",
                "instructions": "Select the correct answer",
                "question_text": "What is the capital of France?",
                "correct_answers": ["Paris"],
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "difficulty_level": 1,
                "tags": ["geography", "europe"]
            }
            
            content = await exercise_service.create_content(content_data, teacher.id)
            assert content.id is not None, "Content should be created with ID"
            
            # Step 4: Assign the exercise to a student
            assignment_data = {
                "student_id": student.id,
                "content_id": content.id,
                "due_date": "2050-12-31T23:59:59Z",  # Far future
                "max_attempts": 3
            }
            
            assignment = await exercise_service.assign_exercise(
                assignment_data, teacher.id
            )
            assert assignment.id is not None, "Assignment should be created with ID"
            
            # Step 5: Student submits a response
            submission_service = SubmissionService(db)
            response_data = {
                "exercise_content_id": content.id,
                "response": {
                    "selected_option": "Paris"  # Correct answer
                },
                "time_spent": 45  # seconds
            }
            
            submission = await submission_service.create_submission(
                response_data, student.id
            )
            assert submission.id is not None, "Submission should be created with ID"
            assert submission.status == "submitted", "Initial status should be 'submitted'"
            
            # Step 6: Grade the submission
            grading_service = GradingService(db)
            grading_result = await grading_service.grade_submission(submission.id)
            
            # Step 7: Check the grading results
            assert grading_result.is_correct is True, "Answer should be marked correct"
            assert grading_result.score == 10, "Score should be 10 points"
            
            # Step 8: Student views their submission
            student_submission = await submission_service.get_submission(
                submission.id, student.id
            )
            assert student_submission.id == submission.id, "Should retrieve the same submission"
            assert student_submission.status == "graded", "Status should be updated to 'graded'"
            assert student_submission.score == 10, "Score should be included"
            
            # Step 9: Teacher views student submissions
            teacher_submissions = await submission_service.get_submissions_for_content(
                content.id, teacher.id
            )
            assert len(teacher_submissions) >= 1, "Teacher should see at least one submission"
            
            # Close the database session
            await db.close()
    
    @pytest.mark.asyncio
    async def test_incorrect_submission_workflow(self, initialize_db, test_users):
        """Test submission workflow with incorrect answers"""
        # Get services and session
        async for db in get_test_db():
            # Similar setup as above, but testing incorrect submission
            teacher = test_users["teacher"]
            student = test_users["student"]
            
            # Create template, content, and assignment as before
            exercise_service = ExerciseService(db)
            template = await exercise_service.create_template({
                "name": "Math Quiz Template",
                "type": "multiple_choice",
                "validation_rules": {"allow_multiple": False},
                "scoring_mechanism": {"correct_points": 5, "incorrect_points": -1}
            }, teacher.id)
            
            content = await exercise_service.create_content({
                "template_id": template.id,
                "title": "Math Question",
                "question_text": "What is 2+2?",
                "correct_answers": ["4"],
                "options": ["3", "4", "5", "6"]
            }, teacher.id)
            
            # Student submits an incorrect response
            submission_service = SubmissionService(db)
            response_data = {
                "exercise_content_id": content.id,
                "response": {
                    "selected_option": "5"  # Incorrect answer
                }
            }
            
            submission = await submission_service.create_submission(
                response_data, student.id
            )
            
            # Grade the submission
            grading_service = GradingService(db)
            grading_result = await grading_service.grade_submission(submission.id)
            
            # Check the grading results
            assert grading_result.is_correct is False, "Answer should be marked incorrect"
            assert grading_result.score == -1, "Score should be -1 points for incorrect answer"
            
            # Verify submission status
            submission = await submission_service.get_submission(submission.id, student.id)
            assert submission.status == "graded", "Status should be 'graded'"
            assert submission.score == -1, "Score should be -1"
            
            # Close the database session
            await db.close() 