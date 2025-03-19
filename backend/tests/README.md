# LMS Testing Framework

This directory contains the test suite for the Learning Management System (LMS) backend. The tests have been consolidated and organized to improve maintainability and coverage.

## Test Structure

The tests are organized into three main categories:

### 1. Unit Tests (`./unit/`)

Unit tests focus on testing individual components in isolation:

- **Database Tests**: Tests for database connectivity, models, and CRUD operations
  - `test_database.py` - Core database functionality tests
  - `test_exercises.py` - Tests for exercise-related models
  
### 2. Integration Tests (`./integration/`)

Integration tests verify that different components work together correctly:

- **Service Tests**: Tests for service-level functionality
- **Repository Tests**: Tests for data access layer
- **Business Logic Tests**: Tests for complex business rules

### 3. API Tests (`./api/`)

API tests verify the REST API endpoints behave as expected:

- `test_api_endpoints.py` - Tests for general API functionality
- Future specialized endpoint tests will be added here

## Test Fixtures

Common test fixtures are defined in `conftest.py` in the root of the tests directory. These include:

- Database initialization
- Test users and authentication
- Test data generation

## Naming Conventions

- Test files should be named with `test_` prefix
- Test classes should be named with `Test` prefix
- Test methods should be named with `test_` prefix followed by descriptive name
- Test fixtures should have descriptive names indicating their purpose

## Running Tests

To run all tests:

```bash
cd /home/ubuntu/lms/backend
pytest
```

To run specific test categories:

```bash
# Run unit tests only
pytest tests/unit/

# Run API tests only
pytest tests/api/

# Run database tests specifically
pytest tests/unit/test_database.py
```

## Test Tags

Tests can be tagged using pytest markers for selective execution:

- `@pytest.mark.asyncio` - Tests that use asyncio
- `@pytest.mark.direct_db` - Tests that use direct database connections
- `@pytest.mark.api` - API tests
- `@pytest.mark.slow` - Tests that take longer to run

## Adding New Tests

When adding new tests:

1. Identify the appropriate category (unit, integration, or API)
2. Follow the naming conventions
3. Use appropriate fixtures from `conftest.py`
4. Add appropriate pytest markers
5. Keep tests focused and efficient

## Migrated Tests

The following legacy test files have been consolidated into the new structure:

- `test_database.py` (root)
- `test_db_layer.py` (root)
- `simple_test_db.py` (backend/app)
- `test_db.py` (backend/app)
- `test_exercises.py` (root and backend)
- `test_api.py` (backend)
- `test_exercise_api.py` (backend)

When modifying functionality tested by these files, refer to the consolidated test files in the new structure. 