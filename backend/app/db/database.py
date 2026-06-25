import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

HOST: str = os.getenv("HOST", "localhost")
PORT: str = os.getenv("PORT", "3306")
DB: str = os.getenv("DB", "clothing_market")
USER: str = os.getenv("USER", "root")
PASSWORD: str = os.getenv("PASSWORD", "")

DATABASE_URL: str = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(DATABASE_URL, echo=False,  pool_pre_ping=True)

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
