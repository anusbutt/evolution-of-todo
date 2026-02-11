# [Task]: T095 [US9] | MCP tools for bundled stdio transport
"""
MCP Tools for task management - consolidated from phase-03/mcp-servers/tools/.
All 5 tools: add_task, list_tasks, complete_task, delete_task, update_task.
"""
from datetime import datetime
from typing import Any, Optional

from sqlmodel import select

from mcp_server.database import async_session
from mcp_server.models import Task

VALID_PRIORITIES = {"P1", "P2", "P3"}


async def add_task(
    user_id: int,
    title: str,
    description: str | None = None,
    priority: str | None = None,
) -> dict[str, Any]:
    """Add a new task to the user's task list."""
    if not title or not title.strip():
        return {"success": False, "error": "Title cannot be empty"}

    title = title.strip()
    if len(title) > 255:
        return {"success": False, "error": "Title cannot exceed 255 characters"}

    if description:
        description = description.strip()
        if len(description) > 1000:
            return {"success": False, "error": "Description cannot exceed 1000 characters"}

    if priority:
        priority = priority.upper().strip()
        if priority not in VALID_PRIORITIES:
            return {"success": False, "error": f"Invalid priority '{priority}'. Use P1, P2, or P3"}
    else:
        priority = "P2"

    try:
        async with async_session() as session:
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
                },
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to create task: {str(e)}"}


async def list_tasks(
    user_id: int,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
) -> dict[str, Any]:
    """Get all tasks for the user, optionally filtered by status and priority."""
    try:
        async with async_session() as session:
            query = select(Task).where(Task.user_id == user_id)
            if completed is not None:
                query = query.where(Task.completed == completed)
            if priority:
                priority = priority.upper().strip()
                if priority in VALID_PRIORITIES:
                    query = query.where(Task.priority == priority)
            query = query.order_by(Task.created_at.desc())
            result = await session.execute(query)
            tasks = result.scalars().all()
            return {
                "success": True,
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "priority": t.priority,
                        "created_at": t.created_at.isoformat() + "Z" if t.created_at else None,
                    }
                    for t in tasks
                ],
                "count": len(tasks),
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to list tasks: {str(e)}"}


async def complete_task(user_id: int, task_id: int) -> dict[str, Any]:
    """Mark a task as complete."""
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found or doesn't belong to you"}
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
                "message": f"Task '{task.title}' marked as complete",
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to complete task: {str(e)}"}


async def delete_task(user_id: int, task_id: int) -> dict[str, Any]:
    """Delete a task from the user's task list."""
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found or doesn't belong to you"}
            task_info = {"id": task.id, "title": task.title, "completed": task.completed}
            await session.delete(task)
            await session.commit()
            return {
                "success": True,
                "deleted_task": task_info,
                "message": f"Task '{task_info['title']}' has been deleted",
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to delete task: {str(e)}"}


async def update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> dict[str, Any]:
    """Update a task's title, description, or priority."""
    if not title and description is None and priority is None:
        return {"success": False, "error": "Please provide a new title, description, or priority to update"}
    if title and len(title.strip()) == 0:
        return {"success": False, "error": "Task title cannot be empty"}
    if title and len(title) > 255:
        return {"success": False, "error": "Task title must be 255 characters or less"}
    if priority:
        priority = priority.upper().strip()
        if priority not in VALID_PRIORITIES:
            return {"success": False, "error": f"Invalid priority '{priority}'. Use P1, P2, or P3"}

    try:
        async with async_session() as session:
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found or doesn't belong to you"}
            if title:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip() if description else None
            if priority:
                task.priority = priority
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
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                },
                "message": "Task updated",
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to update task: {str(e)}"}
