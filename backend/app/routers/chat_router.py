from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.chat import ChatMessageCreate, ChatMessageUpdate
from ..services import auth_service, chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/messages")
def list_chat_messages(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """BabyChat.tsx — { id, from, text }."""
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.list_messages(user_id, db)


@router.post("/messages")
def post_chat_message(payload: ChatMessageCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.create_message(user_id, payload, db)


@router.put("/messages/{message_id}")
def put_chat_message(
    message_id: int, payload: ChatMessageUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.update_message(user_id, message_id, payload, db)


@router.delete("/messages/{message_id}")
def delete_chat_message(message_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return chat_service.delete_message(user_id, message_id, db)
