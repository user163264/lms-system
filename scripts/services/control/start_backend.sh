#!/bin/bash
# Script Name: start_backend.sh
# Description: Starts the LMS backend API service using Uvicorn
#
# Usage:
#   ./scripts/services/control/start_backend.sh [port]
#
# Dependencies:
#   - uvicorn
#   - FastAPI backend application
#
# Output:
#   Starts the backend API service and logs to the console
#
# Author: LMS Team
# Last Modified: 2025-03-19

# Default port
PORT=${1:-8000}

# Navigate to backend directory (use absolute path for reliability)
cd /home/ubuntu/lms/backend

# Start the application using uvicorn
echo "Starting backend service on port $PORT..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT 