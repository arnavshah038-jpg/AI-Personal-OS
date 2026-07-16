"""add memory_type and updated_at

Revision ID: 87f4106d0856
Revises: 311c40784b70
Create Date: 2026-07-09 10:55:27.064714
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "87f4106d0856"
down_revision: Union[str, Sequence[str], None] = "311c40784b70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "memories",
        sa.Column(
            "memory_type",
            sa.String(),
            nullable=False,
            server_default="fact",
        ),
    )

    op.add_column(
        "memories",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.alter_column(
        "memories",
        "memory_type",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "memories",
        "updated_at",
    )

    op.drop_column(
        "memories",
        "memory_type",
    )