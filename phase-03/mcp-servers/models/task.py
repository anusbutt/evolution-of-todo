# [Task]: T014 [P] | [Spec]: specs/003-phase-03-ai-chatbot/data-model.md
# [Task]: T117 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added Priority
"""
Task model for MCP Server - mirrors backend Task model.
Used for database operations in MCP tools.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Priority(str, Enum):
    """Task priority levels."""
    P1 = "P1"  # High priority
    P2 = "P2"  # Medium priority (default)
    P3 = "P3"  # Low priority


class Task(SQLModel, table=True):
    """
    Task model for MCP Server database operations.

    Attributes:
        id: Primary key, auto-incremented
        user_id: Foreign key to users.id
        title: Task title (required)
        description: Task description (optional)
        completed: Completion status
        priority: Task priority (P1=High, P2=Medium, P3=Low)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: str = Field(default="P2", index=True)  # P1, P2, P3
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
