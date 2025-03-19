#!/usr/bin/env python3

"""
Test script for verifying the database layer functionality.
"""

import sys
import os
import time
import random
from datetime import datetime, timedelta

# Add parent directory to path to allow importing from the project root
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database import (
    DBManager, Student, Exercise, Test, TestQuestion, StudentTest,
    Submission, SubmissionAnswer, Score, ValidationError,
    TestService, SubmissionService, generate_test_data, clean_test_data
)

def test_connection():
    """Test database connection."""
    print("\n==== Testing Database Connection ====")
    try:
        with DBManager() as db:
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_model_validation():
    """Test model validation."""
    print("\n==== Testing Model Validation ====")
    
    # Test student validation
    try:
        invalid_student = Student(
            username="u",  # Too short
            email="not-an-email",
            full_name="",  # Empty
            password_hash="password"  # Not hashed
        )
        invalid_student.validate()
        print("❌ Student validation should have failed")
    except ValidationError as e:
        print(f"✅ Student validation correctly failed: {e}")
    
    # Test exercise validation
    try:
        invalid_exercise = Exercise(
            exercise_type="invalid_type",
            question="Sample question",
            answer_data={},
            max_score=-1  # Invalid score
        )
        invalid_exercise.validate()
        print("❌ Exercise validation should have failed")
    except ValidationError as e:
        print(f"✅ Exercise validation correctly failed: {e}")
    
    # Test valid models
    try:
        valid_student = Student(
            username="valid_user",
            email="valid@example.com",
            full_name="Valid User",
            password_hash=Student.hash_password("password")
        )
        valid_student.validate()
        print("✅ Valid student passed validation")
        
        valid_exercise = Exercise(
            exercise_type="multiple_choice",
            question="Sample question",
            answer_data={"options": ["A", "B", "C"], "correct_option": "B"},
            max_score=1,
            grading_type="auto"
        )
        valid_exercise.validate()
        print("✅ Valid exercise passed validation")
        
        return True
    except ValidationError as e:
        print(f"❌ Validation failed for valid model: {e}")
        return False

def test_crud_operations():
    """Test CRUD operations on models."""
    print("\n==== Testing CRUD Operations ====")
    
    with DBManager() as db:
        # Create a student
        student = Student(
            username=f"test_user_{int(time.time())}",
            email=f"test_{int(time.time())}@example.com",
            full_name="Test User",
            password_hash=Student.hash_password("password"),
            created_at=datetime.now(),
            is_active=True
        )
        student_id = student.save(db)
        print(f"✅ Created student with ID: {student_id}")
        
        # Read the student
        retrieved_student = Student.find_by_id(student_id, db)
        if retrieved_student and retrieved_student.username == student.username:
            print(f"✅ Retrieved student: {retrieved_student.username}")
        else:
            print("❌ Failed to retrieve student")
            return False
        
        # Update the student
        retrieved_student.full_name = "Updated Test User"
        retrieved_student.save(db)
        
        # Verify update
        updated_student = Student.find_by_id(student_id, db)
        if updated_student and updated_student.full_name == "Updated Test User":
            print(f"✅ Updated student name: {updated_student.full_name}")
        else:
            print("❌ Failed to update student")
            return False
        
        # Delete the student
        Student.delete_by_id(student_id, db)
        
        # Verify deletion
        deleted_student = Student.find_by_id(student_id, db)
        if not deleted_student:
            print("✅ Student successfully deleted")
        else:
            print("❌ Failed to delete student")
            return False
        
        return True

def test_generate_data():
    """Test generating test data."""
    print("\n==== Testing Data Generation ====")
    
    try:
        # First clean any existing test data
        clean_test_data()
        
        # Generate a small amount of test data
        result = generate_test_data(num_students=2, num_exercises_per_type=1, num_tests=1)
        
        if result:
            print("✅ Successfully generated test data")
            return True
        else:
            print("❌ Failed to generate test data")
            return False
    except Exception as e:
        print(f"❌ Error generating test data: {e}")
        return False

