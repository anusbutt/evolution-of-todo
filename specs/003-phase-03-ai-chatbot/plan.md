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

## Deployment Architecture: Vercel + Railway

### Context

The DigitalOcean DOKS cluster was deleted to stop ~$36/mo billing. The application is migrated to free-tier hosting: Vercel (frontend) + Railway (backend). The Neon PostgreSQL database is unchanged.

**Services excluded**: Audit Service (requires Dapr/Redpanda — not viable on free tier). `DAPR_ENABLED=false` by default.

### Architecture Diagram

```
┌─────────────────────────────────────────┐
│            User's Browser               │
│  https://<app>.vercel.app               │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│          Vercel (Frontend)              │
│          Next.js SSR + Static           │
│                                         │
│  Rewrite: /api/* → HF Spaces backend   │
│  (same-origin proxy — no CORS needed    │
│   for browser requests)                 │
└────────────┬────────────────────────────┘
             │ HTTPS (server-side rewrite)
             ▼
┌─────────────────────────────────────────┐
│      HF Spaces (Backend)               │
│      FastAPI + Uvicorn (:7860)          │
│      anusbutt-todo-app.hf.space         │
│                                         │
│  Chat: Agents SDK → MCP Server ────────┼──┐
│  Cookies: SameSite=None, Secure=True    │  │
└────────────┬────────────────────────────┘  │
             │                               │ HTTPS (SSE transport)
             │ SSL (asyncpg)                 ▼
             │              ┌─────────────────────────────────┐
             │              │   HF Spaces (MCP Server)        │
             │              │   Starlette + Uvicorn (:7860)   │
             │              │   anusbutt-todo-mcp-server       │
             │              │   .hf.space                     │
             │              │                                 │
             │              │   Tools: add_task, list_tasks,  │
             │              │   complete_task, delete_task,    │
             │              │   update_task                   │
             │              └──────────┬──────────────────────┘
             │                         │ SSL (asyncpg)
             ▼                         ▼
┌─────────────────────────────────────────┐
│       Neon PostgreSQL (shared)          │
│  Tables: users, tasks, conversations,  │
│  messages, tags, audit_logs             │
└─────────────────────────────────────────┘
```

### Rewrite-Proxy Approach

Vercel's `next.config.ts` rewrites proxy `/api/*` requests server-side to the Railway backend URL. This makes API calls appear same-origin to the browser, avoiding CORS issues for most requests. The `INTERNAL_API_URL` env var on Vercel points to the Railway backend URL.

```typescript
// next.config.ts
async rewrites() {
  const backendUrl = process.env.INTERNAL_API_URL
  if (!backendUrl) return []
  return [{ source: '/api/:path*', destination: `${backendUrl}/api/:path*` }]
}
```

### Cross-Origin Cookie Strategy

Since the Vercel rewrite proxy forwards cookies between domains, cookies must be configured for cross-origin:
- `SameSite=None` — required for cross-origin cookie sending
- `Secure=True` — required when SameSite=None (both Vercel and Railway use HTTPS)
- `path="/"` — cookie available on all paths

### Railway Backend Configuration

- **Dockerfile CMD**: `--proxy-headers --forwarded-allow-ips *` trusts Railway's reverse proxy headers
- **No HTTP→HTTPS redirect**: Railway terminates TLS at its proxy and forwards HTTP internally; the app-level redirect causes infinite loops
- **Environment variables**: DATABASE_URL, JWT_SECRET, ENVIRONMENT=production, CORS_ORIGINS, GEMINI_API_KEY, DAPR_ENABLED=false, PORT=7860

### MCP Server Deployment (HF Spaces)

The MCP server runs as a second HF Space. It has **no Dapr/Redpanda dependency** — only needs `DATABASE_URL` to connect to the shared Neon PostgreSQL database.

**MCP Server config**:
- **HF Space**: `anusbutt/todo-mcp-server`
- **Source**: `phase-03/mcp-servers/`
- **Port**: 7860 (HF Spaces requirement, overrides default 5001)
- **Dockerfile**: Already exists at `phase-03/mcp-servers/Dockerfile`
- **Transport**: SSE (Server-Sent Events) at `/sse` and `/messages` endpoints
- **Health check**: `GET /health`

