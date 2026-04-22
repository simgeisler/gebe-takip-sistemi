from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_user_id
from app.models import CounterLog
from app.schemas import (
    ContractionEventRequest,
    ContractionEventUpdateRequest,
    KickSessionRequest,
    KickSessionUpdateRequest,
)

router = APIRouter(prefix="/counters", tags=["counters"])


@router.post("/kick-session")
def create_kick_session(payload: KickSessionRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    duration_seconds = int((payload.end_time - payload.start_time).total_seconds())
    db.add(
        CounterLog(
            user_id=user_id,
            type="kick",
            start_time=payload.start_time,
            end_time=payload.end_time,
            duration_seconds=max(duration_seconds, 0),
            frequency_seconds=None,
            meta_json={"total_count": payload.total_count},
        )
    )
    db.commit()
    return {"ok": True}


@router.get("/kick-session")
def list_kick_sessions(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    rows = db.query(CounterLog).filter(CounterLog.user_id == user_id, CounterLog.type == "kick").order_by(desc(CounterLog.start_time)).all()
    return [
        {
            "id": row.id,
            "start_time": row.start_time.isoformat(),
            "end_time": row.end_time.isoformat(),
            "duration_seconds": row.duration_seconds,
            "total_count": row.meta_json.get("total_count"),
        }
        for row in rows
    ]


@router.get("/kick-session/{session_id}")
def get_kick_session(session_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    row = db.get(CounterLog, session_id)
    if not row or row.user_id != user_id or row.type != "kick":
        raise HTTPException(status_code=404, detail="Kick session not found")
    return {
        "id": row.id,
        "start_time": row.start_time.isoformat(),
        "end_time": row.end_time.isoformat(),
        "duration_seconds": row.duration_seconds,
        "total_count": row.meta_json.get("total_count"),
    }


@router.put("/kick-session/{session_id}")
def update_kick_session(
    session_id: int, payload: KickSessionUpdateRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    row = db.get(CounterLog, session_id)
    if not row or row.user_id != user_id or row.type != "kick":
        raise HTTPException(status_code=404, detail="Kick session not found")
    if payload.start_time is not None:
        row.start_time = payload.start_time
    if payload.end_time is not None:
        row.end_time = payload.end_time
    if payload.total_count is not None:
        row.meta_json = {**row.meta_json, "total_count": payload.total_count}
    row.duration_seconds = max(int((row.end_time - row.start_time).total_seconds()), 0)
    db.commit()
    return {"ok": True}


@router.delete("/kick-session/{session_id}")
def delete_kick_session(session_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(CounterLog, session_id)
    if not row or row.user_id != user_id or row.type != "kick":
        raise HTTPException(status_code=404, detail="Kick session not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.post("/contraction-event")
def create_contraction_event(
    payload: ContractionEventRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    duration_seconds = int((payload.end_time - payload.start_time).total_seconds())
    previous = (
        db.query(CounterLog)
        .filter(CounterLog.user_id == user_id, CounterLog.type == "contraction")
        .order_by(desc(CounterLog.start_time))
        .first()
    )
    frequency_seconds = int((payload.start_time - previous.start_time).total_seconds()) if previous else None
    db.add(
        CounterLog(
            user_id=user_id,
            type="contraction",
            start_time=payload.start_time,
            end_time=payload.end_time,
            duration_seconds=max(duration_seconds, 0),
            frequency_seconds=frequency_seconds,
            meta_json={},
        )
    )
    db.commit()
    return {"ok": True}


@router.get("/contraction-event")
def list_contraction_events(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    rows = (
        db.query(CounterLog)
        .filter(CounterLog.user_id == user_id, CounterLog.type == "contraction")
        .order_by(desc(CounterLog.start_time))
        .all()
    )
    return [
        {
            "id": row.id,
            "start_time": row.start_time.isoformat(),
            "end_time": row.end_time.isoformat(),
            "duration_seconds": row.duration_seconds,
            "frequency_seconds": row.frequency_seconds,
        }
        for row in rows
    ]


@router.get("/contraction-event/{event_id}")
def get_contraction_event(event_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    row = db.get(CounterLog, event_id)
    if not row or row.user_id != user_id or row.type != "contraction":
        raise HTTPException(status_code=404, detail="Contraction event not found")
    return {
        "id": row.id,
        "start_time": row.start_time.isoformat(),
        "end_time": row.end_time.isoformat(),
        "duration_seconds": row.duration_seconds,
        "frequency_seconds": row.frequency_seconds,
    }


@router.put("/contraction-event/{event_id}")
def update_contraction_event(
    event_id: int, payload: ContractionEventUpdateRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    row = db.get(CounterLog, event_id)
    if not row or row.user_id != user_id or row.type != "contraction":
        raise HTTPException(status_code=404, detail="Contraction event not found")
    if payload.start_time is not None:
        row.start_time = payload.start_time
    if payload.end_time is not None:
        row.end_time = payload.end_time
    row.duration_seconds = max(int((row.end_time - row.start_time).total_seconds()), 0)
    db.commit()
    return {"ok": True}


@router.delete("/contraction-event/{event_id}")
def delete_contraction_event(event_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(CounterLog, event_id)
    if not row or row.user_id != user_id or row.type != "contraction":
        raise HTTPException(status_code=404, detail="Contraction event not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.post("/contraction-session/analyze")
def analyze_contractions(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, Any]:
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    rows = (
        db.query(CounterLog)
        .filter(CounterLog.user_id == user_id, CounterLog.type == "contraction", CounterLog.start_time >= one_hour_ago)
        .order_by(desc(CounterLog.start_time))
        .all()
    )
    if not rows:
        return {"danger": False, "message": "Yeterli veri yok"}

    frequencies = [row.frequency_seconds for row in rows if row.frequency_seconds]
    average_frequency_seconds = int(sum(frequencies) / len(frequencies)) if frequencies else None
    average_duration_seconds = int(sum(row.duration_seconds for row in rows) / len(rows))
    is_danger = bool(average_frequency_seconds and average_frequency_seconds <= 300 and average_duration_seconds >= 60)
    message = "Hastaneye gitme vaktiniz gelmis olabilir" if is_danger else "Takibe devam edin"
    return {
        "danger": is_danger,
        "average_frequency_seconds": average_frequency_seconds,
        "average_duration_seconds": average_duration_seconds,
        "message": message,
    }
