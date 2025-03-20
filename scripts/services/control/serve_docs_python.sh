#!/bin/bash

# Script to serve LMS documentation using Python's HTTP server
# This script creates a simple redirect page to serve documentation under /docs/

PORT=8000
DOC_DIR="/home/ubuntu/lms/documentation"
TEMP_DIR="/tmp/lms-docs-redirect"

echo "Setting up documentation server with /docs/ path..."

# Check if port is available
if lsof -i:$PORT &>/dev/null; then
    echo "Port $PORT is already in use. Please choose another port."
    exit 1
fi

# Create temporary directory for redirect
mkdir -p $TEMP_DIR
mkdir -p $TEMP_DIR/docs

# Create a symlink to the actual documentation
ln -sf $DOC_DIR/* $TEMP_DIR/docs/

# Create index.html with redirect to /docs/
cat > $TEMP_DIR/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=/docs/auth/login.html">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="/docs/auth/login.html">documentation</a>...</p>
</body>
</html>
EOF

# Go to the temporary directory
cd $TEMP_DIR

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

echo "Documentation server is starting..."
echo "Documentation is accessible at:"
echo "  - http://$PUBLIC_IP:$PORT/docs/"
echo "  - http://localhost:$PORT/docs/"
echo ""
echo "Login credentials:"
echo "  Username: admin"
echo "  Password: lmsdocs"
echo ""
echo "Press Ctrl+C to stop the server"

# Start the server
python3 -m http.server $PORT 