from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.firebase import init_firebase
from app.db.database import init_db
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    init_firebase()
    yield


app = FastAPI(lifespan=lifespan)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Backend funcionando"}


@app.get("/health")
def health():
    return {"status": "healthy"}
