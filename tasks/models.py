from typing import Optional, TYPE_CHECKING
from datetime import datetime

from core.database import Base
from sqlalchemy import DateTime, func, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from users.models import User


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    date_create: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_exp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="tasks")

    def __str__(self):
        return (
            f"Task {self.id}, context {self.task}, data create {self.date_create},"
            f"data exception {self.date_exp}, id user {self.user_id}"
        )
