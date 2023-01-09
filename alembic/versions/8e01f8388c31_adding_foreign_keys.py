"""Adding Foreign Keys

Revision ID: 8e01f8388c31
Revises: 4ec4b00b2e9d
Create Date: 2023-01-08 23:09:54.678981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e01f8388c31'
down_revision = '4ec4b00b2e9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk", source_table="posts", referent_table="users",
        local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
