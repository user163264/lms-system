#!/bin/bash

# Script to configure Nginx for LMS Documentation
set -e

echo "Setting up Nginx for LMS Documentation..."

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run with sudo. Please run: sudo $0"
  exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LMS_ROOT="$(realpath $SCRIPT_DIR/../../../)"

# Check if Nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Installing..."
    apt-get update
    apt-get install -y nginx
fi

# Stop existing documentation service if running
echo "Stopping any existing documentation services..."
systemctl stop lms-docs.service || true
pkill -f "python3 -m http.server" || true

# Create directories for logs
echo "Creating log directories..."
mkdir -p /var/log/nginx/

# Copy Nginx configuration
echo "Copying Nginx configuration file..."
cp "$LMS_ROOT/nginx/docs.conf" /etc/nginx/sites-available/lms-docs

# Create symlink to enable the configuration
echo "Enabling Nginx configuration..."
ln -sf /etc/nginx/sites-available/lms-docs /etc/nginx/sites-enabled/

# Test Nginx configuration
echo "Testing Nginx configuration..."
nginx -t

# Restart Nginx to apply changes
echo "Restarting Nginx..."
systemctl restart nginx

# Display information about the setup
echo ""
echo "LMS Documentation has been set up with Nginx!"
echo "You can access the documentation at:"
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
echo "  http://$PUBLIC_IP/docs/"
echo ""
echo "Login credentials:"
echo "  Username: admin"
echo "  Password: lmsdocs"
echo ""
echo "The documentation will be accessible after system reboots." 