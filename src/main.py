from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from sqlalchemy.dialects.postgresql import UUID

from src.auth.config import auth_backend
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.manager import get_user_manager

from src.teams.router import router as teams_router
from src.games.router import router as games_router

app = FastAPI(
    title="Запись на игру",
    version="0.1",
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
