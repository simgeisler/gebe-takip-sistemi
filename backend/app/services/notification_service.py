from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.time_format import format_relative_time_tr
from app.models.entities import Notification, User


def _serialize_notification(notification: Notification, actor: User | None) -> dict:
    actor_name = (actor.name if actor else "").strip() or "Kullanıcı"
    return {
        "id": notification.id,
        "type": notification.type,
        "actor_name": actor_name,
        "question_id": notification.question_id,
        "question_title": notification.question_title,
        "is_read": notification.is_read,
        "time_label": format_relative_time_tr(notification.created_at),
        "created_at": notification.created_at.isoformat() if notification.created_at else None,
    }


def create_notification(
    *,
    recipient_id: int,
    actor_id: int,
    notification_type: str,
    question_id: int,
    question_title: str,
    db: Session,
) -> None:
    if recipient_id == actor_id:
        return

    notification = Notification(
        user_id=recipient_id,
        actor_id=actor_id,
        type=notification_type,
        question_id=question_id,
        question_title=question_title,
        is_read=False,
    )
    db.add(notification)
    db.commit()


def list_notifications(user_id: int, db: Session) -> dict:
    rows = (
        db.query(Notification, User)
        .outerjoin(User, User.id == Notification.actor_id)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc(), Notification.id.desc())
        .all()
    )
    notifications = [_serialize_notification(n, actor) for n, actor in rows]
    unread_count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read.is_(False),
    ).count()
    return {"notifications": notifications, "unread_count": unread_count}


def get_unread_count(user_id: int, db: Session) -> dict:
    unread_count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read.is_(False),
    ).count()
    return {"unread_count": unread_count}


def mark_as_read(user_id: int, notification_id: int, db: Session) -> dict:
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Bildirim bulunamadı.")

    if not notification.is_read:
        notification.is_read = True
        db.commit()
        db.refresh(notification)

    actor = db.query(User).filter(User.id == notification.actor_id).first()
    return _serialize_notification(notification, actor)


def mark_all_as_read(user_id: int, db: Session) -> dict:
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read.is_(False),
    ).update({"is_read": True})
    db.commit()
    return {"ok": True, "unread_count": 0}
