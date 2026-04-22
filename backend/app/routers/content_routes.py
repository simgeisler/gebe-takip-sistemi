from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_user_id
from app.models import ForumCategory, ForumReport, ForumReply, ForumThread, LibraryItem, WeeklyMetadata
from app.schemas import (
    CreateReplyRequest,
    CreateThreadRequest,
    ReportThreadRequest,
    UpdateLibraryItemRequest,
    UpdateReplyRequest,
    UpdateThreadRequest,
)

router = APIRouter(tags=["content"])


@router.get("/weekly-metadata/{week_number}")
def get_weekly_metadata(week_number: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    _ = user_id
    row = db.get(WeeklyMetadata, week_number)
    if not row:
        raise HTTPException(status_code=404, detail="Week not found")
    return {
        "week_number": row.week_number,
        "fetus_size_cm": row.fetus_size_cm,
        "fetus_weight_gr": row.fetus_weight_gr,
        "development_milestones": row.development_milestones_json,
        "symptom_analysis_text": row.symptom_analysis_text,
        "comparison_object_name": row.comparison_object_name,
        "image_url": row.image_url,
    }


@router.get("/library/search")
def search_library(
    q: str = Query(default=""), user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    _ = user_id
    query = db.query(LibraryItem)
    if q:
        query = query.filter((LibraryItem.title.ilike(f"%{q}%")) | (LibraryItem.content.ilike(f"%{q}%")))
    rows = query.order_by(LibraryItem.category.asc()).all()
    return [{"id": row.id, "category": row.category, "title": row.title, "content": row.content} for row in rows]


@router.get("/library/{item_id}")
def get_library_item(item_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    _ = user_id
    row = db.get(LibraryItem, item_id)
    if not row:
        raise HTTPException(status_code=404, detail="Library item not found")
    return {"id": row.id, "category": row.category, "title": row.title, "content": row.content}


@router.post("/library")
def create_library_item(payload: UpdateLibraryItemRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, int]:
    _ = user_id
    if not payload.category or not payload.title or not payload.content:
        raise HTTPException(status_code=400, detail="category, title, content zorunlu")
    item = LibraryItem(category=payload.category, title=payload.title, content=payload.content)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id}


@router.put("/library/{item_id}")
def update_library_item(
    item_id: int, payload: UpdateLibraryItemRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    _ = user_id
    row = db.get(LibraryItem, item_id)
    if not row:
        raise HTTPException(status_code=404, detail="Library item not found")
    if payload.category is not None:
        row.category = payload.category
    if payload.title is not None:
        row.title = payload.title
    if payload.content is not None:
        row.content = payload.content
    db.commit()
    return {"ok": True}


@router.delete("/library/{item_id}")
def delete_library_item(item_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    _ = user_id
    row = db.get(LibraryItem, item_id)
    if not row:
        raise HTTPException(status_code=404, detail="Library item not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.get("/forum/categories")
def list_forum_categories(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    _ = user_id
    rows = db.query(ForumCategory).all()
    return [{"id": row.id, "name": row.name} for row in rows]


@router.get("/forum/threads")
def list_threads(
    category_id: Optional[int] = None, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    _ = user_id
    query = db.query(ForumThread)
    if category_id:
        query = query.filter(ForumThread.category_id == category_id)
    rows = query.order_by(desc(ForumThread.created_at)).all()
    return [{"id": row.id, "title": row.title, "body": row.body, "category_id": row.category_id} for row in rows]


@router.post("/forum/threads")
def create_thread(payload: CreateThreadRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, int]:
    category = db.get(ForumCategory, payload.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    thread = ForumThread(category_id=payload.category_id, user_id=user_id, title=payload.title, body=payload.body)
    db.add(thread)
    db.commit()
    db.refresh(thread)
    return {"id": thread.id}


@router.get("/forum/threads/{thread_id}")
def get_thread(thread_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    _ = user_id
    row = db.get(ForumThread, thread_id)
    if not row:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {
        "id": row.id,
        "title": row.title,
        "body": row.body,
        "category_id": row.category_id,
        "user_id": row.user_id,
        "created_at": row.created_at.isoformat(),
    }


@router.put("/forum/threads/{thread_id}")
def update_thread(
    thread_id: int, payload: UpdateThreadRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    row = db.get(ForumThread, thread_id)
    if not row:
        raise HTTPException(status_code=404, detail="Thread not found")
    if row.user_id != user_id:
        raise HTTPException(status_code=403, detail="Bu thread size ait degil")
    if payload.category_id is not None:
        category = db.get(ForumCategory, payload.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        row.category_id = payload.category_id
    if payload.title is not None:
        row.title = payload.title
    if payload.body is not None:
        row.body = payload.body
    db.commit()
    return {"ok": True}


@router.delete("/forum/threads/{thread_id}")
def delete_thread(thread_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(ForumThread, thread_id)
    if not row:
        raise HTTPException(status_code=404, detail="Thread not found")
    if row.user_id != user_id:
        raise HTTPException(status_code=403, detail="Bu thread size ait degil")
    db.query(ForumReply).filter(ForumReply.thread_id == row.id).delete()
    db.query(ForumReport).filter(ForumReport.thread_id == row.id).delete()
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.post("/forum/replies")
def create_reply(payload: CreateReplyRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, int]:
    thread = db.get(ForumThread, payload.thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    reply = ForumReply(thread_id=payload.thread_id, user_id=user_id, body=payload.body)
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return {"id": reply.id}


@router.get("/forum/replies/{reply_id}")
def get_reply(reply_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    _ = user_id
    row = db.get(ForumReply, reply_id)
    if not row:
        raise HTTPException(status_code=404, detail="Reply not found")
    return {
        "id": row.id,
        "thread_id": row.thread_id,
        "user_id": row.user_id,
        "body": row.body,
        "created_at": row.created_at.isoformat(),
    }


@router.put("/forum/replies/{reply_id}")
def update_reply(
    reply_id: int, payload: UpdateReplyRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    row = db.get(ForumReply, reply_id)
    if not row:
        raise HTTPException(status_code=404, detail="Reply not found")
    if row.user_id != user_id:
        raise HTTPException(status_code=403, detail="Bu yorum size ait degil")
    if payload.body is not None:
        row.body = payload.body
    db.commit()
    return {"ok": True}


@router.delete("/forum/replies/{reply_id}")
def delete_reply(reply_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(ForumReply, reply_id)
    if not row:
        raise HTTPException(status_code=404, detail="Reply not found")
    if row.user_id != user_id:
        raise HTTPException(status_code=403, detail="Bu yorum size ait degil")
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.post("/forum/report")
def report_thread(payload: ReportThreadRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    thread = db.get(ForumThread, payload.thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    db.add(ForumReport(thread_id=payload.thread_id, user_id=user_id, reason=payload.reason))
    db.commit()
    return {"ok": True}


@router.get("/forum/report")
def list_reports(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    rows = db.query(ForumReport).filter(ForumReport.user_id == user_id).order_by(desc(ForumReport.created_at)).all()
    return [{"id": row.id, "thread_id": row.thread_id, "reason": row.reason, "created_at": row.created_at.isoformat()} for row in rows]


@router.delete("/forum/report/{report_id}")
def delete_report(report_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(ForumReport, report_id)
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")
    if row.user_id != user_id:
        raise HTTPException(status_code=403, detail="Bu rapor size ait degil")
    db.delete(row)
    db.commit()
    return {"ok": True}
