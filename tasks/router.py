from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from tasks.schemas import TaskRead, TaskCreate, TaskOut
from tasks.crud import get_all_tasks_user, add_new_task_bd, get_task_by_id
from core.database import get_async_session
from core.config import templates
from core.exceptions import ExceptDB
from users.models import User
from auth.dependencies import current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_task_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> list[TaskRead]:
    try:
        res: list[TaskRead] = await get_all_tasks_user(
            session=session, username=user.email
        )
    except ExceptDB as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title_error": "Проблема c поиском задач",
                "text_error": "Ошибка в БД",
            },
        )
    return res


@router.post("/task", response_model=TaskRead)
async def add_new_task(
    request: Request,
    task: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> TaskRead:
    try:
        new_task: TaskRead = await add_new_task_bd(
            session=session, username=user.email, task=task
        )
    except ExceptDB:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title_error": "Пользователь не найден",
                "text_error": "Ошибка в БД",
            },
        )
    return new_task


@router.get("/task/{id}", response_model=TaskOut)
async def get_task_user_id(
    id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> TaskOut:
    try:
        task: TaskOut = await get_task_by_id(
            session=session,
            username=user.email,
            id=id,
        )
    except ExceptDB:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title_error": "Задача не найдена",
                "text_error": "Ошибка в БД",
            },
        )
    return task
