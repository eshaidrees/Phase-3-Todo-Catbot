"""MCP Tool for adding tasks"""

from ...database.session import engine
from ...models.task import Task, TaskCreate
from sqlmodel import Session
import uuid
from datetime import datetime


def add_task(user_id: str, title: str, description: str = "") -> dict:
    """
    Add a new task for a user.

    Args:
        user_id: The ID of the user
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with result information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Create a database session using the engine directly
        with Session(engine) as session:
            # Create the task
            task_create = TaskCreate(
                title=title,
                description=description or "",
                completed=False  # Default to not completed
            )

            # Create the task object with all required fields
            db_task = Task(
                title=task_create.title,
                description=task_create.description,
                completed=task_create.completed,
                due_date=task_create.due_date,
                user_id=user_uuid,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            # Add to session and commit
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "success": True,
                "message": f"Task '{db_task.title}' has been added successfully.",
                "task_id": str(db_task.id),
                "task": {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "description": db_task.description,
                    "completed": db_task.completed,
                    "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                    "created_at": db_task.created_at.isoformat()
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add task"
        }


if __name__ == "__main__":
    # Example usage
    result = add_task(str(uuid.uuid4()), "Test task", "This is a test task")
    print(result)