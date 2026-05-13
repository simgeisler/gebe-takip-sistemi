from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.health import (
    ContractionAnalysisRequest,
    KickSessionRequest,
    KickSessionUpdateRequest,
)
from ..services import auth_service, health_service

router = APIRouter(prefix="/wellbeing", tags=["wellbeing"])


@router.post("/kick-sessions")
def add_kick_session(payload: KickSessionRequest, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return health_service.create_kick_session(user_id, payload, db)


@router.get("/kick-sessions")
def list_kick_sessions(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return health_service.list_kick_sessions(user_id, db)


@router.get("/kick-sessions/{session_id}")
def get_kick_session(session_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return health_service.get_kick_session(user_id, session_id, db)


@router.put("/kick-sessions/{session_id}")
def update_kick_session(
    session_id: int, payload: KickSessionUpdateRequest, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    user_id = auth_service.resolve_token(authorization, db=db)
    return health_service.update_kick_session(user_id, session_id, payload, db)


@router.delete("/kick-sessions/{session_id}")
def delete_kick_session(session_id: int, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_id = auth_service.resolve_token(authorization, db=db)
    return health_service.delete_kick_session(user_id, session_id, db)


@router.post("/contractions/analyze")
def analyze_contraction(payload: ContractionAnalysisRequest, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    auth_service.resolve_token(authorization, db=db)
    return health_service.analyze_contraction(payload)
