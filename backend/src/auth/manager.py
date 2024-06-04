from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from backend.src.base_config import USER_MANAGER_SECRET
from backend.src.auth.models import User
from backend.src.auth.utils import get_user_db
from backend.src.scheduler.clr import send_email_verify


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_MANAGER_SECRET
    verification_token_secret = USER_MANAGER_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None) -> None:
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict['role_id'] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ) -> None:
        send_email_verify.delay(user.username, user.email, token, "Подтверждение аккаунта")
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_forgot_password(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ) -> None:
        send_email_verify.delay(user.username, user.email, token, "Восстановление пароля")
        print(f"User {user.id} has forgot their password. Reset token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
