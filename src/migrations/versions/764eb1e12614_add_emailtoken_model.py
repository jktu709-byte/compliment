"""add emailtoken model

Revision ID: 764eb1e12614
Revises: 73b2fb9f4a9f
Create Date: 2026-11-21 16:24:10.108669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '764eb1e12614'
down_revision: Union[str, Sequence[str], None] = '73b2fb9f4a9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the email verification token table."""
    op.create_table(
        "email_verification_token",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("token_hash"),
    )


def downgrade() -> None:
    """Remove the email verification token table."""
    op.drop_table("email_verification_token")
