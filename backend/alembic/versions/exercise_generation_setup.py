"""Exercise generation system tables

Revision ID: exercise_generation_setup
Revises: 09930279e14c
Create Date: 2023-06-10 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON, ARRAY


# revision identifiers, used by Alembic.
revision = 'exercise_generation_02'
down_revision = '09930279e14c'
branch_labels = None
depends_on = None


def upgrade():
    # Create exercise types enum
    op.execute("""
        CREATE TYPE exercise_type AS ENUM (
            'word_scramble', 'multiple_choice', 'fill_blank', 'true_false',
            'long_answer', 'syn_ant', 'sentence_reordering', 'matching_words',
            'short_answer', 'cloze_test', 'comprehension', 'image_labeling'
        )
    """)
    
    # Create exercise_templates table
    op.create_table(
        'exercise_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('type', sa.Enum('word_scramble', 'multiple_choice', 'fill_blank', 'true_false',
                                   'long_answer', 'syn_ant', 'sentence_reordering', 'matching_words',
                                   'short_answer', 'cloze_test', 'comprehension', 'image_labeling',
                                   name='exercise_type'), nullable=False),
        sa.Column('validation_rules', JSON, nullable=True),
        sa.Column('scoring_mechanism', JSON, nullable=True),
        sa.Column('display_parameters', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_templates_id'), 'exercise_templates', ['id'], unique=False)
    
    # Create exercise_content table
    op.create_table(
        'exercise_content',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('correct_answers', JSON, nullable=False),
        sa.Column('alternate_answers', JSON, nullable=True),
        sa.Column('difficulty_level', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('tags', ARRAY(sa.String()), nullable=True),
        sa.Column('subject_area', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['exercise_templates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_content_id'), 'exercise_content', ['id'], unique=False)
    op.create_index(op.f('ix_exercise_content_template_id'), 'exercise_content', ['template_id'], unique=False)
    
    # Create media_assets table
    op.create_table(
        'media_assets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('exercise_content_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=False),
        sa.Column('asset_type', sa.String(length=50), nullable=False),
        sa.Column('alt_text', sa.String(length=255), nullable=True),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('license_info', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['exercise_content_id'], ['exercise_content.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_media_assets_id'), 'media_assets', ['id'], unique=False)
    op.create_index(op.f('ix_media_assets_exercise_content_id'), 'media_assets', ['exercise_content_id'], unique=False)
    
    # Create user_responses table
    op.create_table(
        'user_responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exercise_content_id', sa.Integer(), nullable=False),
        sa.Column('response_data', JSON, nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('completion_status', sa.String(length=20), nullable=False, server_default=sa.text("'started'")),
        sa.Column('attempt_number', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['exercise_content_id'], ['exercise_content.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_responses_id'), 'user_responses', ['id'], unique=False)
    op.create_index(op.f('ix_user_responses_user_id'), 'user_responses', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_responses_exercise_content_id'), 'user_responses', ['exercise_content_id'], unique=False)


def downgrade():
    # Drop tables in reverse order of creation
    op.drop_table('user_responses')
    op.drop_table('media_assets')
    op.drop_table('exercise_content')
    op.drop_table('exercise_templates')
    
    # Drop the enum type
    op.execute('DROP TYPE exercise_type') 