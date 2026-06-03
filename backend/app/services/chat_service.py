from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.entities import ChatMessage, ChatSession
from ..schemas.chat import ChatMessageCreate, ChatMessageUpdate
from . import assistant_service


def _session_for_user(user_id: int, session_id: int, db: Session) -> ChatSession:
    row = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == user_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı.")
    return row


def _msg_for_user(user_id: int, message_id: int, db: Session) -> ChatMessage:
    row = db.query(ChatMessage).filter(
        ChatMessage.id == message_id,
        ChatMessage.user_id == user_id,
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Mesaj bulunamadı.")
    return row


def _to_api(row: ChatMessage) -> dict:
    return {"id": row.id, "from": row.role, "text": row.text}


def _to_session_api(row: ChatSession) -> dict:
    return {
        "id": row.id,
        "title": row.title,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


def _touch_session(session: ChatSession) -> None:
    session.updated_at = datetime.now(timezone.utc)


def _title_from_message(text: str, max_len: int = 48) -> str:
    t = " ".join((text or "").strip().split())
    if not t:
        return "Yeni Sohbet"
    if len(t) <= max_len:
        return t
    return t[: max_len - 1].rstrip() + "…"


def list_sessions(user_id: int, db: Session) -> list[dict]:
    rows = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc(), ChatSession.id.desc())
        .all()
    )
    return [_to_session_api(s) for s in rows]


def create_session(user_id: int, db: Session) -> dict:
    session = assistant_service.create_session_with_welcome(user_id, db)
    return _to_session_api(session)


def delete_session(user_id: int, session_id: int, db: Session) -> dict:
    session = _session_for_user(user_id, session_id, db)
    db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id,
        ChatMessage.user_id == user_id,
    ).delete()
    db.delete(session)
    db.commit()
    return {"ok": True}


def list_messages(user_id: int, session_id: int, db: Session) -> list[dict]:
    _session_for_user(user_id, session_id, db)
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id, ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id)
        .all()
    )
    return [_to_api(m) for m in rows]


def create_message(user_id: int, payload: ChatMessageCreate, db: Session) -> dict:
    role = payload.from_
    if role not in ("baby", "me"):
        raise HTTPException(status_code=400, detail="from: baby veya me olmalı.")
    if not payload.session_id:
        raise HTTPException(status_code=400, detail="session_id gerekli.")
    _session_for_user(user_id, payload.session_id, db)
    row = ChatMessage(
        user_id=user_id,
        session_id=payload.session_id,
        role=role,
        text=payload.text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_api(row)


def send_assistant_message(user_id: int, session_id: int, text: str, db: Session) -> dict:
    text = (text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Mesaj boş olamaz.")

    session = _session_for_user(user_id, session_id, db)

    user_row = ChatMessage(user_id=user_id, session_id=session_id, role="me", text=text)
    db.add(user_row)
    db.flush()

    if session.title == "Yeni Sohbet":
        session.title = _title_from_message(text)
    _touch_session(session)

    try:
        reply_text = assistant_service.generate_assistant_reply(
            user_id, session_id, text, db
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=502, detail=f"AI yanıtı oluşturulamadı: {exc}")

    assistant_row = ChatMessage(
        user_id=user_id, session_id=session_id, role="baby", text=reply_text
    )
    db.add(assistant_row)
    _touch_session(session)
    db.commit()
    db.refresh(user_row)
    db.refresh(assistant_row)
    db.refresh(session)

    return {
        "user_message": _to_api(user_row),
        "assistant_message": _to_api(assistant_row),
        "session": _to_session_api(session),
    }


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
