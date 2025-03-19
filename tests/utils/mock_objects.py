#!/usr/bin/env python3
"""
Mock objects for testing the LMS system.
These objects can be used as substitutes for real components in tests.
"""

import json
import random
from datetime import datetime, timedelta
from unittest.mock import MagicMock

class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.data = {
            "users": {},
            "courses": {},
            "lessons": {},
            "exercises": {},
            "submissions": {}
        }
        self.id_counters = {table: 1 for table in self.data.keys()}
    
    def insert(self, table, record):
        """Insert a record into a table."""
        if table not in self.data:
            raise ValueError(f"Table {table} does not exist")
        
        record_id = self.id_counters[table]
        self.id_counters[table] += 1
        
        record = record.copy()
        record["id"] = record_id
        
        # Add timestamps if not present
        now = datetime.now().isoformat()
        if "created_at" not in record:
            record["created_at"] = now
        if "updated_at" not in record:
            record["updated_at"] = now
            
        self.data[table][record_id] = record
        return record_id
    
    def get(self, table, record_id):
        """Get a record from a table by ID."""
        if table not in self.data:
            raise ValueError(f"Table {table} does not exist")
        
        return self.data[table].get(record_id)
    
    def query(self, table, **filters):
        """Query records from a table with filters."""
        if table not in self.data:
            raise ValueError(f"Table {table} does not exist")
        
        results = []
        for record in self.data[table].values():
            match = True
            for key, value in filters.items():
                if key not in record or record[key] != value:
                    match = False
                    break
            if match:
                results.append(record)
        
        return results
    
    def update(self, table, record_id, updates):
        """Update a record in a table."""
        if table not in self.data:
            raise ValueError(f"Table {table} does not exist")
        
        record = self.get(table, record_id)
        if not record:
            return False
        
        for key, value in updates.items():
            record[key] = value
        
        record["updated_at"] = datetime.now().isoformat()
        return True
    
    def delete(self, table, record_id):
        """Delete a record from a table."""
        if table not in self.data:
            raise ValueError(f"Table {table} does not exist")
        
        if record_id in self.data[table]:
            del self.data[table][record_id]
            return True
        return False
    
    def clear(self):
        """Clear all data from the database."""
        for table in self.data:
            self.data[table] = {}
        self.id_counters = {table: 1 for table in self.data.keys()}


class MockUser:
    """Mock user for testing."""
    
    def __init__(self, id=None, username=None, email=None, user_type="student"):
        self.id = id or random.randint(1, 1000)
        self.username = username or f"user_{self.id}"
        self.email = email or f"{self.username}@example.com"
        self.user_type = user_type
        self.created_at = datetime.now()
        self.active = True
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "user_type": self.user_type,
            "created_at": self.created_at.isoformat(),
            "active": self.active
        }


class MockCourse:
    """Mock course for testing."""
    
    def __init__(self, id=None, title=None, description=None, creator_id=None):
        self.id = id or random.randint(1, 1000)
        self.title = title or f"Course {self.id}"
        self.description = description or f"Description for course {self.id}"
        self.creator_id = creator_id or random.randint(1, 100)
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.active = True
        self.lessons = []
    
    def add_lesson(self, lesson):
        """Add a lesson to the course."""
        lesson.course_id = self.id
        self.lessons.append(lesson)
        return lesson
    
    def to_dict(self):
        """Convert course to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "creator_id": self.creator_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "active": self.active,
            "lessons": [lesson.to_dict() for lesson in self.lessons]
        }


class MockLesson:
    """Mock lesson for testing."""
    
    def __init__(self, id=None, title=None, content=None, course_id=None, order=None):
        self.id = id or random.randint(1, 1000)
        self.title = title or f"Lesson {self.id}"
        self.content = content or f"Content for lesson {self.id}"
        self.course_id = course_id
        self.order = order or 1
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.exercises = []
    
    def add_exercise(self, exercise):
        """Add an exercise to the lesson."""
        exercise.lesson_id = self.id
        self.exercises.append(exercise)
        return exercise
    
    def to_dict(self):
        """Convert lesson to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "course_id": self.course_id,
            "order": self.order,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "exercises": [exercise.to_dict() for exercise in self.exercises]
        }


