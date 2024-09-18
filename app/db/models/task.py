from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

from app.db.common.enums import PriorityEnum, StatusEnum
from app.db.models.base import TimedBaseModel
from app.db.models.associations import task_assignee


class Task(TimedBaseModel):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text(), nullable=True, index=True)
    responsible_person_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.TODO)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    
    # Relationships
    responsible_person = relationship("User", foreign_keys=[responsible_person_id], back_populates="responsible_for_tasks", passive_deletes=True)
    assignees = relationship("User", secondary=task_assignee, back_populates="assigned_tasks")

    def __str__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status}, priority={self.priority})>"
    
    def __repr__(self):
        return self.__str__()
