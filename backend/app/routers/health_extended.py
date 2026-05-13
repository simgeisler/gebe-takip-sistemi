from typing import Optional

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.health_extended import MeasurementSummaryResponse, MeasurementTrendResponse
from ..services import auth_service, measurement_api

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/measurements/summary", response_model=MeasurementSummaryResponse)
def get_measurements_summary(
    limit: int = Query(3, description="Kaç adet son ölçüm getirilecek"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Son N ölçümün özetini getir"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.get_measurements_summary(user_id, db, limit)


@router.get("/measurements/trends/{trend_type}", response_model=MeasurementTrendResponse)
def get_measurements_trends(
    trend_type: str,
    limit: int = Query(6, description="Kaç adet ölçüm grafiğe dahil edilecek"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Ölçüm trendlerini getir - tansiyon, kilo, şeker"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.get_measurements_trends(user_id, db, trend_type, limit)


@router.get("/measurements/trends", response_model=MeasurementTrendResponse)
def get_all_trends(
    limit: int = Query(6, description="Kaç adet ölçüm grafiğe dahil edilecek"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Tüm trend türlerini getir"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.get_all_trends(user_id, db, limit)
