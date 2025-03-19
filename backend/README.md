# LMS Backend

This directory contains the backend code for the Learning Management System (LMS).

## Project Structure

The project follows a domain-driven design approach with clear separation of concerns:

```
lms/backend/
│
├── app/                      # Main application package
│   ├── crud/                 # Database operations (Create, Read, Update, Delete)
│   │   ├── __init__.py       # Exports all CRUD operations
│   │   ├── course.py         # Course-related operations
│   │   ├── exercise.py       # Exercise-related operations
│   │   ├── lesson.py         # Lesson-related operations
│   │   ├── submission.py     # Submission-related operations
│   │   └── user.py           # User-related operations
│   │
│   ├── models/               # SQLAlchemy database models
│   │   ├── __init__.py       # Exports all models and Base
│   │   ├── course.py         # Course-related models
│   │   ├── exercise.py       # Exercise-related models
│   │   ├── lesson.py         # Lesson-related models
│   │   ├── submission.py     # Submission-related models
│   │   └── user.py           # User-related models
│   │
│   ├── routes/               # API route definitions
│   │   ├── __init__.py       # Exports router
│   │   ├── auth_routes.py    # Authentication routes
│   │   ├── course_routes.py  # Course-related routes
│   │   ├── exercise_routes.py# Exercise-related routes
│   │   ├── lesson_routes.py  # Lesson-related routes
│   │   └── user_routes.py    # User-related routes
│   │
│   ├── schemas/              # Pydantic models for request/response validation
│   │   ├── __init__.py       # Exports all schemas
│   │   ├── course.py         # Course-related schemas
│   │   ├── exercise.py       # Exercise-related schemas
│   │   ├── lesson.py         # Lesson-related schemas
│   │   ├── submission.py     # Submission-related schemas
│   │   └── user.py           # User-related schemas
│   │
│   ├── services/             # Business logic services
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Authentication service
│   │   └── email_service.py  # Email service
│   │
│   ├── utils/                # Utility functions and helpers
│   │   ├── __init__.py       # Exports utility functions
│   │   ├── auth.py           # Authentication utilities
│   │   ├── logging.py        # Logging utilities
│   │   ├── pagination.py     # Pagination utilities
│   │   └── validation.py     # Input validation utilities
│   │
│   ├── main.py               # Application entry point
│   ├── config.py             # Application configuration
│   └── dependencies.py       # FastAPI dependencies
│
├── tests/                    # Test suite
│   ├── conftest.py           # Test configuration and fixtures
│   ├── test_api/             # API tests
│   └── test_utils/           # Utility tests
│
├── alembic/                  # Database migration scripts
├── logs/                     # Application logs
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Design Principles

1. **Domain-Driven Design**: Code is organized by domain (lessons, courses, etc.) rather than by technical function.
2. **Separation of Concerns**: Clear separation between models, schemas, API routes, and business logic.
3. **Type Safety**: Extensive use of Python type hints and Pydantic for validation.
4. **Dependency Injection**: Using FastAPI's dependency injection system for clean, testable code.
5. **Asynchronous**: Built on FastAPI and SQLAlchemy's async capabilities for high performance.

## Key Components

### Models

SQLAlchemy models representing database tables, organized by domain. All models inherit from `Base`.

### Schemas

Pydantic models for request/response validation and serialization/deserialization:
- `*Base`: Base schemas with common fields
- `*Create`: Schemas for creation requests
- `*Update`: Schemas for update requests
- `*InDB`: Schemas representing database state
- `*`: Schemas for API responses

### CRUD Operations

Database operations organized by domain, with async functions for all CRUD operations.

### Routes

API endpoints defined using FastAPI routers, organized by domain.

### Services

Business logic services that orchestrate operations across multiple domains or provide external functionality.

### Utils

Utility functions and helpers used throughout the application, including authentication, logging, and validation.

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
uvicorn app.main:app --reload
```

3. Access the API documentation:
```
http://localhost:8000/docs
```

## Database Management

Database migrations are managed using Alembic. See `lms/database/README.md` for more information.