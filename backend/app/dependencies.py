import os
from datetime import date, timedelta
from typing import Any, Generator, Optional

import firebase_admin
from fastapi import Depends, Header, HTTPException
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import UserProfile


def init_firebase() -> None:
    if firebase_admin._apps:
        return
    cred_path = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if cred_path and os.path.exists(cred_path):
        firebase_admin.initialize_app(credentials.Certificate(cred_path))
        return
    firebase_admin.initialize_app()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_id(authorization: Optional[str] = Header(default=None, alias="Authorization")) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        decoded = auth.verify_id_token(token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc
    user_id = decoded.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token uid missing")
    return user_id


def ensure_profile(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> UserProfile:
    profile = db.get(UserProfile, user_id)
    if not profile:
        raise HTTPException(status_code=400, detail="Onboarding gerekli")
    return profile


def compute_status(profile: UserProfile) -> dict[str, Any]:
    today = date.today()
    pregnancy_days = (today - profile.last_menstrual_period).days
    week = max(0, pregnancy_days // 7)
    day = max(0, pregnancy_days % 7)
    trimester = 1 if week <= 13 else 2 if week <= 26 else 3
    due_in_days = (profile.expected_due_date - today).days
    week_label = "40+ hafta" if week > 40 else f"{week} hafta {day} gun"
    is_due_far_future = profile.expected_due_date > today + timedelta(days=320)
    return {
        "week": week,
        "day": day,
        "trimester": trimester,
        "pregnancy_day_index": pregnancy_days,
        "days_until_due": due_in_days,
        "week_label": week_label,
        "is_due_far_future": is_due_far_future,
    }
