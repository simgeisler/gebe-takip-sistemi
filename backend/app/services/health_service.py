from datetime import date, datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..core.pregnancy import get_today
from ..models.entities import DailyLog, KickSession
from ..schemas.health import (
    ContractionAnalysisRequest,
    DailyLogRequest,
    DailyLogUpdateRequest,
    KickSessionRequest,
    KickSessionUpdateRequest,
)


def _get_user_daily_log(user_id: int, log_id: int, db: Session) -> DailyLog:
    daily_log = db.query(DailyLog).filter(
        DailyLog.id == log_id,
        DailyLog.user_id == user_id
    ).first()
    if not daily_log:
        raise HTTPException(status_code=404, detail="Gunluk kayit bulunamadi.")
    return daily_log


def _get_user_kick_session(user_id: int, session_id: int, db: Session) -> KickSession:
    kick_session = db.query(KickSession).filter(
        KickSession.id == session_id,
        KickSession.user_id == user_id
    ).first()
    if not kick_session:
        raise HTTPException(status_code=404, detail="Tekme oturumu bulunamadi.")
    return kick_session


def create_daily_log(user_id: int, payload: DailyLogRequest, db: Session) -> dict:
    if payload.date > get_today():
        raise HTTPException(status_code=400, detail="Gelecek tarihli veri girişi yapılamaz.")
    daily_log = DailyLog(
        user_id=user_id,
        date=payload.date,
        weight=payload.weight,
        water_liters=payload.water_liters,
        systolic=payload.systolic,
        diastolic=payload.diastolic,
        blood_glucose=payload.blood_glucose,
        pulse=payload.pulse,
        notes=payload.notes,
    )
    db.add(daily_log)
    db.commit()
    db.refresh(daily_log)
    return {
        "id": daily_log.id,
        "user_id": daily_log.user_id,
        "date": daily_log.date.isoformat() if daily_log.date else None,
        "weight": daily_log.weight,
        "water_liters": daily_log.water_liters,
        "systolic": daily_log.systolic,
        "diastolic": daily_log.diastolic,
        "blood_glucose": daily_log.blood_glucose,
        "pulse": daily_log.pulse,
        "notes": daily_log.notes,
        "created_at": daily_log.created_at.isoformat() if daily_log.created_at else None,
    }


def list_daily_logs(user_id: int, db: Session) -> list[dict]:
    """En son kaydedilen önce (aynı gün birden fazla satır için created_at + id)."""
    daily_logs = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == user_id)
        .order_by(DailyLog.created_at.desc(), DailyLog.id.desc())
        .all()
    )
    return [{
        "id": log.id,
        "user_id": log.user_id,
        "date": log.date.isoformat() if log.date else None,
        "weight": log.weight,
        "water_liters": log.water_liters,
        "systolic": log.systolic,
        "diastolic": log.diastolic,
        "blood_glucose": log.blood_glucose,
        "pulse": log.pulse,
        "notes": log.notes,
        "created_at": log.created_at.isoformat() if log.created_at else None,
    } for log in daily_logs]


def get_daily_log(user_id: int, log_id: int, db: Session) -> dict:
    daily_log = _get_user_daily_log(user_id, log_id, db)
    return {
        "id": daily_log.id,
        "user_id": daily_log.user_id,
        "date": daily_log.date.isoformat() if daily_log.date else None,
        "weight": daily_log.weight,
        "water_liters": daily_log.water_liters,
        "systolic": daily_log.systolic,
        "diastolic": daily_log.diastolic,
        "blood_glucose": daily_log.blood_glucose,
        "pulse": daily_log.pulse,
        "notes": daily_log.notes,
        "created_at": daily_log.created_at.isoformat() if daily_log.created_at else None,
    }


def update_daily_log(user_id: int, log_id: int, payload: DailyLogUpdateRequest, db: Session) -> dict:
    if payload.date and payload.date > get_today():
        raise HTTPException(status_code=400, detail="Gelecek tarihli veri girişi yapılamaz.")
    patch = payload.model_dump(exclude_unset=True)
    if not patch:
        raise HTTPException(status_code=400, detail="Guncellenecek en az bir alan gonderin.")
    daily_log = _get_user_daily_log(user_id, log_id, db)
    for key, value in patch.items():
        setattr(daily_log, key, value)
    db.commit()
    db.refresh(daily_log)
    return {
        "id": daily_log.id,
        "user_id": daily_log.user_id,
        "date": daily_log.date.isoformat() if daily_log.date else None,
        "weight": daily_log.weight,
        "water_liters": daily_log.water_liters,
        "systolic": daily_log.systolic,
        "diastolic": daily_log.diastolic,
        "blood_glucose": daily_log.blood_glucose,
        "pulse": daily_log.pulse,
        "notes": daily_log.notes,
        "created_at": daily_log.created_at.isoformat() if daily_log.created_at else None,
    }


def delete_daily_log(user_id: int, log_id: int, db: Session) -> dict:
    daily_log = _get_user_daily_log(user_id, log_id, db)
    db.delete(daily_log)
    db.commit()
    return {"ok": True}


