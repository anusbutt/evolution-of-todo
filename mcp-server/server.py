# [Task]: T018, T030, T047 | [Spec]: specs/003-phase-03-ai-chatbot/plan.md
"""
MCP Server for Task Management - Phase 3 AI Chatbot.
Provides tools for task CRUD operations via HTTP/SSE transport.
"""
import asyncio
import logging
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse

from config import settings
from tools.add_task import add_task
from tools.list_tasks import list_tasks
from tools.complete_task import complete_task
from tools.delete_task import delete_task
from tools.update_task import update_task

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create MCP server instance
mcp_server = Server("task-management-mcp")


@mcp_server.list_tools()
async def list_tools():
    """List available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Add a new task to the user's task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user's ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title (required)",
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                        "maxLength": 1000
                    }
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Get all tasks for the user, optionally filtered by status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user's ID"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "Filter by completion status (optional)"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task from the user's task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update a task's title or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task (optional)",
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task (optional)",
                        "maxLength": 1000
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""
    if name == "add_task":
        return await add_task(
            user_id=arguments["user_id"],
            title=arguments["title"],
            description=arguments.get("description")
        )
    elif name == "list_tasks":
        return await list_tasks(
            user_id=arguments["user_id"],
            completed=arguments.get("completed")
        )
    elif name == "complete_task":
        return await complete_task(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"]
        )
    elif name == "delete_task":
        return await delete_task(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"]
        )
    elif name == "update_task":
        return await update_task(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"],
            title=arguments.get("title"),
            description=arguments.get("description")
        )
    else:
        raise ValueError(f"Unknown tool: {name}")


# Health check endpoint
async def health_check(request):
    """Health check endpoint for service verification."""
    return JSONResponse({"status": "ok", "service": "mcp-server", "port": settings.mcp_port})


# SSE endpoint handler
async def handle_sse(request):
    """Handle SSE connections for MCP protocol."""
    transport = SseServerTransport("/messages")
    async with transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp_server.run(
            streams[0], streams[1], mcp_server.create_initialization_options()
        )


# Message endpoint for SSE
async def handle_messages(request):
    """Handle messages endpoint for SSE transport."""
    transport = SseServerTransport("/messages")
    return await transport.handle_post_message(request.scope, request.receive, request._send)


# Create Starlette app
app = Starlette(
    debug=settings.debug,
    routes=[
        Route("/health", health_check, methods=["GET"]),
        Route("/sse", handle_sse, methods=["GET"]),
        Route("/messages", handle_messages, methods=["POST"]),
    ],
)


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting MCP Server on port {settings.mcp_port}")
    uvicorn.run(app, host="0.0.0.0", port=settings.mcp_port)
