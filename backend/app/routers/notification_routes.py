from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_user_id
from app.models import FCMToken
from app.schemas import RegisterFCMTokenRequest, UpdateFCMTokenRequest

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/fcm-token")
def register_fcm_token(
    payload: RegisterFCMTokenRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    existing = db.query(FCMToken).filter(FCMToken.token == payload.token).first()
    if not existing:
        db.add(FCMToken(user_id=user_id, token=payload.token))
        db.commit()
    return {"ok": True}


@router.get("/fcm-token")
def list_fcm_tokens(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> list[dict[str, str | int]]:
    rows = db.query(FCMToken).filter(FCMToken.user_id == user_id).all()
    return [{"id": row.id, "token": row.token, "created_at": row.created_at.isoformat()} for row in rows]


@router.get("/fcm-token/{token_id}")
def get_fcm_token(token_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, str | int]:
    row = db.get(FCMToken, token_id)
    if not row or row.user_id != user_id:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"id": row.id, "token": row.token, "created_at": row.created_at.isoformat()}


@router.put("/fcm-token/{token_id}")
def update_fcm_token(
    token_id: int, payload: UpdateFCMTokenRequest, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)
) -> dict[str, bool]:
    row = db.get(FCMToken, token_id)
    if not row or row.user_id != user_id:
        raise HTTPException(status_code=404, detail="Token not found")
    duplicate = db.query(FCMToken).filter(FCMToken.token == payload.token, FCMToken.id != token_id).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Token already registered")
    row.token = payload.token
    db.commit()
    return {"ok": True}


@router.delete("/fcm-token/{token_id}")
def delete_fcm_token(token_id: int, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    row = db.get(FCMToken, token_id)
    if not row or row.user_id != user_id:
        raise HTTPException(status_code=404, detail="Token not found")
    db.delete(row)
    db.commit()
    return {"ok": True}
