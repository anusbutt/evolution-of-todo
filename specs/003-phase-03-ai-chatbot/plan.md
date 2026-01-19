# Implementation Plan: Phase 3 - AI Chatbot with MCP Integration

**Branch**: `003-phase-03-ai-chatbot` | **Date**: 2026-01-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/003-phase-03-ai-chatbot/spec.md`

## Summary

Phase 3 adds an AI-powered chatbot interface to the existing Todo application, enabling users to manage tasks through natural language conversation. The implementation introduces a separate MCP Server for tool execution, integrates with Gemini API via OpenAI-compatible endpoint, and adds a chat sidebar UI to the existing tasks page.

## Technical Context

**Language/Version**: Python 3.12+ (Backend, MCP Server), TypeScript 5.x (Frontend)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK, SQLModel, Pydantic
- MCP Server: MCP SDK (Python), SQLModel, asyncpg
- Frontend: Next.js 16+, React, Tailwind CSS

**Storage**: PostgreSQL (Neon) - shared with Phase 2, new tables for conversations/messages
**Testing**: pytest (Backend, MCP), Vitest (Frontend)
**Target Platform**: Web (Linux server deployment ready)
**Project Type**: Web application (monorepo with 3 services)
**Performance Goals**: <3s response time for chat, <500ms sidebar open
**Constraints**: Stateless services, session-based conversations, user isolation
**Scale/Scope**: Same as Phase 2 (~1000 concurrent users)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | ✅ PASS | Plan references spec.md, tasks will reference plan |
| II. Single Source of Truth | ✅ PASS | Following Constitution > Spec > Plan > Tasks > Code |
| III. AI-Native Development | ✅ PASS | MCP servers for tool interfaces, PHRs created |
| IV. Progressive Enhancement | ✅ PASS | Building on Phase 2 (auth, tasks, database) |
| V. Feature Scope Discipline | ✅ PASS | Basic features only (Add, Delete, Update, View, Complete) |
| VI. Technology Stack | ✅ PASS | Using constitution-mandated stack for Phase III |
| VII. Quality Standards | ✅ PASS | Type hints, async/await, error handling planned |

**Phase III Stack Compliance**:
- ✅ AI UI: Custom Chat Sidebar (React + Tailwind)
- ✅ AI Logic: OpenAI Agents SDK (with Gemini backend)
- ✅ LLM Provider: Gemini API via OpenAI-compatible endpoint
- ✅ LLM Model: gemini-2.5-flash
- ✅ Tool Interface: Official MCP SDK (Python)
- ✅ MCP Server: Separate service (port 5001)
- ✅ MCP Transport: HTTP with SSE
- ✅ MCP Tools: add_task, list_tasks, complete_task, delete_task, update_task
- ✅ Architecture: Stateless chat endpoint, MCP server as independent service
- ✅ Conversations: Session-based (cleared on logout)

## Project Structure

### Documentation (this feature)

```text
specs/003-phase-03-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── chat-api.md      # Chat endpoint contract
│   └── mcp-tools.md     # MCP tool schemas
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
# Existing from Phase 2 (modifications)
backend/
├── app/
│   ├── models/
│   │   ├── conversation.py    # NEW: Conversation model
│   │   └── message.py         # NEW: Message model
│   ├── routes/
│   │   └── chat.py            # NEW: Chat API endpoint
│   ├── services/
│   │   └── chat_service.py    # NEW: Chat orchestration
│   └── schemas/
│       └── chat.py            # NEW: Chat request/response schemas
├── alembic/
│   └── versions/
│       └── xxx_add_chat_tables.py  # NEW: Migration
└── tests/
    └── test_chat.py           # NEW: Chat endpoint tests

# NEW: MCP Server (separate service)
mcp-server/
├── pyproject.toml
├── requirements.txt
├── .env.example
├── server.py                  # MCP server entry point
├── config.py                  # Configuration (DB URL, etc.)
├── database.py                # Database connection
├── models/                    # Shared models (Task, User)
│   ├── __init__.py
│   ├── task.py
│   └── user.py
├── tools/                     # MCP tool implementations
│   ├── __init__.py
│   ├── add_task.py
│   ├── list_tasks.py
│   ├── complete_task.py
│   ├── delete_task.py
│   └── update_task.py
└── tests/
    ├── __init__.py
    └── test_tools.py          # MCP tool tests

# Existing from Phase 2 (modifications)
frontend/
├── components/
│   └── chat/                  # NEW: Chat components
│       ├── chat-sidebar.tsx   # Sidebar container
│       ├── chat-message.tsx   # Message bubble
│       ├── chat-input.tsx     # Input field
│       └── chat-toggle.tsx    # Toggle button
├── app/
│   └── (dashboard)/
│       └── tasks/
│           └── page.tsx       # MODIFY: Add chat sidebar
└── services/
    └── chat.ts                # NEW: Chat API client
