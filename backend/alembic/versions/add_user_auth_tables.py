"""Add user authentication tables

Revision ID: 4a1c5e9b8e7d
Revises: d877fcfee79b
Create Date: 2023-07-10 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '4a1c5e9b8e7d'
down_revision = 'd877fcfee79b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_role enum type
    op.execute("CREATE TYPE user_role AS ENUM ('admin', 'teacher', 'student')")
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(100), nullable=False, index=True, unique=True),
        sa.Column('email', sa.String(100), nullable=False, index=True, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(100), nullable=True),
        sa.Column('role', sa.Enum('admin', 'teacher', 'student', name='user_role'), nullable=False, default='student'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add foreign key to user_responses table
    op.add_column('user_responses', sa.Column('attempt_number', sa.Integer(), nullable=False, server_default='1'))
    
    # Add completed_at column to user_responses
    op.add_column('user_responses', sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True))
    
    # Create index on user_id in user_responses
    op.create_index('ix_user_responses_user_id', 'user_responses', ['user_id'])


def downgrade() -> None:
    # Remove index on user_id in user_responses
    op.drop_index('ix_user_responses_user_id', 'user_responses')
    
    # Remove completed_at column from user_responses
    op.drop_column('user_responses', 'completed_at')
    
    # Remove attempt_number column from user_responses
    op.drop_column('user_responses', 'attempt_number')
    
    # Drop users table
    op.drop_table('users')
    
    # Drop user_role enum type
    op.execute('DROP TYPE user_role') 