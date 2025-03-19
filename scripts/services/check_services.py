#!/usr/bin/env python3

"""
Service Health Check Script

This script checks the status of all services required for the LMS:
1. Database connection
2. Backend services
3. Frontend services
4. Other necessary services
"""

import os
import sys
import socket
import subprocess
import time
import logging
from datetime import datetime
from pathlib import Path

# Add the project root to sys.path to enable imports
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

# Import from database module (using environment variables for configuration)
from database.db_manager import get_db_params
import psycopg2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / "logs" / "service_check.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
def get_service_config():
    """Get service configuration from environment variables or use defaults."""
    return {
        'db_params': get_db_params(),
        'backend_port': int(os.environ.get('BACKEND_PORT', '8000')),
        'frontend_port': int(os.environ.get('FRONTEND_PORT', '3000')),
    }

def check_database():
    """Check if the database is running and accessible."""
    logger.info("\n📊 Checking Database Connection...")
    try:
        config = get_service_config()
        conn = psycopg2.connect(**config['db_params'])
        cur = conn.cursor()
        
        # Check connection
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        logger.info(f"✅ Database connected successfully")
        
        # Check tables
        cur.execute("""
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
        """)
        tables = [row[0] for row in cur.fetchall()]
        logger.info(f"✅ Found {len(tables)} tables in database")
        
        # Check running queries
        try:
            cur.execute("""
                SELECT pid, query, state, query_start
                FROM pg_stat_activity
                WHERE state <> 'idle'
                AND query NOT ILIKE '%pg_stat_activity%'
            """)
            queries = cur.fetchall()
            if queries:
                logger.info(f"Current active queries: {len(queries)}")
            else:
                logger.info("No active queries.")
        except Exception as e:
            logger.warning(f"Could not check active queries: {e}")
        
        # Clean up
        cur.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

def check_port(host, port, service_name):
    """Check if a port is open on the specified host."""
    logger.info(f"Checking if {service_name} is running on port {port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            logger.info(f"✅ {service_name} is running on port {port}")
            return True
        else:
            logger.error(f"❌ {service_name} is not running on port {port}")
            return False
    finally:
        sock.close()

def check_process(process_name):
    """Check if a process is running using grep."""
    logger.info(f"Checking if {process_name} process is running...")
    try:
        # Use pgrep to search for the process
        result = subprocess.run(
            ["pgrep", "-f", process_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            logger.info(f"✅ Process {process_name} is running")
            return True
        else:
            logger.error(f"❌ Process {process_name} is not running")
            return False
    except Exception as e:
        logger.error(f"❌ Error checking process {process_name}: {e}")
        return False

def check_system_resources():
    """Check system resources like CPU, memory, and disk space."""
    logger.info("\n💻 Checking System Resources...")
    
    try:
        # Check CPU usage
        cpu_usage = None
        try:
            cpu_cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"
            result = subprocess.run(cpu_cmd, shell=True, capture_output=True, text=True)
            cpu_usage = result.stdout.strip()
            logger.info(f"CPU usage: {cpu_usage}%")
            if cpu_usage and float(cpu_usage) > 90:
                logger.warning(f"❌ CPU usage critical: {cpu_usage}%")
            else:
                logger.info(f"✅ CPU usage OK: {cpu_usage}%")
        except Exception as e:
            logger.error(f"Could not check CPU usage: {e}")
        
        # Check memory usage
        memory_usage = None
        try:
            mem_cmd = "free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2}'"
            result = subprocess.run(mem_cmd, shell=True, capture_output=True, text=True)
            memory_usage = result.stdout.strip()
            logger.info(f"Memory usage: {memory_usage}%")
            if memory_usage and float(memory_usage) > 90:
                logger.warning(f"❌ Memory usage critical: {memory_usage}%")
            else:
                logger.info(f"✅ Memory usage OK: {memory_usage}%")
        except Exception as e:
            logger.error(f"Could not check memory usage: {e}")
        
        # Check disk usage
        disk_usage = None
        try:
            disk_cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
            result = subprocess.run(disk_cmd, shell=True, capture_output=True, text=True)
            disk_usage = result.stdout.strip()
            logger.info(f"Disk usage: {disk_usage}")
            if disk_usage and int(disk_usage.rstrip('%')) > 90:
                logger.warning(f"❌ Disk usage critical: {disk_usage}")
            else:
                logger.info(f"✅ Disk usage OK: {disk_usage}")
        except Exception as e:
            logger.error(f"Could not check disk usage: {e}")
            
        return True
    except Exception as e:
        logger.error(f"❌ Error checking system resources: {e}")
        return False

def check_backend_services():
    """Check if backend services are running."""
    logger.info("\n🔄 Checking Backend Services...")
    
    config = get_service_config()
    
    # Check PostgreSQL database
    db_running = check_port('localhost', int(config['db_params']['port']), 'PostgreSQL Database')
    
    # Check for Python backend process - using the actual pattern from our system
    backend_running = check_process('uvicorn app.main:app')
    
    # Check if API is responding on port 8000
    api_running = check_port('localhost', config['backend_port'], 'Backend API')
    
    return db_running and (backend_running or api_running)

def check_frontend_services():
    """Check if frontend services are running."""
    logger.info("\n🖥️ Checking Frontend Services...")
    
    config = get_service_config()
    
    # Check for Node.js/React frontend
    frontend_running = check_port('localhost', config['frontend_port'], 'Frontend Server')
    
    # Check for Nginx if it's being used
    nginx_running = check_process('nginx')
    
    return frontend_running or nginx_running

def check_all_services():
    """Check all services."""
    logger.info(f"\n{'='*20} LMS Service Health Check {'='*20}")
    logger.info(f"Running health check at {datetime.now()}\n")
    
    results = {}
    
    # Check database
    results['Database'] = check_database()
    
    # Check backend services
    results['Backend Services'] = check_backend_services()
    
    # Check frontend services
    results['Frontend Services'] = check_frontend_services()
    
    # Check system resources
    results['System Resources'] = check_system_resources()
    
    # Print summary
    logger.info("\n" + "="*50)
    logger.info("Service Health Summary:")
    success_count = sum(1 for result in results.values() if result)
    
    for name, result in results.items():
        status = "✅ ONLINE" if result else "❌ OFFLINE"
        logger.info(f"{status} - {name}")
    
    logger.info(f"\n{success_count}/{len(results)} services are online.")
    
    if success_count == len(results):
        logger.info("\n🎉 All services are running properly!")
        return True
    else:
        logger.warning("\n⚠️ Some services are offline. See details above.")
        return False

if __name__ == "__main__":
    success = check_all_services()
    
    if not success:
        sys.exit(1) 