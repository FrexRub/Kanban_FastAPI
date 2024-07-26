from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_async_session


async def get_user_db(
    session: Annotated[AsyncSession, Depends(get_async_session)], name: str
):
    pass
