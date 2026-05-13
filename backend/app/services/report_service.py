def generate_report_content(user_logs: list[dict]) -> bytes:
    rows = sorted(user_logs, key=lambda r: (str(r.get("date") or ""), r.get("id") or 0))
    content = "Gebelik Takip Raporu\n\n" + "\n".join(
        [
            f"{row['date']} | kilo={row.get('weight')} | tansiyon={row.get('systolic')}/{row.get('diastolic')} | not={row.get('note')}"
            for row in rows
        ]
    )
    return f"%PDF-1.4\n{content}\n%%EOF".encode("utf-8")
