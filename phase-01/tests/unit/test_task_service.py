"""Unit tests for TaskService.

This module tests TaskService CRUD operations.
"""

import sys
import pytest

# Add project root to path
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.task_service import TaskService


def test_task_service_initialization():
    """Test TaskService initializes with empty task list."""
    service = TaskService()

    assert service.tasks == []
    assert service.next_id == 1


def test_add_task_simple():
    """Test adding a task with title only."""
    service = TaskService()

    task = service.add_task("Buy groceries")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == ""
    assert task.completed is False
    assert len(service.tasks) == 1


def test_add_task_with_description():
    """Test adding a task with title and description."""
    service = TaskService()

    task = service.add_task("Buy groceries", "Milk, eggs, bread")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False


def test_add_task_auto_increment_id():
    """Test task IDs auto-increment correctly."""
    service = TaskService()

    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    task3 = service.add_task("Task 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3
    assert service.next_id == 4


def test_add_task_invalid_title_raises_error():
    """Test adding task with invalid title raises ValueError."""
    service = TaskService()

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.add_task("")


def test_get_all_tasks_empty():
    """Test get_all_tasks returns empty list when no tasks."""
    service = TaskService()

    tasks = service.get_all_tasks()

    assert tasks == []


def test_get_all_tasks_with_tasks():
    """Test get_all_tasks returns all tasks."""
    service = TaskService()
    service.add_task("Task 1")
    service.add_task("Task 2")
    service.add_task("Task 3")

    tasks = service.get_all_tasks()

    assert len(tasks) == 3
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    assert tasks[2].title == "Task 3"


def test_get_all_tasks_returns_copy():
    """Test get_all_tasks returns a copy to prevent external modification."""
    service = TaskService()
    service.add_task("Task 1")

    tasks = service.get_all_tasks()
    tasks.append("fake task")

    # Original list should not be affected
    assert len(service.tasks) == 1


def test_get_task_by_id_found():
    """Test get_task_by_id returns task when found."""
    service = TaskService()
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")

    found_task = service.get_task_by_id(2)

    assert found_task is not None
    assert found_task.id == 2
    assert found_task.title == "Task 2"


def test_get_task_by_id_not_found():
    """Test get_task_by_id returns None when task not found."""
    service = TaskService()
    service.add_task("Task 1")

    found_task = service.get_task_by_id(999)

    assert found_task is None


def test_get_task_by_id_empty_list():
    """Test get_task_by_id returns None on empty list."""
    service = TaskService()

    found_task = service.get_task_by_id(1)

    assert found_task is None


def test_add_task_strips_title_whitespace():
    """Test add_task strips whitespace from title."""
    service = TaskService()

    task = service.add_task("  Buy groceries  ")

    assert task.title == "Buy groceries"


def test_add_multiple_tasks_preserves_order():
    """Test tasks are returned in the order they were added."""
    service = TaskService()

    service.add_task("First task")
    service.add_task("Second task")
    service.add_task("Third task")

    tasks = service.get_all_tasks()

    assert tasks[0].title == "First task"
    assert tasks[1].title == "Second task"
    assert tasks[2].title == "Third task"


def test_mark_complete_existing_task():
    """Test marking an existing task as complete."""
    service = TaskService()
    task = service.add_task("Task 1")

    assert task.completed is False

    result = service.mark_complete(task.id)

    assert result is True
    assert task.completed is True


def test_mark_complete_nonexistent_task():
    """Test marking non-existent task returns False."""
    service = TaskService()

    result = service.mark_complete(999)

    assert result is False


def test_mark_incomplete_existing_task():
    """Test marking a complete task as incomplete."""
    service = TaskService()
    task = service.add_task("Task 1")
    service.mark_complete(task.id)

    assert task.completed is True

    result = service.mark_incomplete(task.id)

    assert result is True
    assert task.completed is False


def test_mark_incomplete_nonexistent_task():
    """Test marking non-existent task as incomplete returns False."""
    service = TaskService()

    result = service.mark_incomplete(999)

    assert result is False


def test_mark_complete_multiple_tasks():
    """Test marking multiple specific tasks as complete."""
    service = TaskService()
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    task3 = service.add_task("Task 3")

    service.mark_complete(task1.id)
    service.mark_complete(task3.id)

    assert task1.completed is True
    assert task2.completed is False
    assert task3.completed is True


def test_mark_complete_toggle():
    """Test toggling task completion status."""
    service = TaskService()
    task = service.add_task("Task 1")

    # Initially incomplete
    assert task.completed is False

    # Mark complete
    service.mark_complete(task.id)
    assert task.completed is True

    # Mark incomplete
    service.mark_incomplete(task.id)
    assert task.completed is False

    # Mark complete again
    service.mark_complete(task.id)
    assert task.completed is True


def test_update_task():
    """Test updating an existing task."""
    service = TaskService()
    task = service.add_task("Original Title", "Original Description")

    # Update both title and description
    result = service.update_task(task.id, title="Updated Title", description="Updated Description")

    assert result is True
    assert task.title == "Updated Title"
    assert task.description == "Updated Description"
    assert task.id == 1  # ID should not change
    assert task.completed is False  # Status should not change


def test_update_nonexistent_task():
    """Test updating a non-existent task returns False."""
    service = TaskService()

    result = service.update_task(999, title="New Title", description="New Description")

    assert result is False


def test_update_with_empty_title():
    """Test updating task with empty title raises ValueError."""
    service = TaskService()
    task = service.add_task("Original Title")

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.update_task(task.id, title="", description="New Description")


def test_update_title_only():
    """Test updating only the title preserves description."""
    service = TaskService()
    task = service.add_task("Original Title", "Original Description")

    result = service.update_task(task.id, title="New Title")

    assert result is True
    assert task.title == "New Title"
    assert task.description == "Original Description"


def test_update_description_only():
    """Test updating only the description preserves title."""
    service = TaskService()
    task = service.add_task("Original Title", "Original Description")

    result = service.update_task(task.id, description="New Description")

    assert result is True
    assert task.title == "Original Title"
    assert task.description == "New Description"


def test_delete_task():
    """Test deleting an existing task."""
    service = TaskService()
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    task3 = service.add_task("Task 3")

    # Delete task 2
    result = service.delete_task(task2.id)

    assert result is True
    assert len(service.tasks) == 2
    assert service.get_task_by_id(2) is None
    assert service.get_task_by_id(1) is not None
    assert service.get_task_by_id(3) is not None


def test_delete_nonexistent_task():
    """Test deleting non-existent task returns False."""
    service = TaskService()
    service.add_task("Task 1")

    result = service.delete_task(999)

    assert result is False
    assert len(service.tasks) == 1


def test_delete_preserves_ids():
    """Test that deleting tasks preserves IDs and doesn't reuse them."""
    service = TaskService()
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    task3 = service.add_task("Task 3")

    # Delete task 2
    service.delete_task(task2.id)

    # Add new task - should get ID 4, not reuse ID 2
    task4 = service.add_task("Task 4")

    assert task4.id == 4
    assert service.next_id == 5
    assert len(service.tasks) == 3

    # Verify only tasks 1, 3, 4 exist
    assert service.get_task_by_id(1) is not None
    assert service.get_task_by_id(2) is None
    assert service.get_task_by_id(3) is not None
    assert service.get_task_by_id(4) is not None
