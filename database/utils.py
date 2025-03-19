#!/usr/bin/env python3

import re
import json
import uuid
import secrets
import datetime
import hashlib
import random
from typing import List, Dict, Any, Optional, Union

from .db_manager import DBManager
from .models import Student, Test, Exercise, TestQuestion, StudentTest


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """Validate username format."""
    if not username or not isinstance(username, str):
        return False
    if len(username) < 3 or len(username) > 50:
        return False
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))


def generate_secure_token(length=32):
    """Generate a secure random token for authentication."""
    return secrets.token_hex(length)


def create_session(student_id, ip_address=None, user_agent=None, 
                 db=None, username=None, session_id=None, source_ip=None):
    """Create a new session for a student."""
    token = generate_secure_token()
    session_id = str(uuid.uuid4())
    
    should_close_db = False
    try:
        if db is None:
            db = DBManager()
            should_close_db = True
            
        # Insert session record
        query = """
            INSERT INTO auth_logs 
            (student_id, token, session_id, ip_address, user_agent, created_at, expires_at, is_active)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, TRUE)
            RETURNING id
        """
        
        # Session expires in 12 hours
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=12)
        
        result = db.fetch_one(
            query, 
            [student_id, token, session_id, ip_address, user_agent, expires_at],
            username, session_id, source_ip
        )
        
        if result:
            return {
                'id': result[0],
                'token': token,
                'session_id': session_id,
                'expires_at': expires_at
            }
        return None
    finally:
        if should_close_db and db:
            db.close()


def validate_session(token, session_id, db=None, username=None, user_session_id=None, source_ip=None):
    """Validate a session token."""
    should_close_db = False
    try:
        if db is None:
            db = DBManager()
            should_close_db = True
            
        # Check for valid session
        query = """
            SELECT student_id, expires_at, is_active
            FROM auth_logs
            WHERE token = %s AND session_id = %s
        """
        
        result = db.fetch_one(
            query, 
            [token, session_id],
            username, user_session_id, source_ip
        )
        
        if not result:
            return None
            
        student_id, expires_at, is_active = result
        
        # Check if session is expired or inactive
        if not is_active or datetime.datetime.now() > expires_at:
            # Mark as inactive
            update_query = """
                UPDATE auth_logs
                SET is_active = FALSE
                WHERE token = %s AND session_id = %s
            """
            db.execute(update_query, [token, session_id], username, user_session_id, source_ip)
            return None
            
        return student_id
    finally:
        if should_close_db and db:
            db.close()


def end_session(token, session_id, db=None, username=None, user_session_id=None, source_ip=None):
    """End a session (logout)."""
    should_close_db = False
    try:
        if db is None:
            db = DBManager()
            should_close_db = True
            
        # Mark session as inactive
        query = """
            UPDATE auth_logs
            SET is_active = FALSE
            WHERE token = %s AND session_id = %s
        """
        
        db.execute(query, [token, session_id], username, user_session_id, source_ip)
        return True
    finally:
        if should_close_db and db:
            db.close()


def generate_test_data(db=None, num_students=10, num_exercises_per_type=2, num_tests=3):
    """Generate test data for development and testing."""
    should_close_db = False
    try:
        if db is None:
            db = DBManager()
            should_close_db = True
            
        print("Generating test data...")
        
        # Create students
        student_ids = []
        for i in range(num_students):
            student = Student(
                username=f"student{i+1}",
                email=f"student{i+1}@example.com",
                full_name=f"Student {i+1}",
                password_hash=Student.hash_password("password"),
                created_at=datetime.datetime.now(),
                is_active=True
            )
            student_id = student.save(db)
            student_ids.append(student_id)
            print(f"Created student {student_id}: {student.username}")
            
        # Create exercises for each type
        exercise_types = [
            'multiple_choice', 'true_false', 'fill_blank', 
            'matching_words', 'sentence_reordering', 'cloze_test',
            'word_scramble', 'image_labeling', 'long_answer'
        ]
        
        exercise_ids_by_type = {}
        
        for exercise_type in exercise_types:
            exercise_ids = []
            
            for i in range(num_exercises_per_type):
                # Create exercise data based on type
                answer_data = generate_exercise_data(exercise_type, i+1)
                
                exercise = Exercise(
                    exercise_type=exercise_type,
                    question=f"Sample question for {exercise_type} #{i+1}",
                    answer_data=answer_data,
                    created_at=datetime.datetime.now(),
                    max_score=get_max_score_for_type(exercise_type),
                    grading_type=get_grading_type_for_type(exercise_type)
                )
                
                exercise_id = exercise.save(db)
                exercise_ids.append(exercise_id)
                print(f"Created {exercise_type} exercise {exercise_id}")
                
            exercise_ids_by_type[exercise_type] = exercise_ids
            
        # Create tests
        test_ids = []
        for i in range(num_tests):
            test = Test(
                title=f"Sample Test {i+1}",
                description=f"Description for Sample Test {i+1}",
                duration_minutes=60,
                randomize_questions=(i % 2 == 0),  # Every other test randomizes
                passing_score=70,
                created_at=datetime.datetime.now(),
                created_by="admin",
                is_active=True
            )
            
            test_id = test.save(db)
            test_ids.append(test_id)
            print(f"Created test {test_id}: {test.title}")
            
            # Add questions to test
            question_order = 1
            for exercise_type, exercise_ids in exercise_ids_by_type.items():
                for exercise_id in exercise_ids:
                    question = TestQuestion(
                        test_id=test_id,
                        exercise_id=exercise_id,
                        question_order=question_order,
                        weight=1.0,
                        is_required=True
                    )
                    
                    question_id = question.save(db)
                    print(f"Added question {question_id} to test {test_id}")
                    
                    question_order += 1
                    
        # Assign tests to students
        for student_id in student_ids:
            for test_id in test_ids:
                student_test = StudentTest(
                    student_id=student_id,
                    test_id=test_id,
                    assigned_at=datetime.datetime.now(),
                    due_at=datetime.datetime.now() + datetime.timedelta(days=7),
                    max_attempts=2,
                    attempts_used=0
                )
                
                assignment_id = student_test.save(db)
                print(f"Assigned test {test_id} to student {student_id}, ID: {assignment_id}")
                
        print("Test data generation complete!")
        return True
    finally:
        if should_close_db and db:
            db.close()


