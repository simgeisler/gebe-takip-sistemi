from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.entities import User
from ..services import auth_service, health_service, report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/pdf")
def generate_pdf(
    start_date: date = Query(..., description="Rapor başlangıç tarihi (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Rapor bitiş tarihi (YYYY-MM-DD)"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user_id = auth_service.resolve_token(authorization, db=db)
    user_logs = health_service.list_daily_logs_in_range(user_id, db, start_date, end_date)

    if not user_logs:
        raise HTTPException(
            status_code=404,
            detail="Seçilen tarih aralığında sağlık kaydı bulunamadı.",
        )

    user = db.query(User).filter(User.id == user_id).first()
    user_name = user.name if user else None

    pdf_content = report_service.generate_report_pdf(
        user_logs, start_date, end_date, user_name=user_name
    )
    filename = f"saglik-raporu_{start_date.isoformat()}_{end_date.isoformat()}.pdf"

    return StreamingResponse(
        iter([pdf_content]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
