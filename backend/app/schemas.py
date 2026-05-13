from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ProfileUpsertRequest(BaseModel):
    full_name: str = Field(min_length=2)
    email: EmailStr
    last_menstrual_period: Optional[date] = None
    expected_due_date: Optional[date] = None
    starting_weight: float = Field(gt=20, lt=300)


class WeightLogRequest(BaseModel):
    value: float = Field(gt=20, lt=300)
    note: Optional[str] = None


class WeightLogUpdateRequest(BaseModel):
    value: Optional[float] = Field(default=None, gt=20, lt=300)
    note: Optional[str] = None


class BloodPressureLogRequest(BaseModel):
    systolic: int = Field(gt=50, lt=260)
    diastolic: int = Field(gt=30, lt=180)
    pulse: Optional[int] = Field(default=None, gt=20, lt=240)
    note: Optional[str] = None


class BloodPressureLogUpdateRequest(BaseModel):
    systolic: Optional[int] = Field(default=None, gt=50, lt=260)
    diastolic: Optional[int] = Field(default=None, gt=30, lt=180)
    pulse: Optional[int] = Field(default=None, gt=20, lt=240)
    note: Optional[str] = None


class KickSessionRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    total_count: int = Field(ge=0)


class KickSessionUpdateRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_count: Optional[int] = Field(default=None, ge=0)


class ContractionEventRequest(BaseModel):
    start_time: datetime
    end_time: datetime


class ContractionEventUpdateRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class CreateThreadRequest(BaseModel):
    category_id: int
    title: str = Field(min_length=3)
    body: str = Field(min_length=3)


class UpdateThreadRequest(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = Field(default=None, min_length=3)
    body: Optional[str] = Field(default=None, min_length=3)


class CreateReplyRequest(BaseModel):
    thread_id: int
    body: str = Field(min_length=1)


class UpdateReplyRequest(BaseModel):
    body: Optional[str] = Field(default=None, min_length=1)


class ReportThreadRequest(BaseModel):
    thread_id: int
    reason: str = Field(min_length=3)


class UpdateLibraryItemRequest(BaseModel):
    category: Optional[str] = Field(default=None, min_length=2)
    title: Optional[str] = Field(default=None, min_length=2)
    content: Optional[str] = Field(default=None, min_length=2)


class UpdateFCMTokenRequest(BaseModel):
    token: str = Field(min_length=16)


class RegisterFCMTokenRequest(BaseModel):
    token: str = Field(min_length=16)
