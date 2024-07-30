import logging

from pathlib import Path
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic_settings import BaseSettings

templates = Jinja2Templates("templates")

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "kanban.db"

SECRET = "secret-key"
lifetime_seconds = 3600
COOKIE_NAME = "bonds"


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )


class DbSetting(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "serts" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "serts" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_day: int = 30


class Setting(BaseSettings):
    db: DbSetting = DbSetting()
    auth_jwt: AuthJWT = AuthJWT()


setting = Setting()
