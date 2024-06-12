from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi_users import FastAPIUsers
from typing import Generic

from fastapi import Response, status

from fastapi_users import models
from fastapi_users.authentication.strategy import Strategy
from backend.src.auth.models import User
from backend.src.auth.manager import get_user_manager
from backend.src.base_config import JWT_SECRET


class Transport(CookieTransport):
    def _set_login_cookie(self, response: Response, token: str) -> Response:
        response.set_cookie(
            self.cookie_name,
            token,
            max_age=self.cookie_max_age,
            path=self.cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )
        return response


cookie_transport = Transport(
    cookie_name="auth_token",
    cookie_max_age=3600,
    cookie_path="/",
    cookie_httponly=True,
    cookie_secure=False,
    cookie_samesite="lax",
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=JWT_SECRET,
        lifetime_seconds=3600,
    )


class Backend(AuthenticationBackend):
    async def login(
        self, strategy: Strategy[models.UP, models.ID], user: models.UP
    ) -> Response:
        token = await strategy.write_token(user)
        return await self.transport.get_login_response(token)


auth_backend = Backend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(verified=True)
current_superuser = fastapi_users.current_user(superuser=True)
