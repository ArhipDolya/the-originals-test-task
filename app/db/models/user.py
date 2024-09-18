from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.db.common.enums import RoleEnum
from app.db.models.associations import task_assignee
from app.db.models.base import TimedBaseModel
from app.db.models.task import Task


class User(TimedBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.USER)

    # Relationships
    responsible_for_tasks = relationship(
        "Task",
        back_populates="responsible_person",
        foreign_keys=[Task.responsible_person_id],
        cascade="all, delete-orphan",
    )
    assigned_tasks = relationship(
        "Task", secondary=task_assignee, back_populates="assignees"
    )

    def __str__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"

    def __repr__(self):
        return self.__str__()
