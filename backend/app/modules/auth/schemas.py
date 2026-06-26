from pydantic import BaseModel


class AuthSyncRequest(BaseModel):
    id_token: str


class TokenResponse(BaseModel):
    user_id: int
    firebase_uid: str
    email: str
    display_name: str
    avatar_url: str | None