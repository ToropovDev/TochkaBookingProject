from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from sqlalchemy.dialects.postgresql import UUID

from auth.config import auth_backend
from auth.models import User
from auth.schemas import UserRead, UserCreate
from auth.manager import get_user_manager

from database import create_db_and_tables

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
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup():
    await create_db_and_tables()