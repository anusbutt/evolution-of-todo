"""Task model for Phase 1 Console Todo Application.

This module defines the Task entity with validation rules.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (positive integer, auto-assigned)
        title: Task name/summary (1-200 characters, non-empty)
        description: Optional detailed information (0-1000 characters)
        completed: Completion status (False = incomplete, True = complete)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        """Validate task attributes after initialization.

        Raises:
            ValueError: If validation rules are violated
        """
        # Validate title
        stripped_title = self.title.strip()
        if not stripped_title:
            raise ValueError("Task title cannot be empty or whitespace only")
        if len(stripped_title) > 200:
            raise ValueError("Task title must be 200 characters or less")

        # Store stripped title
        self.title = stripped_title

        # Validate description
        if len(self.description) > 1000:
            raise ValueError("Task description must be 1000 characters or less")

        # Ensure completed is boolean
        if not isinstance(self.completed, bool):
            raise ValueError("Task completed status must be a boolean")

    def to_dict(self) -> dict:
        """Convert Task to dictionary for display/testing.

        Returns:
            Dictionary with id, title, description, and completed fields
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    def __repr__(self) -> str:
        """String representation for debugging.

        Returns:
            String representation of Task
        """
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"
