#!/bin/bash

# Script to start a documentation server for LMS configuration
echo "Setting up documentation server..."

# Check if we have Nginx installed
if ! command -v nginx &> /dev/null; then
    echo "Nginx not found. Installing a simple Python web server instead."
    
    # Use Python's built-in HTTP server instead
    cd ~/lms/documentation
    
    # Check which Python version is available
    if command -v python3 &> /dev/null; then
        echo "Starting Python3 HTTP server on port 8080..."
        python3 -m http.server 8080
    elif command -v python &> /dev/null; then
        echo "Starting Python HTTP server on port 8080..."
        python -m SimpleHTTPServer 8080
    else
        echo "ERROR: Neither Python3 nor Python is installed. Cannot start documentation server."
        exit 1
    fi
else
    # Use Nginx if available
    echo "Using Nginx for documentation server"
    
    # Create a symlink to the Nginx sites-available directory if it exists
    if [ -d "/etc/nginx/sites-available" ]; then
        echo "Creating Nginx configuration symlink..."
        sudo cp ~/lms/nginx/documentation.conf /etc/nginx/sites-available/lms-documentation
        
        # Create symlink to sites-enabled if it doesn't exist
        if [ ! -L "/etc/nginx/sites-enabled/lms-documentation" ]; then
            sudo ln -s /etc/nginx/sites-available/lms-documentation /etc/nginx/sites-enabled/
        fi
        
        # Test Nginx configuration
        if sudo nginx -t; then
            echo "Nginx configuration is valid. Restarting Nginx..."
            sudo systemctl restart nginx
            echo "Documentation server started at: http://localhost:8080"
            echo "You can also access it from your server's IP address on port 8080"
        else
            echo "ERROR: Nginx configuration test failed. Please check the configuration."
            exit 1
        fi
    else
        # Simple approach - create a temporary nginx.conf
        echo "Setting up temporary Nginx configuration..."
        
        # Create a temporary directory for Nginx if it doesn't exist
        mkdir -p ~/lms/tmp/nginx
        
        # Create a basic nginx.conf
        cat > ~/lms/tmp/nginx/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Include our documentation server configuration
    include /home/ubuntu/lms/nginx/documentation.conf;
}
EOF
        
        # Start Nginx with our configuration
        echo "Starting Nginx with custom configuration..."
        sudo nginx -c /home/ubuntu/lms/tmp/nginx/nginx.conf
        
        echo "Documentation server started at: http://localhost:8080"
        echo "You can also access it from your server's IP address on port 8080"
    fi
fi

# Print instructions for stopping the server
if command -v nginx &> /dev/null; then
    echo ""
    echo "To stop the server, run: sudo nginx -s stop"
else
    echo ""
    echo "To stop the server, press Ctrl+C"
fi 