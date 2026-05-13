from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.entities import CalendarEvent, Reminder
from ..schemas.planner import CalendarEventCreate, CalendarEventUpdate, ReminderCreate, ReminderUpdate


def _event_for_user(user_id: int, event_id: int, db: Session) -> CalendarEvent:
    row = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == user_id
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Takvim etkinliği bulunamadı.")
    return row


def _reminder_for_user(user_id: int, reminder_id: int, db: Session) -> Reminder:
    row = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user_id
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Hatırlatıcı bulunamadı.")
    return row


def list_calendar_events(user_id: int, db: Session) -> list[dict]:
    rows = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.user_id == user_id)
        .order_by(CalendarEvent.event_on, CalendarEvent.date, CalendarEvent.id)
        .all()
    )
    return [_event_public(e) for e in rows]


def get_calendar_event(user_id: int, event_id: int, db: Session) -> dict:
    return _event_public(_event_for_user(user_id, event_id, db))


def create_calendar_event(user_id: int, payload: CalendarEventCreate, db: Session) -> dict:
    row = CalendarEvent(
        user_id=user_id,
        day=payload.day,
        date=payload.date,
        event_on=payload.event_on,
        title=payload.title,
        time=payload.time,
        type=payload.type,
        place=payload.place,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _event_public(row)


def update_calendar_event(user_id: int, event_id: int, payload: CalendarEventUpdate, db: Session) -> dict:
    patch = payload.model_dump(exclude_unset=True)
    if not patch:
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    row = _event_for_user(user_id, event_id, db)
    for key, value in patch.items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return _event_public(row)


def delete_calendar_event(user_id: int, event_id: int, db: Session) -> dict:
    row = _event_for_user(user_id, event_id, db)
    db.delete(row)
    db.commit()
    return {"ok": True}


def _event_public(row: CalendarEvent) -> dict:
    return {
        "id": row.id,
        "day": row.day,
        "date": row.date,
        "event_on": row.event_on.isoformat() if row.event_on else None,
        "title": row.title,
        "time": row.time,
        "type": row.type,
        "place": row.place,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def list_reminders(user_id: int, db: Session) -> list[dict]:
    rows = db.query(Reminder).filter(Reminder.user_id == user_id).order_by(Reminder.id).all()
    return [_reminder_public(r) for r in rows]


def get_reminder(user_id: int, reminder_id: int, db: Session) -> dict:
    return _reminder_public(_reminder_for_user(user_id, reminder_id, db))


def create_reminder(user_id: int, payload: ReminderCreate, db: Session) -> dict:
    row = Reminder(
        user_id=user_id,
        title=payload.title,
        time=payload.time,
        tag=payload.tag,
        color=payload.color,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _reminder_public(row)


def update_reminder(user_id: int, reminder_id: int, payload: ReminderUpdate, db: Session) -> dict:
    patch = payload.model_dump(exclude_unset=True)
    if not patch:
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    row = _reminder_for_user(user_id, reminder_id, db)
    for key, value in patch.items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return _reminder_public(row)


def delete_reminder(user_id: int, reminder_id: int, db: Session) -> dict:
    row = _reminder_for_user(user_id, reminder_id, db)
    db.delete(row)
    db.commit()
    return {"ok": True}


def _reminder_public(row: Reminder) -> dict:
    return {
        "id": row.id,
        "title": row.title,
        "time": row.time,
        "tag": row.tag,
        "color": row.color,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }
