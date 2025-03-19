import asyncio
import sys
import os
import json
from sqlalchemy import text

# Add parent directory to path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

# Database URL
DATABASE_URL = "postgresql+asyncpg://lms_user:lms_password@localhost/lms_db"

async def reset_db():
    """Reset the database using raw SQL"""
    
    # Create a new engine and connection
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # Drop tables in correct order to avoid foreign key constraints
        await conn.execute(text("DROP TABLE IF EXISTS submissions"))
        await conn.execute(text("DROP TABLE IF EXISTS exercises"))
        await conn.execute(text("DROP TABLE IF EXISTS lesson_students"))
        await conn.execute(text("DROP TABLE IF EXISTS lessons"))
        await conn.execute(text("DROP TABLE IF EXISTS users"))
        
        # Create users table
        await conn.execute(text("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR NOT NULL UNIQUE,
            email VARCHAR NOT NULL UNIQUE,
            password_hash VARCHAR NOT NULL,
            user_type VARCHAR NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        )
        """))
        
        # Create lessons table
        await conn.execute(text("""
        CREATE TABLE lessons (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            owner_id INTEGER NOT NULL REFERENCES users(id),
            description TEXT,
            content TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        )
        """))
        
        # Create lesson_students join table
        await conn.execute(text("""
        CREATE TABLE lesson_students (
            lesson_id INTEGER NOT NULL REFERENCES lessons(id),
            student_id INTEGER NOT NULL REFERENCES users(id),
            PRIMARY KEY (lesson_id, student_id)
        )
        """))
        
        # Create exercises table
        await conn.execute(text("""
        CREATE TABLE exercises (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER NOT NULL REFERENCES lessons(id),
            exercise_type VARCHAR NOT NULL,
            question TEXT NOT NULL,
            options JSON,
            correct_answer JSON NOT NULL,
            max_score INTEGER,
            grading_type VARCHAR
        )
        """))
        
        # Create submissions table
        await conn.execute(text("""
        CREATE TABLE submissions (
            id SERIAL PRIMARY KEY,
            student_id INTEGER NOT NULL REFERENCES users(id),
            exercise_id INTEGER NOT NULL REFERENCES exercises(id),
            answer TEXT,
            score INTEGER,
            submitted_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        )
        """))
    
    print("Database reset complete")
    return engine

async def create_test_data(engine):
    """Create sample data for testing"""
    
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Create users
            result = await session.execute(text("""
            INSERT INTO users (username, email, password_hash, user_type)
            VALUES 
                ('admin', 'admin@example.com', 'admin_password', 'admin'),
                ('teacher', 'teacher@example.com', 'teacher_password', 'teacher'),
                ('student', 'student@example.com', 'student_password', 'student')
            RETURNING id, username, user_type
            """))
            users = result.fetchall()
            
            admin_id = users[0][0]
            teacher_id = users[1][0]
            student_id = users[2][0]
            
            # Create a lesson
            result = await session.execute(
                text("""
                INSERT INTO lessons (title, owner_id, description, content)
                VALUES (
                    'Introduction to Art History',
                    :teacher_id,
                    'Learn about famous paintings and artists',
                    'This lesson covers the history of art from the Renaissance to Modern art.'
                )
                RETURNING id, title
                """).bindparams(teacher_id=teacher_id)
            )
            lesson = result.fetchone()
            lesson_id = lesson[0]
            
            # Associate student with the lesson
            await session.execute(
                text("""
                INSERT INTO lesson_students (lesson_id, student_id)
                VALUES (:lesson_id, :student_id)
                """).bindparams(lesson_id=lesson_id, student_id=student_id)
            )
            
            # Create exercises - need to use proper parameter binding
            fill_blank = await session.execute(
                text("""
                INSERT INTO exercises (lesson_id, exercise_type, question, options, correct_answer, max_score, grading_type)
                VALUES (
                    :lesson_id,
                    'fill_blank',
                    'The glimlach van de _______ is wereldberoemd en blijft een mysterie.',
                    NULL,
                    :correct_answer_1,
                    1,
                    'auto'
                )
                RETURNING id, exercise_type
                """).bindparams(
                    lesson_id=lesson_id, 
                    correct_answer_1=json.dumps(["Mona Lisa"])
                )
            )
            fill_blank_result = fill_blank.fetchone()
            fill_blank_id = fill_blank_result[0]
            
            true_false = await session.execute(
                text("""
                INSERT INTO exercises (lesson_id, exercise_type, question, options, correct_answer, max_score, grading_type)
                VALUES (
                    :lesson_id,
                    'true_false',
                    'Mona Lisa werd geschilderd door Vincent van Gogh.',
                    :options_2,
                    :correct_answer_2,
                    1,
                    'auto'
                )
                RETURNING id, exercise_type
                """).bindparams(
                    lesson_id=lesson_id,
                    options_2=json.dumps(["waar", "niet waar"]),
                    correct_answer_2=json.dumps(["niet waar"])
                )
            )
            
            multiple_choice = await session.execute(
                text("""
                INSERT INTO exercises (lesson_id, exercise_type, question, options, correct_answer, max_score, grading_type)
                VALUES (
                    :lesson_id,
                    'multiple_choice',
                    'Welk museum herbergt de Mona Lisa?',
                    :options_3,
                    :correct_answer_3,
                    1,
                    'auto'
                )
                RETURNING id, exercise_type
                """).bindparams(
                    lesson_id=lesson_id,
                    options_3=json.dumps(["Prado", "Louvre", "Rijksmuseum"]),
                    correct_answer_3=json.dumps(["Louvre"])
                )
            )
            
            # Create a submission
            await session.execute(
                text("""
                INSERT INTO submissions (student_id, exercise_id, answer, score)
                VALUES (
                    :student_id,
                    :exercise_id,
                    'Mona Lisa',
                    1
                )
                """).bindparams(student_id=student_id, exercise_id=fill_blank_id)
            )
    
    print("Test data created:")
    print(f"- Admin user (ID: {admin_id})")
    print(f"- Teacher user (ID: {teacher_id})")
    print(f"- Student user (ID: {student_id})")
    print(f"- Lesson: Introduction to Art History (ID: {lesson_id})")
    print(f"- Exercises created: 3")
    print(f"- Submission created for student")

async def main():
    """Main function to run the test"""
    print("Starting database test...")
    engine = await reset_db()
    await create_test_data(engine)
    print("Database test completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())