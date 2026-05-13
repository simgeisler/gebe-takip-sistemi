from datetime import datetime, timedelta
from os import getenv
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..core.pregnancy import due_date_from_lmp
from ..core.security import create_access_token, hash_password, verify_password
from ..models.entities import User, Token
from ..schemas.auth import LoginRequest, RegisterRequest, UserProfileUpdate


def _normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def _user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "last_menstrual_period": user.last_menstrual_period.isoformat() if user.last_menstrual_period else None,
        "expected_due_date": user.expected_due_date.isoformat() if user.expected_due_date else None,
        "starting_weight": user.starting_weight,
        "is_app_owner": bool(getattr(user, "is_app_owner", False)),
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def serialize_user(user: User) -> dict:
    return _user_to_dict(user)


def user_is_library_owner(user: User) -> bool:
    if getattr(user, "is_app_owner", False):
        return True
    raw = getenv("APP_OWNER_EMAILS", "") or ""
    allowed = {e.strip().lower() for e in raw.split(",") if e.strip()}
    return bool(user.email and user.email.lower() in allowed)


def ensure_library_owner(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    if not user_is_library_owner(user):
        raise HTTPException(
            status_code=403,
            detail="Kütüphane içeriğini yalnızca uygulama yöneticisi ekleyebilir veya düzenleyebilir.",
        )
    return user


def register_user(payload: RegisterRequest, db: Session) -> dict:
    email_norm = _normalize_email(str(payload.email))
    existing_user = db.query(User).filter(func.lower(User.email) == email_norm).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Bu e-posta zaten kayıtlı")
    
    # Handle string dates
    lmp = None
    if payload.sat:
        if isinstance(payload.sat, str):
            try:
                lmp = datetime.strptime(payload.sat, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="SAT formatı hatalı. YYYY-MM-DD olmalı.")
        else:
            lmp = payload.sat
    
    if payload.expected_due_date and not lmp:
        if isinstance(payload.expected_due_date, str):
            try:
                lmp = datetime.strptime(payload.expected_due_date, "%Y-%m-%d").date() - timedelta(days=280)
            except ValueError:
                raise HTTPException(status_code=400, detail="Dogum tarihi formatı hatalı. YYYY-MM-DD olmalı.")
        else:
            lmp = payload.expected_due_date - timedelta(days=280)
    
    if not lmp:
        raise HTTPException(status_code=400, detail="SAT veya beklenen dogum tarihi gerekli.")
    
    user = User(
        name=payload.name,
        email=email_norm,
        password_hash=hash_password(payload.password),
        last_menstrual_period=lmp,
        expected_due_date=due_date_from_lmp(lmp),
        starting_weight=payload.kilo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token(user.id)
    db_token = Token(token=token, user_id=user.id)
    db.add(db_token)
    db.commit()
    
    return {"access_token": token, "token_type": "bearer", "user": _user_to_dict(user)}


def login_user(payload: LoginRequest, db: Session) -> dict:
    email_norm = _normalize_email(str(payload.email))
    user = db.query(User).filter(func.lower(User.email) == email_norm).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Hatalı e-posta veya şifre")
    token = create_access_token(user.id)
    db_token = Token(token=token, user_id=user.id)
    db.add(db_token)
    db.commit()
    return {"access_token": token, "token_type": "bearer", "user_name": user.name}


def resolve_token(authorization: Optional[str], db: Session) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Yetkisiz erisim.")
    token = authorization.replace("Bearer ", "")
    db_token = db.query(Token).filter(Token.token == token).first()
    if not db_token:
        raise HTTPException(status_code=401, detail="Gecersiz token.")
    return db_token.user_id


def update_profile(user_id: int, payload: UserProfileUpdate, db: Session) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    
    patch = payload.model_dump(exclude_unset=True, by_alias=False)
    if not patch:
        raise HTTPException(status_code=400, detail="Güncellenecek alan yok.")
    
    # Handle aliased fields
    if "sat" in patch:
        patch["last_menstrual_period"] = patch.pop("sat")
        patch["expected_due_date"] = due_date_from_lmp(patch["last_menstrual_period"])
    if "kilo" in patch:
        patch["starting_weight"] = patch.pop("kilo")
    
    for key, value in patch.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return _user_to_dict(user)


def logout_user(authorization: Optional[str], db: Session) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        return {"ok": True}
    token = authorization.replace("Bearer ", "")
    db_token = db.query(Token).filter(Token.token == token).first()
    if db_token:
        db.delete(db_token)
        db.commit()
    return {"ok": True}
