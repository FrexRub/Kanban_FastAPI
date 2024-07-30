from datetime import datetime

from pydantic import BaseModel

class TaskBase(BaseModel):
    task: int
    date_exp: datetime
