from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import CookieTransport

from users.models import User, get_user_db
from .strategies import get_jwt_strategy

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# BearerTransport

# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
#
# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )


# Использование Cookie

cookie_transport = CookieTransport(
    cookie_name="bonds",
    cookie_max_age=3600,
)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
