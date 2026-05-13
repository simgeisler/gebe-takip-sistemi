from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class DailyLogRequest(BaseModel):
    date: date
    weight: Optional[float] = None
    water_liters: Optional[float] = None
    blood_glucose: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    pulse: Optional[int] = None
    notes: Optional[str] = None


class DailyLogUpdateRequest(BaseModel):
    date: Optional[date] = None
    weight: Optional[float] = None
    water_liters: Optional[float] = None
    blood_glucose: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    pulse: Optional[int] = None
    notes: Optional[str] = None


class KickSessionRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    kick_count: int = Field(ge=0)


class KickSessionUpdateRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    kick_count: Optional[int] = Field(default=None, ge=0)


class ContractionAnalysisRequest(BaseModel):
    starts: list[datetime]
    ends: list[datetime]
