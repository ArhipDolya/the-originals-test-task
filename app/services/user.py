from abc import ABC, abstractmethod

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.main import get_db
from app.db.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import get_hashed_password, verify_password
from app.services.exceptions.user import InvalidCredentialsError, UserAlreadyExistsError, UserNotFoundError


class BaseUserService(ABC):
    @abstractmethod
    async def register_user(self, username: str, email: str, password: str) -> User:
        ...

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> User:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        ...


class UserService(BaseUserService):
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def register_user(self, username: str, email: str, password: str) -> User:
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required")
        
        hashed_password = get_hashed_password(password)
        try:
            new_user = await self.user_repository.create(username=username, email=email, hashed_password=hashed_password)
            return new_user
        except IntegrityError:
            raise UserAlreadyExistsError("A user with this username or email already exists")

    async def authenticate_user(self, username: str, password: str) -> User:
        if not username or not password:
            raise ValueError("Username and password are required")

        user = await self.user_repository.get_by_username(username=username)

        if not user:
            raise UserNotFoundError("User not found")

        if not verify_password(password, user.password):
            raise InvalidCredentialsError("Invalid password")

        return user

    async def get_by_username(self, username: str) -> User:
        user = await self.user_repository.get_by_username(username=username)

        if not user:
            raise UserNotFoundError("User not found")
        
        return user


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)
