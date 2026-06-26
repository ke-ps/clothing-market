from sqlalchemy.orm import Session

from app.core.firebase import verify_firebase_token_sync
from app.db.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def sync_user_from_token(self, id_token: str) -> User:
        decoded_token = verify_firebase_token_sync(id_token)
        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture")

        if not firebase_uid or not email:
            raise ValueError("Token inválido: faltan uid o email")

        existing_user = self.repo.get_by_firebase_uid(firebase_uid)
        if existing_user:
            return existing_user

        user_data = UserCreate(
            firebase_uid=firebase_uid,
            email=email,
            display_name=name or email.split("@")[0],
            avatar_url=picture,
        )
        return self.repo.create(user_data)

    def get_me(self, user: User) -> UserResponse:
        return UserResponse.model_validate(user)

    def update_me(self, user: User, user_data: UserUpdate) -> UserResponse:
        updated_user = self.repo.update(user, user_data)
        return UserResponse.model_validate(updated_user)

    def delete_me(self, user: User) -> None:
        self.repo.delete(user)

    def get_public_profile(self, user_id: int) -> UserResponse | None:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)