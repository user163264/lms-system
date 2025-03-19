#!/usr/bin/env python3
"""
Script Name: import_exercise.py
Description: Imports exercise data from a JSON file into the LMS database

Usage:
    python scripts/import/import_exercise.py

Dependencies:
    - psycopg2
    - json

Output:
    Imported exercise data and status messages

Author: LMS Team
Last Modified: 2025-03-19
"""

import json
import psycopg2

# PostgreSQL connection config
DB_HOST = "localhost"
DB_NAME = "lms_db"
DB_USER = "lms_user"
DB_PASS = "lms_password"  # Updated password

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    print("✅ Connected to the database!")
except Exception as e:
    print("❌ Failed to connect to the database.")
    print(e)
    exit(1)

cur = conn.cursor()

# Load exercise JSON from the correct path
try:
    with open("/home/ubuntu/lms/test_import.json", "r") as file:
        data = json.load(file)
    print("✅ JSON file loaded successfully!")
except Exception as e:
    print("❌ Failed to load JSON file.")
    print(e)
    exit(1)

# Extract lesson_id
lesson_id = data.get("lesson_id")
if not lesson_id:
    print("❌ 'lesson_id' not found in JSON.")
    exit(1)

# Iterate over exercises and insert them
for exercise in data.get("exercises", []):
    try:
        # Prepare correct_answer and options as PostgreSQL arrays
        correct_answer = exercise.get("correct_answer", [])
        options = exercise.get("options", [])

        # Ensure both are lists
        if not isinstance(correct_answer, list):
            correct_answer = [correct_answer]
        if not isinstance(options, list):
            options = [options]

        # Execute the insert query
        cur.execute(
            """
            INSERT INTO exercises (lesson_id, exercise_type, question, correct_answer, options)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                lesson_id,
                exercise.get("exercise_type"),
                exercise.get("question"),
                correct_answer,  # Insert as PostgreSQL array
                options          # Insert as PostgreSQL array
            )
        )
        print(f"✅ Inserted exercise: {exercise.get('question')[:50]}...")
    except Exception as e:
        print(f"❌ Failed to insert exercise: {exercise.get('question')[:50]}...")
        print(e)
        conn.rollback()

# Commit all changes
conn.commit()
print("✅ All exercises imported successfully!")

cur.close()
conn.close()
print("✅ Database connection closed.")