```

**Structure Decision**: Web application with 3 services (Frontend, Backend, MCP Server). MCP Server is a new independent Python service sharing the same PostgreSQL database. Frontend and Backend are modified from Phase 2.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                        │
│                         localhost:3000                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Tasks Page                                                 │ │
│  │  ┌─────────────────────────┐  ┌──────────────────────────┐ │ │
│  │  │   Task List (existing)  │  │   Chat Sidebar (NEW)     │ │ │
│  │  │   - Add task form       │  │   - Message history      │ │ │
│  │  │   - Task items          │  │   - Input field          │ │ │
│  │  │   - Status toggle       │  │   - Loading indicator    │ │ │
│  │  └─────────────────────────┘  └──────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
            │ REST API                    │ Chat API
            │ (existing)                  │ (NEW)
            ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                         │
│                         localhost:8000                           │
│  ┌──────────────────┐  ┌──────────────────────────────────────┐ │
│  │  Task Routes     │  │  Chat Route (NEW)                    │ │
│  │  /api/tasks      │  │  POST /api/chat                      │ │
│  │  (existing)      │  │  - Validate JWT                      │ │
│  └──────────────────┘  │  - Save user message                 │ │
│                        │  - Call OpenAI Agents SDK            │ │
│                        │  - Agent uses MCP tools              │ │
│                        │  - Save assistant message            │ │
│                        │  - Return response                   │ │
│                        └──────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   │ MCP Protocol (HTTP/SSE)
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MCP SERVER (Python)                         │
│                        localhost:5001                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Tools:                                                     │ │
│  │  - add_task(user_id, title, description?)                  │ │
│  │  - list_tasks(user_id)                                     │ │
│  │  - complete_task(user_id, task_id, completed)              │ │
│  │  - delete_task(user_id, task_id)                           │ │
│  │  - update_task(user_id, task_id, title?, description?)     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   │ SQL (asyncpg)
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL (Neon Cloud)                       │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  ┌────────────┐ │
│  │  users   │  │  tasks   │  │ conversations │  │  messages  │ │
│  │ (exist)  │  │ (exist)  │  │    (NEW)      │  │   (NEW)    │ │
│  └──────────┘  └──────────┘  └───────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. User types: "Add buy milk to my tasks"
   │
   ▼
2. Frontend: POST /api/chat
   {
     "message": "Add buy milk to my tasks",
     "conversation_id": "uuid" (optional, creates new if not provided)
   }
   │
   ▼
3. Backend (Chat Route):
   a. Validate JWT → get user_id
   b. Get/create conversation
   c. Save user message to DB
   d. Build agent with MCP tools config
   e. Call OpenAI Agents SDK with Gemini
   │
   ▼
4. OpenAI Agents SDK:
   - Analyzes message
   - Decides: use add_task tool
   - Calls MCP Server
   │
   ▼
5. MCP Server (HTTP/SSE):
   - Receives: add_task(user_id=2, title="buy milk")
   - Validates input (Pydantic)
   - INSERT INTO tasks (user_id, title, ...)
   - Returns: {"success": true, "task": {...}}
   │
   ▼
6. Agent formats response:
   "✓ Done! I've added 'buy milk' to your task list."
   │
   ▼
7. Backend:
   - Save assistant message to DB
   - Return response to frontend
   │
   ▼
8. Frontend:
   - Display message in chat
   - Optionally refresh task list
```

## Complexity Tracking

> No constitution violations requiring justification. Design follows all mandated patterns.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Separate MCP Server | 3 services total | Constitution mandates MCP as separate service; prepares for Phase 4 containerization |
| Shared Database | Single PostgreSQL | Constitution allows "shared DB with clear boundaries"; simpler than DB per service |
| Session-based Chat | No persistence | Constitution specifies session-based conversations |

## Key Implementation Notes

### Agent Configuration

```python
# Backend: Chat service agent setup
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

agent = Agent(
    name="TaskAssistant",
    model=llm_model,
    instructions="""You are a helpful task management assistant...""",
    mcp_servers=[mcp_server_config]  # HTTP transport to localhost:5001
)
```

### MCP Tool Schema Example

```python
# MCP Server: add_task tool
@mcp.tool()
async def add_task(
    user_id: int,
    title: str,
    description: str | None = None
) -> dict:
    """
    Add a new task for the user.

    Args:
        user_id: The authenticated user's ID
        title: The task title (required)
        description: Optional task description

    Returns:
        dict with success status and created task
    """
    ...
```

### Environment Variables (New)

```bash
# Backend .env additions
GEMINI_API_KEY=your-gemini-api-key
MCP_SERVER_URL=http://localhost:5001

# MCP Server .env
DATABASE_URL=postgresql+asyncpg://...  # Same as backend
MCP_PORT=5001
```
