# Research: Phase 3 - AI Chatbot with MCP Integration

**Date**: 2026-01-15
**Feature**: 003-phase-03-ai-chatbot

## Research Tasks

### 1. OpenAI Agents SDK with Gemini Integration

**Decision**: Use OpenAI Agents SDK with custom AsyncOpenAI client pointing to Gemini API

**Rationale**:
- OpenAI Agents SDK provides robust agent framework with tool calling support
- Gemini API exposes OpenAI-compatible endpoint at `generativelanguage.googleapis.com/v1beta/openai/`
- This allows using familiar OpenAI SDK patterns with Gemini's cost-effective models
- `gemini-2.5-flash` provides good balance of speed and capability

**Alternatives Considered**:
- **Direct Gemini SDK**: More native but less feature-rich for agent orchestration
- **LangChain**: More abstraction layers, heavier dependency
- **Custom agent loop**: More control but significant implementation effort

**Implementation Pattern**:
```python
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)
```

---

### 2. MCP SDK for Python (HTTP Transport)

**Decision**: Use official MCP SDK with HTTP/SSE transport

**Rationale**:
- MCP (Model Context Protocol) is the standard for AI tool interfaces
- HTTP transport allows MCP server to run as separate service (constitution requirement)
- SSE enables streaming responses for better UX
- Official SDK ensures compatibility with OpenAI Agents SDK

**Alternatives Considered**:
- **stdio transport**: Simpler but requires subprocess management, not suitable for separate service
- **Custom REST API**: More familiar but loses MCP ecosystem benefits
- **gRPC**: Higher performance but overkill for this use case

**Key Resources**:
- MCP SDK: `pip install mcp`
- Transport: `mcp.server.sse` for HTTP/SSE server
- Tools defined with `@mcp.tool()` decorator

---

### 3. Session-based Conversation Management

**Decision**: Store conversations in PostgreSQL, cleared on logout

**Rationale**:
- Constitution specifies session-based conversations
- Database storage enables stateless backend (horizontal scaling)
- Simple cleanup on logout (DELETE WHERE user_id = ?)
- Supports multi-turn context within session

**Alternatives Considered**:
- **In-memory storage**: Not stateless, lost on restart
- **Redis**: Additional infrastructure, overkill for session data
- **Persistent conversations**: Out of scope per constitution

**Schema**:
```sql
conversations (id, user_id, created_at, updated_at)
messages (id, conversation_id, role, content, created_at)
```

---

### 4. Chat Sidebar UI Component

**Decision**: Custom React component with Tailwind CSS

**Rationale**:
- Constitution mandates custom chat sidebar (not ChatKit)
- Tailwind already used in Phase 2, consistent styling
- Full control over UX and behavior
- Integrates seamlessly with existing tasks page

**Alternatives Considered**:
- **OpenAI ChatKit**: Not compatible with Gemini API
- **Third-party chat library**: Additional dependency, less control
- **Separate chat page**: Less integrated UX

**Component Structure**:
```
components/chat/
├── chat-sidebar.tsx   # Container, state management
├── chat-message.tsx   # Message bubble (user/assistant)
├── chat-input.tsx     # Text input with send button
└── chat-toggle.tsx    # Button to open/close sidebar
```

---

### 5. MCP Tool Design Patterns

**Decision**: One tool per atomic operation, user_id passed explicitly

**Rationale**:
- Constitution: "Tools as Primitives: One tool = one atomic operation"
- Explicit user_id ensures user isolation at tool level
- Stateless tools (no session context in MCP server)
- Pydantic validation for all inputs

**Tools**:
| Tool | Parameters | Returns |
|------|-----------|---------|
| `add_task` | user_id, title, description? | task object |
| `list_tasks` | user_id | array of tasks |
| `complete_task` | user_id, task_id, completed | updated task |
| `delete_task` | user_id, task_id | success boolean |
| `update_task` | user_id, task_id, title?, description? | updated task |

---

### 6. Error Handling Strategy

**Decision**: Structured error responses with graceful degradation

**Rationale**:
- Constitution: "Handle errors gracefully with helpful messages"
- Agent should inform user of failures without technical details
- MCP tools return structured errors for agent to interpret

**Error Categories**:
| Category | Agent Response |
|----------|----------------|
| Task not found | "I couldn't find that task. Can you check the task number?" |
| Permission denied | "You don't have access to that task." |
| LLM timeout | "I'm having trouble processing that. Please try again." |
| MCP server down | "The task system is temporarily unavailable. Please use the task list directly." |

---

## Best Practices Applied

### OpenAI Agents SDK
- Use async Runner for non-blocking execution
- Configure appropriate timeouts (30s for LLM calls)
- Implement retry logic with exponential backoff

### MCP Server
- Validate all inputs with Pydantic before DB operations
- Return consistent response format: `{success: bool, data?: any, error?: string}`
- Log all tool invocations for debugging

### Chat UI
- Optimistic UI updates for better responsiveness
- Show loading indicator during agent processing
- Auto-scroll to latest message
- Preserve input on send failure

---

## Dependencies to Install

### Backend (additions to requirements.txt)
```
openai-agents-sdk>=0.1.0
```

### MCP Server (new requirements.txt)
```
mcp>=1.0.0
sqlmodel>=0.0.14
asyncpg>=0.29.0
pydantic>=2.0.0
python-dotenv>=1.0.0
uvicorn>=0.27.0
```

### Frontend (no new dependencies)
- Uses existing React, Tailwind CSS

---

## Resolved Clarifications

All technical unknowns from spec have been resolved:

| Unknown | Resolution |
|---------|------------|
| LLM integration method | OpenAI Agents SDK with Gemini via OpenAI-compatible endpoint |
| MCP transport | HTTP/SSE for separate service |
| Conversation storage | PostgreSQL (session-based) |
| Chat UI framework | Custom React + Tailwind |
| Error handling | Structured responses with user-friendly messages |
