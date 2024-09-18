from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class BaseUserRepository(ABC):
    @abstractmethod
    async def create(
        self, username: str, email: str, hashed_password: str
    ) -> User | None:
        ...

    @abstractmethod
    async def get_by_id(self, id: str) -> User:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        ...


class UserRepository(BaseUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, username: str, email: str, hashed_password: str
    ) -> User | None:
        new_user = User(username=username, email=email, password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def get_by_id(self, id: str) -> User:
        stmt = select(User).where(User.id == id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
