from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('otp_created_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('user', 'otp_created_at')