from pathlib import Path
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic_settings import BaseSettings

templates = Jinja2Templates("templates")


BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "kanban.db"


class DbSetting(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False


class Setting(BaseSettings):
    db: DbSetting = DbSetting()


setting = Setting()
