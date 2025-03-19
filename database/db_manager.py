#!/usr/bin/env python3

import psycopg2
import psycopg2.extras
import time
import traceback
import json
import os
import sys
from datetime import datetime

# Get the database connection parameters from environment variables or use defaults
def get_db_params():
    """Get database connection parameters from environment or use defaults."""
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'dbname': os.environ.get('DB_NAME', 'lms_db'),
        'user': os.environ.get('DB_USER', 'lms_user'),
        'password': os.environ.get('DB_PASSWORD', 'lms_password'),
        'port': os.environ.get('DB_PORT', '5432')
    }

class DBManager:
    """
    Database manager for the test submission system.
    Handles connections, transactions, and query logging.
    """
    
    def __init__(self, auto_commit=True):
        """Initialize the database manager."""
        self.params = get_db_params()
        self.conn = None
        self.cur = None
        self.auto_commit = auto_commit
        self.is_transaction_active = False
        
    def connect(self):
        """Connect to the database."""
        try:
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.params)
                self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                self.log_debug("Database connection established")
        except (Exception, psycopg2.DatabaseError) as e:
            self.log_error(f"Database connection error: {e}")
            raise
            
    def close(self):
        """Close the database connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            self.log_debug("Database connection closed")
        self.conn = None
        self.cur = None
    
    def begin_transaction(self):
        """Begin a database transaction."""
        if not self.is_transaction_active:
            self.connect()
            self.is_transaction_active = True
            self.log_debug("Transaction started")
    
    def commit(self):
        """Commit the current transaction."""
        if self.conn and self.is_transaction_active:
            self.conn.commit()
            self.is_transaction_active = False
            self.log_debug("Transaction committed")
    
    def rollback(self):
        """Roll back the current transaction."""
        if self.conn and self.is_transaction_active:
            self.conn.rollback()
            self.is_transaction_active = False
            self.log_debug("Transaction rolled back")
    
    def log_query(self, query, params=None, execution_time=0, username=None, session_id=None, source_ip=None):
        """Log a database query to the query_logs table."""
        try:
            # Don't log the log_query itself to avoid infinite recursion
            if "INSERT INTO query_logs" in query:
                return
                
            # Convert params to JSON-compatible format
            if params:
                if isinstance(params, dict):
                    json_params = json.dumps(params)
                elif isinstance(params, tuple) or isinstance(params, list):
                    json_params = json.dumps([str(p) if not isinstance(p, (int, float, bool, str, type(None))) else p for p in params])
                else:
                    json_params = json.dumps(str(params))
            else:
                json_params = None
                
            # Insert the log
            self.connect()
            self.cur.execute(
                """
                INSERT INTO query_logs 
                (query_text, execution_time_ms, params, username, timestamp, source_ip, session_id)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
                """,
                (query, int(execution_time * 1000), json_params, username, source_ip, session_id)
            )
            
            # Auto-commit the log entry
            self.conn.commit()
        except Exception as e:
            # Don't crash the application for logging failures
            print(f"Failed to log query: {e}", file=sys.stderr)
    
    def log_error(self, error_message, error_code=None, severity="error", component="database", 
                  username=None, session_id=None, source_ip=None, request_data=None):
        """Log an error to the error_logs table."""
        try:
            # Get stack trace
            stack = traceback.format_exc()
            
            # Convert request data to JSON if provided
            json_request_data = json.dumps(request_data) if request_data else None
            
            # Insert the error log
            self.connect()
            self.cur.execute(
                """
                INSERT INTO error_logs 
                (error_code, error_message, error_stack, severity, component, username, 
                timestamp, source_ip, session_id, request_data)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
                """,
                (error_code, error_message, stack, severity, component, username, 
                source_ip, session_id, json_request_data)
            )
            
            # Always commit error logs immediately
            self.conn.commit()
            
            # Also print to stderr for immediate visibility
            print(f"ERROR [{severity}]: {error_message}", file=sys.stderr)
        except Exception as e:
            # Don't crash for logging failures
            print(f"Failed to log error: {e}", file=sys.stderr)
    
    def log_debug(self, message, component="database"):
        """Log a debug message to stderr (not to the database)."""
        print(f"DEBUG [{component}]: {message}", file=sys.stderr)
    
    def execute(self, query, params=None, username=None, session_id=None, source_ip=None):
        """Execute a database query with logging."""
        self.connect()
        
        start_time = time.time()
        try:
            # Execute the query
            self.cur.execute(query, params)
            
            # Auto-commit if configured
            if self.auto_commit and not self.is_transaction_active:
                self.conn.commit()
                
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Log the query
            self.log_query(query, params, execution_time, username, session_id, source_ip)
            
            return self.cur
        except Exception as e:
            # Roll back if not in an explicit transaction
            if not self.is_transaction_active:
                self.conn.rollback()
            
            # Log the error
            self.log_error(str(e), component="database", username=username, 
                          session_id=session_id, source_ip=source_ip)
            
            # Re-raise the exception
            raise
    
    def fetch_one(self, query, params=None, username=None, session_id=None, source_ip=None):
        """Execute a query and fetch a single result."""
        cur = self.execute(query, params, username, session_id, source_ip)
        return cur.fetchone()
    
    def fetch_all(self, query, params=None, username=None, session_id=None, source_ip=None):
        """Execute a query and fetch all results."""
        cur = self.execute(query, params, username, session_id, source_ip)
        return cur.fetchall()
    
    def fetch_scalar(self, query, params=None, username=None, session_id=None, source_ip=None):
        """Execute a query and fetch a single scalar value."""
        row = self.fetch_one(query, params, username, session_id, source_ip)
        return row[0] if row else None
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if exc_type is not None:
            # An exception occurred, roll back
            self.rollback()
            self.log_error(str(exc_val))
        else:
            # No exception, commit if auto_commit
            if self.auto_commit:
                self.commit()
        
        # Close the connection
        self.close()
        
        # Don't suppress exceptions
        return False 