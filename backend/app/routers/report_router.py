from typing import Optional

from fastapi import APIRouter, Depends, Header
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services import auth_service, health_service, report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/pdf")
def generate_pdf(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    user_logs = health_service.list_daily_logs(user_id, db)
    for_pdf = [{**row, "note": row.get("notes")} for row in user_logs]
    pdf_content = report_service.generate_report_content(for_pdf)
    return StreamingResponse(iter([pdf_content]), media_type="application/pdf")
