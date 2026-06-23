"""describe your change

Revision ID: 0301715cb29f
Revises: 
Create Date: 2026-06-19 16:30:38.242330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0301715cb29f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with backfill for NULL timestamps."""
    # Backfill NULLs before enforcing NOT NULL
    op.execute("UPDATE bio SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('bio', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.add_column('content', sa.Column('changed_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True))
    op.execute("UPDATE content SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('content', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE followers SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('followers', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE password_changes SET changed_at = NOW() WHERE changed_at IS NULL")
    op.alter_column('password_changes', 'changed_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE post_comments SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('post_comments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE post_likes SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('post_likes', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.add_column('posts', sa.Column('changed_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True))
    op.execute("UPDATE posts SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE reel_comments SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('reel_comments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE reel_likes SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('reel_likes', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.add_column('reels', sa.Column('changed_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True))
    op.execute("UPDATE reels SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('reels', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE saved_categories SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('saved_categories', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE saved_items SET saved_at = NOW() WHERE saved_at IS NULL")
    op.alter_column('saved_items', 'saved_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.execute("UPDATE \"user\" SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column('user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    op.create_unique_constraint(None, 'username', ['user_status'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'username', type_='unique')
    op.alter_column('user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('saved_items', 'saved_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('saved_categories', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('reels', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('reels', 'changed_at')
    op.alter_column('reel_likes', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('reel_comments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('posts', 'changed_at')
    op.alter_column('post_likes', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('post_comments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('password_changes', 'changed_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('followers', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('content', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('content', 'changed_at')
    op.alter_column('bio', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
