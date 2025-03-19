# Testing Instructions

This document provides instructions on running tests for the LMS API.

## Setting Up the Test Environment

1. **Install test dependencies**

   ```bash
   pip install -r backend/requirements-test.txt
   ```

2. **Navigate to the project directory**

   ```bash
   cd /home/ubuntu/lms
   ```

## Running Tests

### Running all tests

To run all tests:

```bash
pytest backend/tests -v
```

### Running with coverage report

To run tests with coverage report:

```bash
pytest backend/tests --cov=app -v
```

### Running specific test files

To run a specific test file:

```bash
# Authentication tests
pytest backend/tests/test_auth.py -v

# Exercise tests
pytest backend/tests/test_exercises.py -v

# Evaluation tests
pytest backend/tests/test_evaluation.py -v
```

### Running specific test functions

To run a specific test function:

```bash
pytest backend/tests/test_auth.py::test_login_for_access_token -v
```

## Test Structure

The tests are organized as follows:

1. **Authentication Tests** (`test_auth.py`)
   - User registration
   - Login functionality
   - Token validation
   - Permission checking

2. **Exercise Tests** (`test_exercises.py`)
   - Exercise template creation and retrieval
   - Exercise content management
   - Role-based permission checks
   - Media asset handling

3. **Evaluation Tests** (`test_evaluation.py`)
   - Exercise response evaluation
   - Scoring algorithms for different exercise types
   - Answer validation

## Common Test Fixtures

Common test fixtures are defined in `conftest.py` and include:

- Database setup and teardown
- Test users with different roles
- Authentication tokens
- Test exercise templates and content

## CI/CD Integration

When adding new features, ensure that you:

1. Write tests for new functionality
2. Run the test suite to verify everything still works
3. Fix any failing tests before merging

## Testing API Documentation

To test the enhanced Swagger documentation:

1. Start the FastAPI server
2. Visit `/docs` endpoint in your browser
3. Verify that all endpoints are properly documented
4. Test the authentication using the Authorize button in the Swagger UI 