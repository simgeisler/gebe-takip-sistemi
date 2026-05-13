from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..core.pregnancy import calculate_status
from ..core.database import get_db
from ..models.entities import User
from ..services import auth_service, ui_service

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def get_dashboard_payload(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Web arayüzü Dashboard.tsx ile uyumlu özet JSON."""
    user_id = auth_service.resolve_token(authorization, db=db)
    return ui_service.build_dashboard(user_id, db)


@router.get("/get-current-status")
def get_current_status_legacy(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    return calculate_status(user.last_menstrual_period)


@router.get("/pregnancy/status")
def get_pregnancy_status(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Hamilelik hesap özeti (önceki endpoint ile aynı çıktı)."""
    user_id = auth_service.resolve_token(authorization, db=db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    return calculate_status(user.last_menstrual_period)
