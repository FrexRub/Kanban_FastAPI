from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from tasks.schemas import TaskOut
from tasks.crud import get_all_tasks_user
from core.database import get_async_session
from core.config import templates
from core.exceptions import ExceptDB

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_task_user(
    request: Request, session: AsyncSession = Depends(get_async_session)
) -> list[TaskOut]:
    try:
        res: list[TaskOut] = await get_all_tasks_user(
            session=session, username="frex@mail.ru"
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
