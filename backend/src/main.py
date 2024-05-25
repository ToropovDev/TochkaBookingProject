from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.dialects.postgresql import UUID

from backend.src.auth.config import auth_backend
from backend.src.auth.models import User
from backend.src.auth.schemas import UserRead, UserCreate, UserUpdate
from backend.src.auth.manager import get_user_manager

from backend.src.teams.router import router as teams_router
from backend.src.games.router import router as games_router
from backend.src.fill_default import router as fill_default_router

app = FastAPI(
    title="Запись на игру",
    version="0.1",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(teams_router)
app.include_router(games_router)
app.include_router(fill_default_router)
