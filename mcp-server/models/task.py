# [Task]: T014 [P] | [Spec]: specs/003-phase-03-ai-chatbot/data-model.md
"""
Task model for MCP Server - mirrors backend Task model.
Used for database operations in MCP tools.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task model for MCP Server database operations.

    Attributes:
        id: Primary key, auto-incremented
        user_id: Foreign key to users.id
        title: Task title (required)
        description: Task description (optional)
        completed: Completion status
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
