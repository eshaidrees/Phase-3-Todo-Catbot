from sqlmodel import Session, select
from typing import List, Optional
from src.models.task import Task, TaskCreate, TaskUpdate
from datetime import datetime
import uuid

class TaskService:

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
        # Explicitly set default_factory fields
        db_task = Task(
            id=uuid.uuid4(),
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            due_date=task_create.due_date,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0,
        completed: Optional[bool] = None
    ) -> List[Task]:
        query = select(Task).where(Task.user_id == user_id)
        if completed is not None:
            query = query.where(Task.completed == completed)
        query = query.offset(offset).limit(limit)
        return session.exec(query).all()

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate, user_id: uuid.UUID) -> Optional[Task]:
        db_task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not db_task:
            return None

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.now()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        db_task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not db_task:
            return False

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def update_task_completion(session: Session, task_id: uuid.UUID, completed: bool, user_id: uuid.UUID) -> Optional[Task]:
        db_task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not db_task:
            return None

        db_task.completed = completed
        db_task.updated_at = datetime.now()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
