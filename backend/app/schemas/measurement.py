"""Sağlık Takibi (HealthTracking.tsx) form alanlarıyla aynı isimler."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class MeasurementCreate(BaseModel):
    date: date
    weight: Optional[float] = None
    water_liters: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    blood_glucose: Optional[float] = None
    pulse: Optional[int] = None
    notes: Optional[str] = None


class MeasurementUpdate(BaseModel):
    date: Optional[date] = None
    weight: Optional[float] = None
    water_liters: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    blood_glucose: Optional[float] = None
    pulse: Optional[int] = None
    notes: Optional[str] = None
