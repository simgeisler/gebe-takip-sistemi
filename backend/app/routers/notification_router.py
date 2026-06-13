from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.notification import NotificationListResponse, NotificationResponse, UnreadCountResponse
from ..services import auth_service
from ..services import notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=NotificationListResponse)
def list_notifications(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return notification_service.list_notifications(user_id, db)


@router.get("/unread-count", response_model=UnreadCountResponse)
def unread_count(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return notification_service.get_unread_count(user_id, db)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return notification_service.mark_as_read(user_id, notification_id, db)


@router.patch("/read-all")
def mark_all_notifications_read(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return notification_service.mark_all_as_read(user_id, db)
