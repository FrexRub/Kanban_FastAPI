import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi_users import FastAPIUsers

from users.routers import router as router_user
from core.config import templates
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


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/", name="main:index", response_class=HTMLResponse)
def main_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
