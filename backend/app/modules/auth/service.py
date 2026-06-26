from sqlalchemy.orm import Session

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserResponse
from app.modules.auth.schemas import TokenResponse
from app.core.firebase import verify_firebase_token_sync


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def sync_user(self, id_token: str) -> TokenResponse:
        decoded_token = verify_firebase_token_sync(id_token)
        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture")

        if not firebase_uid or not email:
            raise ValueError("Token inválido: faltan uid o email")

        existing_user = self.user_repo.get_by_firebase_uid(firebase_uid)
        if existing_user:
            return TokenResponse(
                user_id=existing_user.id,
                firebase_uid=existing_user.firebase_uid,
                email=existing_user.email,
                display_name=existing_user.display_name,
                avatar_url=existing_user.avatar_url,
            )

        user_data = UserCreate(
            firebase_uid=firebase_uid,
            email=email,
            display_name=name or email.split("@")[0],
            avatar_url=picture,
        )
        new_user = self.user_repo.create(user_data)

        return TokenResponse(
            user_id=new_user.id,
            firebase_uid=new_user.firebase_uid,
            email=new_user.email,
            display_name=new_user.display_name,
            avatar_url=new_user.avatar_url,
        )