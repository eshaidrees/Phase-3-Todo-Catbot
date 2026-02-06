"""MCP Tool for listing tasks"""

from ...database.session import engine
from ...models.task import Task
from sqlmodel import Session, select
import uuid


def list_tasks(user_id: str, status: str = "all") -> dict:
    """
    List tasks for a user.

    Args:
        user_id: The ID of the user
        status: Filter by status - 'all', 'completed', 'pending'

    Returns:
        Dictionary with result information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Create a database session using the engine directly
        with Session(engine) as session:
            # Build the query
            query = select(Task).where(Task.user_id == user_uuid)

            # Apply status filter if specified
            if status == "completed":
                query = query.where(Task.completed == True)
            elif status == "pending":
                query = query.where(Task.completed == False)

            # Execute query
            tasks = session.exec(query).all()

            # Format tasks for response
            task_list = []
            for task in tasks:
                task_dict = {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                task_list.append(task_dict)

            return {
                "success": True,
                "count": len(task_list),
                "tasks": task_list,
                "message": f"Found {len(task_list)} tasks for user {user_id}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list tasks"
        }


if __name__ == "__main__":
    # Example usage
    import uuid
    result = list_tasks(str(uuid.uuid4()))
    print(result)