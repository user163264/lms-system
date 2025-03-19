#!/bin/bash

# Script to install LMS Documentation Nginx Server as a systemd service
# This will make it start automatically on system boot

set -e

echo "Installing LMS Documentation Nginx Server as a systemd service..."

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LMS_ROOT="$(realpath $SCRIPT_DIR/../../../)"

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run with sudo. Please run: sudo $0"
  exit 1
fi

# Check if Nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Installing..."
    apt-get update
    apt-get install -y nginx
fi

# Stop any existing services
echo "Stopping any existing services..."
systemctl stop lms-docs.service || true
systemctl stop lms-docs-nginx.service || true
nginx -s stop || true
pkill -f "python3 -m http.server" || true
sleep 2

# Copy the service file to systemd directory
echo "Copying service file to /etc/systemd/system/"
cp "$SCRIPT_DIR/lms-docs-nginx.service" /etc/systemd/system/

# Reload systemd to recognize the new service
echo "Reloading systemd..."
systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service to start on boot..."
systemctl enable lms-docs-nginx.service

# Start the service
echo "Starting service now..."
systemctl start lms-docs-nginx.service

# Check status
echo "Checking service status..."
systemctl status lms-docs-nginx.service

echo ""
echo "LMS Documentation Nginx Server has been installed as a systemd service."
echo "It will now start automatically when the system boots."
echo ""
echo "You can manage it with the following commands:"
echo "  - sudo systemctl start lms-docs-nginx.service    # Start the service"
echo "  - sudo systemctl stop lms-docs-nginx.service     # Stop the service"
echo "  - sudo systemctl restart lms-docs-nginx.service  # Restart the service"
echo "  - sudo systemctl status lms-docs-nginx.service   # Check service status"
echo ""
echo "The documentation is available at:"
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
echo "  http://$PUBLIC_IP:8000/docs/"
echo ""
echo "Login credentials:"
echo "  Username: admin"
echo "  Password: lmsdocs" 