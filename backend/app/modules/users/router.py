from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.modules.users.schemas import UserResponse, UserUpdate
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    user_data: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    user = service.update_me(current_user, user_data)
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    service.delete_me(current_user)


@router.get("/{user_id}", response_model=UserResponse)
def get_public_profile(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_public_profile(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user