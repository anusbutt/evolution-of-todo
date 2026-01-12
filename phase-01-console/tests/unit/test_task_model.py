"""Unit tests for Task model.

This module tests Task creation, validation, and serialization.
"""

import sys
import pytest

# Add project root to path
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.models.task import Task


def test_task_creation_minimal():
    """Test creating a task with minimal required fields."""
    task = Task(id=1, title="Buy groceries")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == ""
    assert task.completed is False


def test_task_creation_full():
    """Test creating a task with all fields."""
    task = Task(
        id=5,
        title="Finish quarterly report",
        description="Include Q4 summary, charts, and budget forecast",
        completed=False
    )

    assert task.id == 5
    assert task.title == "Finish quarterly report"
    assert task.description == "Include Q4 summary, charts, and budget forecast"
    assert task.completed is False


def test_task_title_strips_whitespace():
    """Test task title strips leading/trailing whitespace."""
    task = Task(id=1, title="  Buy groceries  ")

    assert task.title == "Buy groceries"


def test_task_title_empty_raises_error():
    """Test empty title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty or whitespace only"):
        Task(id=1, title="")


def test_task_title_whitespace_only_raises_error():
    """Test whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty or whitespace only"):
        Task(id=1, title="   ")


def test_task_title_too_long_raises_error():
    """Test title exceeding 200 characters raises ValueError."""
    long_title = "x" * 201

    with pytest.raises(ValueError, match="Task title must be 200 characters or less"):
        Task(id=1, title=long_title)


def test_task_title_exactly_200_chars():
    """Test title with exactly 200 characters is valid."""
    title_200 = "x" * 200
    task = Task(id=1, title=title_200)

    assert len(task.title) == 200


def test_task_description_optional():
    """Test description is optional and defaults to empty string."""
    task = Task(id=1, title="Buy groceries")

    assert task.description == ""


def test_task_description_too_long_raises_error():
    """Test description exceeding 1000 characters raises ValueError."""
    long_description = "x" * 1001

    with pytest.raises(ValueError, match="Task description must be 1000 characters or less"):
        Task(id=1, title="Valid title", description=long_description)


def test_task_description_exactly_1000_chars():
    """Test description with exactly 1000 characters is valid."""
    description_1000 = "x" * 1000
    task = Task(id=1, title="Valid title", description=description_1000)

    assert len(task.description) == 1000


def test_task_completed_defaults_to_false():
    """Test completed status defaults to False."""
    task = Task(id=1, title="Buy groceries")

    assert task.completed is False


def test_task_completed_can_be_true():
    """Test completed status can be set to True."""
    task = Task(id=1, title="Buy groceries", completed=True)

    assert task.completed is True


def test_task_to_dict():
    """Test to_dict() method returns correct dictionary."""
    task = Task(
        id=3,
        title="Call dentist",
        description="Schedule annual checkup",
        completed=False
    )

    task_dict = task.to_dict()

    assert task_dict == {
        "id": 3,
        "title": "Call dentist",
        "description": "Schedule annual checkup",
        "completed": False
    }


def test_task_repr():
    """Test __repr__() method returns correct string."""
    task = Task(id=1, title="Buy groceries", completed=False)

    repr_str = repr(task)

    assert "Task(id=1" in repr_str
    assert "title='Buy groceries'" in repr_str
    assert "completed=False" in repr_str


def test_task_completed_toggle():
    """Test completed status can be toggled."""
    task = Task(id=1, title="Buy groceries", completed=False)

    # Mark complete
    task.completed = True
    assert task.completed is True

    # Mark incomplete
    task.completed = False
    assert task.completed is False
