# [Task]: T053 [P] [US4] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
"""
MCP Tool: delete_task - Delete a task from the user's list.
"""
from typing import Any

from sqlmodel import select

from database import async_session
from models import Task


async def delete_task(
    user_id: int,
    task_id: int
) -> dict[str, Any]:
    """
    Delete a task from the user's task list.

    Args:
        user_id: The authenticated user's ID
        task_id: The ID of the task to delete

    Returns:
        dict with success status and deleted task info
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

            # Store task info before deletion
            task_info = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
            }

            # Delete the task
            await session.delete(task)
            await session.commit()

            return {
                "success": True,
                "deleted_task": task_info,
                "message": f"Task '{task_info['title']}' has been deleted"
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to delete task: {str(e)}"}
