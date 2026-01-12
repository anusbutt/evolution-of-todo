"""Task service for Phase 1 Console Todo Application.

This module provides business logic for CRUD operations on tasks.
"""

from typing import List, Optional
from src.models.task import Task


class TaskService:
    """Service class for managing tasks with CRUD operations.

    Attributes:
        tasks: List of all Task objects
        next_id: Counter for auto-incrementing task IDs (starts at 1)
    """

    def __init__(self):
        """Initialize TaskService with empty task list and ID counter."""
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task with auto-assigned ID.

        Args:
            title: Task title (required, 1-200 characters)
            description: Task description (optional, 0-1000 characters)

        Returns:
            Created Task object

        Raises:
            ValueError: If validation fails (from Task model)
        """
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks in the list.

        Returns:
            List of all Task objects (copy to prevent external modification)
        """
        return self.tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: Task ID to search for

        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> bool:
        """Update a task's title and/or description.

        Args:
            task_id: Task ID to update
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            True if task was updated, False if task not found

        Raises:
            ValueError: If new title fails validation
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # Update title if provided
        if title is not None:
            stripped_title = title.strip()
            if not stripped_title:
                raise ValueError("Task title cannot be empty or whitespace only")
            if len(stripped_title) > 200:
                raise ValueError("Task title must be 200 characters or less")
            task.title = stripped_title

        # Update description if provided
        if description is not None:
            if len(description) > 1000:
                raise ValueError("Task description must be 1000 characters or less")
            task.description = description

        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Note: Deleted task IDs are NOT reused (next_id counter is never decremented)

        Args:
            task_id: Task ID to delete

        Returns:
            True if task was deleted, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self.tasks.remove(task)
        return True

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as complete.

        Args:
            task_id: Task ID to mark complete

        Returns:
            True if task was marked complete, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.completed = True
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: Task ID to mark incomplete

        Returns:
            True if task was marked incomplete, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.completed = False
        return True
