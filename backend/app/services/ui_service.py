"""Dashboard.tsx bölümleriyle aynı yapıda özet (hero, summary_cards, weight_chart, upcoming)."""

from calendar import monthrange
from datetime import date, datetime, time as time_cls

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..core.pregnancy import calculate_status
from ..data.weekly_baby_reference import NOT_FOUND_LABEL
from ..models.entities import CalendarEvent, DailyLog, User, WeeklyMetadata

UPCOMING_DASHBOARD_LIMIT = 2

_TYPE_LABEL = {"ilac": "İlaç", "randevu": "Randevu", "etkinlik": "Etkinlik"}


def _weekly_metadata_for_week(week: int, db: Session) -> WeeklyMetadata | None:
    return (
        db.query(WeeklyMetadata)
        .filter(WeeklyMetadata.week_number == min(week, 42))
        .first()
    )


def _baby_summary_from_metadata(week: int, db: Session) -> tuple[str, str, str | None]:
    meta = _weekly_metadata_for_week(week, db)
    weight = (meta.baby_weight or "").strip() if meta else ""
    length = (meta.baby_length or "").strip() if meta else ""
    size = (meta.baby_size or "").strip() if meta else ""
    value = weight or NOT_FOUND_LABEL
    hint = f"Boy: {length}" if length else f"Boy: {NOT_FOUND_LABEL.lower()}"
    return value, hint, size or None


def _hero_summary_text(week: int, baby_size: str | None) -> str:
    if baby_size:
        size_part = f"Bebeğin bir {baby_size} büyüklüğünde"
    else:
        size_part = f"Bebeğinin büyüklük bilgisi {NOT_FOUND_LABEL.lower()}"
    return f"Şu an {week}. haftadasın. {size_part} ve seni duyabiliyor 💛"


def _parse_time_hm(value: str | None) -> time_cls:
    if not value or not str(value).strip():
        return time_cls.min
    s = str(value).strip()
    for fmt in ("%H:%M:%S", "%H:%M"):
        n = 8 if fmt == "%H:%M:%S" else 5
        try:
            return datetime.strptime(s[:n], fmt).time()
        except ValueError:
            continue
    return time_cls.min


def _infer_calendar_event_date(ev: CalendarEvent, ref: date) -> date | None:
    if ev.event_on:
        return ev.event_on
    if ev.date is None:
        return None
    try:
        last_d = monthrange(ref.year, ref.month)[1]
        day = min(int(ev.date), last_d)
        return date(ref.year, ref.month, day)
    except ValueError:
        return None


def _calendar_event_sort_dt(ev: CalendarEvent, ref: date) -> datetime | None:
    d = _infer_calendar_event_date(ev, ref)
    if d is None:
        return None
    return datetime.combine(d, _parse_time_hm(ev.time))


def _event_type_label(ev_type: str | None) -> str:
    if not ev_type:
        return "Etkinlik"
    return _TYPE_LABEL.get(ev_type.strip().lower(), ev_type)


def _format_upcoming_when(d: date, time_str: str | None) -> str:
    t = (time_str or "").strip() or "—"
    return f"{d.day:02d}.{d.month:02d}.{d.year} · {t}"


def _dashboard_upcoming_events(user_id: int, db: Session) -> list[dict]:
    today = date.today()
    now = datetime.now()
    rows = db.query(CalendarEvent).filter(CalendarEvent.user_id == user_id).all()
    scored: list[tuple[datetime, CalendarEvent]] = []
    for ev in rows:
        sdt = _calendar_event_sort_dt(ev, today)
        if sdt is None:
            continue
        if sdt >= now:
            scored.append((sdt, ev))
    scored.sort(key=lambda x: (x[0], x[1].id))
    out: list[dict] = []
    for sdt, ev in scored[:UPCOMING_DASHBOARD_LIMIT]:
        d = sdt.date()
        out.append(
            {
                "id": ev.id,
                "title": ev.title,
                "time": _format_upcoming_when(d, ev.time),
                "tag": _event_type_label(ev.type),
                "type": (ev.type or "").lower() if ev.type else None,
                "event_on": ev.event_on.isoformat() if ev.event_on else None,
                "place": ev.place,
            }
        )
    return out


def build_dashboard(user_id: int, db: Session) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    status = calculate_status(user.last_menstrual_period)
    week = int(status["week"])
    total_weeks = 40
    days_left = max(0, int(status["days_to_due"]))
    progress = min(100.0, (week / total_weeks) * 100)

    baby_value, baby_hint, baby_size = _baby_summary_from_metadata(week, db)

    logs = db.query(DailyLog).filter(DailyLog.user_id == user_id).order_by(DailyLog.date.asc(), DailyLog.id.asc()).all()

    last_bp = next((l for l in reversed(logs) if l.systolic is not None and l.diastolic is not None), None)
    bp_value = f"{last_bp.systolic} / {last_bp.diastolic}" if last_bp else "— / —"
    if last_bp:
        bp_hint = (
            f"Son ölçüm · {last_bp.date.strftime('%d.%m.%Y')}"
            if last_bp.date
            else "Son ölçüm"
        )
    else:
        bp_hint = "Henüz kayıt yok"

    last_glucose = next((l for l in reversed(logs) if l.blood_glucose is not None), None)
    if last_glucose:
        glucose_value = f"{float(last_glucose.blood_glucose):g} mg/dL"
        glucose_hint = (
            f"Son ölçüm · {last_glucose.date.strftime('%d.%m.%Y')}"
            if last_glucose.date
            else "Son ölçüm"
        )
    else:
        glucose_value = "—"
        glucose_hint = "Henüz kayıt yok"

    weight_points = []
    for l in logs:
        if l.weight is None:
            continue
        pdays = (l.date - user.last_menstrual_period).days
        if pdays < 0:
            continue
        wk = min(40, pdays // 7 + 1)
        weight_points.append({"w": f"H{wk}", "kg": round(float(l.weight), 1)})

    if len(weight_points) > 7:
        weight_points = weight_points[-7:]

    gain_kg = 0.0
    if logs:
        last_w = next((l.weight for l in reversed(logs) if l.weight is not None), None)
        if last_w is not None:
            gain_kg = round(float(last_w) - float(user.starting_weight), 1)

    preview_name = user.name.strip().split()[0] if user.name else "Anne"

    upcoming = _dashboard_upcoming_events(user_id, db)

    return {
        "hero": {
            "subtitle": f"Merhaba {preview_name} 🌸",
            "headline": f"Bebeğine kavuşmana {days_left} gün kaldı",
            "week": week,
            "total_weeks": total_weeks,
            "days_left": days_left,
            "progress_percent": round(progress),
            "summary_text": _hero_summary_text(week, baby_size),
        },
        "summary_cards": {
            "baby": {
                "label": "Bebek Durumu",
                "value": baby_value,
                "hint": baby_hint,
            },
            "blood_pressure": {
                "label": "Son Tansiyon",
                "value": bp_value,
                "hint": bp_hint,
            },
            "blood_glucose": {
                "label": "Son Kan Şekeri",
                "value": glucose_value,
                "hint": glucose_hint,
            },
        },
        "weight_chart": weight_points,
        "weight_gain_label": f"{gain_kg:+.1f} kg toplam",
        "upcoming": upcoming,
        "pregnancy": status,
    }
