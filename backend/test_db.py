#test_db.py

import asyncio
import json
import sys
import os

# Add parent directory to path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, AsyncSessionLocal
from app.models import Base, User, Lesson, Exercise, Submission

async def reset_db():
    """Drop and recreate all tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database reset complete")

async def create_test_data():
    """Create sample data for testing"""
    async with AsyncSessionLocal() as session:
        # Create users
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash="admin_password",  # In production, use proper hashing
            user_type="admin"
        )
        
        teacher = User(
            username="teacher",
            email="teacher@example.com",
            password_hash="teacher_password",
            user_type="teacher"
        )
        
        student = User(
            username="student",
            email="student@example.com",
            password_hash="student_password",
            user_type="student"
        )
        
        session.add_all([admin, teacher, student])
        await session.commit()
        
        # Create a lesson
        lesson = Lesson(
            title="Introduction to Art History",
            description="Learn about famous paintings and artists",
            content="This lesson covers the history of art from the Renaissance to Modern art.",
            owner_id=teacher.id
        )
        
        session.add(lesson)
        await session.flush()  # To get the lesson ID
        
        # Associate student with the lesson
        student.enrolled_lessons.append(lesson)
        
        # Create exercises
        fill_blank_exercise = Exercise(
            lesson_id=lesson.id,
            exercise_type="fill_blank",
            question="The glimlach van de _______ is wereldberoemd en blijft een mysterie.",
            options=None,
            correct_answer=["Mona Lisa"],
            max_score=1,
            grading_type="auto"
        )
        
        true_false_exercise = Exercise(
            lesson_id=lesson.id,
            exercise_type="true_false",
            question="Mona Lisa werd geschilderd door Vincent van Gogh.",
            options=["waar", "niet waar"],
            correct_answer=["niet waar"],
            max_score=1,
            grading_type="auto"
        )
        
        multiple_choice_exercise = Exercise(
            lesson_id=lesson.id,
            exercise_type="multiple_choice",
            question="Welk museum herbergt de Mona Lisa?",
            options=["Prado", "Louvre", "Rijksmuseum"],
            correct_answer=["Louvre"],
            max_score=1,
            grading_type="auto"
        )
        
        session.add_all([fill_blank_exercise, true_false_exercise, multiple_choice_exercise])
        await session.flush()
        
        # Create a submission
        submission = Submission(
            student_id=student.id,
            exercise_id=fill_blank_exercise.id,
            answer="Mona Lisa",
            score=1  # Correct answer scores 1
        )
        
        session.add(submission)
        await session.commit()
        
        print("Test data created:")
        print(f"- Admin user (ID: {admin.id})")
        print(f"- Teacher user (ID: {teacher.id})")
        print(f"- Student user (ID: {student.id})")
        print(f"- Lesson: {lesson.title} (ID: {lesson.id})")
        print(f"- Exercises created: 3")
        print(f"- Submission created for student")

async def main():
    """Main function to run the test"""
    print("Starting database test...")
    await reset_db()
    await create_test_data()
    print("Database test completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())