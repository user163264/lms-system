#!/usr/bin/env python3

import json
from datetime import datetime
import re
import hashlib
import uuid
from typing import List, Dict, Any, Optional, Union
from .db_manager import DBManager

class ValidationError(Exception):
    """Exception raised for validation errors in model data."""
    pass

class Model:
    """Base model class with common functionality."""
    
    table_name = None
    id_column = 'id'
    
    def __init__(self, **kwargs):
        """Initialize model with data."""
        self.id = kwargs.get('id', None)
        self._data = kwargs
        
    def validate(self) -> bool:
        """
        Validate model data. 
        Returns True if valid, raises ValidationError if invalid.
        """
        # Base validation - implemented by subclasses
        return True
        
    def save(self, db=None, username=None, session_id=None, source_ip=None) -> int:
        """
        Save model to database.
        Creates new record if id is None, updates existing if id is set.
        """
        should_close_db = False
        try:
            if db is None:
                db = DBManager()
                should_close_db = True
                
            if self.id is None:
                # Insert new record
                self.validate()
                
                # Remove id from data for insertion
                insert_data = {k: v for k, v in self._data.items() if k != 'id'}
                
                # Build column list and placeholders
                columns = ', '.join(insert_data.keys())
                placeholders = ', '.join(['%s'] * len(insert_data))
                values = list(insert_data.values())
                
                query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING {self.id_column}"
                
                try:
                    result = db.fetch_one(query, values, username, session_id, source_ip)
                    if result:
                        self.id = result[0]
                        return self.id
                except Exception as e:
                    # If fetch_one fails (no results), try execute and then use lastval()
                    db.execute(query, values, username, session_id, source_ip)
                    # Get the last inserted ID
                    id_result = db.fetch_one("SELECT lastval()", None, username, session_id, source_ip)
                    if id_result:
                        self.id = id_result[0]
                        return self.id
                return None
            else:
                # Update existing record
                self.validate()
                
                # Remove id from data for update clause
                update_data = {k: v for k, v in self._data.items() if k != 'id'}
                
                # Build SET clause
                set_clause = ', '.join([f"{k} = %s" for k in update_data.keys()])
                values = list(update_data.values())
                values.append(self.id)  # Add id for WHERE clause
                
                query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.id_column} = %s"
                
                db.execute(query, values, username, session_id, source_ip)
                return self.id
        finally:
            if should_close_db and db:
                db.close()
                
    @classmethod
    def find_by_id(cls, id, db=None, username=None, session_id=None, source_ip=None):
        """Find model by ID."""
        should_close_db = False
        try:
            if db is None:
                db = DBManager()
                should_close_db = True
                
            query = f"SELECT * FROM {cls.table_name} WHERE {cls.id_column} = %s"
            result = db.fetch_one(query, [id], username, session_id, source_ip)
            
            if result:
                return cls(**result)
            return None
        finally:
            if should_close_db and db:
                db.close()
    
    @classmethod
    def find_all(cls, db=None, conditions=None, params=None, order_by=None, 
                 limit=None, offset=None, username=None, session_id=None, source_ip=None):
        """Find all models matching the conditions."""
        should_close_db = False
        try:
            if db is None:
                db = DBManager()
                should_close_db = True
                
            query = f"SELECT * FROM {cls.table_name}"
            query_params = []
            
            # Add WHERE conditions
            if conditions:
                query += f" WHERE {conditions}"
                if params:
                    query_params.extend(params)
            
            # Add ORDER BY clause
            if order_by:
                query += f" ORDER BY {order_by}"
            
            # Add LIMIT clause
            if limit:
                query += f" LIMIT %s"
                query_params.append(limit)
            
            # Add OFFSET clause
            if offset:
                query += f" OFFSET %s"
                query_params.append(offset)
            
            results = db.fetch_all(query, query_params, username, session_id, source_ip)
            return [cls(**row) for row in results]
        finally:
            if should_close_db and db:
                db.close()
    
    @classmethod
    def delete_by_id(cls, id, db=None, username=None, session_id=None, source_ip=None) -> bool:
        """Delete model by ID."""
        should_close_db = False
        try:
            if db is None:
                db = DBManager()
                should_close_db = True
                
            query = f"DELETE FROM {cls.table_name} WHERE {cls.id_column} = %s"
            db.execute(query, [id], username, session_id, source_ip)
            return True
        finally:
            if should_close_db and db:
                db.close()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return self._data
    
    def __repr__(self) -> str:
        """String representation of model."""
        return f"{self.__class__.__name__}(id={self.id})" 