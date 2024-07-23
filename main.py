import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from users.routers import router as router_user
from core.config import templates

app = FastAPI()

app.include_router(router_user)


@app.get("/", name="main:index", response_class=HTMLResponse)
def main_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
