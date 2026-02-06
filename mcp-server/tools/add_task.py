# [Task]: T029 [P] [US1] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
# [Task]: T117 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added Priority support
"""
MCP Tool: add_task - Create a new task for the user.
"""
from datetime import datetime
from typing import Any

from sqlmodel import select

from database import async_session
from models import Task

# Valid priority values
VALID_PRIORITIES = {"P1", "P2", "P3"}


async def add_task(
    user_id: int,
    title: str,
    description: str | None = None,
    priority: str | None = None
) -> dict[str, Any]:
    """
    Add a new task to the user's task list.

    Args:
        user_id: The authenticated user's ID
        title: The task title (required, max 255 chars)
        description: Optional task description (max 1000 chars)
        priority: Optional priority level (P1=High, P2=Medium, P3=Low). Default: P2

    Returns:
        dict with success status and created task or error message
    """
    # Validate inputs
    if not title or not title.strip():
        return {"success": False, "error": "Title cannot be empty"}

    title = title.strip()
    if len(title) > 255:
        return {"success": False, "error": "Title cannot exceed 255 characters"}

    if description:
        description = description.strip()
        if len(description) > 1000:
            return {"success": False, "error": "Description cannot exceed 1000 characters"}

    # Validate and normalize priority
    if priority:
        priority = priority.upper().strip()
        if priority not in VALID_PRIORITIES:
            return {"success": False, "error": f"Invalid priority '{priority}'. Use P1, P2, or P3"}
    else:
        priority = "P2"  # Default to medium priority

    try:
        async with async_session() as session:
            # Create new task
            task = Task(
                user_id=user_id,
                title=title,
                description=description if description else None,
                completed=False,
                priority=priority,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

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
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() + "Z",
                }
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to create task: {str(e)}"}
