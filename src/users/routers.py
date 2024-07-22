from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

from src.core import templates

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", response_class=HTMLResponse)
def index_user():
    return "<h1> Hello </h1>"


@router.get(
    "/registration",
    name="users:registration",
    response_class=HTMLResponse
)
def registration_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="users/registration.html",
    )


@router.post("/postdata")
def postdata(username=Form(), userage=Form()):
    return {"name": username, "age": userage}
