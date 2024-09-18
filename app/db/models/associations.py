from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.models.base import TimedBaseModel


task_assignee = Table(
    "task_assignee",
    TimedBaseModel.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)
