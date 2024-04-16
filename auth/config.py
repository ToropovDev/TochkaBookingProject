from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi_users import FastAPIUsers

from models import User
from base_config import JWT_SECRET

cookie_transport = CookieTransport(
    cookie_name="auth_token",
    cookie_max_age=3600,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=JWT_SECRET,
        lifetime_seconds=3600,
        algorithm="RS256"
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)


fastapi_users = FastAPIUsers[User, int](
    [auth_backend],
)

current_user = fastapi_users.current_user()
