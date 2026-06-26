"""creator ownership

Revision ID: xxxx_add_creator_owner
Revises: 35eebfd58202
Create Date: 2026-06-18
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# =========================================================
# ALEMBIC METADATA
# =========================================================

revision: str = "xxxx_add_creator_owner"
down_revision: Union[str, None] = "35eebfd58202"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# =========================================================
# UPGRADE
# =========================================================

def upgrade() -> None:
    op.add_column(
        "creators",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_creators_user_id",
        "creators",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_creators_user_id",
        "creators",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # If this is a fresh database with no creator rows,
    # make the column match the SQLAlchemy model.
    op.alter_column(
        "creators",
        "user_id",
        nullable=False,
    )


# =========================================================
# DOWNGRADE
# =========================================================

def downgrade() -> None:
    op.drop_constraint(
        "fk_creators_user_id",
        "creators",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_creators_user_id",
        table_name="creators",
    )

    op.drop_column(
        "creators",
        "user_id",
    )