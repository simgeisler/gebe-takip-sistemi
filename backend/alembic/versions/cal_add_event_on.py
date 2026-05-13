"""calendar_events: tam tarih sütunu event_on

Revision ID: cal_add_event_on
Revises: add_remaining_tables
Create Date: 2026-05-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "cal_add_event_on"
down_revision: Union[str, Sequence[str], None] = "add_remaining_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("calendar_events", sa.Column("event_on", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("calendar_events", "event_on")
