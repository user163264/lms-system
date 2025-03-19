"""
Test data generator for the LMS system
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, get_db
from app.models import Base, Lesson, Exercise, ExerciseTemplate, ExerciseContent
from app.models.exercise import ExerciseType

async def reset_database():
    """Reset the database by dropping and recreating all tables"""
    async with engine.begin() as conn:
        # Drop with CASCADE to handle dependencies
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        
        # Recreate all tables
        await conn.run_sync(Base.metadata.create_all)
    print("Database reset complete")

async def create_test_lessons():
    """Create sample lessons"""
    async for db in get_db():
        lessons = [
            Lesson(
                title="Introduction to Python",
                description="Learn the basics of Python programming",
                content="Python is a high-level, interpreted programming language...",
                order=1
            ),
            Lesson(
                title="Variables and Data Types",
                description="Understanding variables and basic data types",
                content="Variables are used to store information that can be referenced and manipulated...",
                order=2
            ),
            Lesson(
                title="Control Flow",
                description="Learn about if statements, loops, and other control structures",
                content="Control flow is the order in which individual statements are executed...",
                order=3
            )
        ]
        
        for lesson in lessons:
            db.add(lesson)
        
        await db.commit()
        print(f"Created {len(lessons)} sample lessons")
        return lessons

async def create_test_exercises(lessons):
    """Create sample exercises linked to lessons"""
    if not lessons:
        return []
        
    async for db in get_db():
        exercises = [
            Exercise(
                lesson_id=lessons[0].id,
                title="Hello World",
                description="Write your first Python program",
                exercise_type="short_answer",
                content={"prompt": "Write code to print 'Hello, World!' in Python"},
                correct_answer=["print('Hello, World!')", "print(\"Hello, World!\")", "print('Hello, World')"],
                max_score=10,
                grading_type="auto"
            ),
            Exercise(
                lesson_id=lessons[1].id,
                title="Variable Assignment",
                description="Assign values to variables",
                exercise_type="multiple_choice",
                content={
                    "question": "Which of the following is the correct way to assign a value in Python?",
                    "options": [
                        "x <- 5",
                        "x = 5",
                        "x == 5",
                        "x => 5"
                    ]
                },
                correct_answer=["x = 5"],
                max_score=5,
                grading_type="auto"
            ),
            Exercise(
                lesson_id=lessons[2].id,
                title="If Statement",
                description="Write an if statement",
                exercise_type="fill_blank",
                content={
                    "text": "Complete the following if statement: if x > 10: _____"
                },
                correct_answer=["print('x is greater than 10')", "print(\"x is greater than 10\")"],
                max_score=8,
                grading_type="auto"
            )
        ]
        
        for exercise in exercises:
            db.add(exercise)
        
        await db.commit()
        print(f"Created {len(exercises)} sample exercises")
        return exercises

async def create_exercise_templates():
    """Create sample exercise templates"""
    async for db in get_db():
        templates = [
            ExerciseTemplate(
                name="Multiple Choice Question",
                type=ExerciseType.MULTIPLE_CHOICE,
                validation_rules={
                    "min_options": 2,
                    "max_options": 6,
                    "allow_multiple_correct": False
                },
                scoring_mechanism={
                    "correct_points": 1,
                    "incorrect_points": 0
                },
                display_parameters={
                    "shuffle_options": True,
                    "show_feedback_immediately": True
                }
            ),
            ExerciseTemplate(
                name="Fill in the Blank",
                type=ExerciseType.FILL_BLANK,
                validation_rules={
                    "min_blanks": 1,
                    "max_blanks": 5,
                    "case_sensitive": False
                },
                scoring_mechanism={
                    "points_per_blank": 1,
                    "partial_credit": True
                },
                display_parameters={
                    "show_blanks_as": "underscores"
                }
            ),
            ExerciseTemplate(
                name="True/False Question",
                type=ExerciseType.TRUE_FALSE,
                validation_rules={},
                scoring_mechanism={
                    "correct_points": 1,
                    "incorrect_points": 0
                },
                display_parameters={
                    "show_as_buttons": True
                }
            )
        ]
        
        for template in templates:
            db.add(template)
        
        await db.commit()
        print(f"Created {len(templates)} exercise templates")
        return templates

async def create_exercise_content(templates):
    """Create sample exercise content based on templates"""
    if not templates:
        return []
        
    async for db in get_db():
        contents = [
            ExerciseContent(
                template_id=templates[0].id,  # Multiple Choice
                title="Python Creator",
                instructions="Select the correct answer",
                question_text="Who created the Python programming language?",
                correct_answers=["Guido van Rossum"],
                alternate_answers=[],
                difficulty_level=1,
                tags=["python", "history"],
                subject_area="programming"
            ),
            ExerciseContent(
                template_id=templates[1].id,  # Fill in the Blank
                title="Python Print Function",
                instructions="Fill in the blank with the correct code",
                question_text="To display text in Python, use the _____ function.",
                correct_answers=["print"],
                alternate_answers=["print()"],
                difficulty_level=1,
                tags=["python", "basics"],
                subject_area="programming"
            ),
            ExerciseContent(
                template_id=templates[2].id,  # True/False
                title="Python Version",
                instructions="Determine if the statement is true or false",
                question_text="Python 3.0 is backward compatible with Python 2.7.",
                correct_answers=["False"],
                alternate_answers=[],
                difficulty_level=2,
                tags=["python", "versions"],
                subject_area="programming"
            )
        ]
        
        for content in contents:
            db.add(content)
        
        await db.commit()
        print(f"Created {len(contents)} exercise content items")
        return contents

async def generate_all_test_data():
    """Generate all test data"""
    await reset_database()
    lessons = await create_test_lessons()
    await create_test_exercises(lessons)
    templates = await create_exercise_templates()
    await create_exercise_content(templates)
    print("All test data generated successfully")

if __name__ == "__main__":
    asyncio.run(generate_all_test_data()) 