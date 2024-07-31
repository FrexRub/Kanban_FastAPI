from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    task: int
    date_exp: datetime


class TaskOut(TaskBase):
    id: int
    date_create: datetime
    user_id: int
