#!/bin/bash
# Script Name: start_frontend.sh
# Description: Starts the LMS frontend service using Next.js
#
# Usage:
#   ./scripts/services/control/start_frontend.sh [port]
#
# Dependencies:
#   - Node.js
#   - npm
#   - Next.js frontend application
#
# Output:
#   Starts the frontend service and logs to the console
#
# Author: LMS Team
# Last Modified: 2025-03-19

# Default port
PORT=${1:-3000}

# Navigate to frontend directory (use absolute path for reliability)
cd /home/ubuntu/lms/frontend

# Set environment variables
export NODE_ENV=production

# Start the application using npm
echo "Starting frontend service on port $PORT..."
npm run dev -- -p $PORT 