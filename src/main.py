import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from users import router as router_user
from core import templates

app = FastAPI()

app.include_router(router_user)

@app.get(
    "/",
    name="main:index",
    response_class=HTMLResponse
)
def main_index() -> HTMLResponse:
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
