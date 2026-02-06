from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from src.database.session import get_session
from src.services.task_service import TaskService
from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from src.models.user import User
from src.api.deps import get_current_user
import uuid

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the requested user_id matches the authenticated user's ID
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    tasks = TaskService.get_tasks_by_user(session, user_id, limit, offset, completed)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(
    user_id: uuid.UUID,
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the requested user_id matches the authenticated user's ID
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    db_task = TaskService.create_task(session, task, user_id)
    return db_task


@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
def get_task(
    user_id: uuid.UUID,
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the requested user_id matches the authenticated user's ID
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    db_task = TaskService.get_task_by_id_and_user(session, id, user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task


@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
def update_task(
    user_id: uuid.UUID,
    id: uuid.UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the requested user_id matches the authenticated user's ID
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update these tasks"
        )

    db_task = TaskService.update_task(session, id, task_update, user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task


@router.delete("/{user_id}/tasks/{id}")
def delete_task(
    user_id: uuid.UUID,
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the requested user_id matches the authenticated user's ID
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete these tasks"
        )

    success = TaskService.delete_task(session, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
def update_task_completion(
    user_id: uuid.UUID,
    id: uuid.UUID,
    completed: dict,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the requested user_id matches the authenticated user's ID
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update these tasks"
        )

    # Extract the completed value from the request
    completed_value = completed.get("completed")
    if completed_value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing 'completed' field in request body"
        )

    db_task = TaskService.update_task_completion(session, id, completed_value, user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task