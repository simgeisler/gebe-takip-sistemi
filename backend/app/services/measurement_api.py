"""Ölçümler: HealthTracking.tsx alan adları <-> dahili daily_logs."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..schemas.health import DailyLogRequest, DailyLogUpdateRequest
from ..schemas.measurement import MeasurementCreate, MeasurementUpdate
from . import health_service


def _iso_or_str(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _row_to_measurement(row: dict) -> dict:
    return {
        "id": row["id"],
        "date": _iso_or_str(row.get("date")),
        "weight": row.get("weight"),
        "water_liters": row.get("water_liters"),
        "systolic": row.get("systolic"),
        "diastolic": row.get("diastolic"),
        "blood_glucose": row.get("blood_glucose"),
        "pulse": row.get("pulse"),
        "notes": row.get("notes"),
        "created_at": _iso_or_str(row.get("created_at")),
    }


def _create_to_daily(payload: MeasurementCreate) -> DailyLogRequest:
    return DailyLogRequest(
        date=payload.date,
        weight=payload.weight,
        water_liters=payload.water_liters,
        systolic=payload.systolic,
        diastolic=payload.diastolic,
        blood_glucose=payload.blood_glucose,
        pulse=payload.pulse,
        notes=payload.notes,
    )


def _update_to_daily(payload: MeasurementUpdate) -> DailyLogUpdateRequest:
    data = payload.model_dump(exclude_unset=True)
    patch = {}
    if "weight" in data:
        patch["weight"] = data["weight"]
    if "water_liters" in data:
        patch["water_liters"] = data["water_liters"]
    if "systolic" in data:
        patch["systolic"] = data["systolic"]
    if "diastolic" in data:
        patch["diastolic"] = data["diastolic"]
    if "blood_glucose" in data:
        patch["blood_glucose"] = data["blood_glucose"]
    if "pulse" in data:
        patch["pulse"] = data["pulse"]
    if "notes" in data:
        patch["notes"] = data["notes"]
    if "date" in data:
        patch["date"] = data["date"]
    return DailyLogUpdateRequest(**patch)


def create_measurement(user_id: int, payload: MeasurementCreate, db: Session) -> dict:
    row = health_service.create_daily_log(user_id, _create_to_daily(payload), db)
    return _row_to_measurement(row)


def list_measurements(user_id: int, db: Session) -> list[dict]:
    return [_row_to_measurement(r) for r in health_service.list_daily_logs(user_id, db)]


def get_measurement(user_id: int, measurement_id: int, db: Session) -> dict:
    row = health_service.get_daily_log(user_id, measurement_id, db)
    return _row_to_measurement(row)


def update_measurement(user_id: int, measurement_id: int, payload: MeasurementUpdate, db: Session) -> dict:
    if not payload.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    daily_upd = _update_to_daily(payload)
    row = health_service.update_daily_log(user_id, measurement_id, daily_upd, db)
    return _row_to_measurement(row)


def delete_measurement(user_id: int, measurement_id: int, db: Session) -> dict:
    return health_service.delete_daily_log(user_id, measurement_id, db)


def get_charts_for_health_page(user_id: int, db: Session) -> dict:
    """Trend sekmeleri: tansiyon, kilo, şeker — HealthTracking LineChart dataKey uyumu."""
    raw = health_service.get_health_trends(user_id, db)
    fc = raw.get("frontend_charts") or {}
    tansiyon = fc.get("tansiyon") or []
    kilo = fc.get("kilo") or []
    seker_raw = fc.get("seker") or []
    seker = [{"d": x["d"], "mg_dl": x.get("mg_dl")} for x in seker_raw]
    return {"tansiyon": tansiyon, "kilo": kilo, "seker": seker}


def get_measurements_summary(user_id: int, db: Session, limit: int = 3) -> dict:
    """Son N ölçümün özetini getir (en yeni önce)."""
    measurements = list_measurements(user_id, db)
    recent_measurements = measurements[:limit]
    return {
        "summaries": recent_measurements,
        "total_count": len(measurements),
    }


def _trend_points_chronological(measurements: list[dict], limit: int) -> list[dict]:
    """Son kaydedilen `limit` satırı al; grafikte sol=eski, sağ=yeni için (tarih, id) artan sırala."""
    window = measurements[:limit]
    return sorted(
        window,
        key=lambda m: ((m.get("date") or ""), (m.get("id") or 0)),
    )


def get_measurements_trends(user_id: int, db: Session, trend_type: str, limit: int = 6) -> dict:
    """Son N ölçüm — grafik: X ekseninde eski solda, yeni sağda."""
    measurements = list_measurements(user_id, db)
    recent_chrono = _trend_points_chronological(measurements, limit)
    trend_data = []
    for measurement in recent_chrono:
        trend_item = {
            "id": measurement.get("id"),
            "date": measurement["date"],
            "weight": measurement.get("weight"),
            "systolic": measurement.get("systolic"),
            "diastolic": measurement.get("diastolic"),
            "blood_glucose": measurement.get("blood_glucose"),
        }
        trend_data.append(trend_item)
    return {
        "trend_type": trend_type,
        "data": trend_data,
    }


def get_all_trends(user_id: int, db: Session, limit: int = 6) -> dict:
    """Tüm trend türlerini getir"""
    measurements = list_measurements(user_id, db)
    recent_chrono = _trend_points_chronological(measurements, limit)
    trend_data = []
    for measurement in recent_chrono:
        trend_item = {
            "id": measurement.get("id"),
            "date": measurement["date"],
            "weight": measurement.get("weight"),
            "systolic": measurement.get("systolic"),
            "diastolic": measurement.get("diastolic"),
            "blood_glucose": measurement.get("blood_glucose"),
        }
        trend_data.append(trend_item)
    return {
        "trend_type": "all",
        "data": trend_data,
    }
