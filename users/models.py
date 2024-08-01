from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Base, get_async_session

if TYPE_CHECKING:
    from tasks.models import Task


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[str]

    tasks: Mapped["Task"] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
