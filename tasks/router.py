from fastapi import APIRouter

from tasks.schemas import TaskOut

router = APIRouter(prefix="Tasks", tags=["Tasks"])


@router.get("/", response_model=TaskOut)
def get_task_user():
    return {}
