from datetime import date, datetime
from typing import Any, Optional

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    __tablename__ = "user_profile"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    last_menstrual_period: Mapped[date] = mapped_column(Date)
    expected_due_date: Mapped[date] = mapped_column(Date)
    starting_weight: Mapped[float] = mapped_column(Float)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DailyLog(Base):
    __tablename__ = "daily_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, index=True, default=datetime.utcnow)
    pregnancy_day_index: Mapped[Optional[int]] = mapped_column(Integer)
    weight: Mapped[Optional[float]] = mapped_column(Float)
    systolic: Mapped[Optional[int]] = mapped_column(Integer)
    diastolic: Mapped[Optional[int]] = mapped_column(Integer)
    pulse: Mapped[Optional[int]] = mapped_column(Integer)
    water_intake: Mapped[Optional[float]] = mapped_column(Float)
    note: Mapped[Optional[str]] = mapped_column(Text)


class WeeklyMetadata(Base):
    __tablename__ = "weekly_metadata"
    week_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    fetus_size_cm: Mapped[float] = mapped_column(Float)
    fetus_weight_gr: Mapped[float] = mapped_column(Float)
    development_milestones_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    symptom_analysis_text: Mapped[str] = mapped_column(Text)
    comparison_object_name: Mapped[str] = mapped_column(String(128))
    image_url: Mapped[str] = mapped_column(String(512))


class CounterLog(Base):
    __tablename__ = "counter_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[str] = mapped_column(String(32))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    duration_seconds: Mapped[int] = mapped_column(Integer)
    frequency_seconds: Mapped[Optional[int]] = mapped_column(Integer)
    meta_json: Mapped[dict[str, Any]] = mapped_column(JSON, default={})


class FCMToken(Base):
    __tablename__ = "fcm_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    token: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LibraryItem(Base):
    __tablename__ = "library_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(128), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)


class ForumCategory(Base):
    __tablename__ = "forum_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)


class ForumThread(Base):
    __tablename__ = "forum_threads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("forum_categories.id"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ForumReply(Base):
    __tablename__ = "forum_replies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("forum_threads.id"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ForumReport(Base):
    __tablename__ = "forum_reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("forum_threads.id"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
