"""weekly_metadata: tablo kontrolü + 1-42 hafta bebek boy/kilo seed

Revision ID: weekly_metadata_baby_seed
Revises: chat_sessions
Create Date: 2026-06-03

"""
from typing import Sequence, Union

from alembic import op

from app.data.weekly_baby_reference import (
    ensure_weekly_metadata_table,
    upsert_weekly_baby_metadata_connection,
)

revision: str = "weekly_metadata_baby_seed"
down_revision: Union[str, Sequence[str], None] = "chat_sessions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    ensure_weekly_metadata_table(op)
    conn = op.get_bind()
    upsert_weekly_baby_metadata_connection(conn)


def downgrade() -> None:
    import sqlalchemy as sa

    conn = op.get_bind()
    conn.execute(
        sa.text(
            "UPDATE weekly_metadata SET baby_weight = NULL, baby_length = NULL, baby_size = NULL"
        )
    )
