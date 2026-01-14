# [Task]: T059-T061, T072, T074, T081-T082, T101 [US2, US3, US4, US6] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Task service layer for task management.
Handles business logic for task CRUD operations.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import select, func, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    """
    Create a new task for a user.

    Args:
        session: Database session
        task_data: Task creation data (title, description)
        user_id: ID of the user creating the task

    Returns:
        Created Task object

    Process:
        1. Validate title is non-empty (handled by TaskCreate schema)
        2. Create Task object with user_id
        3. Save to database
        4. Return created task
    """
    new_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


async def get_tasks_by_user(session: AsyncSession, user_id: int) -> list[Task]:
    """
    Get all tasks for a specific user, ordered by creation date (newest first).

    Args:
        session: Database session
        user_id: ID of the user whose tasks to fetch

    Returns:
        List of Task objects

    Process:
        1. Query tasks WHERE user_id = current_user_id
        2. Order by created_at DESC (newest first)
        3. Return list of tasks
    """
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    result = await session.execute(statement)
    tasks = result.scalars().all()

    return list(tasks)


async def get_task_by_id(session: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a specific task by ID, ensuring it belongs to the user.

    Args:
        session: Database session
        task_id: ID of the task to fetch
        user_id: ID of the user (for authorization check)

    Returns:
        Task object if found and belongs to user, None otherwise

    Process:
        1. Query task WHERE id = task_id AND user_id = current_user_id
        2. Return task or None
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    return task


async def update_task_status(session: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    """
    Toggle the completion status of a task.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user (for authorization check)

    Returns:
        Updated Task object if found and belongs to user, None otherwise

    Process:
        1. Query task WHERE id = task_id AND user_id = current_user_id
        2. Toggle completed field
        3. Update updated_at timestamp
        4. Save to database
        5. Return updated task or None
    """
    # Get task with authorization check
    task = await get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    # Toggle completed status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def get_task_statistics(session: AsyncSession, user_id: int) -> dict:
    """
    Get task statistics for a user.

    Args:
        session: Database session
        user_id: ID of the user

    Returns:
        Dictionary with task statistics:
            - total: Total number of tasks
            - completed: Number of completed tasks
            - incomplete: Number of incomplete tasks
            - completion_percentage: Percentage of completed tasks (0-100)

    Process:
        1. Query COUNT(*) WHERE user_id = current_user_id
        2. Query COUNT(*) WHERE user_id = current_user_id AND completed = true
        3. Calculate incomplete count and completion percentage
        4. Return stats dictionary
    """
    # Count total tasks
    total_statement = select(func.count(Task.id)).where(Task.user_id == user_id)
    total_result = await session.execute(total_statement)
    total = total_result.scalar() or 0

    # Count completed tasks
    completed_statement = select(func.count(Task.id)).where(
        Task.user_id == user_id,
        Task.completed == True
    )
    completed_result = await session.execute(completed_statement)
    completed = completed_result.scalar() or 0

    # Calculate incomplete and percentage
    incomplete = total - completed
    completion_percentage = round((completed / total * 100), 1) if total > 0 else 0.0

    return {
        "total": total,
        "completed": completed,
        "incomplete": incomplete,
        "completion_percentage": completion_percentage
    }


async def update_task(session: AsyncSession, task_id: int, user_id: int, task_data: TaskUpdate) -> Optional[Task]:
    """
    Update a task's title and/or description.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user (for authorization check)
        task_data: Updated task data (title, description, completed)

    Returns:
        Updated Task object if found and belongs to user, None otherwise

    Process:
        1. Query task WHERE id = task_id AND user_id = current_user_id
        2. Update provided fields (title, description, completed)
        3. Validate title is non-empty
        4. Update updated_at timestamp
        5. Save to database
        6. Return updated task or None
    """
    # Get task with authorization check
    task = await get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(session: AsyncSession, task_id: int, user_id: int) -> bool:
    """
    Delete a task from the database.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user (for authorization check)

    Returns:
        True if task was deleted, False if not found or doesn't belong to user

    Process:
        1. Query task WHERE id = task_id AND user_id = current_user_id
        2. Delete from database
        3. Return success status
    """
    # Get task with authorization check
    task = await get_task_by_id(session, task_id, user_id)

    if not task:
        return False

    # Delete task
    await session.delete(task)
    await session.commit()

    return True


async def search_tasks(session: AsyncSession, user_id: int, query: str) -> list[Task]:
    """
    Search tasks by title or description using case-insensitive matching.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to search
        query: Search query string

    Returns:
        List of Task objects matching the search query

    Process:
        1. Query tasks WHERE user_id = current_user_id AND (title ILIKE %query% OR description ILIKE %query%)
        2. Use parameterized queries to prevent SQL injection
        3. Order by created_at DESC (newest first)
        4. Return list of matching tasks
    """
    # Use parameterized queries with ILIKE for case-insensitive search
    # The % wildcard is added here, not from user input, to prevent SQL injection
    search_pattern = f"%{query}%"

    statement = select(Task).where(
        Task.user_id == user_id,
        (Task.title.ilike(search_pattern) | Task.description.ilike(search_pattern))
    ).order_by(Task.created_at.desc())

    result = await session.execute(statement)
    tasks = result.scalars().all()

    return list(tasks)
