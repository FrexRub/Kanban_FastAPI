from datetime import datetime, timedelta, timezone
import uvicorn
from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_users import FastAPIUsers
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager  # Loginmanager Class
from fastapi_login.exceptions import InvalidCredentialsException  # Exception class

from users.routers import router as router_user
from core.config import templates, SECRET, lifetime_seconds
from users.models import User
from auth import get_user_manager, auth_backend, UserRead, UserCreate, UserUpdate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.include_router(router_user)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
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

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)


# manager = LoginManager(SECRET, token_url="/auth/token", use_cookie=True)
# manager.cookie_name = "bonds"
#
# fake_db = {"johndoe@e.mail": {"password": "hunter2"}}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/", name="main:index", response_class=HTMLResponse)
def main_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user


@app.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException
    """
    {
  "sub": "1",
  "aud": [
    "fastapi-users:auth"
  ],
  "exp": 1721981657
}
    
    data = {"sub": str(user.id), "aud": ["fastapi-users:auth"]}
    
    payload = data.copy()
    if lifetime_seconds:
        expire = datetime.now(timezone.utc) + timedelta(seconds=lifetime_seconds)
        payload["exp"] = expire
    
    """
    payload = dict()
    # payload["sub"] = str(user.id)
    # payload["sub"] = username
    # payload["aud"] = ["fastapi-users:auth"]
    # expire = datetime.now(timezone.utc) + timedelta(seconds=lifetime_seconds)
    # payload["exp"] = expire

    access_token = manager.create_access_token(data={"sub": username})
    # access_token = manager.create_access_token(data={"sub": username})
    # access_token = manager.create_access_token(data=payload)
    resp = RedirectResponse(url="/private", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.get("/private")
def getPrivateendpoint(_=Depends(manager)):
    return "You are an authentciated user"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
