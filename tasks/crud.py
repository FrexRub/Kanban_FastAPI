from typing import TYPE_CHECKING
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Result

from tasks.models import Task
from tasks.schemas import TaskOut
from users.crud import get_user_from_db
from core.config import configure_logging
from core.exceptions import ExceptDB

if TYPE_CHECKING:
    from users.models import User


configure_logging(logging.INFO)
logger = logging.getLogger(__name__)


async def get_all_tasks_user(session: AsyncSession, username: str) -> list[TaskOut]:
    user: User = await get_user_from_db(session=session, name=username)
    logger.info("Start find all tasks user: %s", username)
    stmt = select(Task).where(Task.user_id == user.id)
    try:
        result: Result = await session.execute(stmt)
        user_tasks: list[TaskOut] = result.scalars().all()
    except SQLAlchemyError as exp:
        logger.exception("Error find all tasks user %s", username)
        raise ExceptDB("Error in DB")
    else:
        return user_tasks
