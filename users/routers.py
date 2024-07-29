from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import templates, lifetime_seconds
from core.exceptions import ExceptDB
from users.crud import get_user_from_db, add_user_to_db
from users.models import User
from core.database import get_async_session
from auth.utils import validate_password, create_hash_password, encode_jwt, set_cookie
from auth.dependencies import current_active_user


router = APIRouter(prefix="/users", tags=["User"])


@router.get("/registration", name="users:registration", response_class=HTMLResponse)
def registration_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="users/registration.html",
    )


@router.post("/regdata", response_class=JSONResponse)
async def regdata(
        username=Form(),
        email=Form(),
        password=Form(),
        session: AsyncSession = Depends(get_async_session),
):
    hash_password = create_hash_password(password).decode()
    user: User = User(
        user=username,
        email=email,
        hashed_password=hash_password,
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )
    try:
        id: int = await add_user_to_db(session=session, user=user)
    except ExceptDB as exc:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid add user in DB: {exc}"
            )
    else:
        return {"id": id}


@router.post("/login", name="users:login", response_class=JSONResponse)
async def login(
        data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session),
):
    username = data.username
    password = data.password
    user: User = await get_user_from_db(name=username, session=session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {username} not found",
        )

    if not validate_password(
            password=password,
            hashed_password=user.hashed_password.encode(),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error password for login: {username}",
        )

    payload = dict()
    payload["sub"] = str(user.id)
    payload["aud"] = ["fastapi-users:auth"]
    expire = datetime.now(timezone.utc) + timedelta(seconds=lifetime_seconds)
    payload["exp"] = expire
    access_token = encode_jwt(payload)

    resp = RedirectResponse(url="/users/protected-route", status_code=status.HTTP_302_FOUND)
    set_cookie(resp, access_token)
    return resp


@router.get("/protected-route")
async def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"

# @router.post("/regdata")
# async def regdata(username=Form(), email=Form(), password=Form()):
#     """
#     Регистрация пользователя
#     :param username:
#     :param email:
#     :param password:
#     :return:
#     """
#     async with ClientSession() as session:
#         url = "http://127.0.0.1:8000/auth/register"
#         params = {
#             "user": username,
#             "password": password,
#             "email": email,
#         }
#         async with session.post(url=url, json=params) as response:
#             return_json = await response.json()
#     return return_json
