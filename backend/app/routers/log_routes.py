from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.dependencies import ensure_profile, get_db
from app.models import DailyLog, UserProfile
from app.schemas import (
    BloodPressureLogRequest,
    BloodPressureLogUpdateRequest,
    WeightLogRequest,
    WeightLogUpdateRequest,
)

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/weight")
def create_weight_log(payload: WeightLogRequest, profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> dict[str, bool]:
    now = datetime.utcnow()
    pregnancy_day_index = (now.date() - profile.last_menstrual_period).days
    db.add(
        DailyLog(
            user_id=profile.user_id,
            date_time=now,
            weight=payload.value,
            note=payload.note,
            pregnancy_day_index=pregnancy_day_index,
        )
    )
    db.commit()
    return {"ok": True}


@router.get("/weight")
def list_weight_logs(profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    rows = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == profile.user_id, DailyLog.weight.isnot(None))
        .order_by(desc(DailyLog.date_time))
        .all()
    )
    return [{"date_time": row.date_time.isoformat(), "value": row.weight, "pregnancy_day_index": row.pregnancy_day_index} for row in rows]


@router.get("/weight/{log_id}")
def get_weight_log(log_id: int, profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> dict[str, Any]:
    row = db.get(DailyLog, log_id)
    if not row or row.user_id != profile.user_id or row.weight is None:
        raise HTTPException(status_code=404, detail="Weight log not found")
    return {
        "id": row.id,
        "date_time": row.date_time.isoformat(),
        "value": row.weight,
        "note": row.note,
        "pregnancy_day_index": row.pregnancy_day_index,
    }


@router.put("/weight/{log_id}")
def update_weight_log(
    log_id: int, payload: WeightLogUpdateRequest, profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)
) -> dict[str, bool]:
    row = db.get(DailyLog, log_id)
    if not row or row.user_id != profile.user_id or row.weight is None:
        raise HTTPException(status_code=404, detail="Weight log not found")
    if payload.value is not None:
        row.weight = payload.value
    if payload.note is not None:
        row.note = payload.note
    db.commit()
    return {"ok": True}


@router.delete("/weight/{log_id}")
def delete_weight_log(log_id: int, profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(DailyLog, log_id)
    if not row or row.user_id != profile.user_id or row.weight is None:
        raise HTTPException(status_code=404, detail="Weight log not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.post("/blood-pressure")
def create_blood_pressure_log(
    payload: BloodPressureLogRequest, profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)
) -> dict[str, bool]:
    now = datetime.utcnow()
    pregnancy_day_index = (now.date() - profile.last_menstrual_period).days
    db.add(
        DailyLog(
            user_id=profile.user_id,
            date_time=now,
            systolic=payload.systolic,
            diastolic=payload.diastolic,
            pulse=payload.pulse,
            note=payload.note,
            pregnancy_day_index=pregnancy_day_index,
        )
    )
    db.commit()
    return {"ok": True}


@router.get("/blood-pressure")
def list_blood_pressure_logs(profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    rows = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == profile.user_id, DailyLog.systolic.isnot(None), DailyLog.diastolic.isnot(None))
        .order_by(desc(DailyLog.date_time))
        .all()
    )
    return [
        {
            "date_time": row.date_time.isoformat(),
            "systolic": row.systolic,
            "diastolic": row.diastolic,
            "pulse": row.pulse,
            "is_risky": (row.systolic or 0) > 140 or (row.diastolic or 0) > 90,
        }
        for row in rows
    ]


@router.get("/blood-pressure/{log_id}")
def get_blood_pressure_log(log_id: int, profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> dict[str, Any]:
    row = db.get(DailyLog, log_id)
    if not row or row.user_id != profile.user_id or row.systolic is None or row.diastolic is None:
        raise HTTPException(status_code=404, detail="Blood pressure log not found")
    return {
        "id": row.id,
        "date_time": row.date_time.isoformat(),
        "systolic": row.systolic,
        "diastolic": row.diastolic,
        "pulse": row.pulse,
        "note": row.note,
        "is_risky": (row.systolic or 0) > 140 or (row.diastolic or 0) > 90,
    }


@router.put("/blood-pressure/{log_id}")
def update_blood_pressure_log(
    log_id: int,
    payload: BloodPressureLogUpdateRequest,
    profile: UserProfile = Depends(ensure_profile),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    row = db.get(DailyLog, log_id)
    if not row or row.user_id != profile.user_id or row.systolic is None or row.diastolic is None:
        raise HTTPException(status_code=404, detail="Blood pressure log not found")
    if payload.systolic is not None:
        row.systolic = payload.systolic
    if payload.diastolic is not None:
        row.diastolic = payload.diastolic
    if payload.pulse is not None:
        row.pulse = payload.pulse
    if payload.note is not None:
        row.note = payload.note
    db.commit()
    return {"ok": True}


@router.delete("/blood-pressure/{log_id}")
def delete_blood_pressure_log(log_id: int, profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(DailyLog, log_id)
    if not row or row.user_id != profile.user_id or row.systolic is None or row.diastolic is None:
        raise HTTPException(status_code=404, detail="Blood pressure log not found")
    db.delete(row)
    db.commit()
    return {"ok": True}
