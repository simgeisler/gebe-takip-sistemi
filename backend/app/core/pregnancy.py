from datetime import date, datetime, timedelta, timezone

from fastapi import HTTPException


def get_today() -> date:
    return datetime.now(timezone.utc).date()


def due_date_from_lmp(last_menstrual_period: date) -> date:
    return last_menstrual_period + timedelta(days=280)


def calculate_status(last_menstrual_period: date) -> dict:
    today = get_today()
    pregnancy_days = (today - last_menstrual_period).days
    if pregnancy_days < 0:
        raise HTTPException(status_code=400, detail="SAT gelecekte olamaz.")
    week = pregnancy_days // 7 + 1
    day = pregnancy_days % 7
    due_date = due_date_from_lmp(last_menstrual_period)
    days_to_due = (due_date - today).days
    trimester = 1 if week <= 13 else 2 if week <= 26 else 3
    return {
        "pregnancy_day": pregnancy_days,
        "week": week if week <= 40 else 40,
        "week_label": f"{week if week <= 40 else '40+'} hafta {day} gun",
        "trimester": trimester,
        "days_to_due": days_to_due,
        "is_overdue": week > 40,
        "due_date": due_date.isoformat(),
    }
