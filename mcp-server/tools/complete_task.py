# [Task]: T049 [P] [US3] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
"""
MCP Tool: complete_task - Mark a task as complete.
"""
from typing import Any

from sqlmodel import select

from database import async_session
from models import Task


async def complete_task(
    user_id: int,
    task_id: int
) -> dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        user_id: The authenticated user's ID
        task_id: The ID of the task to complete

    Returns:
        dict with success status and updated task data
    """
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

            # Mark as complete
            task.completed = True
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
                "message": f"Task '{task.title}' marked as complete"
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to complete task: {str(e)}"}
