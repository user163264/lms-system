#!/bin/bash

# Script to install LMS Documentation Python Server as a systemd service
# This will make it start automatically on system boot

set -e

echo "Installing LMS Documentation Python Server as a systemd service..."

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LMS_ROOT="$(realpath $SCRIPT_DIR/../../../)"

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run with sudo. Please run: sudo $0"
  exit 1
fi

# Stop any existing services
echo "Stopping any existing services..."
systemctl stop lms-docs.service || true
systemctl stop lms-docs-nginx.service || true
systemctl stop simple-docs-server.service || true
pkill -f "python3 -m http.server" || true
sleep 2

# Setup the directory structure for /docs/ URL prefix
echo "Setting up directory structure for /docs/ URL prefix..."
TEMP_DIR="/home/ubuntu/lms-docs-public"
mkdir -p $TEMP_DIR/docs

# Copy the documentation (instead of symlink to ensure permissions)
echo "Copying documentation to public directory..."
cp -r "$LMS_ROOT/documentation/"* $TEMP_DIR/docs/

# Create redirect index.html
echo "Creating redirect index page..."
cat > $TEMP_DIR/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=/docs/auth/login.html">
    <title>LMS Documentation</title>
</head>
<body>
    <p>Redirecting to <a href="/docs/auth/login.html">documentation</a>...</p>
</body>
</html>
EOF

# Update the service file
echo "Updating service file..."
cat > "$SCRIPT_DIR/simple-docs-server.service" << EOF
[Unit]
Description=LMS Documentation Python Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$TEMP_DIR
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Copy the service file to systemd directory
echo "Copying service file to /etc/systemd/system/"
cp "$SCRIPT_DIR/simple-docs-server.service" /etc/systemd/system/

# Reload systemd to recognize the new service
echo "Reloading systemd..."
systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service to start on boot..."
systemctl enable simple-docs-server.service

# Start the service
echo "Starting service now..."
systemctl start simple-docs-server.service

# Check status
echo "Checking service status..."
systemctl status simple-docs-server.service

echo ""
echo "LMS Documentation Python Server has been installed as a systemd service."
echo "It will now start automatically when the system boots."
echo ""
echo "You can manage it with the following commands:"
echo "  - sudo systemctl start simple-docs-server.service    # Start the service"
echo "  - sudo systemctl stop simple-docs-server.service     # Stop the service"
echo "  - sudo systemctl restart simple-docs-server.service  # Restart the service"
echo "  - sudo systemctl status simple-docs-server.service   # Check service status"
echo ""
echo "The documentation is available at:"
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
echo "  http://$PUBLIC_IP:8000/"
echo "  http://$PUBLIC_IP:8000/docs/auth/login.html" 