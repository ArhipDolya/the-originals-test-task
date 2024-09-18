from enum import Enum


class StatusEnum(Enum):
    TODO = "TODO"
    IN_PROGRESS = "In progress"
    DONE = "Done"


class RoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class PriorityEnum(Enum):
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"
