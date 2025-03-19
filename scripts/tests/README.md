# Test Scripts

This directory contains scripts for running tests and verification on the LMS system.

## Scripts

- `run_tests.sh` - Main script for running backend tests
- `check_grading.py` - Tests the exercise grading functionality
- `update_grading.py` - Updates exercise grading logic
- `run_simple_test.py` - Runs a simplified test suite for quick verification

## Usage

### Running Backend Tests

To run the complete backend test suite:

```bash
./scripts/tests/run_tests.sh
```

This will run unit tests, integration tests, and API tests for the backend.

### Checking Exercise Grading

To verify the exercise grading functionality:

```bash
python scripts/tests/check_grading.py
```

This will run tests on each exercise type to ensure grading works correctly.

### Updating Exercise Grading

To update the exercise grading logic:

```bash
python scripts/tests/update_grading.py
```

This updates the grading logic based on the latest exercise requirements.

### Running Simple Tests

For a quick verification of the system:

```bash
python scripts/tests/run_simple_test.py
```

This runs a simplified test suite that checks basic functionality. 