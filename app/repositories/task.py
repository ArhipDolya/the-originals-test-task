from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.common.enums import PriorityEnum, StatusEnum
from app.db.models.task import Task


class BaseTaskRepository(ABC):
    @abstractmethod
    async def create(
        self,
        title: str,
        description: str,
        responsible_person_id: int,
        status: StatusEnum,
        priority: PriorityEnum,
    ) -> Task:
        ...

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Task:
        ...

    @abstractmethod
    async def update(self, task_id: int, **kwargs) -> Task:
        ...

    @abstractmethod
    async def update(self, task_id: int) -> Task:
        ...

    @abstractmethod
    async def delete(self, task_id: int) -> bool:
        ...


class TaskRepository(BaseTaskRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        title: str,
        description: str,
        responsible_person_id: int,
        status: StatusEnum,
        priority: PriorityEnum,
    ) -> Task:
        new_task = Task(
            title=title,
            description=description,
            responsible_person_id=responsible_person_id,
            status=status,
            priority=priority,
        )
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)

        return new_task

    async def get_by_id(self, task_id: int) -> Task:
        stmt = (
            select(Task).options(selectinload(Task.assignees)).where(Task.id == task_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update(self, task_id: int, **kwargs) -> Task:
        task = await self.get_by_id(task_id=task_id)

        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            await self.db.commit()
            await self.db.refresh(task)

        return task

    async def delete(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id=task_id)

        if task:
            self.db.delete(task)
            self.db.commit()
            return True

        return False
