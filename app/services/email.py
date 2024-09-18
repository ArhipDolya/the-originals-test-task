from abc import ABC, abstractmethod

from app.db.common.enums import StatusEnum


class BaseEmailService(ABC):
    @abstractmethod
    async def send_email(self, task_id: int, status: StatusEnum) -> str:
        ...


class EmailService(BaseEmailService):
    async def send_email(self, task_id: int, status: StatusEnum) -> str:
        print(
            f"Email sent to responsible person: Task {task_id} status changed to {status}"
        )
