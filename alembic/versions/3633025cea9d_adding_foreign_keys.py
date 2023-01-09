"""Adding Foreign Keys

Revision ID: 3633025cea9d
Revises: 8e01f8388c31
Create Date: 2023-01-08 23:21:55.141001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3633025cea9d'
down_revision = '8e01f8388c31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(),
                  nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text("NOW()")),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