class MockExercise:
    """Mock exercise for testing."""
    
    def __init__(self, id=None, lesson_id=None, question=None, 
                 exercise_type="multiple_choice", answer_options=None, correct_answer=None):
        self.id = id or random.randint(1, 1000)
        self.lesson_id = lesson_id
        self.question = question or f"Question for exercise {self.id}"
        self.exercise_type = exercise_type
        
        if exercise_type == "multiple_choice":
            self.answer_options = answer_options or json.dumps([f"Option {i}" for i in range(1, 5)])
            self.correct_answer = correct_answer or "Option 1"
        else:
            self.answer_options = answer_options
            self.correct_answer = correct_answer or "Correct answer"
            
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    def check_answer(self, answer):
        """Check if an answer is correct."""
        if self.exercise_type == "multiple_choice":
            try:
                answered = json.loads(answer)
                return self.correct_answer in answered
            except:
                return False
        else:
            return answer == self.correct_answer
    
    def to_dict(self):
        """Convert exercise to dictionary."""
        return {
            "id": self.id,
            "lesson_id": self.lesson_id,
            "question": self.question,
            "exercise_type": self.exercise_type,
            "answer_options": self.answer_options,
            "correct_answer": self.correct_answer,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class MockSubmission:
    """Mock submission for testing."""
    
    def __init__(self, id=None, user_id=None, exercise_id=None, answer_text=None):
        self.id = id or random.randint(1, 1000)
        self.user_id = user_id or random.randint(1, 100)
        self.exercise_id = exercise_id
        self.answer_text = answer_text or ""
        self.is_correct = False  # To be set by check_answer
        self.created_at = datetime.now()
    
    def to_dict(self):
        """Convert submission to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "exercise_id": self.exercise_id,
            "answer_text": self.answer_text,
            "is_correct": self.is_correct,
            "created_at": self.created_at.isoformat()
        }


# Mock HTTP/API objects

class MockResponse:
    """Mock HTTP response for testing."""
    
    def __init__(self, status_code=200, data=None, headers=None):
        self.status_code = status_code
        self.data = data or {}
        self.headers = headers or {"Content-Type": "application/json"}
    
    def json(self):
        """Return JSON data."""
        return self.data
    
    def text(self):
        """Return text data."""
        return json.dumps(self.data)


class MockAPIClient:
    """Mock API client for testing."""
    
    def __init__(self):
        self.mock_database = MockDatabase()
        self.base_url = "https://api.example.com"
        self.headers = {"Content-Type": "application/json"}
        self.token = None
    
    def set_token(self, token):
        """Set authentication token."""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def get(self, endpoint, params=None):
        """Mock GET request."""
        # Implement mock API endpoints here
        if endpoint == "/courses":
            courses = list(self.mock_database.data["courses"].values())
            return MockResponse(200, courses)
        elif endpoint.startswith("/courses/"):
            course_id = int(endpoint.split("/")[2])
            course = self.mock_database.get("courses", course_id)
            if not course:
                return MockResponse(404, {"error": "Course not found"})
            return MockResponse(200, course)
        # Add more endpoints as needed
        return MockResponse(404, {"error": "Endpoint not found"})
    
    def post(self, endpoint, data=None, json_data=None):
        """Mock POST request."""
        if endpoint == "/auth/login":
            return MockResponse(200, {"access_token": "mock_token"})
        elif endpoint == "/auth/register":
            user_id = self.mock_database.insert("users", json_data)
            return MockResponse(201, {"id": user_id})
        # Add more endpoints as needed
        return MockResponse(404, {"error": "Endpoint not found"})
    
    def put(self, endpoint, data=None, json_data=None):
        """Mock PUT request."""
        if endpoint.startswith("/courses/"):
            course_id = int(endpoint.split("/")[2])
            success = self.mock_database.update("courses", course_id, json_data)
            if not success:
                return MockResponse(404, {"error": "Course not found"})
            return MockResponse(200, self.mock_database.get("courses", course_id))
        # Add more endpoints as needed
        return MockResponse(404, {"error": "Endpoint not found"})
    
    def delete(self, endpoint):
        """Mock DELETE request."""
        if endpoint.startswith("/courses/"):
            course_id = int(endpoint.split("/")[2])
            success = self.mock_database.delete("courses", course_id)
            if not success:
                return MockResponse(404, {"error": "Course not found"})
            return MockResponse(204)
        # Add more endpoints as needed
        return MockResponse(404, {"error": "Endpoint not found"})


# Mock database session

class MockSession:
    """Mock database session for testing."""
    
    def __init__(self):
        self.mock_database = MockDatabase()
        self.committed = False
        self.rolled_back = False
        self.closed = False
        self.query_results = {}
    
    def add(self, obj):
        """Add an object to the session."""
        if hasattr(obj, 'to_dict'):
            obj_dict = obj.to_dict()
            table_name = obj.__class__.__name__.lower() + 's'  # Simple pluralization
            obj.id = self.mock_database.insert(table_name, obj_dict)
    
    def commit(self):
        """Commit the session."""
        self.committed = True
    
    def rollback(self):
        """Roll back the session."""
        self.rolled_back = True
    
    def close(self):
        """Close the session."""
        self.closed = True
    
    def query(self, model):
        """Create a query object."""
        query = MagicMock()
        table_name = model.__name__.lower() + 's'  # Simple pluralization
        
        # Configure the mock to return data from our mock database
        query.all.return_value = [model(**record) for record in self.mock_database.data.get(table_name, {}).values()]
        query.first.return_value = next(iter([model(**record) for record in self.mock_database.data.get(table_name, {}).values()]), None)
        
        # Store in query_results for later inspection
        self.query_results[model.__name__] = query
        
        return query
    
    def execute(self, statement):
        """Execute a SQL statement."""
        # This is a simplified mock that doesn't parse SQL
        return MagicMock() 