from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", response_class=HTMLResponse)
def index_user():
    return "<h1> Hello </h1>"
