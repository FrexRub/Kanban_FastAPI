from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    task: str
    date_exp: Optional[datetime] = None


class TaskRead(TaskCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_create: datetime
    user_id: int


class TaskOut(BaseModel):
    task: str
    date_exp: Optional[datetime] = None
    date_create: datetime
