from datetime import date, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_user_id
from app.models import User, UserProfile
from app.schemas import ProfileUpsertRequest

router = APIRouter(prefix="", tags=["profile"])


@router.get("/me")
def get_me(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    user = db.get(User, user_id)
    profile = db.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email, "full_name": user.full_name, "profile_complete": profile is not None}


@router.post("/me/profile")
def upsert_profile(payload: ProfileUpsertRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    today = date.today()
    if payload.last_menstrual_period and payload.last_menstrual_period > today:
        raise HTTPException(status_code=400, detail="SAT gelecekte olamaz")
    if payload.expected_due_date and payload.expected_due_date > today + timedelta(days=320):
        raise HTTPException(status_code=400, detail="EDD gecersiz")
    if not payload.last_menstrual_period and not payload.expected_due_date:
        raise HTTPException(status_code=400, detail="SAT veya EDD zorunlu")

    last_menstrual_period = payload.last_menstrual_period
    expected_due_date = payload.expected_due_date
    if last_menstrual_period and not expected_due_date:
        expected_due_date = last_menstrual_period + timedelta(days=280)
    if expected_due_date and not last_menstrual_period:
        last_menstrual_period = expected_due_date - timedelta(days=280)
    if not last_menstrual_period or not expected_due_date:
        raise HTTPException(status_code=400, detail="Tarih donusumu basarisiz")

    user = db.get(User, user_id)
    if not user:
        user = User(id=user_id, email=payload.email, full_name=payload.full_name)
        db.add(user)
    else:
        user.email = payload.email
        user.full_name = payload.full_name

    profile = db.get(UserProfile, user_id)
    if not profile:
        profile = UserProfile(
            user_id=user_id,
            last_menstrual_period=last_menstrual_period,
            expected_due_date=expected_due_date,
            starting_weight=payload.starting_weight,
        )
        db.add(profile)
    else:
        profile.last_menstrual_period = last_menstrual_period
        profile.expected_due_date = expected_due_date
        profile.starting_weight = payload.starting_weight
    db.commit()
    return {"ok": True}


@router.get("/me/profile")
def get_profile(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    user = db.get(User, user_id)
    profile = db.get(UserProfile, user_id)
    if not user or not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "last_menstrual_period": profile.last_menstrual_period.isoformat(),
        "expected_due_date": profile.expected_due_date.isoformat(),
        "starting_weight": profile.starting_weight,
        "updated_at": profile.updated_at.isoformat(),
    }


@router.put("/me/profile")
def update_profile(payload: ProfileUpsertRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    return upsert_profile(payload=payload, user_id=user_id, db=db)


@router.delete("/me/profile")
def delete_profile(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    profile = db.get(UserProfile, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(profile)
    db.commit()
    return {"ok": True}
