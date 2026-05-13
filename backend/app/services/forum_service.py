from datetime import datetime, timezone
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.entities import User, ForumThread, ForumReply, ForumLike
from ..schemas.forum import ForumThreadCreate, ForumThreadUpdate
from ..schemas.forum_extended import ForumQuestionCreate, ForumQuestionUpdate, ForumReplyCreate, ForumLikeCreate


def _get_thread(thread_id: int, db: Session) -> ForumThread:
    thread = db.query(ForumThread).filter(ForumThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Konu bulunamadı.")
    return thread


def _thread_author_label(t: ForumThread) -> str:
    return (t.author_display or "").strip() or "Kullanıcı"


def _thread_time_label(t: ForumThread) -> str:
    return (t.time_label or "").strip() or ""


def _thread_detail_text(t: ForumThread) -> str:
    return (t.detail or t.body or "") or ""


def thread_to_card(t: ForumThread) -> dict:
    """Forum.tsx satır şekli + id (CRUD için)."""
    return {
        "id": t.id,
        "cat": t.category,
        "title": t.title,
        "author": t.author_display or "Kullanıcı",
        "time": t.time_label or "",
        "replies": t.replies or 0,
        "votes": t.votes or 0,
    }


def thread_to_detail(t: ForumThread) -> dict:
    return {
        **thread_to_card(t),
        "body": t.body or "",
        "reports": t.reports or 0,
        "user_id": t.user_id,
    }


def create_thread(user_id: int, payload: ForumThreadCreate, db: Session) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    author = user.name.split()[0] if user else "Kullanıcı"
    thread = ForumThread(
        user_id=user_id,
        category=payload.cat,
        title=payload.title,
        body=payload.body,
        author_display=author,
        time_label="Az önce",
        replies=0,
        votes=0,
        reports=0,
    )
    db.add(thread)
    db.commit()
    db.refresh(thread)
    return thread_to_card(thread)


def list_thread_cards(db: Session) -> list[dict]:
    threads = db.query(ForumThread).order_by(ForumThread.id.desc()).all()
    return [thread_to_card(t) for t in threads]


def get_thread_card(thread_id: int, db: Session) -> dict:
    return thread_to_detail(_get_thread(thread_id, db))


def update_thread(user_id: int, thread_id: int, payload: ForumThreadUpdate, db: Session) -> dict:
    patch = payload.model_dump(exclude_unset=True)
    if "cat" in patch:
        patch["category"] = patch.pop("cat")
    if not patch:
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    thread = _get_thread(thread_id, db)
    if thread.user_id != user_id:
        raise HTTPException(status_code=403, detail="Sadece kendi konunuzu güncelleyebilirsiniz.")
    for key, value in patch.items():
        setattr(thread, key, value)
    db.commit()
    db.refresh(thread)
    return thread_to_card(thread)


def delete_thread(user_id: int, thread_id: int, db: Session) -> dict:
    thread = _get_thread(thread_id, db)
    if thread.user_id != user_id:
        raise HTTPException(status_code=403, detail="Sadece kendi konunuzu silebilirsiniz.")
    db.delete(thread)
    db.commit()
    return {"ok": True}


def vote_thread(thread_id: int, db: Session) -> dict:
    thread = _get_thread(thread_id, db)
    thread.votes = (thread.votes or 0) + 1
    db.commit()
    db.refresh(thread)
    return thread_to_card(thread)


def report_thread(thread_id: int, db: Session) -> dict:
    thread = _get_thread(thread_id, db)
    thread.reports = (thread.reports or 0) + 1
    db.commit()
    return {"ok": True, "reports": thread.reports}


# Yeni CRUD fonksiyonları
def create_question(user_id: int, payload: ForumQuestionCreate, db: Session) -> dict:
    """Yeni forum sorusu oluştur"""
    user = db.query(User).filter(User.id == user_id).first()
    author = user.name.split()[0] if user else "Kullanıcı"
    question = ForumThread(
        user_id=user_id,
        title=payload.title,
        category=payload.category,
        detail=payload.detail,
        author_display=author,
        time_label="Az önce",
        replies=0,
        votes=0,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return {
        "id": question.id,
        "user_id": question.user_id,
        "title": question.title,
        "category": question.category,
        "detail": _thread_detail_text(question),
        "author": _thread_author_label(question),
        "time": _thread_time_label(question),
        "replies": question.replies,
        "votes": question.votes,
        "created_at": question.created_at.isoformat() if question.created_at else None,
    }


def list_questions(user_id: int, db: Session, category: Optional[str] = None) -> List[dict]:
    """Forum sorularını listele - kategori filtreleme ile"""
    query = db.query(ForumThread).order_by(ForumThread.id.desc())
    
    if category and category != "Tümü":
        query = query.filter(ForumThread.category == category)
    
    questions = query.all()
    
    # Yanıt ve beğeni sayılarını ekle
    result = []
    for question in questions:
        replies_count = db.query(ForumReply).filter(ForumReply.question_id == question.id).count()
        likes_count = db.query(ForumLike).filter(ForumLike.question_id == question.id).count()
        result.append({
            "id": question.id,
            "user_id": question.user_id,
            "title": question.title,
            "category": question.category,
            "detail": _thread_detail_text(question),
            "author": _thread_author_label(question),
            "time": _thread_time_label(question),
            "replies": question.replies,
            "votes": question.votes,
            "replies_count": replies_count,
            "likes_count": likes_count,
            "created_at": question.created_at.isoformat() if question.created_at else None,
        })
    
    return result


def get_question(user_id: int, question_id: int, db: Session) -> dict:
    """Forum sorusu detayını getir"""
    question = _get_thread(question_id, db)
    return {
        "id": question.id,
        "user_id": question.user_id,
        "title": question.title,
        "category": question.category,
        "detail": _thread_detail_text(question),
        "author": _thread_author_label(question),
        "time": _thread_time_label(question),
        "replies": question.replies,
        "votes": question.votes,
        "created_at": question.created_at.isoformat() if question.created_at else None,
    }


def update_question(user_id: int, question_id: int, payload: ForumQuestionUpdate, db: Session) -> dict:
    """Forum sorusunu güncelle"""
    patch = payload.model_dump(exclude_unset=True)
    if not patch:
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    
    question = _get_thread(question_id, db)
    if question.user_id != user_id:
        raise HTTPException(status_code=403, detail="Sadece kendi konunuzu güncelleyebilirsiniz.")
    
    for key, value in patch.items():
        setattr(question, key, value)
    db.commit()
    db.refresh(question)
    return {
        "id": question.id,
        "user_id": question.user_id,
        "title": question.title,
        "category": question.category,
        "detail": _thread_detail_text(question),
        "author": _thread_author_label(question),
        "time": _thread_time_label(question),
        "replies": question.replies,
        "votes": question.votes,
        "created_at": question.created_at.isoformat() if question.created_at else None,
    }


def delete_question(user_id: int, question_id: int, db: Session) -> dict:
    """Forum sorusunu sil"""
    question = _get_thread(question_id, db)
    if question.user_id != user_id:
        raise HTTPException(status_code=403, detail="Sadece kendi konunuzu silebilirsiniz.")
    
    db.delete(question)
    db.commit()
    return {"ok": True}


def create_reply(user_id: int, question_id: int, payload: ForumReplyCreate, db: Session) -> dict:
    """Forum yanıtını oluştur"""
    user = db.query(User).filter(User.id == user_id).first()
    author = user.name.split()[0] if user else "Kullanıcı"
    reply = ForumReply(
        question_id=question_id,
        user_id=user_id,
        author=author,
        content=payload.content,
        time="Az önce",
    )
    db.add(reply)
    db.commit()
    db.refresh(reply)
    
    # Sorunun yanıt sayısını güncelle
    question = _get_thread(question_id, db)
    question.replies = db.query(ForumReply).filter(ForumReply.question_id == question_id).count()
    db.commit()
    
    return {
        "id": reply.id,
        "question_id": reply.question_id,
        "user_id": reply.user_id,
        "author": reply.author,
        "content": reply.content,
        "time": reply.time,
        "created_at": reply.created_at.isoformat() if reply.created_at else None,
    }


def list_replies(user_id: int, question_id: int, db: Session) -> list[dict]:
    """Forum yanıtlarını listele"""
    replies = db.query(ForumReply).filter(ForumReply.question_id == question_id).order_by(ForumReply.id.desc()).all()
    return [{
        "id": r.id,
        "question_id": r.question_id,
        "user_id": r.user_id,
        "author": r.author,
        "content": r.content,
        "time": r.time,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    } for r in replies]


def create_like(user_id: int, question_id: int, db: Session) -> dict:
    """Forum sorusunu beğen"""
    # Kullanıcının daha önce beğenip beğenmediğini kontrol et
    existing_like = db.query(ForumLike).filter(
        ForumLike.question_id == question_id,
        ForumLike.user_id == user_id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Bu soruyu zaten beğendiniz.")
    
    like = ForumLike(
        question_id=question_id,
        user_id=user_id,
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    
    # Sorunun beğeni sayısını güncelle
    question = _get_thread(question_id, db)
    question.votes = db.query(ForumLike).filter(ForumLike.question_id == question_id).count()
    db.commit()
    
    return {
        "id": like.id,
        "question_id": like.question_id,
        "user_id": like.user_id,
        "created_at": like.created_at.isoformat() if like.created_at else None,
    }


def delete_like(user_id: int, question_id: int, db: Session) -> dict:
    """Forum sorusu beğenisini kaldır"""
    like = db.query(ForumLike).filter(
        ForumLike.question_id == question_id,
        ForumLike.user_id == user_id
    ).first()
    
    if not like:
        raise HTTPException(status_code=404, detail="Beğeni bulunamadı.")
    
    db.delete(like)
    db.commit()
    
    # Sorunun beğeni sayısını güncelle
    question = _get_thread(question_id, db)
    question.votes = db.query(ForumLike).filter(ForumLike.question_id == question_id).count()
    db.commit()
    
    return {"ok": True}


def list_likes(user_id: int, question_id: int, db: Session) -> list[dict]:
    """Forum sorusu beğenilerini listele"""
    likes = db.query(ForumLike).filter(ForumLike.question_id == question_id).all()
    return [{
        "id": l.id,
        "question_id": l.question_id,
        "user_id": l.user_id,
        "created_at": l.created_at.isoformat() if l.created_at else None,
    } for l in likes]
