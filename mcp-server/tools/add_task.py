# [Task]: T029 [P] [US1] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/mcp-tools.md
"""
MCP Tool: add_task - Create a new task for the user.
"""
from datetime import datetime
from typing import Any

from sqlmodel import select

from database import async_session
from models import Task


async def add_task(
    user_id: int,
    title: str,
    description: str | None = None
) -> dict[str, Any]:
    """
    Add a new task to the user's task list.

    Args:
        user_id: The authenticated user's ID
        title: The task title (required, max 255 chars)
        description: Optional task description (max 1000 chars)

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

    try:
        async with async_session() as session:
            # Create new task
            task = Task(
                user_id=user_id,
                title=title,
                description=description if description else None,
                completed=False,
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
                    "created_at": task.created_at.isoformat() + "Z",
                }
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to create task: {str(e)}"}
