from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.forum import ForumThreadCreate, ForumThreadUpdate
from ..services import auth_service, forum_service

router = APIRouter(prefix="/forum", tags=["forum"])


@router.get("/threads")
def list_forum_threads(db: Session = Depends(get_db)):
    """Forum.tsx — id, cat, title, author, time, replies, votes."""
    return forum_service.list_thread_cards(db)


@router.get("/threads/{thread_id}")
def get_thread(thread_id: int, db: Session = Depends(get_db)):
    return forum_service.get_thread_card(thread_id, db)


@router.post("/threads")
def create_thread(payload: ForumThreadCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_service.create_thread(user_id, payload, db)


@router.put("/threads/{thread_id}")
def update_thread(
    thread_id: int, payload: ForumThreadUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_service.update_thread(user_id, thread_id, payload, db)


@router.delete("/threads/{thread_id}")
def delete_thread(thread_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_service.delete_thread(user_id, thread_id, db)


@router.post("/threads/{thread_id}/vote")
def vote_thread(thread_id: int, db: Session = Depends(get_db)):
    return forum_service.vote_thread(thread_id, db)


@router.post("/threads/{thread_id}/report")
def report_thread(thread_id: int, db: Session = Depends(get_db)):
    return forum_service.report_thread(thread_id, db)
