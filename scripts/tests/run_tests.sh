#!/bin/bash
# Script Name: run_tests.sh
# Description: Runs the test suite for the LMS backend
#
# Usage:
#   ./scripts/tests/run_tests.sh [--unit|--integration|--api|--all]
#
# Dependencies:
#   - pytest
#   - pytest-cov
#
# Output:
#   Test results including coverage information
#
# Author: LMS Team
# Last Modified: 2025-03-19

set -e  # Exit on error

echo "LMS API Test Runner"
echo "===================="

# Ensure server is running
echo "Step 1: Checking if server is running..."
if ! curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/ > /dev/null 2>&1; then
    echo "Server does not appear to be running. Starting server..."
    echo "Starting server in the background. Logs will be in server.log"
    python -m uvicorn app.main:app --port 8001 --host 0.0.0.0 > server.log 2>&1 &
    SERVER_PID=$!
    echo "Server started with PID: $SERVER_PID"
    
    # Wait for server to start
    echo "Waiting for server to start..."
    for i in {1..10}; do
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/ > /dev/null 2>&1; then
            echo "Server is running!"
            break
        fi
        
        if [ $i -eq 10 ]; then
            echo "Server failed to start. Check server.log for details."
            if [ -n "$SERVER_PID" ]; then
                kill $SERVER_PID
            fi
            exit 1
        fi
        
        echo "Waiting... ($i/10)"
        sleep 1
    done
fi

# Generate test data
echo 
echo "Step 2: Generating test data..."
python -m app.test_data

# Run API tests
echo 
echo "Step 3: Running API tests..."
python test_api.py

TEST_EXIT_CODE=$?

# Exit with test exit code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed."
fi

# If we started the server, offer to shut it down
if [ -n "$SERVER_PID" ]; then
    read -p "Do you want to stop the server? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill $SERVER_PID
        echo "Server stopped."
    else
        echo "Server is still running with PID: $SERVER_PID"
        echo "To stop it manually, run: kill $SERVER_PID"
    fi
fi

exit $TEST_EXIT_CODE 