**Environment variables (HF Secrets)**:
- `DATABASE_URL` — same Neon connection string as backend
- `MCP_PORT` — `7860`

**Backend integration**:
- `MCP_SERVER_URL` on backend Space set to `https://anusbutt-todo-mcp-server.hf.space`
- `chat_service.py` refactored to use OpenAI Agents SDK with MCP transport instead of keyword matching + direct DB calls

### Chat Architecture: Keyword Matching → LLM-Driven (MCP)

**Before (current)**:
```
User message → keyword match ("add" in msg?) → direct DB insert → response
```
- Brittle: misses "I need milk", "remember to call mom"
- Can't chain: "add milk and show my list" only does one action
- No LLM reasoning for tool selection

**After (with MCP via SSE — failed on HF Spaces)**:
```
User message → Agents SDK → LLM → decides tool(s) → MCP Server (SSE over network) → DB → response
```
- Failed: HF Spaces containers cannot DNS-resolve other HF Spaces hostnames
- Error: `[Errno -2] Name or service not known` when connecting to `anusbutt-mcp-servers.hf.space`

**After (with MCP via Stdio — current approach)**:
```
User message → Agents SDK → LLM → decides tool(s) → MCP Server (stdio subprocess) → DB → response
```
- LLM understands intent from context, not keywords
- Can chain multiple tools in one turn
- MCP server is discoverable — LLM auto-learns available tools
- No network needed — MCP server runs as subprocess inside backend container
- Fallback: if subprocess fails, return user-friendly error

### MCP Transport: SSE vs Stdio

| Aspect | SSE (MCPServerSse) | Stdio (MCPServerStdio) |
|--------|-------------------|----------------------|
| Communication | HTTP/SSE over network | stdin/stdout pipes |
| Deployment | Separate container/service | Bundled in backend container |
| DNS required | Yes (fails on HF Spaces) | No (in-process) |
| Scaling | Independent scaling | Scales with backend |
| Code location | `phase-03/mcp-servers/` | `phase-02/backend/mcp_server/` (copy) |
| Entrypoint | `server.py` (Starlette HTTP) | `server_stdio.py` (MCP stdio) |

### Stdio Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│  Backend HF Space Container (port 7860)         │
│                                                 │
│  FastAPI (main process)                         │
│    │                                            │
│    │ user sends chat message                    │
│    ▼                                            │
│  chat_service.py                                │
│    │                                            │
│    │ MCPServerStdio spawns subprocess           │
│    ▼                                            │
│  mcp_server/server_stdio.py (child process)     │
│    │  stdin ◄── Agent sends tool calls          │
│    │  stdout ──► Agent receives tool results    │
│    │                                            │
│    ▼                                            │
│  Neon PostgreSQL (external, via DATABASE_URL)   │
└─────────────────────────────────────────────────┘
```

### Bundled MCP Server Structure

```text
phase-02/backend/
├── mcp_server/              # Bundled MCP server (copied from phase-03)
│   ├── __init__.py
│   ├── server_stdio.py      # NEW: stdio entrypoint (mcp.run transport="stdio")
│   ├── tools.py             # Copied from phase-03/mcp-servers/tools.py
│   └── db.py                # Copied from phase-03/mcp-servers/db.py
├── app/
│   └── services/
│       └── chat_service.py  # Modified: MCPServerSse → MCPServerStdio
└── Dockerfile               # Modified: add mcp[cli] + asyncpg dependencies
```

### Urdu Language Support

**Approach**: LLM-native language detection — no translation layer, no i18n library.

The system prompt in `chat_service.py` instructs the LLM to detect the user's language and respond in the same language. Llama 3.3 70B supports Urdu natively (trained on multilingual data).

**What changes**: One line added to `SYSTEM_PROMPT` in `chat_service.py`.

**What doesn't change**: Frontend (React renders UTF-8), Database (PostgreSQL stores UTF-8), MCP tools (pass strings, language-agnostic), API (JSON supports Unicode).

```
User: "دودھ خریدنا ہے"  →  LLM detects Urdu
                          →  calls add_task(title="دودھ خریدنا")
                          →  responds in Urdu
```
