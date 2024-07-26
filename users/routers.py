import requests

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from aiohttp import ClientSession

from core.config import templates

# router = APIRouter(prefix="/users", tags=["User"])
router = APIRouter(tags=["User"])


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


@router.post("/test", response_class=JSONResponse)
# async def test(username=Form(), password=Form()):
def test():
    """
    Вход (логинг) в приложение
    :param username:
    :param password:
    :return:
    """
    data = {"username": "user1@example.com", "password": "1qaz!QAZ"}
    # r = requests.post(
    #     "http://127.0.0.1:8000/auth/jwt/login",
    #     auth=("user1@example.com", "1qaz!QAZ"),
    #     verify=False,
    # )
    r = requests.post("http://127.0.0.1:8000/auth/jwt/login", data=data)
    print(r.status_code)
    # async with ClientSession() as session:
    #     url = "http://127.0.0.1:8000/auth/jwt/login"
    #     async with session.post(url=url, data=data) as response:
    #         # return_json = await response.json(content_type=None)
    #         print(response.status)
    #         # return_json = await response.text()
    return "Ok"
