import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    HOST: str = Field(default="localhost")
    PORT: int = Field(default=8000)

    DATABASE_HOST: str = Field(default="localhost")
    DATABASE_PORT: int = Field(default=3306)
    DATABASE_NAME: str = Field(default="clothing_market")
    DATABASE_USER: str = Field(default="root")
    DATABASE_PASSWORD: str = Field(default="")
    DATABASE_CHARSET: str = Field(default="utf8mb4")
    DATABASE_SSL_CA: Optional[str] = Field(default=None)
    DATABASE_CONNECT_TIMEOUT: int = Field(default=10)
    DATABASE_READ_TIMEOUT: int = Field(default=10)
    DATABASE_WRITE_TIMEOUT: int = Field(default=10)

    FIREBASE_PROJECT_ID: str = Field(default="")
    FIREBASE_PRIVATE_KEY_ID: str = Field(default="")
    FIREBASE_PRIVATE_KEY: str = Field(default="")
    FIREBASE_CLIENT_EMAIL: str = Field(default="")
    FIREBASE_CLIENT_ID: str = Field(default="")
    FIREBASE_AUTH_URI: str = Field(default="https://accounts.google.com/o/oauth2/auth")
    FIREBASE_TOKEN_URI: str = Field(default="https://oauth2.googleapis.com/token")
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str = Field(
        default="https://www.googleapis.com/oauth2/v1/certs"
    )
    FIREBASE_CLIENT_X509_CERT_URL: str = Field(default="")

    CLOUDINARY_CLOUD_NAME: str = Field(default="")
    CLOUDINARY_API_KEY: str = Field(default="")
    CLOUDINARY_API_SECRET: str = Field(default="")

    CORS_ORIGINS: list[str] = Field(default=["http://localhost:4200"])

    @property
    def database_url(self) -> str:
        from urllib.parse import quote

        password = quote(self.DATABASE_PASSWORD) if self.DATABASE_PASSWORD else ""
        user_pass = f"{quote(self.DATABASE_USER)}:{password}" if password else quote(self.DATABASE_USER)
        url = f"mysql+pymysql://{user_pass}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?charset={self.DATABASE_CHARSET}"
        return url

    @property
    def firebase_credentials_dict(self) -> dict:
        private_key = self.FIREBASE_PRIVATE_KEY.replace("\\n", "\n")
        return {
            "type": "service_account",
            "project_id": self.FIREBASE_PROJECT_ID,
            "private_key_id": self.FIREBASE_PRIVATE_KEY_ID,
            "private_key": private_key,
            "client_email": self.FIREBASE_CLIENT_EMAIL,
            "client_id": self.FIREBASE_CLIENT_ID,
            "auth_uri": self.FIREBASE_AUTH_URI,
            "token_uri": self.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": self.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": self.FIREBASE_CLIENT_X509_CERT_URL,
            "universe_domain": "googleapis.com",
        }

    def is_firebase_configured(self) -> bool:
        return bool(
            self.FIREBASE_PROJECT_ID
            and self.FIREBASE_PRIVATE_KEY
            and self.FIREBASE_CLIENT_EMAIL
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()