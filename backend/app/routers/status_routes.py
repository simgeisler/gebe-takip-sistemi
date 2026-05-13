from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.dependencies import compute_status, ensure_profile, get_db
from app.models import DailyLog, UserProfile

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/current")
def get_current_status(profile: UserProfile = Depends(ensure_profile), db: Session = Depends(get_db)) -> dict[str, Any]:
    latest_weight = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == profile.user_id, DailyLog.weight.isnot(None))
        .order_by(desc(DailyLog.date_time))
        .first()
    )
    latest_blood_pressure = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == profile.user_id, DailyLog.systolic.isnot(None), DailyLog.diastolic.isnot(None))
        .order_by(desc(DailyLog.date_time))
        .first()
    )
    status = compute_status(profile)
    return {
        "week": status["week"],
        "day": status["day"],
        "trimester": status["trimester"],
        "pregnancy_day_index": status["pregnancy_day_index"],
        "days_until_due": status["days_until_due"],
        "week_label": status["week_label"],
        "latest_weight": latest_weight.weight if latest_weight else None,
        "latest_blood_pressure": {
            "systolic": latest_blood_pressure.systolic,
            "diastolic": latest_blood_pressure.diastolic,
            "pulse": latest_blood_pressure.pulse,
        }
        if latest_blood_pressure
        else None,
    }
