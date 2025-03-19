#!/bin/bash
# Startup script for LMS frontend
#
# This script starts the Next.js frontend with the configured
# host and port from environment variables (or defaults if not set).

set -e  # Exit immediately if a command exits with a non-zero status

# Change to the frontend directory
cd /home/ubuntu/lms/frontend

# Load environment variables from .env file if it exists
if [ -f ../.env ]; then
  echo "Loading environment variables from .env file"
  set -a
  source ../.env
  set +a
fi

# Get host and port from environment variables or use defaults
HOST=${LMS_FRONTEND_HOST:-localhost}
PORT=${LMS_FRONTEND_PORT:-3000}

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
  export LMS_FRONTEND_PORT=$AVAILABLE_PORT
  # If we're using a different port, we should update the API's CORS settings
  # This is a temporary solution - in production, you'd use a proper reverse proxy
  echo "Warning: Using a non-standard port. CORS settings may need to be updated."
fi

echo "Starting LMS frontend on $HOST:$AVAILABLE_PORT"
export NODE_ENV=production
npm run dev -- -p $AVAILABLE_PORT 