def generate_exercise_data(exercise_type, index):
    """Generate sample answer data for an exercise based on its type."""
    if exercise_type == 'multiple_choice':
        return {
            'options': [
                {'id': 'A', 'text': 'Option A'},
                {'id': 'B', 'text': 'Option B'},
                {'id': 'C', 'text': 'Option C'},
                {'id': 'D', 'text': 'Option D'}
            ],
            'correct_option': 'B'
        }
        
    elif exercise_type == 'true_false':
        return {
            'statement': 'This is a sample true/false statement.',
            'is_true': index % 2 == 0  # Alternates between true and false
        }
        
    elif exercise_type == 'fill_blank':
        return {
            'text': 'The correct answer',
            'alternatives': ['Another accepted answer', 'Yet another accepted answer']
        }
        
    elif exercise_type == 'matching_words':
        return {
            'left_items': [
                {'id': 'L1', 'text': 'Left Item 1'},
                {'id': 'L2', 'text': 'Left Item 2'},
                {'id': 'L3', 'text': 'Left Item 3'}
            ],
            'right_items': [
                {'id': 'R1', 'text': 'Right Item 1'},
                {'id': 'R2', 'text': 'Right Item 2'},
                {'id': 'R3', 'text': 'Right Item 3'}
            ],
            'pairs': [
                ['L1', 'R3'],
                ['L2', 'R1'],
                ['L3', 'R2']
            ]
        }
        
    elif exercise_type == 'sentence_reordering':
        return {
            'items': [
                {'id': '1', 'text': 'First part of the sentence.'},
                {'id': '2', 'text': 'Second part of the sentence.'},
                {'id': '3', 'text': 'Third part of the sentence.'},
                {'id': '4', 'text': 'Fourth part of the sentence.'}
            ],
            'order': ['1', '2', '3', '4']
        }
        
    elif exercise_type == 'cloze_test':
        return {
            'text': 'This is a sample [1] with multiple [2] for testing [3] functionality.',
            'blanks': {
                '1': 'sentence',
                '2': 'blanks',
                '3': 'cloze'
            },
            'alternatives': {
                '1': ['text', 'passage'],
                '2': ['gaps', 'spaces'],
                '3': ['fill-in-the-blank']
            }
        }
        
    elif exercise_type == 'word_scramble':
        words = ['programming', 'database', 'algorithm', 'function', 'variable']
        word = words[index % len(words)]
        scrambled = list(word)
        random.shuffle(scrambled)
        return {
            'scrambled': ''.join(scrambled),
            'word': word
        }
        
    elif exercise_type == 'image_labeling':
        return {
            'image_url': 'https://example.com/sample-image.jpg',
            'labels': {
                'label1': 'Mountain',
                'label2': 'River',
                'label3': 'Forest'
            },
            'alternatives': {
                'label1': ['Peak', 'Hill'],
                'label2': ['Stream', 'Water'],
                'label3': ['Trees', 'Woods']
            }
        }
        
    elif exercise_type == 'long_answer':
        return {
            'min_words': 50,
            'max_words': 200,
            'rubric': [
                {'criterion': 'Content', 'description': 'Addresses all aspects of the prompt', 'points': 5},
                {'criterion': 'Organization', 'description': 'Well-structured with clear flow', 'points': 3},
                {'criterion': 'Language', 'description': 'Proper grammar and vocabulary', 'points': 2}
            ]
        }
        
    # Default case
    return {'sample': 'data'}


def get_max_score_for_type(exercise_type):
    """Get the default max score for an exercise type."""
    if exercise_type == 'long_answer':
        return 10
    elif exercise_type in ['matching_words', 'sentence_reordering', 'cloze_test', 'image_labeling']:
        return 5
    else:
        return 1


def get_grading_type_for_type(exercise_type):
    """Get the default grading type for an exercise type."""
    if exercise_type in ['long_answer']:
        return 'manual'
    else:
        return 'auto'


def clean_test_data(db=None):
    """Clean up test data - useful for resetting the test environment."""
    should_close_db = False
    try:
        if db is None:
            db = DBManager()
            should_close_db = True
            
        # Disable foreign key checks (PostgreSQL version)
        db.execute("SET session_replication_role = 'replica'")
        
        # Clean up tables in reverse order of dependencies
        tables = [
            'scores', 'submission_answers', 'submissions', 'student_tests', 
            'test_questions', 'tests', 'exercises', 'auth_logs', 'students'
        ]
        
        for table in tables:
            db.execute(f"TRUNCATE TABLE {table} CASCADE")
            print(f"Truncated table: {table}")
            
        # Re-enable foreign key checks
        db.execute("SET session_replication_role = 'origin'")
        
        print("Test data cleanup complete!")
        return True
    finally:
        if should_close_db and db:
            db.close() 