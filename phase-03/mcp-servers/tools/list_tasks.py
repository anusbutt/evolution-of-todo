# [Task]: T046 [P] [US2] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
# [Task]: T117 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added Priority support
"""
MCP Tool: list_tasks - Retrieve all tasks for the user.
"""
from typing import Any, Optional

from sqlmodel import select

from database import async_session
from models import Task

# Valid priority values
VALID_PRIORITIES = {"P1", "P2", "P3"}


async def list_tasks(
    user_id: int,
    completed: Optional[bool] = None,
    priority: Optional[str] = None
) -> dict[str, Any]:
    """
    Get all tasks for the user, optionally filtered by status and priority.

    Args:
        user_id: The authenticated user's ID
        completed: Filter by completion status (optional)
        priority: Filter by priority level P1/P2/P3 (optional)

    Returns:
        dict with success status, tasks list, and count
    """
    try:
        async with async_session() as session:
            # Build query
            query = select(Task).where(Task.user_id == user_id)

            # Apply completion filter if provided
            if completed is not None:
                query = query.where(Task.completed == completed)

            # Apply priority filter if provided
            if priority:
                priority = priority.upper().strip()
                if priority in VALID_PRIORITIES:
                    query = query.where(Task.priority == priority)

            # Order by created_at descending (newest first)
            query = query.order_by(Task.created_at.desc())

            result = await session.execute(query)
            tasks = result.scalars().all()

            return {
                "success": True,
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "priority": task.priority,
                        "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                    }
                    for task in tasks
                ],
                "count": len(tasks)
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to list tasks: {str(e)}"}
