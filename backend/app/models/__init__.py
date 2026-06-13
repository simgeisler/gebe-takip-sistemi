from .entities import (
    CalendarEvent,
    ChatMessage,
    ChatSession,
    DailyLog,
    ForumLike,
    ForumReply,
    ForumThread,
    KickSession,
    LibraryArticle,
    LibraryLike,
    Notification,
    Reminder,
    Token,
    User,
    WeeklyMetadata,
)

# Legacy SQLAlchemy 2.0 models (routes not mounted in app.main)
from app.legacy_models import (  # noqa: F401
    Base as LegacyBase,
    CounterLog,
    FCMToken,
    ForumCategory,
    ForumReport,
    ForumThread as LegacyForumThread,
    ForumReply as LegacyForumReply,
    LibraryItem,
    User as LegacyUser,
    UserProfile,
    WeeklyMetadata as LegacyWeeklyMetadata,
)
