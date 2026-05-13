"""Dashboard.tsx bölümleriyle aynı yapıda özet (hero, summary_cards, weight_chart, upcoming)."""

import re
from calendar import monthrange
from datetime import date, datetime, time as time_cls

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..core.pregnancy import calculate_status
from ..models.entities import CalendarEvent, DailyLog, User, WeeklyMetadata

UPCOMING_DASHBOARD_LIMIT = 2

_TYPE_LABEL = {"ilac": "İlaç", "randevu": "Randevu", "etkinlik": "Etkinlik"}


def _comparison_for_week(week: int) -> str:
    if week <= 12:
        return "nar"
    if week <= 20:
        return "limon"
    if week <= 28:
        return "patlıcan"
    if week <= 36:
        return "marul"
    return "karpuz"


def _fmt_kg(weight_gr: int) -> str:
    kg = weight_gr / 1000
    if kg >= 1:
        return f"~ {kg:.1f} kg"
    return f"~ {weight_gr} g"


def _parse_first_number(value: str | None) -> float | None:
    if not value:
        return None
    m = re.search(r"(\d+(?:[.,]\d+)?)", value)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


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

    baby_weight_gr = int(week * 32)
    baby_cm = float(round(week * 0.95, 1))
    meta = db.query(WeeklyMetadata).filter(WeeklyMetadata.week_number == min(week, 42)).first()
    if meta:
        w = _parse_first_number(meta.baby_weight)
        if w is not None:
            if "kg" in (meta.baby_weight or "").lower():
                baby_weight_gr = int(w * 1000)
            else:
                baby_weight_gr = int(w)
        l = _parse_first_number(meta.baby_length)
        if l is not None:
            baby_cm = float(l)

    logs = db.query(DailyLog).filter(DailyLog.user_id == user_id).order_by(DailyLog.date.asc(), DailyLog.id.asc()).all()

    last_bp = next((l for l in reversed(logs) if l.systolic is not None and l.diastolic is not None), None)
    bp_value = f"{last_bp.systolic} / {last_bp.diastolic}" if last_bp else "— / —"
    bp_hint = "Son ölçüm" if last_bp else "Henüz kayıt yok"

    last_water = next((l for l in reversed(logs) if l.water_liters is not None), None)
    water_liters = float(last_water.water_liters) if last_water else 1.8
    water_goal = 2.5

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
    fruit = _comparison_for_week(week)

    upcoming = _dashboard_upcoming_events(user_id, db)

    return {
        "hero": {
            "subtitle": f"Merhaba {preview_name} 🌸",
            "headline": f"Bebeğine kavuşmana {days_left} gün kaldı",
            "week": week,
            "total_weeks": total_weeks,
            "days_left": days_left,
            "progress_percent": round(progress),
            "summary_text": (
                f"Şu an {week}. haftadasın. Bebeğin bir {fruit} büyüklüğünde "
                f"ve seni duyabiliyor 💛"
            ),
        },
        "summary_cards": {
            "baby": {
                "label": "Bebek Durumu",
                "value": _fmt_kg(baby_weight_gr),
                "hint": f"Boy: {baby_cm:.0f} cm",
            },
            "blood_pressure": {
                "label": "Son Tansiyon",
                "value": bp_value,
                "hint": bp_hint,
            },
            "water": {
                "label": "Bugünkü Su",
                "value": f"{water_liters} L",
                "hint": f"Hedef: {water_goal} L",
            },
        },
        "weight_chart": weight_points,
        "weight_gain_label": f"{gain_kg:+.1f} kg toplam",
        "upcoming": upcoming,
        "pregnancy": status,
    }
