#!/usr/bin/env python3

import psycopg2
import sys
import time
from datetime import datetime

# Database connection parameters
params = {
    'host': 'localhost',
    'dbname': 'lms_db',
    'user': 'lms_user',
    'password': 'lms_password'
}

def update_schema():
    """Update the existing database schema to match our new requirements."""
    conn = None
    
    try:
        # Connect to the database
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # Create a cursor
        cur = conn.cursor()
        
        # Create schema_migrations table if it doesn't exist
        print("Setting up schema migration tracking...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                version VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_by VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        
        # Record this migration
        cur.execute(
            "INSERT INTO schema_migrations (version, description, applied_by) VALUES (%s, %s, %s)",
            ('1.0.0', 'Schema update initiation', 'update_script')
        )
        conn.commit()
        
        # Start timing
        start_time = time.time()
        
        # First, check current state of submissions table
        print("Checking current submissions table structure...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'submissions'
        """)
        existing_columns = [col[0] for col in cur.fetchall()]
        print(f"Current columns: {', '.join(existing_columns)}")
        
        # Modify the submissions table to match our schema
        print("Updating submissions table structure...")
        
        # Add test_id column if it doesn't exist
        if 'test_id' not in existing_columns:
            print("Adding test_id column...")
            cur.execute("""
                ALTER TABLE submissions 
                ADD COLUMN test_id INTEGER REFERENCES tests(id) ON DELETE CASCADE
            """)
            conn.commit()
        
        # Add other missing columns
        columns_to_add = {
            'started_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'submitted_at': 'TIMESTAMP',
            'completion_time_minutes': 'INTEGER',
            'status': "VARCHAR(20) DEFAULT 'in_progress'",
            'ip_address': 'VARCHAR(45)',
            'user_agent': 'TEXT',
            'total_score': 'DECIMAL(5,2)',
            'is_passing': 'BOOLEAN',
            'attempt_number': 'INTEGER DEFAULT 1'
        }
        
        for col_name, col_type in columns_to_add.items():
            if col_name not in existing_columns:
                print(f"Adding {col_name} column...")
                cur.execute(f"ALTER TABLE submissions ADD COLUMN {col_name} {col_type}")
                conn.commit()
        
        # Now create any indexes that don't exist
        print("Setting up indexes...")
        
        cur.execute("""
            SELECT indexname FROM pg_indexes
            WHERE tablename = 'submissions' AND indexname = 'idx_submissions_test_id'
        """)
        if not cur.fetchone():
            print("Creating index on test_id...")
            cur.execute("CREATE INDEX idx_submissions_test_id ON submissions(test_id)")
            conn.commit()
        
        # Set up other tables if they don't exist
        tables_to_check = [
            'students',
            'tests',
            'test_questions',
            'student_tests',
            'submission_answers',
            'scores',
            'query_logs',
            'error_logs',
            'auth_logs',
            'submission_logs'
        ]
        
        for table in tables_to_check:
            cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
            if not cur.fetchone()[0]:
                print(f"Table {table} does not exist, creating...")
                
                # Create the table based on its name
                if table == 'students':
                    cur.execute("""
                        CREATE TABLE students (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            full_name VARCHAR(100) NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_login TIMESTAMP,
                            is_active BOOLEAN DEFAULT TRUE
                        )
                    """)
                
                elif table == 'tests':
                    cur.execute("""
                        CREATE TABLE tests (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(100) NOT NULL,
                            description TEXT,
                            duration_minutes INTEGER NOT NULL,
                            randomize_questions BOOLEAN DEFAULT FALSE,
                            passing_score DECIMAL(5,2),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            created_by INTEGER REFERENCES students(id),
                            is_active BOOLEAN DEFAULT TRUE
                        )
                    """)
                
                elif table == 'test_questions':
                    cur.execute("""
                        CREATE TABLE test_questions (
                            id SERIAL PRIMARY KEY,
                            test_id INTEGER REFERENCES tests(id) ON DELETE CASCADE,
                            exercise_id INTEGER REFERENCES exercises(id) ON DELETE CASCADE,
                            question_order INTEGER NOT NULL,
                            weight DECIMAL(5,2) DEFAULT 1.0,
                            is_required BOOLEAN DEFAULT TRUE
                        )
                    """)
                
                elif table == 'student_tests':
                    cur.execute("""
                        CREATE TABLE student_tests (
                            id SERIAL PRIMARY KEY,
                            student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
                            test_id INTEGER REFERENCES tests(id) ON DELETE CASCADE,
                            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            due_at TIMESTAMP,
                            max_attempts INTEGER DEFAULT 1,
                            attempts_used INTEGER DEFAULT 0,
                            UNIQUE (student_id, test_id)
                        )
                    """)
                
                elif table == 'submission_answers':
                    cur.execute("""
                        CREATE TABLE submission_answers (
                            id SERIAL PRIMARY KEY,
                            submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
                            question_id INTEGER REFERENCES test_questions(id) ON DELETE CASCADE,
                            exercise_id INTEGER REFERENCES exercises(id),
                            answer_data JSONB NOT NULL,
                            is_correct BOOLEAN,
                            score DECIMAL(5,2),
                            feedback TEXT,
                            graded_at TIMESTAMP,
                            graded_by VARCHAR(100),
                            grading_notes TEXT
                        )
                    """)
                
                elif table == 'scores':
                    cur.execute("""
                        CREATE TABLE scores (
                            id SERIAL PRIMARY KEY,
                            submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
                            student_id INTEGER REFERENCES students(id),
                            test_id INTEGER REFERENCES tests(id),
                            total_score DECIMAL(5,2) NOT NULL,
                            max_possible_score DECIMAL(5,2) NOT NULL,
                            percentage DECIMAL(5,2) GENERATED ALWAYS AS (total_score / NULLIF(max_possible_score, 0) * 100) STORED,
                            graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            is_passing BOOLEAN,
                            attempt_number INTEGER NOT NULL
                        )
                    """)
                
                elif table == 'query_logs':
                    cur.execute("""
                        CREATE TABLE query_logs (
                            id SERIAL PRIMARY KEY,
                            query_text TEXT NOT NULL,
                            execution_time_ms INTEGER NOT NULL,
                            params JSONB,
                            username VARCHAR(100),
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            source_ip VARCHAR(45),
                            session_id VARCHAR(100)
                        )
                    """)
                
                elif table == 'error_logs':
                    cur.execute("""
                        CREATE TABLE error_logs (
                            id SERIAL PRIMARY KEY,
                            error_code VARCHAR(50),
                            error_message TEXT NOT NULL,
                            error_stack TEXT,
                            severity VARCHAR(20) NOT NULL,
                            component VARCHAR(100),
                            username VARCHAR(100),
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            source_ip VARCHAR(45),
                            session_id VARCHAR(100),
                            request_data JSONB
                        )
                    """)
                
                elif table == 'auth_logs':
                    cur.execute("""
                        CREATE TABLE auth_logs (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(100) NOT NULL,
                            action VARCHAR(50) NOT NULL,
                            status VARCHAR(20) NOT NULL,
                            reason TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            source_ip VARCHAR(45) NOT NULL,
                            user_agent TEXT
                        )
                    """)
                
                elif table == 'submission_logs':
                    cur.execute("""
                        CREATE TABLE submission_logs (
                            id SERIAL PRIMARY KEY,
                            submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
                            student_id INTEGER REFERENCES students(id),
                            test_id INTEGER REFERENCES tests(id),
                            action VARCHAR(50) NOT NULL,
                            details JSONB,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            source_ip VARCHAR(45),
                            session_id VARCHAR(100)
                        )
                    """)
                
                conn.commit()
        
        # Create indexes for performance
        indexes_to_create = {
            'idx_submission_answers_submission_id': 'submission_answers(submission_id)',
            'idx_scores_student_id': 'scores(student_id)',
            'idx_scores_test_id': 'scores(test_id)',
            'idx_test_questions_test_id': 'test_questions(test_id)',
            'idx_student_tests_student_id': 'student_tests(student_id)',
            'idx_student_tests_test_id': 'student_tests(test_id)'
        }
        
        for index_name, index_def in indexes_to_create.items():
            cur.execute(f"""
                SELECT EXISTS (
                    SELECT FROM pg_indexes
                    WHERE indexname = '{index_name}'
                )
            """)
            
            if not cur.fetchone()[0]:
                print(f"Creating index {index_name}...")
                cur.execute(f"CREATE INDEX {index_name} ON {index_def}")
                conn.commit()
        
        # Try to create the view if all required tables exist
        print("Creating test completion status view...")
        try:
            cur.execute("""
                CREATE OR REPLACE VIEW test_completion_status AS
                SELECT 
                    st.student_id,
                    s.username as student_username,
                    st.test_id,
                    t.title as test_title,
                    st.assigned_at,
                    st.due_at,
                    st.max_attempts,
                    st.attempts_used,
                    CASE 
                        WHEN st.attempts_used >= st.max_attempts THEN 'no_attempts_left'
                        WHEN st.due_at < CURRENT_TIMESTAMP THEN 'past_due'
                        WHEN EXISTS (SELECT 1 FROM submissions sub 
                                    WHERE sub.student_id = st.student_id 
                                    AND sub.test_id = st.test_id
                                    AND sub.status = 'graded'
                                    AND sub.is_passing = TRUE) THEN 'passed'
                        WHEN EXISTS (SELECT 1 FROM submissions sub 
                                    WHERE sub.student_id = st.student_id 
                                    AND sub.test_id = st.test_id
                                    AND sub.status = 'in_progress') THEN 'in_progress'
                        ELSE 'not_started'
                    END as status
                FROM 
                    student_tests st
                JOIN 
                    students s ON st.student_id = s.id
                JOIN 
                    tests t ON st.test_id = t.id
            """)
            conn.commit()
            print("View created successfully.")
        except Exception as e:
            print(f"Could not create view: {e}")
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Record the completion of updates
        cur.execute(
            "INSERT INTO schema_migrations (version, description, applied_by) VALUES (%s, %s, %s)",
            ('1.0.4', f'Schema update completed in {execution_time:.2f} seconds', 'update_script')
        )
        conn.commit()
        
        print(f'\nSchema update completed in {execution_time:.2f} seconds.')
        
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
    update_schema() 