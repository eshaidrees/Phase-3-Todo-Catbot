import os
import sys
import uuid
from sqlmodel import Session, select
from typing import Optional

# Add the backend directory to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task
from src.database.session import engine


def list_tasks(user_id: str, status: str = "all") -> dict:
    """
    Lists tasks for a specific user.

    Args:
        user_id: The UUID of the user whose tasks to list
        status: Filter by status ('all', 'completed', 'pending')

    Returns:
        Dictionary containing the list of tasks
    """
    try:
        # Validate that user_id is a valid UUID
        user_uuid = uuid.UUID(user_id)

        # Create a session using the shared engine
        with Session(engine) as session:
            # Build the query based on status filter
            query = select(Task).where(Task.user_id == user_uuid)

            if status == "completed":
                query = query.where(Task.completed == True)
            elif status == "pending":
                query = query.where(Task.completed == False)
            # For "all", no additional filter is needed

            query = query.order_by(Task.created_at.desc())
            tasks_db = session.exec(query).all()

            # Convert to the expected format
            tasks = []
            for task in tasks_db:
                task_dict = {
                    "id": str(task.id),
                    "user_id": str(task.user_id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                tasks.append(task_dict)

            return {
                "success": True,
                "tasks": tasks,
                "count": len(tasks)
            }
    except ValueError as ve:
        return {
            "success": False,
            "error": str(ve),
            "message": f"Invalid user_id format: {str(ve)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to list tasks: {str(e)}"
        }


if __name__ == "__main__":
    # Example usage
    result = list_tasks("test_user", "all")
    print(result)