def test_services():
    """Test service layer functionality."""
    print("\n==== Testing Service Layer ====")
    
    with DBManager() as db:
        try:
            # Find a student 
            students = Student.find_all(db, limit=1)
            if not students:
                print("❌ No students found for testing")
                return False
            student = students[0]
            
            # Find a test
            tests = Test.find_all(db, limit=1)
            if not tests:
                print("❌ No tests found for testing")
                return False
            test = tests[0]
            
            # Test assignment service
            assignment_id = TestService.assign_test_to_student(
                student.id, test.id, 
                due_at=datetime.now() + timedelta(days=7), 
                max_attempts=3,
                db=db
            )
            
            if assignment_id:
                print(f"✅ Assigned test {test.id} to student {student.id}")
            else:
                print("❌ Failed to assign test")
                return False
            
            # Test start submission service
            submission = SubmissionService.start_test(
                student.id, test.id,
                ip_address="127.0.0.1",
                user_agent="Test Script",
                db=db
            )
            
            if submission and submission.id:
                print(f"✅ Started test submission: {submission.id}")
            else:
                print("❌ Failed to start submission")
                return False
            
            # Get questions for the test
            test_data = TestService.get_test_with_questions(test.id, db=db)
            if not test_data or not test_data.get('questions'):
                print("❌ Failed to get test questions")
                return False
            
            print(f"✅ Retrieved {len(test_data['questions'])} questions for test")
            
            # Submit answers for each question
            for question_data in test_data['questions']:
                question = question_data['test_question']
                exercise = question_data['exercise']
                
                # Generate a sample answer based on exercise type
                answer_data = generate_sample_answer(exercise)
                
                answer_id = SubmissionService.submit_answer(
                    submission.id, 
                    question['id'], 
                    exercise['id'],
                    answer_data,
                    db=db
                )
                
                if answer_id:
                    print(f"✅ Submitted answer for question {question['id']}")
                else:
                    print(f"❌ Failed to submit answer for question {question['id']}")
            
            # Complete the submission
            result = SubmissionService.complete_submission(submission.id, db=db)
            
            if result and 'score' in result:
                print(f"✅ Completed submission with score: {result['score']['percentage']}%")
                print(f"✅ Needs manual grading: {result['needs_manual_grading']}")
            else:
                print("❌ Failed to complete submission")
                return False
            
            # Get student submissions
            submissions = SubmissionService.get_student_submissions(student.id, db=db)
            
            if submissions:
                print(f"✅ Retrieved {len(submissions)} test assignments for student")
            else:
                print("❌ Failed to retrieve student submissions")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Service layer test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def generate_sample_answer(exercise):
    """Generate a sample answer for an exercise based on its type."""
    exercise_type = exercise['exercise_type']
    answer_data = exercise['answer_data']
    
    if exercise_type == 'multiple_choice':
        options = answer_data.get('options', [])
        if options:
            return {'selected_option': random.choice([opt['id'] for opt in options])}
        return {'selected_option': 'A'}
        
    elif exercise_type == 'true_false':
        return {'is_true': random.choice([True, False])}
        
    elif exercise_type == 'fill_blank':
        return {'text': 'Sample answer text'}
        
    elif exercise_type == 'matching_words':
        left_items = [item['id'] for item in answer_data.get('left_items', [])]
        right_items = [item['id'] for item in answer_data.get('right_items', [])]
        
        # Shuffle to create somewhat random pairs
        random.shuffle(right_items)
        
        pairs = []
        for i in range(min(len(left_items), len(right_items))):
            pairs.append([left_items[i], right_items[i]])
            
        return {'pairs': pairs}
        
    elif exercise_type == 'sentence_reordering':
        items = [item['id'] for item in answer_data.get('items', [])]
        random.shuffle(items)
        return {'order': items}
        
    elif exercise_type == 'cloze_test':
        blanks = {}
        for blank_id in answer_data.get('blanks', {}).keys():
            blanks[blank_id] = f"Answer for blank {blank_id}"
        return {'blanks': blanks}
        
    elif exercise_type == 'word_scramble':
        return {'word': 'unscrambled'}
        
    elif exercise_type == 'image_labeling':
        labels = {}
        for label_id in answer_data.get('labels', {}).keys():
            labels[label_id] = f"Label {label_id}"
        return {'labels': labels}
        
    elif exercise_type == 'long_answer':
        return {'text': 'This is a long answer response for testing purposes. ' * 5}
        
    # Default case
    return {'answer': 'Sample answer'}

def run_all_tests():
    """Run all tests."""
    tests = [
        test_connection,
        test_model_validation,
        test_crud_operations,
        test_generate_data,
        test_services
    ]
    
    results = []
    for test_func in tests:
        result = test_func()
        results.append(result)
    
    print("\n==== Test Summary ====")
    for i, result in enumerate(results):
        test_name = tests[i].__name__
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
    
    if all(results):
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed. Check the logs above for details.")


if __name__ == "__main__":
    run_all_tests() 