#!/bin/bash

# Script to install LMS Documentation Server as a systemd service
# This will make it start automatically on system boot

set -e

echo "Installing LMS Documentation Server as a systemd service..."

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LMS_ROOT="$(realpath $SCRIPT_DIR/../../../)"

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run with sudo. Please run: sudo $0"
  exit 1
fi

# Stop any existing Python HTTP servers to avoid conflicts
echo "Stopping any running HTTP servers..."
pkill -f "python3 -m http.server" || true

# Copy the service file to systemd directory
echo "Copying service file to /etc/systemd/system/"
cp "$SCRIPT_DIR/lms-docs.service" /etc/systemd/system/

# Make sure the scripts are executable
echo "Setting execute permissions on scripts..."
chmod +x "$SCRIPT_DIR/start_docs_server.sh"

# Reload systemd to recognize the new service
echo "Reloading systemd..."
systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service to start on boot..."
systemctl enable lms-docs.service

# Start the service
echo "Starting service now..."
systemctl start lms-docs.service

# Check status
echo "Checking service status..."
systemctl status lms-docs.service

echo ""
echo "LMS Documentation Server has been installed as a systemd service."
echo "It will now start automatically when the system boots."
echo ""
echo "You can manage it with the following commands:"
echo "  - sudo systemctl start lms-docs.service    # Start the service"
echo "  - sudo systemctl stop lms-docs.service     # Stop the service"
echo "  - sudo systemctl restart lms-docs.service  # Restart the service"
echo "  - sudo systemctl status lms-docs.service   # Check service status"
echo ""
echo "The documentation is available at:"
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
echo "  http://$PUBLIC_IP:8090/index.html" 