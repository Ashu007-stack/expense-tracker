from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a82f4c9d7b31"
down_revision: Union[str, Sequence[str], None] = "19e94f7fe5f4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add mobile number as nullable first.
    op.add_column(
        "users",
        sa.Column(
            "mobile_number",
            sa.String(length=15),
            nullable=True,
        ),
    )

    # Add verification fields.
    op.add_column(
        "users",
        sa.Column(
            "is_mobile_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "is_email_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # Create unique index for mobile numbers.
    op.create_index(
        "ix_users_mobile_number",
        "users",
        ["mobile_number"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_users_mobile_number",
        table_name="users",
    )

    op.drop_column(
        "users",
        "is_active",
    )

    op.drop_column(
        "users",
        "is_email_verified",
    )

    op.drop_column(
        "users",
        "is_mobile_verified",
    )

    op.drop_column(
        "users",
        "mobile_number",
    )