def _fmt_chart_day(d: date) -> str:
    return d.strftime("%d.%m")


def get_health_trends(user_id: int, db: Session) -> dict:
    logs = db.query(DailyLog).filter(DailyLog.user_id == user_id).order_by(DailyLog.date).all()
    weights = [{"x": l.date.isoformat(), "y": l.weight} for l in logs if l.weight is not None]
    blood_pressure = [
        {
            "date": l.date.isoformat(),
            "systolic": l.systolic,
            "diastolic": l.diastolic,
            "is_risky": bool(l.systolic and l.diastolic and (l.systolic > 140 or l.diastolic > 90)),
        }
        for l in logs
        if l.systolic is not None and l.diastolic is not None
    ]
    blood_pressure.reverse()

    tansiyon = [
        {"d": _fmt_chart_day(l.date), "sis": l.systolic, "dia": l.diastolic}
        for l in logs
        if l.systolic is not None and l.diastolic is not None
    ]
    kilo = [{"d": _fmt_chart_day(l.date), "kg": round(float(l.weight), 1)} for l in logs if l.weight is not None]
    seker = [
        {"d": _fmt_chart_day(l.date), "mg_dl": float(l.blood_glucose)}
        for l in logs
        if l.blood_glucose is not None
    ]

    return {
        "weights": weights,
        "blood_pressure": blood_pressure,
        "frontend_charts": {"tansiyon": tansiyon, "kilo": kilo, "seker": seker},
    }


def create_kick_session(user_id: int, payload: KickSessionRequest, db: Session) -> dict:
    session = KickSession(
        user_id=user_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        kick_count=payload.kick_count,
        notes=payload.notes,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {
        "id": session.id,
        "user_id": session.user_id,
        "start_time": session.start_time.isoformat() if session.start_time else None,
        "end_time": session.end_time.isoformat() if session.end_time else None,
        "kick_count": session.kick_count,
        "notes": session.notes,
        "created_at": session.created_at.isoformat() if session.created_at else None,
    }


def list_kick_sessions(user_id: int, db: Session) -> list[dict]:
    kick_sessions = db.query(KickSession).filter(KickSession.user_id == user_id).order_by(KickSession.start_time.desc()).all()
    return [{
        "id": s.id,
        "user_id": s.user_id,
        "start_time": s.start_time.isoformat() if s.start_time else None,
        "end_time": s.end_time.isoformat() if s.end_time else None,
        "kick_count": s.kick_count,
        "notes": s.notes,
        "created_at": s.created_at.isoformat() if s.created_at else None,
    } for s in kick_sessions]


def get_kick_session(user_id: int, session_id: int, db: Session) -> dict:
    kick_session = _get_user_kick_session(user_id, session_id, db)
    return {
        "id": kick_session.id,
        "user_id": kick_session.user_id,
        "start_time": kick_session.start_time.isoformat() if kick_session.start_time else None,
        "end_time": kick_session.end_time.isoformat() if kick_session.end_time else None,
        "kick_count": kick_session.kick_count,
        "notes": kick_session.notes,
        "created_at": kick_session.created_at.isoformat() if kick_session.created_at else None,
    }


def update_kick_session(user_id: int, session_id: int, payload: KickSessionUpdateRequest, db: Session) -> dict:
    patch = payload.model_dump(exclude_unset=True)
    if not patch:
        raise HTTPException(status_code=400, detail="Guncellenecek en az bir alan gonderin.")
    kick_session = _get_user_kick_session(user_id, session_id, db)
    for key, value in patch.items():
        setattr(kick_session, key, value)
    db.commit()
    db.refresh(kick_session)
    return {
        "id": kick_session.id,
        "user_id": kick_session.user_id,
        "start_time": kick_session.start_time.isoformat() if kick_session.start_time else None,
        "end_time": kick_session.end_time.isoformat() if kick_session.end_time else None,
        "kick_count": kick_session.kick_count,
        "notes": kick_session.notes,
        "created_at": kick_session.created_at.isoformat() if kick_session.created_at else None,
    }


def delete_kick_session(user_id: int, session_id: int, db: Session) -> dict:
    kick_session = _get_user_kick_session(user_id, session_id, db)
    db.delete(kick_session)
    db.commit()
    return {"ok": True}


def analyze_contraction(payload: ContractionAnalysisRequest) -> dict:
    if len(payload.starts) < 2 or len(payload.ends) < 1:
        return {"danger_zone": False, "message": "Yetersiz veri"}
    durations = [int((end - start).total_seconds()) for start, end in zip(payload.starts, payload.ends)]
    frequencies = [int((payload.starts[idx] - payload.starts[idx - 1]).total_seconds()) for idx in range(1, len(payload.starts))]
    avg_duration = sum(durations) / len(durations)
    avg_frequency = sum(frequencies) / len(frequencies) if frequencies else 0
    danger = avg_duration >= 60 and avg_frequency <= 300
    result = {
        "danger_zone": danger,
        "average_duration_seconds": avg_duration,
        "average_frequency_seconds": avg_frequency,
        "message": "Hastaneye gitme vaktiniz gelmiş olabilir" if danger else "Takibe devam edin",
    }
    return result
