import os
import sys
import uuid
from datetime import datetime
from sqlmodel import Session, select
from typing import Optional

# Add the backend directory to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task
from src.database.session import engine


def update_task(user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> dict:
    """
    Updates a task.

    Args:
        user_id: The UUID of the user who owns the task
        task_id: The UUID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        completed: New completion status for the task (optional)

    Returns:
        Dictionary containing the result of the operation
    """
    try:
        # Validate that user_id and task_id are valid UUIDs
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)

        # Create a session using the shared engine
        with Session(engine) as session:
            # Find the task that belongs to the user
            statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
            db_task = session.exec(statement).first()

            if not db_task:
                return {
                    "success": False,
                    "message": f"No task found with ID {task_id} for user {user_id}"
                }

            # Update the fields if provided
            if title is not None:
                db_task.title = title
            if description is not None:
                db_task.description = description
            if completed is not None:
                db_task.completed = completed

            # Update the timestamp
            db_task.updated_at = datetime.now()

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "success": True,
                "task_id": str(db_task.id),
                "message": f"Task {db_task.id} updated successfully"
            }
    except ValueError as ve:
        return {
            "success": False,
            "error": str(ve),
            "message": f"Invalid UUID format: {str(ve)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to update task: {str(e)}"
        }


if __name__ == "__main__":
    # Example usage
    result = update_task("test_user", 1, title="Updated Title", description="Updated Description")
    print(result)