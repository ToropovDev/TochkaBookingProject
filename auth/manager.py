from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
import smtplib

from base_config import USER_MANAGER_SECRET
from auth.models import User
from auth.utils import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_MANAGER_SECRET
    verification_token_secret = USER_MANAGER_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
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
            self, user: User, token: str, request: Optional[Request] = None
    ):
        await send_email(user.email, token)
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        await send_email(user.email, token)
        print(f"User {user.id} has forgot their password. Reset token: {token}")


async def send_email(email, text):
    sender = "ToropovDevTochkaProject@yandex.ru"
    sender_password = "ToropovDevTochkaProjectPass"
    mail_lib = smtplib.SMTP("smtp.yandex.ru", 465)
    mail_lib.login(sender, sender_password)
    msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
        sender, email, 'Тема сообщения')
    msg += text
    mail_lib.sendmail(sender, email, msg.encode('utf-8'))
    mail_lib.quit()


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

