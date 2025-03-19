#!/usr/bin/env python3

"""
Script to directly fix the save method in models.py
"""

fixed_method = """    def save(self, db=None, username=None, session_id=None, source_ip=None) -> int:
        \"\"\"
        Save model to database.
        Creates new record if id is None, updates existing if id is set.
        \"\"\"
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
"""

with open('/home/ubuntu/lms/database/models.py', 'r') as f:
    content = f.read()

with open('/home/ubuntu/lms/database/models.py.bak2', 'w') as f:
    f.write(content)

start_marker = "    def save(self, db=None, username=None, session_id=None, source_ip=None) -> int:"
end_marker = "            if should_close_db and db:"

start_pos = content.find(start_marker)
end_pos = content.find(end_marker, start_pos)

if start_pos != -1 and end_pos != -1:
    new_content = content[:start_pos] + fixed_method + content[end_pos:]
    
    with open('/home/ubuntu/lms/database/models.py', 'w') as f:
        f.write(new_content)
    
    print("Successfully fixed the save method in models.py")
else:
    print("Could not find the save method in models.py") 