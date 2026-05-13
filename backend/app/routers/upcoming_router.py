from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.planner import ReminderCreate, ReminderUpdate
from ..services import auth_service, planner_service

router = APIRouter(prefix="/upcoming", tags=["upcoming"])


@router.get("/")
def list_upcoming(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.list_reminders(user_id, db)


@router.get("/{item_id}")
def get_upcoming_item(item_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.get_reminder(user_id, item_id, db)


@router.post("/")
def create_upcoming_item(payload: ReminderCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.create_reminder(user_id, payload, db)


@router.put("/{item_id}")
def update_upcoming_item(
    item_id: int, payload: ReminderUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.update_reminder(user_id, item_id, payload, db)


@router.delete("/{item_id}")
def delete_upcoming_item(item_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.delete_reminder(user_id, item_id, db)
