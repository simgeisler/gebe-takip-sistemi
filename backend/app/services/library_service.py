from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.entities import LibraryArticle, LibraryLike
from ..schemas.library_extended import LibraryArticleCreate, LibraryArticleUpdate
from ..services import auth_service


def _get_article(article_id: int, db: Session) -> LibraryArticle:
    article = db.query(LibraryArticle).filter(LibraryArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Makale bulunamadı.")
    return article


def create_article(user_id: int, payload: LibraryArticleCreate, db: Session) -> dict:
    """Yeni kütüphane makalesi oluştur (yalnızca uygulama yöneticisi)."""
    auth_service.ensure_library_owner(user_id, db)
    article = LibraryArticle(
        user_id=None,
        title=payload.title,
        category=payload.category,
        description=payload.description,
        read_minutes=payload.read_minutes,
        body=payload.body,
        image_url=payload.image_url,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    likes_count = db.query(LibraryLike).filter(LibraryLike.article_id == article.id).count()
    liked_by_me = (
        db.query(LibraryLike)
        .filter(LibraryLike.article_id == article.id, LibraryLike.user_id == user_id)
        .first()
        is not None
    )
    return {
        "id": article.id,
        "user_id": article.user_id,
        "title": article.title,
        "category": article.category,
        "description": article.description,
        "read_minutes": article.read_minutes,
        "body": article.body,
        "image_url": article.image_url,
        "created_at": article.created_at.isoformat() if article.created_at else None,
        "likes_count": likes_count,
        "liked_by_me": liked_by_me,
    }


def list_articles(user_id: int, db: Session, search: Optional[str] = None, category: Optional[str] = None) -> List[dict]:
    """Kütüphane makalelerini listele - arama ve kategori filtreleme ile"""
    query = db.query(LibraryArticle).order_by(LibraryArticle.id.desc())
    
    # Kategori filtreleme
    if category and category != "Tümü":
        query = query.filter(LibraryArticle.category == category)
    
    articles = query.all()
    
    # Arama filtreleme
    if search:
        search_lower = search.lower()
        articles = [
            a for a in articles 
            if search_lower in a.title.lower() 
            or search_lower in (a.description or "").lower() 
            or search_lower in a.category.lower()
        ]
    
    # Beğeni sayısını ekle
    result = []
    for article in articles:
        likes_count = db.query(LibraryLike).filter(LibraryLike.article_id == article.id).count()
        result.append({
            "id": article.id,
            "user_id": article.user_id,
            "title": article.title,
            "category": article.category,
            "description": article.description,
            "read_minutes": article.read_minutes,
            "body": article.body,
            "image_url": article.image_url,
            "likes_count": likes_count,
            "created_at": article.created_at.isoformat() if article.created_at else None,
        })
    
    return result


def get_article(user_id: int, article_id: int, db: Session) -> dict:
    """Kütüphane makalesi detayını getir"""
    article = _get_article(article_id, db)
    likes_count = db.query(LibraryLike).filter(LibraryLike.article_id == article.id).count()
    liked_by_me = (
        db.query(LibraryLike)
        .filter(LibraryLike.article_id == article.id, LibraryLike.user_id == user_id)
        .first()
        is not None
    )
    return {
        "id": article.id,
        "user_id": article.user_id,
        "title": article.title,
        "category": article.category,
        "description": article.description,
        "read_minutes": article.read_minutes,
        "body": article.body,
        "image_url": article.image_url,
        "created_at": article.created_at.isoformat() if article.created_at else None,
        "likes_count": likes_count,
        "liked_by_me": liked_by_me,
    }


def update_article(user_id: int, article_id: int, payload: LibraryArticleUpdate, db: Session) -> dict:
    """Kütüphane makalesini güncelle (yalnızca uygulama yöneticisi)."""
    auth_service.ensure_library_owner(user_id, db)
    patch = payload.model_dump(exclude_unset=True)
    if not patch:
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    
    article = _get_article(article_id, db)
    
    for key, value in patch.items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    likes_count = db.query(LibraryLike).filter(LibraryLike.article_id == article.id).count()
    liked_by_me = (
        db.query(LibraryLike)
        .filter(LibraryLike.article_id == article.id, LibraryLike.user_id == user_id)
        .first()
        is not None
    )
    return {
        "id": article.id,
        "user_id": article.user_id,
        "title": article.title,
        "category": article.category,
        "description": article.description,
        "read_minutes": article.read_minutes,
        "body": article.body,
        "image_url": article.image_url,
        "created_at": article.created_at.isoformat() if article.created_at else None,
        "likes_count": likes_count,
        "liked_by_me": liked_by_me,
    }


def delete_article(user_id: int, article_id: int, db: Session) -> dict:
    """Kütüphane makalesini sil (yalnızca uygulama yöneticisi)."""
    auth_service.ensure_library_owner(user_id, db)
    article = _get_article(article_id, db)
    
    db.delete(article)
    db.commit()
    return {"ok": True}


def create_like(user_id: int, article_id: int, db: Session) -> dict:
    """Kütüphane makalesini beğen"""
    # Kullanıcının daha önce beğenip beğenmediğini kontrol et
    existing_like = db.query(LibraryLike).filter(
        LibraryLike.article_id == article_id,
        LibraryLike.user_id == user_id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Bu makaleyi zaten beğendiniz.")
    
    like = LibraryLike(
        article_id=article_id,
        user_id=user_id,
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    
    return {
        "id": like.id,
        "article_id": like.article_id,
        "user_id": like.user_id,
        "created_at": like.created_at.isoformat() if like.created_at else None,
    }


def delete_like(user_id: int, article_id: int, db: Session) -> dict:
    """Kütüphane makalesi beğenisini kaldır"""
    like = db.query(LibraryLike).filter(
        LibraryLike.article_id == article_id,
        LibraryLike.user_id == user_id
    ).first()
    
    if not like:
        raise HTTPException(status_code=404, detail="Beğeni bulunamadı.")
    
    db.delete(like)
    db.commit()
    return {"ok": True}


def list_likes(user_id: int, article_id: int, db: Session) -> list[dict]:
    """Kütüphane makalesi beğenilerini listele"""
    likes = db.query(LibraryLike).filter(LibraryLike.article_id == article_id).all()
    return [{
        "id": l.id,
        "article_id": l.article_id,
        "user_id": l.user_id,
        "created_at": l.created_at.isoformat() if l.created_at else None,
    } for l in likes]
