from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_user_id
from app.models import DailyLog

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/pdf")
def export_pdf(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> StreamingResponse:
    rows = db.query(DailyLog).filter(DailyLog.user_id == user_id).order_by(desc(DailyLog.date_time)).limit(50).all()
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
    pdf_canvas.drawString(50, 800, "Gebelik Takibi - Teknik Veri Raporu")
    y = 770
    for row in rows:
        blood_pressure = f"{row.systolic}/{row.diastolic}" if row.systolic and row.diastolic else "-"
        line = f"{row.date_time.strftime('%Y-%m-%d %H:%M')} Kilo:{row.weight or '-'} Tansiyon:{blood_pressure}"
        pdf_canvas.drawString(50, y, line[:120])
        y -= 18
        if y < 60:
            pdf_canvas.showPage()
            y = 800
    pdf_canvas.save()
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=gebelik-rapor.pdf"},
    )
