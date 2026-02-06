"""MCP Tool for completing tasks"""

from ...database.session import engine
from ...models.task import Task
from sqlmodel import Session, select
import uuid
from datetime import datetime


def complete_task(user_id: str, task_id: str) -> dict:
    """
    Mark a task as completed.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to complete

    Returns:
        Dictionary with result information
    """
    try:
        # Convert user_id and task_id to UUIDs
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)

        # Create a database session using the engine directly
        with Session(engine) as session:
            # Find the task for the specific user
            statement = select(Task).where(
                Task.id == task_uuid,
                Task.user_id == user_uuid
            )
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found for user {user_id}",
                    "error": "Task not found"
                }

            # Update the task as completed
            task.completed = True
            task.updated_at = datetime.now()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Task '{task.title}' has been marked as completed.",
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "updated_at": task.updated_at.isoformat()
                }
            }

    except ValueError as ve:
        # Handle invalid UUID format
        return {
            "success": False,
            "error": str(ve),
            "message": "Invalid user_id or task_id format"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to complete task"
        }


if __name__ == "__main__":
    # Example usage
    import uuid
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    result = complete_task(user_id, task_id)
    print(result)