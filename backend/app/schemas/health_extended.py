from typing import Optional, List
from pydantic import BaseModel


class MeasurementSummary(BaseModel):
    id: int
    date: str
    weight: Optional[float] = None
    water_liters: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    blood_glucose: Optional[float] = None
    pulse: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None


class MeasurementTrend(BaseModel):
    id: Optional[int] = None
    date: str
    weight: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    blood_glucose: Optional[float] = None


class MeasurementTrendResponse(BaseModel):
    trend_type: str
    data: List[MeasurementTrend]


class MeasurementSummaryResponse(BaseModel):
    summaries: List[MeasurementSummary]
    total_count: int
