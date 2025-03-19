#start_backend.sh

#!/bin/bash
# Start the LMS backend API service
#
# This script starts the FastAPI backend using Uvicorn with the configured
# host and port from environment variables (or defaults if not set).

set -e  # Exit immediately if a command exits with a non-zero status

# Change to the backend directory
cd /home/ubuntu/lms/backend

# Load environment variables from .env file if it exists
if [ -f .env ]; then
  echo "Loading environment variables from .env file"
  set -a
  source .env
  set +a
fi

# Get host and port from environment variables or use defaults
HOST=${LMS_API_HOST:-0.0.0.0}
PORT=${LMS_API_PORT:-8000}

# Check if the port is available
check_port() {
  local port=$1
  if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
    return 1  # Port is in use
  else
    return 0  # Port is available
  fi
}

# Find an available port starting from the configured one
find_available_port() {
  local base_port=$1
  local port=$base_port
  local max_attempts=10
  local attempt=0
  
  while ! check_port $port && [ $attempt -lt $max_attempts ]; do
    echo "Port $port is in use, trying the next one"
    port=$((port + 1))
    attempt=$((attempt + 1))
  done
  
  if [ $attempt -eq $max_attempts ]; then
    echo "Error: Could not find an available port after $max_attempts attempts"
    exit 1
  fi
  
  echo $port
}

# Get an available port
AVAILABLE_PORT=$(find_available_port $PORT)
if [ "$AVAILABLE_PORT" != "$PORT" ]; then
  echo "Original port $PORT is in use, using port $AVAILABLE_PORT instead"
  export LMS_API_PORT=$AVAILABLE_PORT
fi

echo "Starting LMS backend API service on $HOST:$AVAILABLE_PORT"
uvicorn app.main:app --host $HOST --port $AVAILABLE_PORT
