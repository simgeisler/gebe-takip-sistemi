from typing import List, Optional

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.library_extended import (
    LibraryArticleCreate,
    LibraryArticleList,
    LibraryArticleResponse,
    LibraryArticleUpdate,
    LibraryLikeCreate,
    LibraryLikeResponse,
)
from ..services import auth_service
from ..services import library_service as library_api

router = APIRouter(prefix="/library", tags=["library"])


@router.post("/articles", response_model=LibraryArticleResponse)
def create_library_article(payload: LibraryArticleCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Yeni kütüphane makalesi oluştur"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.create_article(user_id, payload, db)


@router.get("/articles", response_model=List[LibraryArticleList])
def list_library_articles(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Kütüphane makalelerini listele - arama ve kategori filtreleme ile"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.list_articles(user_id, db, search, category)


@router.get("/articles/{article_id}", response_model=LibraryArticleResponse)
def get_library_article(article_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Kütüphane makalesi detayını getir"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.get_article(user_id, article_id, db)


@router.put("/articles/{article_id}", response_model=LibraryArticleResponse)
def update_library_article(
    article_id: int, payload: LibraryArticleUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """Kütüphane makalesini güncelle"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.update_article(user_id, article_id, payload, db)


@router.delete("/articles/{article_id}")
def delete_library_article(article_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Kütüphane makalesini sil"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.delete_article(user_id, article_id, db)


@router.post("/articles/{article_id}/likes", response_model=LibraryLikeResponse)
def create_library_like(article_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Kütüphane makalesini beğen"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.create_like(user_id, article_id, db)


@router.delete("/articles/{article_id}/likes")
def delete_library_like(article_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Kütüphane makalesi beğenisini kaldır"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.delete_like(user_id, article_id, db)


@router.get("/articles/{article_id}/likes", response_model=List[LibraryLikeResponse])
def list_library_likes(article_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Kütüphane makalesi beğenilerini listele"""
    user_id = auth_service.resolve_token(authorization, db=db)
    return library_api.list_likes(user_id, article_id, db)
