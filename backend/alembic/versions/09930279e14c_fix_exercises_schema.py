"""Fix exercises schema"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision = "09930279e14c"
down_revision = "d877fcfee79b"
branch_labels = None
depends_on = None

def upgrade():
    # Remove max_length if it exists
    with op.batch_alter_table("exercises") as batch_op:
        batch_op.drop_column("max_length", if_exists=True)

def downgrade():
    # Re-add max_length if needed for rollback
    with op.batch_alter_table("exercises") as batch_op:
        batch_op.add_column(sa.Column("max_length", sa.Integer(), nullable=True))
