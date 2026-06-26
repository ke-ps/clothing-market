from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.firebase import verify_firebase_token_sync
from app.db.database import get_db
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserResponse


security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserResponse:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        decoded_token = verify_firebase_token_sync(credentials.credentials)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    firebase_uid = decoded_token.get("uid")
    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: sin uid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repo = UserRepository(db)
    user = user_repo.get_by_firebase_uid(firebase_uid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado en la base de datos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse.model_validate(user)


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserResponse | None:
    if credentials is None:
        return None

    try:
        decoded_token = verify_firebase_token_sync(credentials.credentials)
    except ValueError:
        return None

    firebase_uid = decoded_token.get("uid")
    if not firebase_uid:
        return None

    user_repo = UserRepository(db)
    user = user_repo.get_by_firebase_uid(firebase_uid)

    if not user:
        return None

    return UserResponse.model_validate(user)