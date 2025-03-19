#!/bin/bash

# Script to run Nginx with standalone configuration for LMS Documentation
set -e

echo "Starting standalone Nginx for LMS Documentation..."

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LMS_ROOT="$(realpath $SCRIPT_DIR/../../../)"

# Check if Nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Stop any existing Python HTTP servers
echo "Stopping any existing Python HTTP servers..."
pkill -f "python3 -m http.server" || true

# Stop existing Nginx if running
echo "Stopping any existing Nginx instances..."
sudo nginx -s stop || true
sleep 2

# Create directories for logs
echo "Creating log directories..."
sudo mkdir -p /var/log/nginx/

# Run Nginx with our custom configuration
echo "Starting Nginx with custom configuration..."
sudo nginx -c "$LMS_ROOT/nginx/docs_standalone.conf"

# Display information about the setup
echo ""
echo "LMS Documentation is now available!"
echo "You can access the documentation at:"
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
echo "  http://$PUBLIC_IP:8000/docs/"
echo ""
echo "Login credentials:"
echo "  Username: admin"
echo "  Password: lmsdocs"
echo ""
echo "To stop the server, run: sudo nginx -s stop" 