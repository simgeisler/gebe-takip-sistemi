from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.forum_extended import (
    ForumLikeCreate,
    ForumLikeResponse,
    ForumQuestionCreate,
    ForumQuestionList,
    ForumQuestionResponse,
    ForumQuestionUpdate,
    ForumReplyCreate,
    ForumReplyResponse,
)
from ..services import auth_service
from ..services import forum_service as forum_api

router = APIRouter(prefix="/forum", tags=["forum"])


@router.get("", response_model=List[ForumQuestionList])
def list_forum_posts(category: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """Forum gönderilerini listele - kategori filtreleme ile"""
    user_id = 0
    return forum_api.list_questions(user_id, db, category)


@router.post("", response_model=ForumQuestionResponse)
def create_forum_post(payload: ForumQuestionCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Yeni forum gönderisi oluştur"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_api.create_question(user_id, payload, db)


@router.post("/questions", response_model=ForumQuestionResponse)
def create_forum_question(payload: ForumQuestionCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Yeni forum sorusu oluştur"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_api.create_question(user_id, payload, db)


@router.get("/questions", response_model=List[ForumQuestionList])
def list_forum_questions(category: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """Forum sorularını listele - kategori filtreleme ile"""
    user_id = 0
    return forum_api.list_questions(user_id, db, category)


@router.get("/questions/{question_id}", response_model=ForumQuestionResponse)
def get_forum_question(question_id: int, db: Session = Depends(get_db)):
    """Forum sorusu detayını getir"""
    user_id = 0
    return forum_api.get_question(user_id, question_id, db)


@router.put("/questions/{question_id}", response_model=ForumQuestionResponse)
def update_forum_question(
    question_id: int, payload: ForumQuestionUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """Forum sorusunu güncelle"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_api.update_question(user_id, question_id, payload, db)


@router.delete("/questions/{question_id}")
def delete_forum_question(question_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Forum sorusunu sil"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_api.delete_question(user_id, question_id, db)


@router.post("/questions/{question_id}/replies", response_model=ForumReplyResponse)
def create_forum_reply(
    question_id: int, payload: ForumReplyCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """Forum yanıtını oluştur"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_api.create_reply(user_id, question_id, payload, db)


@router.get("/questions/{question_id}/replies", response_model=List[ForumReplyResponse])
def list_forum_replies(question_id: int, db: Session = Depends(get_db)):
    """Forum yanıtlarını listele (herkese açık okuma)"""
    return forum_api.list_replies(0, question_id, db)


@router.post("/questions/{question_id}/likes", response_model=ForumLikeResponse)
def create_forum_like(question_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Forum sorusunu beğen"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_api.create_like(user_id, question_id, db)


@router.delete("/questions/{question_id}/likes")
def delete_forum_like(question_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Forum sorusu beğenisini kaldır"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return forum_api.delete_like(user_id, question_id, db)


@router.get("/questions/{question_id}/likes", response_model=List[ForumLikeResponse])
def list_forum_likes(question_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Giriş yapmış kullanıcı için yalnızca kendi beğenisi (UI: beğenildi mi). Token yoksa boş liste."""
    all_likes = forum_api.list_likes(0, question_id, db)
    if not authorization or not authorization.startswith("Bearer "):
        return []
    try:
        uid = auth_service.resolve_token(authorization, db=db)
    except HTTPException:
        return []
    return [like for like in all_likes if like.get("user_id") == uid]
