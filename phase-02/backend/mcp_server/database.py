# [Task]: T096 [US9] | Database connection for bundled MCP server
"""Database connection for MCP Server (stdio transport)."""
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Read DATABASE_URL from environment (same as backend)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://localhost/todo_db")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
