from sqlalchemy.orm import Session

from app.db.models import User
from app.modules.users.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_firebase_uid(self, firebase_uid: str) -> User | None:
        return self.db.query(User).filter(User.firebase_uid == firebase_uid).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_data: UserCreate) -> User:
        user = User(
            firebase_uid=user_data.firebase_uid,
            email=user_data.email,
            display_name=user_data.display_name,
            phone=user_data.phone,
            avatar_url=user_data.avatar_url,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, user_data: UserUpdate) -> User:
        if user_data.display_name is not None:
            user.display_name = user_data.display_name
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.avatar_url is not None:
            user.avatar_url = user_data.avatar_url

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def exists_by_firebase_uid(self, firebase_uid: str) -> bool:
        return self.db.query(User).filter(User.firebase_uid == firebase_uid).first() is not None

    def exists_by_email(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).first() is not None