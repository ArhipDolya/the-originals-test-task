from abc import ABC, abstractmethod

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.common.enums import PriorityEnum, StatusEnum
from app.db.main import get_db
from app.db.models.task import Task
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.services.email import EmailService
from app.services.exceptions.task import TaskNotFoundException


class BaseTaskService(ABC):
    @abstractmethod
    async def create_task(self, title: str, description: str, responsible_person_id: int, status: StatusEnum, priority: PriorityEnum) -> Task:
        ...

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> Task:
        ...

    @abstractmethod
    async def update_task(self, task_id: int, **kwargs) -> Task:
        ...

    @abstractmethod
    async def delete_task(self, task_id: int) -> bool:
        ...

    @abstractmethod
    async def assign_task(self, task_id: int, user_id: int) -> Task:
        ...

    @abstractmethod
    async def change_task_status(self, task_id: int, new_status: StatusEnum) -> Task:
        ...


class TaskService(BaseTaskService):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repository = TaskRepository(db)
        self.email_service = EmailService()
        self.user_repository = UserRepository(db)

    async def create_task(self, title: str, description: str, responsible_person_id: int, status: StatusEnum, priority: PriorityEnum) -> Task:
        new_task = await self.task_repository.create(title, description, responsible_person_id, status, priority)
        return new_task
    
    async def get_task_by_id(self, task_id: int) -> Task:
        task = await self.task_repository.get_by_id(task_id=task_id)
        
        if not task:
            raise TaskNotFoundException(f"Task with id {task_id} not found")
        
        return task
    
    async def update_task(self, task_id: int, **kwargs) -> Task:
        task = await self.task_repository.update(task_id, **kwargs)
        
        if not task:
            raise TaskNotFoundException(f"Task with id {task_id} not found")
        
        return task
    
    async def delete_task(self, task_id: int) -> bool:
        deleted = await self.task_repository.delete(task_id)

        if not deleted:
            raise TaskNotFoundException(f"Task with id {task_id} not found")
        
        return True
    
    async def assign_task(self, task_id: int, user_id: int) -> Task:
        task = await self.task_repository.get_by_id(task_id=task_id)

        await self.db.refresh(task, ["assignees"])

        user = await self.user_repository.get_by_id(id=user_id)
        task.assignees.append(user)

        return await self.task_repository.update(task_id=task_id, assignees=task.assignees)
    

    async def change_task_status(self, task_id: int, new_status: StatusEnum) -> Task:
        task = await self.update_task(task_id=task_id, status=new_status)
        await self.email_service.send_email(task_id=task.id, status=task.status)

        return task


def get_task_service(db: AsyncSession = Depends(get_db)):
    return TaskService(db)
