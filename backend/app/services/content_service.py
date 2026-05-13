from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.entities import LibraryArticle, WeeklyMetadata
from ..schemas.content import LibraryArticleCreate, LibraryArticleUpdate


def get_weekly_data(week_number: int, db: Session) -> dict:
    weekly_data = db.query(WeeklyMetadata).filter(WeeklyMetadata.week_number == week_number).first()
    if not weekly_data:
        raise HTTPException(status_code=404, detail="Hafta bulunamadı.")
    return {
        "id": weekly_data.id,
        "week_number": weekly_data.week_number,
        "title": weekly_data.title,
        "description": weekly_data.description,
        "baby_size": weekly_data.baby_size,
        "baby_weight": weekly_data.baby_weight,
        "baby_length": weekly_data.baby_length,
        "common_symptoms": weekly_data.common_symptoms,
        "tips": weekly_data.tips,
        "created_at": weekly_data.created_at.isoformat() if weekly_data.created_at else None,
    }


def _article_to_list_item(r: LibraryArticle) -> dict:
    desc = r.description or (r.body or "")[:160]
    mins = int(r.read_minutes or 5)
    return {
        "id": r.id,
        "cat": r.category,
        "title": r.title,
        "desc": desc,
        "time": f"{mins} dk",
    }


def _article_to_detail(r: LibraryArticle) -> dict:
    out = _article_to_list_item(r)
    out["body"] = r.body or ""
    return out


def _filter_articles(db: Session, query: str = "", cat: str = "") -> list[LibraryArticle]:
    rows = db.query(LibraryArticle).all()
    if cat:
        rows = [r for r in rows if r.category.lower() == cat.lower()]
    if query:
        q = query.lower()
        rows = [
            r
            for r in rows
            if q in r.title.lower()
            or q in (r.body or "").lower()
            or q in (r.description or "").lower()
        ]
    return rows


def list_library_articles(db: Session, query: str = "", cat: str = "") -> list[dict]:
    return [_article_to_list_item(r) for r in _filter_articles(db, query, cat)]


def get_library_article_public(article_id: int, db: Session) -> dict:
    return _article_to_detail(_get_article(article_id, db))


def _get_article(article_id: int, db: Session) -> LibraryArticle:
    article = db.query(LibraryArticle).filter(LibraryArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="İçerik bulunamadı.")
    return article


def create_library_article(payload: LibraryArticleCreate, db: Session) -> dict:
    article = LibraryArticle(
        category=payload.cat,
        title=payload.title,
        description=payload.desc,
        body=payload.body or payload.desc,
        read_minutes=payload.read_minutes,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return _article_to_list_item(article)


def update_library_article(article_id: int, payload: LibraryArticleUpdate, db: Session) -> dict:
    patch = payload.model_dump(exclude_unset=True)
    if "cat" in patch:
        patch["category"] = patch.pop("cat")
    if "desc" in patch:
        patch["description"] = patch.pop("desc")
    if not patch:
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    article = _get_article(article_id, db)
    for key, value in patch.items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return _article_to_list_item(article)


def delete_library_article(article_id: int, db: Session) -> dict:
    article = _get_article(article_id, db)
    db.delete(article)
    db.commit()
    return {"ok": True}
