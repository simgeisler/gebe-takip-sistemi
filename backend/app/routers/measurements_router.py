from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.measurement import MeasurementCreate, MeasurementUpdate
from ..services import auth_service, measurement_api

router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.get("/charts")
def get_health_charts(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Sağlık Takibi — Trend sekmeleri (tansiyon, kilo, şeker)."""
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.get_charts_for_health_page(user_id, db)


@router.post("/")
def create_measurement(payload: MeasurementCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.create_measurement(user_id, payload, db)


@router.get("/")
def list_measurements(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.list_measurements(user_id, db)


@router.get("/{measurement_id}")
def get_measurement(measurement_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.get_measurement(user_id, measurement_id, db)


@router.put("/{measurement_id}")
def update_measurement(
    measurement_id: int, payload: MeasurementUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.update_measurement(user_id, measurement_id, payload, db)


@router.delete("/{measurement_id}")
def delete_measurement(measurement_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return measurement_api.delete_measurement(user_id, measurement_id, db)
