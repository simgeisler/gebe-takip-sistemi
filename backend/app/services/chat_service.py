from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.entities import ChatMessage
from ..schemas.chat import ChatMessageCreate, ChatMessageUpdate


def _msg_for_user(user_id: int, message_id: int, db: Session) -> ChatMessage:
    row = db.query(ChatMessage).filter(
        ChatMessage.id == message_id,
        ChatMessage.user_id == user_id
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Mesaj bulunamadı.")
    return row


def _to_api(row: ChatMessage) -> dict:
    return {"id": row.id, "from": row.role, "text": row.text}


def list_messages(user_id: int, db: Session) -> list[dict]:
    rows = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).order_by(ChatMessage.id).all()
    return [_to_api(m) for m in rows]


def create_message(user_id: int, payload: ChatMessageCreate, db: Session) -> dict:
    role = payload.from_
    if role not in ("baby", "me"):
        raise HTTPException(status_code=400, detail="from: baby veya me olmalı.")
    row = ChatMessage(
        user_id=user_id,
        role=role,
        text=payload.text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_api(row)


def update_message(user_id: int, message_id: int, payload: ChatMessageUpdate, db: Session) -> dict:
    row = _msg_for_user(user_id, message_id, db)
    row.text = payload.text
    db.commit()
    db.refresh(row)
    return _to_api(row)


def delete_message(user_id: int, message_id: int, db: Session) -> dict:
    row = _msg_for_user(user_id, message_id, db)
    db.delete(row)
    db.commit()
    return {"ok": True}
