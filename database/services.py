#!/usr/bin/env python3

import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from .db_manager import DBManager
from .models import Student, Test, Exercise, TestQuestion, StudentTest, Submission, SubmissionAnswer, Score, ValidationError


class TestService:
    """Service for test-related operations."""
    
    @staticmethod
    def create_test(title, description, duration_minutes, passing_score=None, 
                   randomize_questions=False, created_by=None, db=None, 
                   username=None, session_id=None, source_ip=None) -> int:
        """Create a new test."""
        test = Test(
            title=title,
            description=description,
            duration_minutes=duration_minutes,
            passing_score=passing_score,
            randomize_questions=randomize_questions,
            created_by=created_by,
            created_at=datetime.now(),
            is_active=True
        )
        
        return test.save(db, username, session_id, source_ip)
    
    @staticmethod
    def add_question_to_test(test_id, exercise_id, question_order, weight=1.0, 
                            is_required=True, db=None, username=None, 
                            session_id=None, source_ip=None) -> int:
        """Add a question to a test."""
        # Check if test exists
        test = Test.find_by_id(test_id, db, username, session_id, source_ip)
        if not test:
            raise ValidationError(f"Test with ID {test_id} not found")
            
        # Check if exercise exists
        exercise = Exercise.find_by_id(exercise_id, db, username, session_id, source_ip)
        if not exercise:
            raise ValidationError(f"Exercise with ID {exercise_id} not found")
            
        # Create test question
        test_question = TestQuestion(
            test_id=test_id,
            exercise_id=exercise_id,
            question_order=question_order,
            weight=weight,
            is_required=is_required
        )
        
        return test_question.save(db, username, session_id, source_ip)
    
    @staticmethod
    def get_test_with_questions(test_id, db=None, username=None, session_id=None, source_ip=None) -> dict:
        """Get test with all questions and exercises."""
        # Check if test exists
        test = Test.find_by_id(test_id, db, username, session_id, source_ip)
        if not test:
            raise ValidationError(f"Test with ID {test_id} not found")
            
        # Get questions with exercises
        questions = test.get_exercises(db, username, session_id, source_ip)
        
        # Format result
        result = test.to_dict()
        result['questions'] = []
        
        for question in questions:
            # Extract exercise data
            exercise_data = {k.replace('exercises.', ''): v for k, v in question.items() 
                            if k.startswith('exercises.')}
            
            # Extract question data
            question_data = {k: v for k, v in question.items() 
                            if not k.startswith('exercises.')}
            
            # Parse answer data if it's a JSON string
            if isinstance(exercise_data.get('answer_data'), str):
                try:
                    exercise_data['answer_data'] = json.loads(exercise_data['answer_data'])
                except:
                    pass
            
            # Add to result
            result['questions'].append({
                'test_question': question_data,
                'exercise': exercise_data
            })
        
        return result
    
    @staticmethod
    def assign_test_to_student(student_id, test_id, due_at=None, max_attempts=1, 
                             db=None, username=None, session_id=None, source_ip=None) -> int:
        """Assign a test to a student."""
        # Check if student exists
        student = Student.find_by_id(student_id, db, username, session_id, source_ip)
        if not student:
            raise ValidationError(f"Student with ID {student_id} not found")
            
        # Check if test exists
        test = Test.find_by_id(test_id, db, username, session_id, source_ip)
        if not test:
            raise ValidationError(f"Test with ID {test_id} not found")
            
        # Check if already assigned
        existing = StudentTest.find_by_student_and_test(
            student_id, test_id, db, username, session_id, source_ip
        )
        
        if existing:
            # Update if already assigned
            existing.due_at = due_at
            existing.max_attempts = max_attempts
            return existing.save(db, username, session_id, source_ip)
        else:
            # Create new assignment
            student_test = StudentTest(
                student_id=student_id,
                test_id=test_id,
                assigned_at=datetime.now(),
                due_at=due_at,
                max_attempts=max_attempts,
                attempts_used=0
            )
            
            return student_test.save(db, username, session_id, source_ip)


