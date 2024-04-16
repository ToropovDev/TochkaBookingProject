from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    id: int
    email: str
    role_id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
