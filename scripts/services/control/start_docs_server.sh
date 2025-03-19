#!/bin/bash

# Improved script to start a documentation server with auto-restart capability
echo "Setting up documentation server..."

# Default port
PORT=8090
DOC_DIR="$HOME/lms/documentation"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--port) PORT="$2"; shift ;;
        -d|--dir) DOC_DIR="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if the documentation directory exists
if [ ! -d "$DOC_DIR" ]; then
    echo "Error: Documentation directory $DOC_DIR does not exist!"
    exit 1
fi

# Function to check if a port is available
check_port() {
    local port=$1
    if command -v nc &> /dev/null; then
        nc -z localhost $port &> /dev/null
        return $?
    elif command -v lsof &> /dev/null; then
        lsof -i:"$port" &> /dev/null
        return $?
    else
        # Fallback to direct connection check
        (echo > /dev/tcp/localhost/$port) &> /dev/null
        return $?
    fi
}

# Function to find an available port
find_available_port() {
    local start_port=$1
    local current_port=$start_port
    local max_attempts=10
    
    for ((i=0; i<max_attempts; i++)); do
        if ! check_port $current_port; then
            echo $current_port
            return 0
        else
            echo "Port $current_port is in use, trying next port..."
            current_port=$((current_port + 1))
        fi
    done
    
    echo "Could not find an available port after $max_attempts attempts."
    return 1
}

# Find an available port
PORT=$(find_available_port $PORT)
if [ $? -ne 0 ]; then
    echo "Error finding available port. Exiting."
    exit 1
fi

echo "Starting documentation server on port $PORT..."

# Check which method to use for serving files
if command -v watchmedo &> /dev/null; then
    echo "Using watchdog for file monitoring and auto-restart..."
    cd "$DOC_DIR"
    watchmedo auto-restart \
        --directory=. \
        --pattern="*.html;*.md;*.css;*.js" \
        --recursive \
        -- python3 -m http.server $PORT
elif command -v python3 &> /dev/null; then
    # No watchdog, use regular Python server
    echo "Starting Python3 HTTP server on port $PORT..."
    echo "Note: Server will not auto-restart when files change."
    echo "Install watchdog with: pip install watchdog"
    cd "$DOC_DIR"
    
    # Get server's public IP
    if command -v curl &> /dev/null; then
        PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
        if [ -n "$PUBLIC_IP" ]; then
            echo "Documentation server available at:"
            echo "  - http://localhost:$PORT"
            echo "  - http://$PUBLIC_IP:$PORT"
        else
            echo "Documentation server available at: http://localhost:$PORT"
        fi
    else
        echo "Documentation server available at: http://localhost:$PORT"
    fi
    
    # Start the server
    python3 -m http.server $PORT
else
    echo "ERROR: Python3 is not installed. Cannot start documentation server."
    exit 1
fi

echo "Documentation server stopped." 