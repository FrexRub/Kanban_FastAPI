from typing import TYPE_CHECKING
import logging

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Result

from tasks.models import Task
from tasks.schemas import TaskCreate, TaskRead, TaskOut
from users.crud import get_user_from_db
from core.config import configure_logging
from core.exceptions import ExceptDB

if TYPE_CHECKING:
    from users.models import User


configure_logging(logging.INFO)
logger = logging.getLogger(__name__)


async def get_all_tasks_user(session: AsyncSession, username: str) -> list[TaskRead]:
    user: User = await get_user_from_db(session=session, name=username)
    logger.info("Start find all tasks user: %s", username)
    stmt = select(Task).where(Task.user_id == user.id)
    try:
        result: Result = await session.execute(stmt)
        user_tasks = result.scalars().all()
    except SQLAlchemyError as exp:
        logger.exception("Error find all tasks user %s", username)
        raise ExceptDB("Error in DB")
    else:
        return list(user_tasks)


async def add_new_task_bd(
    session: AsyncSession,
    username: str,
    task: TaskCreate,
) -> TaskRead:
    logger.info("Start add task to bd")
    logger.info("Find in bd user %s", username)
    user: User = await get_user_from_db(session=session, name=username)
    if not user:
        logger.info("Not found in bd user %s", username)
        raise ExceptDB("User not found")

    new_task = Task(
        **task.model_dump()
    )  # pydantic модель преобразовываем м словарь и его распаковываем в экземпляр класса БД
    new_task.user_id = user.id
    session.add(new_task)
    await session.commit()
    logger.info(f"new task {new_task}")
    return TaskRead.model_validate(new_task)  # загружаем запись БД в модель pydantic


async def get_task_by_id(
    session: AsyncSession,
    username: str,
    id: int,
):
    logger.info("Start get task by id")
    logger.info("Find in bd user %s", username)
    user: User = await get_user_from_db(session=session, name=username)
    if not user:
        logger.info("Not found in bd user %s", username)
        raise ExceptDB("User not found")
    stmt = select(Task).filter(and_(Task.id == id, Task.user_id == user.id))
    result: Result = await session.execute(stmt)
    task: Task = result.scalars().one_or_none()
    if not task:
        logger.info("Not found task user %s by id %s", username, id)
        raise ExceptDB("Task by id not found")

    return TaskOut(task=task.task, date_create=task.date_create, date_exp=task.date_exp)
