# [Task]: T046 [P] [US2] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
"""
MCP Tool: list_tasks - Retrieve all tasks for the user.
"""
from typing import Any, Optional

from sqlmodel import select

from database import async_session
from models import Task


async def list_tasks(
    user_id: int,
    completed: Optional[bool] = None
) -> dict[str, Any]:
    """
    Get all tasks for the user, optionally filtered by status.

    Args:
        user_id: The authenticated user's ID
        completed: Filter by completion status (optional)

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
                        "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                    }
                    for task in tasks
                ],
                "count": len(tasks)
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to list tasks: {str(e)}"}
