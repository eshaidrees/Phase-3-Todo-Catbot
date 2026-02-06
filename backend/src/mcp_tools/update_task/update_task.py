"""MCP Tool for updating tasks"""

from ...database.session import engine
from ...models.task import Task
from sqlmodel import Session, select
import uuid
from datetime import datetime


def update_task(user_id: str, task_id: str, title: str = None, description: str = None, completed: bool = None) -> dict:
    """
    Update a task.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        completed: New completion status (optional)

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

            # Update the task fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed

            # Update the timestamp
            task.updated_at = datetime.now()

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Task '{task.title}' has been updated successfully.",
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
            "message": "Failed to update task"
        }


if __name__ == "__main__":
    # Example usage
    import uuid
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    result = update_task(user_id, task_id, title="Updated title")
    print(result)