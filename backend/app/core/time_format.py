from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo

    TR_TZ = ZoneInfo("Europe/Istanbul")
except Exception:
    TR_TZ = timezone(timedelta(hours=3))


def format_relative_time_tr(dt: datetime | None, now: datetime | None = None) -> str:
    """Bugun saat / Dun saat / tam tarih-saat."""
    if dt is None:
        return ""

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    dt_local = dt.astimezone(TR_TZ)
    now_local = now.astimezone(TR_TZ)

    start_of_today = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_yesterday = start_of_today - timedelta(days=1)
    clock = dt_local.strftime("%H:%M")

    if dt_local >= start_of_today:
        return f"Bugün saat {clock}"

    if start_of_yesterday <= dt_local < start_of_today:
        return f"Dün saat {clock}"

    return dt_local.strftime("%d.%m.%Y %H:%M")
