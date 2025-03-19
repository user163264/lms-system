-- LMS Database Schema
-- Consolidated version combining database_schema.sql and database_schema_fixed.sql

-- Schema migration logging table
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_by VARCHAR(100) NOT NULL
);

-- Insert initial migration record
INSERT INTO schema_migrations (version, description, applied_by)
VALUES ('1.0.0', 'Initial schema creation', 'system')
ON CONFLICT (version) DO NOTHING;

-- Main Tables

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tests table
CREATE TABLE IF NOT EXISTS tests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    subject_area VARCHAR(50),
    difficulty_level INTEGER,
    time_limit INTEGER,  -- in minutes
    passing_score INTEGER,  -- minimum score to pass
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creator_id INTEGER, -- ID of the user who created the test
    is_active BOOLEAN DEFAULT TRUE
);

-- Test questions table
CREATE TABLE IF NOT EXISTS test_questions (
    id SERIAL PRIMARY KEY,
    test_id INTEGER REFERENCES tests(id) ON DELETE CASCADE,
    exercise_id INTEGER,  -- ID of the exercise template
    question_order INTEGER NOT NULL,  -- Order of the question within the test
    weight INTEGER DEFAULT 1,  -- Weight of the question for scoring
    is_required BOOLEAN DEFAULT TRUE,
    question_type VARCHAR(50) NOT NULL,  -- Type of question (multiple choice, fill-in-blank, etc.)
    UNIQUE (test_id, question_order)
);

-- Student-Test assignments
CREATE TABLE IF NOT EXISTS student_tests (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    test_id INTEGER REFERENCES tests(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_at TIMESTAMP,
    max_attempts INTEGER DEFAULT 1,
    attempts_used INTEGER DEFAULT 0,
    UNIQUE (student_id, test_id)
);

-- Submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    test_id INTEGER REFERENCES tests(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'submitted', 'graded', 'abandoned')),
    ip_address VARCHAR(45),
    user_agent TEXT,
    attempt_number INTEGER DEFAULT 1,
    is_passing BOOLEAN
);

-- Submission answers table
CREATE TABLE IF NOT EXISTS submission_answers (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES test_questions(id) ON DELETE CASCADE,
    answer TEXT, -- JSON or plain text depending on question type
    is_correct BOOLEAN,
    score INTEGER,
    feedback TEXT,
    submit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scores table
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    test_id INTEGER REFERENCES tests(id),
    total_score INTEGER,
    max_possible_score INTEGER,
    graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_passing BOOLEAN,
    attempt_number INTEGER DEFAULT 1
);

-- Logging tables

-- Query logs for performance monitoring
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    query_text TEXT,
    parameters TEXT,
    execution_time REAL, -- in milliseconds
    row_count INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    ip_address VARCHAR(45)
);

-- Error logs for debugging
CREATE TABLE IF NOT EXISTS error_logs (
    id SERIAL PRIMARY KEY,
    error_message TEXT,
    error_type VARCHAR(100),
    stack_trace TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    ip_address VARCHAR(45),
    request_path TEXT,
    request_method VARCHAR(10)
);

-- Authentication logs for security
CREATE TABLE IF NOT EXISTS auth_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    username VARCHAR(50),
    action VARCHAR(50), -- login, logout, password change, etc.
    status VARCHAR(20), -- success, failure
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    failure_reason TEXT
);

-- Submission activity logs
CREATE TABLE IF NOT EXISTS submission_logs (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
    action VARCHAR(50), -- started, resumed, saved, submitted, etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    details TEXT -- JSON with additional details
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_submissions_student_id ON submissions(student_id);
CREATE INDEX IF NOT EXISTS idx_submissions_test_id ON submissions(test_id);
CREATE INDEX IF NOT EXISTS idx_submission_answers_submission_id ON submission_answers(submission_id);
CREATE INDEX IF NOT EXISTS idx_scores_student_id ON scores(student_id);
CREATE INDEX IF NOT EXISTS idx_scores_test_id ON scores(test_id);
CREATE INDEX IF NOT EXISTS idx_test_questions_test_id ON test_questions(test_id);
CREATE INDEX IF NOT EXISTS idx_student_tests_student_id ON student_tests(student_id);
CREATE INDEX IF NOT EXISTS idx_student_tests_test_id ON student_tests(test_id);

-- Schema change logging function
CREATE OR REPLACE FUNCTION log_schema_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO schema_migrations (version, description, applied_by)
    VALUES (TG_ARGV[0], TG_ARGV[1], CURRENT_USER);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Test completion status view
CREATE OR REPLACE VIEW test_completion_status AS
SELECT
    st.student_id,
    st.test_id,
    t.title as test_title,
    CASE
        WHEN EXISTS (
            SELECT 1 FROM submissions sub 
            WHERE sub.student_id = st.student_id AND sub.test_id = st.test_id 
            AND sub.status = 'graded' AND sub.is_passing = true
        ) THEN 'passed'
        WHEN EXISTS (
            SELECT 1 FROM submissions sub 
            WHERE sub.student_id = st.student_id AND sub.test_id = st.test_id 
            AND sub.status = 'in_progress'
        ) THEN 'in_progress'
        ELSE 'not_started'
    END as status,
    st.assigned_at,
    st.due_at,
    st.max_attempts,
    st.attempts_used
FROM
    student_tests st
JOIN
    tests t ON st.test_id = t.id;

-- Record this in migrations
INSERT INTO schema_migrations (version, description, applied_by)
VALUES ('1.0.2', 'Created test_completion_status view', 'system')
ON CONFLICT (version) DO NOTHING; 