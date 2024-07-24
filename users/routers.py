from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from aiohttp import ClientSession

from core.config import templates

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", response_class=HTMLResponse)
def index_user():
    return "<h1> Hello </h1>"


@router.get("/registration", name="users:registration", response_class=HTMLResponse)
def registration_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="users/registration.html",
    )


@router.post("/postdata")
async def postdata(username=Form(), email=Form(), password=Form()):
    async with ClientSession() as session:
        url = 'http://127.0.0.1:8000/auth/register'
        params = {'username': username, 'email': email, 'password': password}

        async with session.post(
                url=url,
                data=params,
                headers={"Content-Type": "application/json"}
        ) as response:
            return_json = await response.json()
    return return_json


@router.post("/regdata")
def regdata(username=Form(), email=Form()):
    return {"name": username, "email": email}
