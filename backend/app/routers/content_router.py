from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.content import LibraryArticleCreate, LibraryArticleUpdate
from ..services import content_service

router = APIRouter(tags=["content"])


@router.get("/content/weekly/{week_number}")
def get_weekly_data(week_number: int, db: Session = Depends(get_db)):
    return content_service.get_weekly_data(week_number, db)


@router.get("/library/articles")
def list_library_articles(query: str = "", cat: str = "", db: Session = Depends(get_db)):
    """Library.tsx grid — id, cat, title, desc, time."""
    return content_service.list_library_articles(db, query, cat)


@router.get("/library/articles/{article_id}")
def get_library_article(article_id: int, db: Session = Depends(get_db)):
    return content_service.get_library_article_public(article_id, db)


@router.post("/library/articles")
def post_library_article(payload: LibraryArticleCreate, db: Session = Depends(get_db)):
    return content_service.create_library_article(payload, db)


@router.put("/library/articles/{article_id}")
def put_library_article(article_id: int, payload: LibraryArticleUpdate, db: Session = Depends(get_db)):
    return content_service.update_library_article(article_id, payload, db)


@router.delete("/library/articles/{article_id}")
def delete_library_article(article_id: int, db: Session = Depends(get_db)):
    return content_service.delete_library_article(article_id, db)
