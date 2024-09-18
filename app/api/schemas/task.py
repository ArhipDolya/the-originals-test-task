from pydantic import BaseModel

from app.db.common.enums import StatusEnum, PriorityEnum


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: StatusEnum
    priority: PriorityEnum


class TaskCreate(BaseModel):
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum


class TaskUpdate(TaskBase):
    title: str | None = None
    description: str | None = None
    status: StatusEnum | None = None
    priority: PriorityEnum | None = None


class TaskResponse(TaskBase):
    id: int
    responsible_person_id: int

    class Config:
        orm_mode = True
