#!/bin/bash
# Script Name: deploy.sh
# Description: Master deployment script for the entire LMS application
#
# Usage:
#   ./scripts/deployment/deploy.sh [environment]
#
# Arguments:
#   environment: Optional - The deployment environment (dev, staging, prod)
#                Defaults to dev if not specified
#
# Dependencies:
#   - npm
#   - pip
#   - pm2
#   - systemd
#
# Output:
#   Deploys both backend and frontend components
#
# Author: LMS Team
# Last Modified: 2025-03-19

set -e  # Exit immediately if a command exits with a non-zero status

# Define environment
ENV=${1:-dev}
echo "🚀 Starting LMS deployment for environment: $ENV..."

# Navigate to project root
cd /home/ubuntu/lms

# Function to deploy the backend
deploy_backend() {
    echo "📦 Deploying backend..."
    
    # Navigate to backend directory
    cd /home/ubuntu/lms/backend

    # Install or update dependencies
    pip install -r requirements.txt

    # Create systemd service file if it doesn't exist
    if [ ! -f /etc/systemd/system/lms-backend.service ]; then
        echo "Creating systemd service file..."
        sudo cp lms-backend.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable lms-backend
    fi

    # Restart the service
    sudo systemctl restart lms-backend

    # Check the status
    echo "Backend service status:"
    sudo systemctl status lms-backend --no-pager
}

# Function to deploy the frontend
deploy_frontend() {
    echo "🎨 Deploying frontend..."
    
    # Navigate to frontend directory
    cd /home/ubuntu/lms/frontend

    # Install or update dependencies
    npm install

    # Build the Next.js application
    npm run build

    # Set up PM2 if it's not already installed
    if ! command -v pm2 &> /dev/null; then
        echo "Installing PM2..."
        npm install -g pm2
    fi

    # Check if the app is already running with PM2
    if pm2 list | grep -q "lms-frontend"; then
        # Restart the app
        pm2 restart lms-frontend
    else
        # Start the app with PM2
        pm2 start npm --name "lms-frontend" -- start
        # Save the PM2 configuration to ensure it starts on reboot
        pm2 save
        # Set up PM2 to start on system boot if not already done
        pm2 startup | tail -n 1 | bash
    fi

    echo "Frontend service status:"
    pm2 status lms-frontend
}

# Deploy backend
deploy_backend

# Deploy frontend
deploy_frontend

# Verify all services are running
echo "🔍 Verifying services..."
python /home/ubuntu/lms/scripts/services/check/check_services.py

echo "✅ Deployment completed successfully!" 