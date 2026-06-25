import os
from typing import Generator
from urllib.parse import quote

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

HOST: str = os.getenv("HOST", "localhost")
PORT: str = os.getenv("PORT", "3306")
DB: str = os.getenv("DB", "clothing_market")
USER: str = os.getenv("USER", "root")
PASSWORD: str = os.getenv("PASSWORD", "")
CHARSET: str = os.getenv("CHARSET", "utf8mb4")
SSL_CA: str | None = os.getenv("SSL_CA")
CONNECT_TIMEOUT: int = int(os.getenv("CONNECT_TIMEOUT", "10"))
READ_TIMEOUT: int = int(os.getenv("READ_TIMEOUT", "10"))
WRITE_TIMEOUT: int = int(os.getenv("WRITE_TIMEOUT", "10"))

DATABASE_URL: str = (
    f"mysql+pymysql://{quote(USER)}:{quote(PASSWORD)}@{HOST}:{PORT}/{DB}?charset={CHARSET}"
)

connect_args: dict = {
    "connect_timeout": CONNECT_TIMEOUT,
    "read_timeout": READ_TIMEOUT,
    "write_timeout": WRITE_TIMEOUT,
}

if SSL_CA:
    connect_args["ssl"] = {"ca": SSL_CA}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
