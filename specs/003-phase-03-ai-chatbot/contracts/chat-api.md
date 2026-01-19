# API Contract: Chat Endpoint

**Date**: 2026-01-15
**Feature**: 003-phase-03-ai-chatbot
**Base URL**: `/api/chat`

## Overview

The Chat API provides a single endpoint for natural language task management. It accepts user messages, processes them through the AI agent, and returns assistant responses.

---

## Endpoints

### POST /api/chat

Send a message to the AI assistant and receive a response.

#### Authentication

- **Required**: Yes (JWT token in httpOnly cookie)
- **Header**: Cookie with `access_token`

#### Request

```json
{
  "message": "string (required)",
  "conversation_id": "uuid (optional)"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | User's natural language input (1-1000 chars) |
| conversation_id | UUID | No | Existing conversation ID for context. If omitted, creates new conversation |

#### Response (200 OK)

```json
{
  "response": "string",
  "conversation_id": "uuid",
  "task_updated": true | false,
  "timestamp": "ISO 8601 datetime"
}
```

| Field | Type | Description |
|-------|------|-------------|
| response | string | AI assistant's response text |
| conversation_id | UUID | Conversation ID (use for subsequent messages) |
| task_updated | boolean | True if a task was created/modified/deleted |
| timestamp | datetime | Response timestamp |

#### Response (400 Bad Request)

```json
{
  "detail": "Message is required"
}
```

#### Response (401 Unauthorized)

```json
{
  "detail": "Not authenticated"
}
```

#### Response (500 Internal Server Error)

```json
{
  "detail": "AI service temporarily unavailable",
  "fallback_message": "Please try using the task list directly."
}
```

---

## Examples

### Example 1: Create a Task

**Request**:
```http
POST /api/chat
Cookie: access_token=eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "message": "Add buy groceries to my list"
}
```

**Response**:
```json
{
  "response": "Done! I've added 'buy groceries' to your task list.",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_updated": true,
  "timestamp": "2026-01-15T10:30:00Z"
}
```

### Example 2: List Tasks

**Request**:
```http
POST /api/chat
Cookie: access_token=eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "message": "Show my tasks",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "response": "Here are your tasks:\n\n1. Buy groceries (pending)\n2. Call mom (completed)\n3. Finish report (pending)",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_updated": false,
  "timestamp": "2026-01-15T10:31:00Z"
}
```

### Example 3: Mark Task Complete

**Request**:
```http
POST /api/chat
Cookie: access_token=eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "message": "Mark task 1 as done",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "response": "Great job! I've marked 'buy groceries' as complete.",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_updated": true,
  "timestamp": "2026-01-15T10:32:00Z"
}
```

### Example 4: Ambiguous Request

**Request**:
```http
POST /api/chat
Cookie: access_token=eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "message": "Delete the task",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "response": "Which task would you like to delete? You have:\n\n1. Buy groceries (completed)\n2. Finish report (pending)\n\nPlease specify the task number or name.",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_updated": false,
  "timestamp": "2026-01-15T10:33:00Z"
}
```

---

## Rate Limiting

- **Limit**: 100 requests per minute per user (same as other API endpoints)
- **Header**: `X-RateLimit-Remaining` indicates remaining requests
- **Response (429)**: Too many requests

---

## Error Handling

| Error Code | Scenario | User-Facing Message |
|------------|----------|---------------------|
| 400 | Empty message | "Please enter a message" |
| 401 | No/invalid token | "Please log in to use the assistant" |
| 429 | Rate limited | "Too many requests. Please wait a moment." |
| 500 | LLM timeout | "I'm having trouble processing that. Please try again." |
| 503 | MCP server down | "The task system is temporarily unavailable." |

---

## Pydantic Schemas

### ChatRequest
```python
from pydantic import BaseModel, Field
from uuid import UUID

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: UUID | None = None
```

### ChatResponse
```python
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID
    task_updated: bool
    timestamp: datetime
```
