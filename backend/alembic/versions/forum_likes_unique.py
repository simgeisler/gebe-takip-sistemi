"""unique constraint on forum_likes (question_id, user_id)

Revision ID: forum_likes_unique
Revises: notifications_table
Create Date: 2026-06-13

"""
from typing import Sequence, Union

from alembic import op


revision: str = "forum_likes_unique"
down_revision: Union[str, Sequence[str], None] = "notifications_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_forum_likes_question_user",
        "forum_likes",
        ["question_id", "user_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_forum_likes_question_user", "forum_likes", type_="unique")
