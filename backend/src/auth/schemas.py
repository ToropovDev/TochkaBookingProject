from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    id: int
    email: str
    games_played: int = 0
    games_organized: int = 0
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    games_played: int
    games_organized: int
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: str
    games_played: int
    games_organized: int
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
