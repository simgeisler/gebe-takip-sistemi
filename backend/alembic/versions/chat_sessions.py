"""chat_sessions table; chat_messages.session_id

Revision ID: chat_sessions
Revises: lib_app_owner_seed
Create Date: 2026-06-03

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "chat_sessions"
down_revision: Union[str, Sequence[str], None] = "lib_app_owner_seed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False, server_default="Yeni Sohbet"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_chat_sessions_user_id", "chat_sessions", ["user_id"])

    op.add_column("chat_messages", sa.Column("session_id", sa.Integer(), nullable=True))
    op.create_index("ix_chat_messages_session_id", "chat_messages", ["session_id"])

    conn = op.get_bind()
    rows = conn.execute(
        sa.text("SELECT DISTINCT user_id FROM chat_messages ORDER BY user_id")
    ).fetchall()
    for (user_id,) in rows:
        result = conn.execute(
            sa.text(
                "INSERT INTO chat_sessions (user_id, title) "
                "VALUES (:uid, 'Sohbet 1') RETURNING id"
            ),
            {"uid": user_id},
        )
        session_id = result.scalar()
        conn.execute(
            sa.text("UPDATE chat_messages SET session_id = :sid WHERE user_id = :uid"),
            {"sid": session_id, "uid": user_id},
        )

    op.alter_column("chat_messages", "session_id", nullable=False)
    op.create_foreign_key(
        "fk_chat_messages_session_id",
        "chat_messages",
        "chat_sessions",
        ["session_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_chat_messages_session_id", "chat_messages", type_="foreignkey")
    op.drop_index("ix_chat_messages_session_id", table_name="chat_messages")
    op.drop_column("chat_messages", "session_id")
    op.drop_index("ix_chat_sessions_user_id", table_name="chat_sessions")
    op.drop_table("chat_sessions")
