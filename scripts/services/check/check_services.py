#!/usr/bin/env python3
"""
Script Name: check_services.py
Description: Checks the status of all services required for the LMS system

Usage:
    python scripts/services/check/check_services.py [--verbose] [--quiet]
    
Options:
    --verbose, -v   Show detailed information about each service
    --quiet, -q     Only output errors, no status messages
    
Dependencies:
    - psycopg2
    - requests
    
Output:
    Status report of database, backend, and frontend services
    Exit code 0 if all services are running, non-zero otherwise
    
Author: LMS Team
Last Modified: 2025-03-19
"""

import os
import sys
import socket
import subprocess
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Add the project root to sys.path to enable imports
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

# Import from database module (using environment variables for configuration)
try:
    from database.db_manager import get_db_params
    import psycopg2
    import requests
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure you have all required packages installed.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(project_root, 'logs', 'service_check.log'))
    ]
)
logger = logging.getLogger("service_check")

# Get environment variables with defaults
def get_env_str(name, default):
    return os.environ.get(name, default)

def get_env_int(name, default):
    try:
        value = os.environ.get(name)
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

# Service configurations
SERVICE_CONFIG = {
    "database": {
        "name": "PostgreSQL Database",
        "port": get_env_int("LMS_DB_PORT", 5432),
        "host": get_env_str("LMS_DB_HOST", "localhost"),
    },
    "backend": {
        "name": "FastAPI Backend",
        "port": get_env_int("LMS_API_PORT", 8000),
        "host": get_env_str("LMS_API_HOST", "localhost"),
        "health_endpoint": "/health",
    },
    "frontend": {
        "name": "Next.js Frontend",
        "port": get_env_int("LMS_FRONTEND_PORT", 3000),
        "host": get_env_str("LMS_FRONTEND_HOST", "localhost"),
    }
}

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Check LMS service status")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed information")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only output errors")
    return parser.parse_args()

def check_port(host, port):
    """Check if a TCP port is open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def check_database():
    """Check if the database is running and accessible."""
    try:
        db_params = get_db_params()
        # Override with service config if needed
        db_params["host"] = SERVICE_CONFIG["database"]["host"]
        db_params["port"] = SERVICE_CONFIG["database"]["port"]
        
        # Try to connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return True, version
    except Exception as e:
        return False, str(e)

def check_backend():
    """Check if the backend API is running."""
    host = SERVICE_CONFIG["backend"]["host"]
    port = SERVICE_CONFIG["backend"]["port"]
    health_endpoint = SERVICE_CONFIG["backend"]["health_endpoint"]
    
    # First check if the port is open
    if not check_port(host, port):
        return False, "Port is not open"
    
    # Then check the health endpoint if available
    try:
        response = requests.get(f"http://{host}:{port}{health_endpoint}", timeout=5)
        if response.status_code == 200:
            return True, f"Status code: {response.status_code}"
        return False, f"Unexpected status code: {response.status_code}"
    except requests.RequestException:
        # If health endpoint fails, just check if something is responding
        try:
            response = requests.get(f"http://{host}:{port}/", timeout=5)
            return True, "Service responding but health endpoint not available"
        except requests.RequestException as e:
            return False, str(e)

def check_frontend():
    """Check if the frontend service is running."""
    host = SERVICE_CONFIG["frontend"]["host"]
    port = SERVICE_CONFIG["frontend"]["port"]
    
    if check_port(host, port):
        try:
            response = requests.get(f"http://{host}:{port}/", timeout=5)
            return True, f"Status code: {response.status_code}"
        except requests.RequestException as e:
            return False, f"Port is open but HTTP request failed: {e}"
    return False, "Port is not open"

def main():
    """Main function to check all services."""
    args = parse_args()
    
    if args.quiet:
        logger.setLevel(logging.ERROR)
    elif args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info("Starting service health check")
    
    # Check database
    logger.info("Checking database service...")
    db_status, db_message = check_database()
    if db_status:
        logger.info(f"✅ Database is running: {db_message}")
    else:
        logger.error(f"❌ Database check failed: {db_message}")
    
    # Check backend
    logger.info("Checking backend service...")
    backend_status, backend_message = check_backend()
    if backend_status:
        logger.info(f"✅ Backend is running: {backend_message}")
    else:
        logger.error(f"❌ Backend check failed: {backend_message}")
    
    # Check frontend
    logger.info("Checking frontend service...")
    frontend_status, frontend_message = check_frontend()
    if frontend_status:
        logger.info(f"✅ Frontend is running: {frontend_message}")
    else:
        logger.error(f"❌ Frontend check failed: {frontend_message}")
    
    # Overall status
    all_ok = db_status and backend_status and frontend_status
    if all_ok:
        logger.info("All services are running correctly")
        return 0
    else:
        logger.error("One or more services have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 