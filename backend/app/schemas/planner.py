from datetime import date as Date  # "date" alanı Field ile çakışmasın diye Date kullan
from typing import Literal

from pydantic import BaseModel, Field

EventType = Literal["ilac", "randevu", "etkinlik"]


class CalendarEventCreate(BaseModel):
    # Türkçe tam gün adı (ör. "Cumartesi") 8+ karakter
    day: str = Field(min_length=1, max_length=48)
    date: int = Field(ge=1, le=31)
    event_on: Date | None = None
    title: str = Field(min_length=1)
    time: str = Field(min_length=1)
    type: EventType
    place: str | None = None


class CalendarEventUpdate(BaseModel):
    day: str | None = Field(default=None, min_length=1, max_length=48)
    date: int | None = Field(default=None, ge=1, le=31)
    event_on: Date | None = None
    title: str | None = None
    time: str | None = None
    type: EventType | None = None
    place: str | None = None


class ReminderCreate(BaseModel):
    title: str = Field(min_length=1)
    time: str = Field(min_length=1)
    tag: str = Field(min_length=1)
    color: str = Field(min_length=1)


class ReminderUpdate(BaseModel):
    title: str | None = None
    time: str | None = None
    tag: str | None = None
    color: str | None = None
