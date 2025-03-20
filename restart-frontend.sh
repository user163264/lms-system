#!/bin/bash

# Stop any running frontend server instances more aggressively
echo "Stopping any running Next.js servers..."
pkill -f "next dev" || true
pkill -f "node.*3002" || true
sleep 1

# Load environment variables from .env file if it exists
if [ -f .env ]; then
  echo "Loading environment variables from .env file"
  set -a
  source .env
  set +a
fi

# Use environment variable or default port
PORT=${LMS_FRONTEND_PORT:-3002}

# Make sure we have the right environment variables
echo "Setting up environment variables..."
echo "NEXT_PUBLIC_API_URL=http://localhost:$PORT/api" > frontend/.env.local
echo "NEXT_PUBLIC_USE_MOCK_DATA=true" >> frontend/.env.local

# Move to the frontend directory
echo "Changing to frontend directory..."
cd frontend

# Start the server on the configured port
echo "Starting LMS frontend on 0.0.0.0:$PORT"
npm run dev -- -p $PORT --hostname 0.0.0.0

# This script should be run with: cd ~/lms && ./restart-frontend.sh 