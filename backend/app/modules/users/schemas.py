from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    avatar_url: Optional[str] = Field(default=None, max_length=512)


class UserCreate(UserBase):
    firebase_uid: str = Field(min_length=1, max_length=128)


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    avatar_url: Optional[str] = Field(default=None, max_length=512)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    firebase_uid: str
    created_at: datetime
    updated_at: datetime


class PublicProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str
    avatar_url: Optional[str]
    created_at: datetime