#!/bin/bash
# scripts/deploy.sh
# Master deployment script for the entire LMS application

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting LMS deployment..."

# Navigate to project root
cd /home/ubuntu/lms

# Deploy backend
echo "📦 Deploying backend..."
bash ./scripts/deploy_backend.sh

# Deploy frontend
echo "🎨 Deploying frontend..."
bash ./scripts/deploy_frontend.sh

echo "✅ Deployment completed successfully!"

#!/bin/bash
# scripts/deploy_frontend.sh
# Frontend deployment script

set -e  # Exit immediately if a command exits with a non-zero status

echo "🎨 Starting frontend deployment..."

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

echo "✅ Frontend deployment completed successfully!"

#!/bin/bash
# scripts/deploy_backend.sh
# Backend deployment script

set -e  # Exit immediately if a command exits with a non-zero status

echo "📦 Starting backend deployment..."

# Navigate to backend directory
cd /home/ubuntu/lms/backend

# Update from git repository
# git pull origin main

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

echo "✅ Backend deployment completed successfully!"