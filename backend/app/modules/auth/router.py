from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.schemas import AuthSyncRequest, TokenResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sync", response_model=TokenResponse)
def sync_user(request: AuthSyncRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.sync_user(request.id_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))