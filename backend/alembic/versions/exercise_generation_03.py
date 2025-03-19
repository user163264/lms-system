"""Add exercise generation tables

Revision ID: exercise_generation_03
Revises: exercise_generation_02
Create Date: 2023-06-11 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON, ARRAY


# revision identifiers, used by Alembic.
revision = 'exercise_generation_03'
down_revision = 'exercise_generation_02'
branch_labels = None
depends_on = None


def upgrade():
    # Create exercise types enum
    op.execute("""
        CREATE TYPE IF NOT EXISTS exercise_type AS ENUM (
            'word_scramble', 'multiple_choice', 'fill_blank', 'true_false',
            'long_answer', 'syn_ant', 'sentence_reordering', 'matching_words',
            'short_answer', 'cloze_test', 'comprehension', 'image_labeling'
        )
    """)
    
    # Create exercise_templates table if it doesn't exist
    op.execute("""
        CREATE TABLE IF NOT EXISTS exercise_templates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type exercise_type NOT NULL,
            validation_rules JSONB,
            scoring_mechanism JSONB,
            display_parameters JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)
    op.create_index(op.f('ix_exercise_templates_id'), 'exercise_templates', ['id'], unique=False)
    
    # Create exercise_content table if it doesn't exist
    op.execute("""
        CREATE TABLE IF NOT EXISTS exercise_content (
            id SERIAL PRIMARY KEY,
            template_id INTEGER NOT NULL REFERENCES exercise_templates(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            instructions TEXT,
            question_text TEXT NOT NULL,
            correct_answers JSONB NOT NULL,
            alternate_answers JSONB,
            difficulty_level INTEGER NOT NULL DEFAULT 1,
            tags VARCHAR[],
            subject_area VARCHAR(100),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)
    op.create_index(op.f('ix_exercise_content_id'), 'exercise_content', ['id'], unique=False)
    op.create_index(op.f('ix_exercise_content_template_id'), 'exercise_content', ['template_id'], unique=False)
    
    # Create media_assets table if it doesn't exist
    op.execute("""
        CREATE TABLE IF NOT EXISTS media_assets (
            id SERIAL PRIMARY KEY,
            exercise_content_id INTEGER NOT NULL REFERENCES exercise_content(id) ON DELETE CASCADE,
            file_path VARCHAR(255) NOT NULL,
            asset_type VARCHAR(50) NOT NULL,
            alt_text VARCHAR(255),
            caption TEXT,
            license_info VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)
    op.create_index(op.f('ix_media_assets_id'), 'media_assets', ['id'], unique=False)
    op.create_index(op.f('ix_media_assets_exercise_content_id'), 'media_assets', ['exercise_content_id'], unique=False)
    
    # Create user_responses table if it doesn't exist
    op.execute("""
        CREATE TABLE IF NOT EXISTS user_responses (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            exercise_content_id INTEGER NOT NULL REFERENCES exercise_content(id) ON DELETE CASCADE,
            response_data JSONB NOT NULL,
            score INTEGER,
            completion_status VARCHAR(20) NOT NULL DEFAULT 'started',
            attempt_number INTEGER NOT NULL DEFAULT 1,
            started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            completed_at TIMESTAMP WITH TIME ZONE
        )
    """)
    op.create_index(op.f('ix_user_responses_id'), 'user_responses', ['id'], unique=False)
    op.create_index(op.f('ix_user_responses_user_id'), 'user_responses', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_responses_exercise_content_id'), 'user_responses', ['exercise_content_id'], unique=False)


def downgrade():
    # Drop tables in reverse order of creation
    op.drop_table('user_responses', if_exists=True)
    op.drop_table('media_assets', if_exists=True)
    op.drop_table('exercise_content', if_exists=True)
    op.drop_table('exercise_templates', if_exists=True)
    
    # Drop the enum type
    op.execute('DROP TYPE IF EXISTS exercise_type') 