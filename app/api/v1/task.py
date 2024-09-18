from fastapi import APIRouter, Depends, HTTPException

from app.api.exceptions.task import UnauthorizedException
from app.services.exceptions.task import TaskNotFoundException
from app.services.task import BaseTaskService, TaskService, get_task_service
from app.services.auth import get_current_user, role_required

from app.db.common.enums import StatusEnum, RoleEnum
from app.api.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.user import BaseUserService, get_user_service


router = APIRouter(prefix="/api/v1", tags=["Tasks"])


@router.post("/tasks", response_model=TaskCreate)
async def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    task_service: BaseTaskService = Depends(get_task_service),
    user_service: BaseUserService = Depends(get_user_service)
):
    user = await user_service.get_by_username(username=current_user["sub"])
    print(user)
    try:
        return await task_service.create_task(
            title=task.title,
            description=task.description,
            responsible_person_id=user.id,
            status=task.status,
            priority=task.priority
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/tasks/{task_id}', response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    task_service: BaseTaskService = Depends(get_task_service)
):
    try:
        return await task_service.get_task_by_id(task_id=task_id)
    except TaskNotFoundException as e:
        raise TaskNotFoundException(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/tasks/{task_id}', response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    task_service: BaseTaskService = Depends(get_task_service),
    current_user: dict = Depends(role_required(RoleEnum.MANAGER))
):
    try:
        return await task_service.update_task(task_id=task_id, **task_update.dict(exclude_unset=True))
    except TaskNotFoundException as e:
        raise TaskNotFoundException(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/tasks/{task_id}')
async def delete_task(
    task_id: int,
    task_service: BaseTaskService = Depends(get_task_service),
    current_user: dict = Depends(role_required(RoleEnum.ADMIN))
):
    try:
        await task_service.delete_task(task_id=task_id)
        return {"message": "Task deleted successfully"}
    except TaskNotFoundException as e:
        raise TaskNotFoundException(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/tasks/{task_id}/assign/{user_id}', response_model=TaskResponse)
async def assign_task(
    task_id: int,
    user_id: int,
    task_service: BaseTaskService = Depends(get_task_service),
    current_user: dict = Depends(role_required(RoleEnum.MANAGER))
):
    return await task_service.assign_task(task_id=task_id, user_id=user_id)


@router.put("/tasks/{task_id}/status", response_model=TaskResponse)
async def change_task_status(
    task_id: int,
    new_status: StatusEnum,
    task_service: BaseTaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    return await task_service.change_task_status(task_id=task_id, new_status=new_status)
