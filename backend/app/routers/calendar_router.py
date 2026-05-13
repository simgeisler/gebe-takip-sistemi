from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.planner import CalendarEventCreate, CalendarEventUpdate
from ..services import auth_service, planner_service

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/events")
def list_calendar_events(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.list_calendar_events(user_id, db)


@router.get("/events/{event_id}")
def get_calendar_event(event_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.get_calendar_event(user_id, event_id, db)


@router.post("/events")
def create_calendar_event(payload: CalendarEventCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.create_calendar_event(user_id, payload, db)


@router.put("/events/{event_id}")
def update_calendar_event(
    event_id: int, payload: CalendarEventUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.update_calendar_event(user_id, event_id, payload, db)


@router.delete("/events/{event_id}")
def delete_calendar_event(event_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return planner_service.delete_calendar_event(user_id, event_id, db)
