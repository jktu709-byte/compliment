"""add email verified at to users
Revision ID: 73b2fb9f4a9f
Revises: 58737cb8bca2
Create Date: 2026-11-21 15:31:50.406301
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73b2fb9f4a9f'
down_revision: str | Sequence[str] | None = '58737cb8bca2'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add the email confirmation timestamp."""
    op.add_column(
        "users",
        sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Remove the email confirmation timestamp."""
    op.drop_column("users", "email_verified_at")
