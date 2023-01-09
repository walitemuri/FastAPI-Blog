"""create posts table

Revision ID: daefc8689a24
Revises: 
Create Date: 2023-01-07 21:52:00.408899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daefc8689a24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("post_id", sa.Integer(), nullable=False,
                    primary_key=True), sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
