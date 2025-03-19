# LMS Testing Framework

This directory contains the testing framework for the LMS system. The tests are organized into different categories based on their scope and purpose.

## Test Directory Structure

```
tests/
├── api/             # API endpoint tests
├── integration/     # Integration tests between components
├── unit/            # Unit tests for individual components
├── utils/           # Test utilities and helpers
│   ├── test_helpers.py  # Common fixtures and utility functions
│   └── mock_objects.py  # Mock implementations for test isolation
├── conftest.py      # Shared pytest configuration and fixtures
├── fixtures/        # Test data fixtures
├── run_all_tests.py # Script to run all tests
└── pytest.ini       # Pytest configuration
```

## Test Categories

1. **Unit Tests**: Tests for individual functions and classes
   - Located in `tests/unit/`
   - Fast to run, minimal dependencies
   - Example: `test_database.py` - Tests database operations in isolation

2. **Integration Tests**: Tests for interactions between components
   - Located in `tests/integration/`
   - May require multiple components or database
   - Example: `test_database_workflow.py` - Tests relationships between entities

3. **API Tests**: Tests for API endpoints
   - Located in `tests/api/`
   - Requires the full application stack
   - Example: `test_api_endpoints.py` - Tests HTTP endpoints

## Environment Setup

Before running tests, ensure your environment is properly configured:

1. **Database Setup**:
   ```bash
   # Set database connection parameters
   export DB_HOST=localhost
   export DB_NAME=lms_test_db
   export DB_USER=lms_user
   export DB_PASSWORD=lms_password
   export DB_PORT=5432
   ```

2. **Create Test Database**:
   ```bash
   # For PostgreSQL
   createdb lms_test_db
   
   # Or run SQL
   psql -U postgres -c "CREATE DATABASE lms_test_db;"
   psql -U postgres -c "CREATE USER lms_user WITH PASSWORD 'lms_password';"
   psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE lms_test_db TO lms_user;"
   ```

3. **Install Dependencies**:
   ```bash
   pip install pytest pytest-cov pytest-asyncio psycopg2-binary requests
   ```

## Running Tests

You can run the tests using the provided `run_all_tests.py` script:

```bash
# Run all tests
python tests/run_all_tests.py

# Run only unit tests
python tests/run_all_tests.py --unit

# Run with coverage report
python tests/run_all_tests.py --coverage
```

Alternatively, you can use pytest directly:

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only tests with a specific marker
pytest -m unit

# Run with verbose output
pytest -v

# Run asyncio tests
pytest -xvs tests/unit/test_database.py::test_sqlalchemy_crud
```

## Key Fixtures

The test suite provides several useful fixtures defined in `conftest.py` and `tests/utils/test_helpers.py`:

| Fixture | Description | Scope |
|---------|-------------|-------|
| `db_connection` | Direct PostgreSQL connection | function |
| `db_cursor` | Database cursor with automatic rollback | function |
| `async_db_session` | Async SQLAlchemy session | function |
| `reset_sqlalchemy_db` | Resets database schema for each test | function |
| `random_string` | Generates random strings for test data | function |
| `sample_course_data` | Sample course data dictionary | function |
| `sample_user_data` | Sample user data dictionary | function |
| `temp_dir` | Temporary directory for file-based tests | function |

## Writing New Tests

When writing new tests, follow these guidelines:

1. Place tests in the appropriate directory based on their category
2. Use pytest fixtures for setup and teardown
3. Use appropriate markers as defined in pytest.ini
4. Import utility functions from `tests/utils/test_helpers.py`
5. Use mock objects from `tests/utils/mock_objects.py` when appropriate
6. Add thorough docstrings to all test functions
7. Follow the naming convention:
   - Test files: `test_*.py`
   - Test classes: `Test*`
   - Test functions: `test_*`

## Test Dependencies

The tests may require the following dependencies:

- pytest - Test framework
- pytest-cov - For coverage reports
- pytest-asyncio - For async tests
- requests - For API tests
- psycopg2 - For database tests

You can install these dependencies with:

```bash
pip install pytest pytest-cov pytest-asyncio requests psycopg2-binary
```

## Example Test

```python
import pytest
from tests.utils.test_helpers import assert_dict_contains_subset
from tests.utils.mock_objects import MockUser, MockCourse

@pytest.mark.unit
def test_example():
    """Example test function demonstrating fixture usage."""
    # Using mock objects
    user = MockUser(username="testuser")
    course = MockCourse(title="Python Programming")
    
    # Test logic
    assert user.username == "testuser"
    assert course.title == "Python Programming"
    
    # Using helper functions
    user_dict = user.to_dict()
    assert_dict_contains_subset({"username": "testuser"}, user_dict)
```

## Error Handling

Tests handle missing dependencies gracefully:

1. Try/except blocks for import failures
2. Tests skip when required components are unavailable 
3. Database connections roll back after each test
4. Mock objects are provided for testing in isolation

## Test Database

Some tests require a database connection. By default, tests use an in-memory SQLite database for SQLAlchemy tests. To use a different database, set the `TEST_DATABASE_URL` environment variable:

```bash
export TEST_DATABASE_URL="postgresql://user:password@localhost/test_db"
python tests/run_all_tests.py
```

## Continuous Integration

Tests are automatically run on every pull request and push to the main branch. The CI workflow is defined in `.github/workflows/tests.yml`. 