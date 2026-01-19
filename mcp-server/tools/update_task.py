# [Task]: T056 [P] [US5] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
"""
MCP Tool: update_task - Update a task's title or description.
"""
from typing import Any, Optional

from sqlmodel import select

from database import async_session
from models import Task


async def update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict[str, Any]:
    """
    Update a task's title or description.

    Args:
        user_id: The authenticated user's ID
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        dict with success status and updated task data
    """
    # Validate input
    if not title and description is None:
        return {
            "success": False,
            "error": "Please provide a new title or description to update"
        }

    if title and len(title.strip()) == 0:
        return {
            "success": False,
            "error": "Task title cannot be empty"
        }

    if title and len(title) > 255:
        return {
            "success": False,
            "error": "Task title must be 255 characters or less"
        }

    try:
        async with async_session() as session:
            # Find the task
            result = await session.execute(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
            )
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found or doesn't belong to you"
                }

            # Store old values for response
            old_title = task.title

            # Update fields
            if title:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip() if description else None

            session.add(task)
            await session.commit()
            await session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                },
                "message": f"Task updated from '{old_title}' to '{task.title}'"
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to update task: {str(e)}"}
