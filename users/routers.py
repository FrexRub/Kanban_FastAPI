import requests

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from aiohttp import ClientSession

from core.config import templates

# router = APIRouter(prefix="/users", tags=["User"])
router = APIRouter(tags=["User"])


@router.get("/", response_class=HTMLResponse)
def index_user():
    return "<h1> Hello </h1>"


@router.get("/registration", name="users:registration", response_class=HTMLResponse)
def registration_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="users/registration.html",
    )


@router.post("/regdata")
async def regdata(username=Form(), email=Form(), password=Form()):
    """
    Регистрация пользователя
    :param username:
    :param email:
    :param password:
    :return:
    """
    async with ClientSession() as session:
        url = "http://127.0.0.1:8000/auth/register"
        params = {
            "user": username,
            "password": password,
            "email": email,
        }
        async with session.post(url=url, json=params) as response:
            return_json = await response.json()
    return return_json
