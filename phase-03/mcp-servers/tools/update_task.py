# [Task]: T056 [P] [US5] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
# [Task]: T117 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added Priority support
"""
MCP Tool: update_task - Update a task's title, description, or priority.
"""
from typing import Any, Optional

from sqlmodel import select

from database import async_session
from models import Task

# Valid priority values
VALID_PRIORITIES = {"P1", "P2", "P3"}


async def update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None
) -> dict[str, Any]:
    """
    Update a task's title, description, or priority.

    Args:
        user_id: The authenticated user's ID
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        priority: New priority level P1/P2/P3 (optional)

    Returns:
        dict with success status and updated task data
    """
    # Validate input - at least one field must be provided
    if not title and description is None and priority is None:
        return {
            "success": False,
            "error": "Please provide a new title, description, or priority to update"
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

    # Validate priority if provided
    if priority:
        priority = priority.upper().strip()
        if priority not in VALID_PRIORITIES:
            return {
                "success": False,
                "error": f"Invalid priority '{priority}'. Use P1, P2, or P3"
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
            old_priority = task.priority

            # Update fields
            if title:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip() if description else None
            if priority:
                task.priority = priority

            session.add(task)
            await session.commit()
            await session.refresh(task)

            # Build update message
            changes = []
            if title and title.strip() != old_title:
                changes.append(f"title from '{old_title}' to '{task.title}'")
            if priority and priority != old_priority:
                changes.append(f"priority from {old_priority} to {task.priority}")
            message = f"Task updated: {', '.join(changes)}" if changes else "Task updated"

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                },
                "message": message
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to update task: {str(e)}"}
