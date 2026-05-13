"""
Database initialization script
Creates all tables in the database using SQLAlchemy models
"""
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.entities import (
    User,
    Token,
    LibraryArticle,
    LibraryLike,
    ForumThread,
    ForumReply,
    ForumLike,
    ChatMessage,
    CalendarEvent,
    Reminder,
    DailyLog,
    KickSession,
    WeeklyMetadata,
)


def init_db():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
