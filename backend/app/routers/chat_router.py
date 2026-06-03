from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.chat import AssistantMessageRequest, ChatMessageCreate, ChatMessageUpdate
from ..services import auth_service, chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/sessions")
def list_chat_sessions(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.list_sessions(user_id, db)


@router.post("/sessions")
def post_chat_session(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Yeni sohbet + karşılama mesajı."""
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.create_session(user_id, db)


@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.delete_session(user_id, session_id, db)


@router.get("/sessions/{session_id}/messages")
def list_session_messages(
    session_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.list_messages(user_id, session_id, db)


@router.post("/sessions/{session_id}/assistant")
def post_session_assistant_message(
    session_id: int,
    payload: AssistantMessageRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.send_assistant_message(user_id, session_id, payload.text, db)


@router.post("/messages")
def post_chat_message(
    payload: ChatMessageCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.create_message(user_id, payload, db)


@router.put("/messages/{message_id}")
def put_chat_message(
    message_id: int,
    payload: ChatMessageUpdate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.update_message(user_id, message_id, payload, db)


@router.delete("/messages/{message_id}")
def delete_chat_message(
    message_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.delete_message(user_id, message_id, db)
