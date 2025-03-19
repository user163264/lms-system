#!/usr/bin/env python3

import psycopg2
import psycopg2.extras
import sys
import json

# Database connection parameters
params = {
    'host': 'localhost',
    'dbname': 'lms_db',
    'user': 'lms_user',
    'password': 'lms_password'
}

def check_grading_info():
    """Connect to the PostgreSQL database and check grading information for each exercise type."""
    conn = None
    try:
        # Connect to the database
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # Create a cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Get all exercises with their grading information
        cur.execute("""
            SELECT id, exercise_type, question, max_score, grading_type
            FROM exercises
            ORDER BY exercise_type, id;
        """)
        exercises = cur.fetchall()
        
        if not exercises:
            print("No exercises found in the database.")
            return
        
        # Process exercises by type
        exercise_types = {}
        for ex in exercises:
            ex_type = ex['exercise_type']
            if ex_type not in exercise_types:
                exercise_types[ex_type] = []
            exercise_types[ex_type].append(ex)
        
        # Print summary table
        print("\nGrading Information Summary by Exercise Type:")
        print("-" * 80)
        print(f"{'Exercise Type':<20} {'Count':<6} {'Max Score':<15} {'Grading Type':<15} {'Status'}")
        print("-" * 80)
        
        for ex_type, exs in exercise_types.items():
            # Check if all exercises of this type have consistent grading info
            max_scores = set(ex['max_score'] if ex['max_score'] is not None else 'NULL' for ex in exs)
            grading_types = set(ex['grading_type'] if ex['grading_type'] is not None else 'NULL' for ex in exs)
            
            # Format as comma-separated if multiple values exist
            max_score_str = ', '.join(map(str, max_scores))
            grading_type_str = ', '.join(map(str, grading_types))
            status = "Consistent" if len(max_scores) == 1 and len(grading_types) == 1 else "Inconsistent"
            
            print(f"{ex_type:<20} {len(exs):<6} {max_score_str:<15} {grading_type_str:<15} {status}")
        
        # Print detailed information for each exercise
        print("\nDetailed Exercise Grading Information:")
        print("-" * 100)
        print(f"{'ID':<4} {'Type':<20} {'Question':<50} {'Max Score':<10} {'Grading Type'}")
        print("-" * 100)
        
        for ex in exercises:
            question = ex['question'][:47] + "..." if len(ex['question']) > 47 else ex['question']
            max_score = ex['max_score'] if ex['max_score'] is not None else "NULL"
            grading_type = ex['grading_type'] if ex['grading_type'] is not None else "NULL"
            
            print(f"{ex['id']:<4} {ex['exercise_type']:<20} {question:<50} {max_score:<10} {grading_type}")
        
        # Close the cursor
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            print('\nDatabase connection closed.')

if __name__ == '__main__':
    check_grading_info() 