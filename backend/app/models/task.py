# [Task]: T055 [P] [US2] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Task SQLModel for database table.
Stores user tasks with title, description, and completion status.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task model representing a user's task.

    Attributes:
        id: Primary key, auto-incremented
        user_id: Foreign key to users.id (CASCADE DELETE)
        title: Task title (required, 1-200 characters)
        description: Task description (optional, 0-1000 characters)
        completed: Completion status (default False)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
