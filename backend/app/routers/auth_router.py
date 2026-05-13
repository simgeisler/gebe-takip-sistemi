from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.entities import Token, User
from ..schemas.auth import LoginRequest, RegisterRequest, UserProfileUpdate
from ..services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(payload, db=db)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(payload, db=db)


@router.post("/logout")
def logout(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    return auth_service.logout_user(authorization, db=db)


@router.get("/me")
def me(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    return auth_service.serialize_user(user)


@router.patch("/me")
def patch_me(payload: UserProfileUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return auth_service.update_profile(user_id, payload, db=db)


@router.delete("/me")
def delete_me(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    db.query(Token).filter(Token.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"message": "Hesabınız başarıyla silindi"}


@router.get("/users")
def list_users(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    return {
        "users": [
            auth_service.serialize_user(user),
        ]
    }


@router.get("/users/{user_id}")
def get_user(user_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    current_user_id = auth_service.resolve_token(authorization, db=db)
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Erişim reddedildi.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    return auth_service.serialize_user(user)
