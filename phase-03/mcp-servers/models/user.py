# [Task]: T015 [P] | [Spec]: specs/003-phase-03-ai-chatbot/data-model.md
"""
User model for MCP Server - mirrors backend User model (read-only).
Used for user validation in MCP tools.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User model for MCP Server database operations (read-only).

    Attributes:
        id: Primary key
        email: User email address
        hashed_password: Password hash (not used in MCP)
        created_at: Account creation timestamp
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
