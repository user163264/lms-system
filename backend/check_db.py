#!/usr/bin/env python3

import psycopg2
import psycopg2.extras
import sys
import json
import argparse

# Database connection parameters
params = {
    'host': 'localhost',
    'dbname': 'lms_db',
    'user': 'lms_user',
    'password': 'lms_password'
}

def check_exercises():
    """Connect to the PostgreSQL database and check exercise types."""
    conn = None
    try:
        # Connect to the database
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # Create a cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Execute a query to check if the exercises table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = 'exercises'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            print("The 'exercises' table does not exist in the database.")
            return
        
        # Get the count of exercises in the database
        cur.execute("SELECT COUNT(*) FROM exercises;")
        count = cur.fetchone()[0]
        print(f"Total exercises in database: {count}")
        
        # Get the distinct exercise types
        cur.execute("SELECT DISTINCT exercise_type FROM exercises;")
        types = cur.fetchall()
        if types:
            print("\nExercise types in database:")
            for t in types:
                cur.execute("SELECT COUNT(*) FROM exercises WHERE exercise_type = %s;", (t[0],))
                type_count = cur.fetchone()[0]
                print(f"  - {t[0]}: {type_count} exercises")
                
            # Get sample exercises for each type
            print("\nSample exercises:")
            for t in types:
                cur.execute("""
                    SELECT id, lesson_id, exercise_type, question, options, correct_answer 
                    FROM exercises 
                    WHERE exercise_type = %s 
                    LIMIT 1
                """, (t[0],))
                exercise = cur.fetchone()
                if exercise:
                    print(f"\n  Exercise ID: {exercise['id']} (Type: {exercise['exercise_type']})")
                    print(f"  Question: {exercise['question']}")
                    if exercise['options']:
                        print(f"  Options: {json.dumps(exercise['options'], indent=2)}")
                    print(f"  Correct Answer: {json.dumps(exercise['correct_answer'], indent=2)}")
        else:
            print("No exercise types found in the database.")
        
        # Close the cursor
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            print('\nDatabase connection closed.')

def add_test_exercises():
    """Add test exercises for each of the newly aligned exercise types."""
    conn = None
    try:
        # Connect to the database
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # Create a cursor
        cur = conn.cursor()
        
        # First, get a valid lesson_id to use
        cur.execute("SELECT id FROM lessons LIMIT 1;")
        result = cur.fetchone()
        if not result:
            print("No lessons found in the database. Please create a lesson first.")
            return
        
        lesson_id = result[0]
        print(f"Using lesson_id: {lesson_id} for test exercises")
        
        # Define test exercises with the correctly aligned types
        test_exercises = [
            {
                'lesson_id': lesson_id,
                'exercise_type': 'matching_words',  # Previously word_match
                'question': 'Match the following words to their definitions',
                'options': json.dumps({
                    'items_a': ['Apple', 'Banana', 'Cherry'],
                    'items_b': ['Red fruit', 'Yellow fruit', 'Red small fruit']
                }),
                'correct_answer': json.dumps({'0': '0', '1': '1', '2': '2'})
            },
            {
                'lesson_id': lesson_id,
                'exercise_type': 'sentence_reordering',  # Previously sentence_order
                'question': 'Arrange the sentences in the correct order',
                'options': json.dumps({
                    'sentences': ['First sentence', 'Second sentence', 'Third sentence']
                }),
                'correct_answer': json.dumps([0, 1, 2])
            },
            {
                'lesson_id': lesson_id,
                'exercise_type': 'cloze_test',  # Previously gap_text
                'question': 'Fill in the blanks with appropriate words',
                'options': json.dumps({
                    'word_bank': ['quickly', 'slowly', 'carefully']
                }),
                'correct_answer': json.dumps(['quickly'])
            },
            {
                'lesson_id': lesson_id,
                'exercise_type': 'word_scramble',  # New type
                'question': 'Unscramble the words to form a sentence',
                'options': json.dumps({
                    'sentence': 'The quick brown fox jumps over the lazy dog'
                }),
                'correct_answer': json.dumps(['The quick brown fox jumps over the lazy dog'])
            },
            {
                'lesson_id': lesson_id,
                'exercise_type': 'image_labeling',  # New type
                'question': 'Label the parts of the cell',
                'options': json.dumps({
                    'image_url': 'https://example.com/cell.jpg',
                    'labels': ['Nucleus', 'Cell Membrane', 'Mitochondrion'],
                    'label_points': [
                        {'id': '1', 'x': 30, 'y': 30},
                        {'id': '2', 'x': 50, 'y': 60},
                        {'id': '3', 'x': 70, 'y': 40}
                    ]
                }),
                'correct_answer': json.dumps({
                    '1': 'Nucleus',
                    '2': 'Cell Membrane',
                    '3': 'Mitochondrion'
                })
            },
            {
                'lesson_id': lesson_id,
                'exercise_type': 'long_answer',  # Previously summarization
                'question': 'Write an essay about climate change',
                'options': json.dumps({
                    'min_words': 100,
                    'max_words': 500
                }),
                'correct_answer': json.dumps([])  # Empty for manual grading
            }
        ]
        
        # Insert the test exercises
        for exercise in test_exercises:
            cur.execute("""
                INSERT INTO exercises (lesson_id, exercise_type, question, options, correct_answer)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                exercise['lesson_id'], 
                exercise['exercise_type'], 
                exercise['question'], 
                exercise['options'], 
                exercise['correct_answer']
            ))
            exercise_id = cur.fetchone()[0]
            print(f"Added {exercise['exercise_type']} exercise with ID: {exercise_id}")
        
        # Commit the transaction
        conn.commit()
        
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

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Database exercise type checker')
    parser.add_argument('--add', action='store_true', help='Add test exercises for newly aligned types')
    
    args = parser.parse_args()
    
    if args.add:
        add_test_exercises()
    else:
        check_exercises()

if __name__ == '__main__':
    main() 