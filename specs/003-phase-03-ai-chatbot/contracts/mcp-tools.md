# MCP Tool Schemas: Task Management

**Date**: 2026-01-15
**Feature**: 003-phase-03-ai-chatbot
**Server**: MCP Server (localhost:5001)
**Transport**: HTTP with SSE

## Overview

The MCP Server exposes 5 tools for task management operations. All tools require a `user_id` parameter for user isolation.

---

## Tool: add_task

Create a new task for the user.

### Schema

```json
{
  "name": "add_task",
  "description": "Add a new task to the user's task list",
  "parameters": {
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
}
```

### Response

**Success**:
```json
{
  "success": true,
  "task": {
    "id": 5,
    "title": "buy groceries",
    "description": null,
    "completed": false,
    "created_at": "2026-01-15T10:30:00Z"
  }
}
```

**Error**:
```json
{
  "success": false,
  "error": "Title cannot be empty"
}
```

---

## Tool: list_tasks

Retrieve all tasks for the user.

### Schema

```json
{
  "name": "list_tasks",
  "description": "Get all tasks for the user, optionally filtered by status",
  "parameters": {
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
}
```

### Response

**Success**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": 1,
      "title": "buy groceries",
      "description": "From the supermarket",
      "completed": false,
      "created_at": "2026-01-15T09:00:00Z"
    },
    {
      "id": 2,
      "title": "call mom",
      "description": null,
      "completed": true,
      "created_at": "2026-01-14T15:00:00Z"
    }
  ],
  "count": 2
}
```

**Empty**:
```json
{
  "success": true,
  "tasks": [],
  "count": 0
}
```

---

## Tool: complete_task

Mark a task as complete or incomplete.

### Schema

```json
{
  "name": "complete_task",
  "description": "Toggle the completion status of a task",
  "parameters": {
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
      "completed": {
        "type": "boolean",
        "description": "The new completion status"
      }
    },
    "required": ["user_id", "task_id", "completed"]
  }
}
```

### Response

**Success**:
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "buy groceries",
    "completed": true,
    "updated_at": "2026-01-15T10:35:00Z"
  }
}
```

**Error (not found)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

**Error (wrong user)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

Note: "Task not found" is returned for both non-existent tasks and tasks belonging to other users (security: don't reveal task existence).

---

## Tool: delete_task

Remove a task from the user's list.

### Schema

```json
{
  "name": "delete_task",
  "description": "Delete a task from the user's task list",
  "parameters": {
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
}
```

### Response

**Success**:
```json
{
  "success": true,
  "deleted_task_id": 3
}
```

**Error**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

---

## Tool: update_task

Modify an existing task's title or description.

### Schema

```json
{
  "name": "update_task",
  "description": "Update the title or description of an existing task",
  "parameters": {
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
        "description": "New task title (optional)",
        "maxLength": 255
      },
      "description": {
        "type": "string",
        "description": "New task description (optional)",
        "maxLength": 1000
      }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### Response

**Success**:
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "buy organic groceries",
    "description": "From the farmers market",
    "completed": false,
    "updated_at": "2026-01-15T10:40:00Z"
  }
}
```

**Error (no changes)**:
```json
{
  "success": false,
  "error": "No fields to update"
}
```

---

## Python Implementation Signatures

```python
from mcp import tool

@tool()
async def add_task(user_id: int, title: str, description: str | None = None) -> dict:
    """Add a new task to the user's task list."""
    ...

@tool()
async def list_tasks(user_id: int, completed: bool | None = None) -> dict:
    """Get all tasks for the user, optionally filtered by status."""
    ...

@tool()
async def complete_task(user_id: int, task_id: int, completed: bool) -> dict:
    """Toggle the completion status of a task."""
    ...

@tool()
async def delete_task(user_id: int, task_id: int) -> dict:
    """Delete a task from the user's task list."""
    ...

@tool()
async def update_task(
    user_id: int,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> dict:
    """Update the title or description of an existing task."""
    ...
```

---

## Security Considerations

1. **User Isolation**: All tools require `user_id` and filter queries by it
2. **No Enumeration**: "Task not found" for both missing and unauthorized tasks
3. **Input Validation**: All inputs validated via Pydantic before DB operations
4. **No Secrets in Responses**: Task data only, no internal IDs or sensitive info
5. **Rate Limiting**: Inherited from backend (100 req/min per user)