class SubmissionService:
    """Service for test submission operations."""
    
    @staticmethod
    def start_test(student_id, test_id, ip_address=None, user_agent=None, 
                  db=None, username=None, session_id=None, source_ip=None) -> Submission:
        """Start a new test submission."""
        # Check if student can take the test
        student_test = StudentTest.find_by_student_and_test(
            student_id, test_id, db, username, session_id, source_ip
        )
        
        if not student_test:
            raise ValidationError(f"Test {test_id} is not assigned to student {student_id}")
            
        if not student_test.can_take_test():
            raise ValidationError("Cannot take this test. It may be past due or max attempts reached.")
            
        # Increment attempts
        student_test.increment_attempts(db, username, session_id, source_ip)
        
        # Create submission
        submission = Submission(
            student_id=student_id,
            test_id=test_id,
            started_at=datetime.now(),
            status='in_progress',
            ip_address=ip_address,
            user_agent=user_agent,
            attempt_number=student_test.attempts_used
        )
        
        submission_id = submission.save(db, username, session_id, source_ip)
        submission.id = submission_id
        
        return submission
    
    @staticmethod
    def submit_answer(submission_id, question_id, exercise_id, answer_data,
                     db=None, username=None, session_id=None, source_ip=None) -> int:
        """Submit an answer for a question."""
        # Check if submission exists and is in progress
        submission = Submission.find_by_id(submission_id, db, username, session_id, source_ip)
        if not submission:
            raise ValidationError(f"Submission with ID {submission_id} not found")
            
        if submission.status != 'in_progress':
            raise ValidationError("Cannot submit answer. Test is not in progress.")
            
        # Check if question exists
        question = TestQuestion.find_by_id(question_id, db, username, session_id, source_ip)
        if not question:
            raise ValidationError(f"Question with ID {question_id} not found")
            
        if question.test_id != submission.test_id:
            raise ValidationError("Question does not belong to the test being taken")
            
        # Check if exercise exists
        exercise = Exercise.find_by_id(exercise_id, db, username, session_id, source_ip)
        if not exercise:
            raise ValidationError(f"Exercise with ID {exercise_id} not found")
            
        if exercise.id != question.exercise_id:
            raise ValidationError("Exercise does not match the question")
            
        # Check if answer already exists for this question
        should_close_db = False
        try:
            if db is None:
                db = DBManager()
                should_close_db = True
                
            query = """
                SELECT id FROM submission_answers 
                WHERE submission_id = %s AND question_id = %s
            """
            existing = db.fetch_one(query, [submission_id, question_id], username, session_id, source_ip)
            
            if existing:
                # Update existing answer
                answer = SubmissionAnswer.find_by_id(existing[0], db, username, session_id, source_ip)
                answer.answer_data = answer_data
                return answer.save(db, username, session_id, source_ip)
            else:
                # Create new answer
                answer = SubmissionAnswer(
                    submission_id=submission_id,
                    question_id=question_id,
                    exercise_id=exercise_id,
                    answer_data=answer_data
                )
                
                return answer.save(db, username, session_id, source_ip)
        finally:
            if should_close_db and db:
                db.close()
    
    @staticmethod
    def complete_submission(submission_id, db=None, username=None, session_id=None, source_ip=None) -> dict:
        """Complete a test submission and calculate initial automatic scores."""
        # Check if submission exists and is in progress
        submission = Submission.find_by_id(submission_id, db, username, session_id, source_ip)
        if not submission:
            raise ValidationError(f"Submission with ID {submission_id} not found")
            
        if submission.status != 'in_progress':
            raise ValidationError("Cannot complete submission. Test is not in progress.")
            
        # Get all answers for the submission
        answers = submission.get_answers(db, username, session_id, source_ip)
        
        # Submit the test (updates status and timestamps)
        submission.submit(db, username, session_id, source_ip)
        
        # Auto-grade answers where possible
        should_close_db = False
        try:
            if db is None:
                db = DBManager()
                should_close_db = True
                
            # Process each answer
            for answer in answers:
                # Get exercise to check answer against
                exercise = Exercise.find_by_id(answer.exercise_id, db, username, session_id, source_ip)
                
                # Skip if not auto-gradable
                if exercise.grading_type != 'auto':
                    continue
                    
                # Auto-grade based on exercise type
                is_correct, score, feedback = SubmissionService._auto_grade_answer(
                    exercise, answer.answer_data
                )
                
                # Save grading results
                answer.grade(
                    is_correct=is_correct, 
                    score=score, 
                    feedback=feedback,
                    graded_by='auto',
                    db=db, 
                    username=username, 
                    session_id=session_id, 
                    source_ip=source_ip
                )
            
            # Calculate final score
            score = Score.calculate_for_submission(
                submission_id, db, username, session_id, source_ip
            )
            
            # Return submission and score details
            return {
                'submission': submission.to_dict(),
                'score': score.to_dict() if score else None,
                'needs_manual_grading': any(
                    Exercise.find_by_id(a.exercise_id, db, username, session_id, source_ip).grading_type == 'manual' 
                    for a in answers
                )
            }
        finally:
            if should_close_db and db:
                db.close()
    
    @staticmethod
    def _auto_grade_answer(exercise, student_answer):
        """
        Auto-grade an answer based on exercise type.
        Returns (is_correct, score, feedback)
        """
        # Get correct answer from exercise
        correct_answer = exercise.answer_data
        
        # Default values
        is_correct = False
        score = 0
        feedback = None
        
        try:
            # Grade based on exercise type
            if exercise.exercise_type == 'multiple_choice':
                # Check if selected option matches correct option
                if student_answer.get('selected_option') == correct_answer.get('correct_option'):
                    is_correct = True
                    score = exercise.max_score
                    feedback = "Correct!"
                else:
                    feedback = f"Incorrect. The correct answer was: {correct_answer.get('correct_option')}"
                    
            elif exercise.exercise_type == 'true_false':
                # Check if boolean answer matches
                if student_answer.get('is_true') == correct_answer.get('is_true'):
                    is_correct = True
                    score = exercise.max_score
                    feedback = "Correct!"
                else:
                    feedback = f"Incorrect. The correct answer was: {'True' if correct_answer.get('is_true') else 'False'}"
                    
            elif exercise.exercise_type == 'fill_blank':
                # Compare student answer with correct answer, ignoring case
                student_text = student_answer.get('text', '').strip().lower()
                correct_text = correct_answer.get('text', '').strip().lower()
                
                if student_text == correct_text:
                    is_correct = True
                    score = exercise.max_score
                    feedback = "Correct!"
                else:
                    # Check for alternative answers if provided
                    alternatives = [alt.strip().lower() for alt in correct_answer.get('alternatives', [])]
                    if student_text in alternatives:
                        is_correct = True
                        score = exercise.max_score
                        feedback = "Correct!"
                    else:
                        feedback = f"Incorrect. The correct answer was: {correct_answer.get('text')}"
                        
            elif exercise.exercise_type == 'matching_words':
                # Compare student pairings with correct pairings
                student_pairs = student_answer.get('pairs', [])
                correct_pairs = correct_answer.get('pairs', [])
                
                # Count correct matches
                correct_count = sum(1 for sp in student_pairs if sp in correct_pairs)
                total_pairs = len(correct_pairs)
                
                if correct_count == total_pairs:
                    is_correct = True
                    score = exercise.max_score
                    feedback = "All pairs matched correctly!"
                else:
                    # Partial credit
                    score = (correct_count / total_pairs) * exercise.max_score
                    feedback = f"You matched {correct_count} out of {total_pairs} pairs correctly."
                    
            elif exercise.exercise_type == 'sentence_reordering':
                # Compare student order with correct order
                student_order = student_answer.get('order', [])
                correct_order = correct_answer.get('order', [])
                
                if student_order == correct_order:
                    is_correct = True
                    score = exercise.max_score
                    feedback = "Correct ordering!"
                else:
                    # Count items in correct position
                    correct_positions = sum(1 for i, item in enumerate(student_order) 
                                          if i < len(correct_order) and item == correct_order[i])
                    total_items = len(correct_order)
                    
                    # Partial credit
                    score = (correct_positions / total_items) * exercise.max_score
                    feedback = f"You placed {correct_positions} out of {total_items} items in the correct position."
                    
            elif exercise.exercise_type == 'cloze_test':
                # Grade each blank separately
                student_blanks = student_answer.get('blanks', {})
                correct_blanks = correct_answer.get('blanks', {})
                
                total_blanks = len(correct_blanks)
                correct_count = 0
                
                for blank_id, correct_text in correct_blanks.items():
                    # Get student answer for this blank
                    student_text = student_blanks.get(blank_id, '').strip().lower()
                    correct_text = correct_text.strip().lower()
                    
                    # Check if correct
                    alternatives = [alt.strip().lower() for alt in correct_answer.get('alternatives', {}).get(blank_id, [])]
                    if student_text == correct_text or student_text in alternatives:
                        correct_count += 1
                
                # Calculate score
                if correct_count == total_blanks:
                    is_correct = True
                    score = exercise.max_score
                    feedback = "All blanks filled correctly!"
                else:
                    # Partial credit
                    score = (correct_count / total_blanks) * exercise.max_score
                    feedback = f"You filled {correct_count} out of {total_blanks} blanks correctly."
                    
            elif exercise.exercise_type == 'word_scramble':
                # Compare unscrambled word with correct word
                student_word = student_answer.get('word', '').strip().lower()
                correct_word = correct_answer.get('word', '').strip().lower()
                
                if student_word == correct_word:
                    is_correct = True
                    score = exercise.max_score
                    feedback = "Correct unscrambling!"
                else:
                    feedback = f"Incorrect. The correct word was: {correct_word}"
                    
            elif exercise.exercise_type == 'image_labeling':
                # Compare student labels with correct labels
                student_labels = student_answer.get('labels', {})
                correct_labels = correct_answer.get('labels', {})
                
                total_labels = len(correct_labels)
                correct_count = 0
                
                for label_id, correct_text in correct_labels.items():
                    # Get student answer for this label
                    student_text = student_labels.get(label_id, '').strip().lower()
                    correct_text = correct_text.strip().lower()
                    
                    # Check if correct
                    alternatives = [alt.strip().lower() for alt in correct_answer.get('alternatives', {}).get(label_id, [])]
                    if student_text == correct_text or student_text in alternatives:
                        correct_count += 1
                
                # Calculate score
                if correct_count == total_labels:
                    is_correct = True
                    score = exercise.max_score
                    feedback = "All labels correct!"
                else:
                    # Partial credit
                    score = (correct_count / total_labels) * exercise.max_score
                    feedback = f"You labeled {correct_count} out of {total_labels} items correctly."
                    
            elif exercise.exercise_type == 'long_answer':
                # Long answers require manual grading
                feedback = "This answer requires manual grading."
                
            else:
                # Unknown exercise type
                feedback = f"Unsupported exercise type for auto-grading: {exercise.exercise_type}"
                
        except Exception as e:
            # Handle any errors in grading logic
            feedback = f"Error during auto-grading: {str(e)}"
            
        return is_correct, score, feedback
    
    @staticmethod
    def manually_grade_answer(answer_id, is_correct, score, feedback=None, 
                            grading_notes=None, db=None, username=None, 
                            session_id=None, source_ip=None) -> dict:
        """Manually grade a submission answer."""
        # Get the answer
        answer = SubmissionAnswer.find_by_id(answer_id, db, username, session_id, source_ip)
        if not answer:
            raise ValidationError(f"Answer with ID {answer_id} not found")
            
        # Grade the answer
        answer.grade(
            is_correct=is_correct,
            score=score,
            feedback=feedback,
            graded_by=username or 'manual',
            grading_notes=grading_notes,
            db=db,
            username=username,
            session_id=session_id,
            source_ip=source_ip
        )
        
        # Recalculate submission score
        score = Score.calculate_for_submission(
            answer.submission_id, db, username, session_id, source_ip
        )
        
        return {
            'answer': answer.to_dict(),
            'score': score.to_dict() if score else None
        }
    
    @staticmethod
    def get_student_submissions(student_id, db=None, username=None, 
                              session_id=None, source_ip=None) -> list:
        """Get all submissions for a student."""
        should_close_db = False
        try:
            if db is None:
                db = DBManager()
                should_close_db = True
                
            # Get student test assignments
            query = """
                SELECT st.*, t.title as test_title, t.passing_score
                FROM student_tests st
                JOIN tests t ON st.test_id = t.id
                WHERE st.student_id = %s
                ORDER BY st.assigned_at DESC
            """
            assignments = db.fetch_all(query, [student_id], username, session_id, source_ip)
            
            result = []
            for assignment in assignments:
                # Get submissions for this test
                submissions = Submission.find_by_student_and_test(
                    student_id, assignment['test_id'], db=db, 
                    username=username, session_id=session_id, source_ip=source_ip
                )
                
                # Get scores for this test
                scores = Score.find_by_student_and_test(
                    student_id, assignment['test_id'], db=db,
                    username=username, session_id=session_id, source_ip=source_ip
                )
                
                # Format result
                result.append({
                    'test_id': assignment['test_id'],
                    'test_title': assignment['test_title'],
                    'assigned_at': assignment['assigned_at'],
                    'due_at': assignment['due_at'],
                    'max_attempts': assignment['max_attempts'],
                    'attempts_used': assignment['attempts_used'],
                    'passing_score': assignment['passing_score'],
                    'submissions': [s.to_dict() for s in submissions],
                    'scores': [s.to_dict() for s in scores],
                    'best_score': max([s.percentage for s in scores], default=0) if scores else None,
                    'has_passed': any(s.is_passing for s in scores) if scores else False
                })
                
            return result
        finally:
            if should_close_db and db:
                db.close() 