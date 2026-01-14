# [Task]: T056 [US2] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Pydantic schemas for task-related requests and responses.
Provides validation and serialization for task API endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """
    Schema for task creation request.

    Validation:
        - title: 1-200 characters, non-empty
        - description: Optional, 0-1000 characters
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, v: str) -> str:
        """Validate title is not only whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be only whitespace")
        return v.strip()


class TaskUpdate(BaseModel):
    """
    Schema for task update request.

    Allows partial updates (all fields optional).
    """

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not only whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be only whitespace")
        return v.strip() if v is not None else None


class TaskResponse(BaseModel):
    """
    Schema for task response.

    Used in all task endpoint responses.
    """

    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow creation from SQLModel instances


class TaskListResponse(BaseModel):
    """
    Schema for task list response.

    Returns array of tasks with metadata.
    """

    tasks: list[TaskResponse]
    total: int

    class Config:
        from_attributes = True
