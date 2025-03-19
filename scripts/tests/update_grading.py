#!/usr/bin/env python3
"""
Script Name: update_grading.py
Description: Updates exercise grading logic in the LMS system

Usage:
    python scripts/tests/update_grading.py

Dependencies:
    - psycopg2

Output:
    Updated grading logic for exercises

Author: LMS Team
Last Modified: 2025-03-19
"""

#!/usr/bin/env python3

import psycopg2
import sys

# Database connection parameters
params = {
    'host': 'localhost',
    'dbname': 'lms_db',
    'user': 'lms_user',
    'password': 'lms_password'
}

def update_grading_info():
    """Update the grading information for all exercise types in the database."""
    conn = None
    try:
        # Connect to the database
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # Create a cursor
        cur = conn.cursor()
        
        # Define the updates to be applied
        updates = [
            {
                'exercise_type': 'cloze_test',
                'max_score': 2,
                'grading_type': 'auto'
            },
            {
                'exercise_type': 'matching_words',
                'max_score': 3,
                'grading_type': 'auto'
            },
            {
                'exercise_type': 'sentence_reordering',
                'max_score': 1,
                'grading_type': 'auto'
            },
            {
                'exercise_type': 'word_scramble',
                'max_score': 1,
                'grading_type': 'auto'
            },
            {
                'exercise_type': 'image_labeling',
                'max_score': 1,
                'grading_type': 'auto'
            },
            {
                'exercise_type': 'long_answer',
                'max_score': 5,
                'grading_type': 'manual'
            }
        ]
        
        # Execute updates
        for update in updates:
            cur.execute(
                """
                UPDATE exercises
                SET max_score = %s, grading_type = %s
                WHERE exercise_type = %s
                """,
                (update['max_score'], update['grading_type'], update['exercise_type'])
            )
            row_count = cur.rowcount
            print(f"Updated {row_count} {update['exercise_type']} exercises: max_score={update['max_score']}, grading_type={update['grading_type']}")
        
        # Add default values to the database schema
        try:
            cur.execute("""
                ALTER TABLE exercises 
                ALTER COLUMN max_score SET DEFAULT 1,
                ALTER COLUMN grading_type SET DEFAULT 'auto';
            """)
            print("Added default values to the database schema: max_score=1, grading_type='auto'")
        except Exception as e:
            print(f"Warning: Could not add default values to the schema: {e}")
        
        # Commit the transaction
        conn.commit()
        print("All updates committed successfully!")
        
        # Close the cursor
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            print('\nDatabase connection closed.')

if __name__ == '__main__':
    update_grading_info() 