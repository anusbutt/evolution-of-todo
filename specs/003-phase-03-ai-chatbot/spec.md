# Feature Specification: Phase 3 - AI Chatbot with MCP Integration

**Feature Branch**: `003-phase-03-ai-chatbot`
**Created**: 2026-01-15
**Status**: Draft
**Input**: User description: "Phase 3 AI Chatbot with MCP Server and Gemini Integration - Natural language interface for task management using OpenAI Agents SDK with Gemini LLM and separate MCP Server"

## Overview

Phase 3 enhances the Todo application by adding an AI-powered chatbot interface that allows users to manage their tasks through natural language conversation. The chatbot is integrated as a sidebar on the existing tasks page, providing an alternative interaction method alongside the traditional UI.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Creation (Priority: P1)

As a user, I want to create tasks by typing natural language commands in the chat sidebar, so I can quickly add tasks without using form inputs.

**Why this priority**: Core chatbot functionality - without task creation via chat, the feature provides no value. This is the foundational capability that proves the AI integration works.

**Independent Test**: Can be fully tested by opening chat sidebar, typing "Add buy groceries" and verifying a new task appears in the task list.

**Acceptance Scenarios**:

1. **Given** I am logged in and on the tasks page, **When** I type "Add a task to buy groceries", **Then** a new task with title "buy groceries" is created and confirmed in chat
2. **Given** I am logged in, **When** I type "Remember to call mom tomorrow", **Then** a new task "call mom tomorrow" is created
3. **Given** I am logged in, **When** I type "I need to finish the report", **Then** a new task "finish the report" is created
4. **Given** I type an ambiguous message like "hello", **When** the system cannot determine intent, **Then** it asks for clarification

---

### User Story 2 - View Tasks via Chat (Priority: P1)

As a user, I want to ask the chatbot to show my tasks, so I can quickly see what I need to do without scrolling through the UI.

**Why this priority**: Essential read capability - users need to see their tasks to interact with them via chat. Pairs with task creation as core functionality.

**Independent Test**: Can be fully tested by typing "Show my tasks" and verifying the chat displays the current task list.

**Acceptance Scenarios**:

1. **Given** I have 3 tasks, **When** I type "Show my tasks", **Then** the chat displays all 3 tasks with their status
2. **Given** I have no tasks, **When** I type "What's on my list?", **Then** the chat responds that I have no tasks
3. **Given** I have tasks, **When** I type "List all", **Then** the chat shows all tasks in a readable format

---

### User Story 3 - Mark Task Complete via Chat (Priority: P2)

As a user, I want to mark tasks as complete using natural language, so I can update task status without clicking checkboxes.

**Why this priority**: Important for full task lifecycle management via chat. Depends on being able to view tasks first.

**Independent Test**: Can be tested by listing tasks, then typing "Mark task 1 as done" and verifying the task status changes.

**Acceptance Scenarios**:

1. **Given** I have a task "buy groceries" with ID 5, **When** I type "Mark task 5 as complete", **Then** the task is marked complete and chat confirms
2. **Given** I just asked about tasks, **When** I type "Done with the first one", **Then** the most recently referenced task is marked complete
3. **Given** I type "Complete groceries task", **When** a task matching "groceries" exists, **Then** that task is marked complete
4. **Given** I type "Mark task as done" ambiguously, **When** multiple tasks exist, **Then** the chat asks which task I mean

---

### User Story 4 - Delete Task via Chat (Priority: P2)

As a user, I want to delete tasks using natural language, so I can remove tasks without using the delete button.

**Why this priority**: Completes CRUD operations via chat. Users need ability to remove tasks they no longer need.

**Independent Test**: Can be tested by typing "Delete task 3" and verifying the task is removed from the list.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 3, **When** I type "Delete task 3", **Then** the task is deleted and chat confirms
2. **Given** I just created a task, **When** I type "Remove that task", **Then** the recently created task is deleted
3. **Given** I type "Delete the groceries task", **When** a matching task exists, **Then** that task is deleted

---

### User Story 5 - Update Task via Chat (Priority: P3)

As a user, I want to update task details using natural language, so I can modify tasks without opening the edit modal.

**Why this priority**: Nice-to-have enhancement. Basic task management works without this, but it completes the feature set.

**Independent Test**: Can be tested by typing "Change task 2 title to review documents" and verifying the update.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 2, **When** I type "Update task 2 to review documents", **Then** the task title is updated
2. **Given** I have a task "buy groceries", **When** I type "Change groceries to buy organic groceries", **Then** the task is updated

---

### User Story 6 - Chat Sidebar Toggle (Priority: P1)

As a user, I want to open and close the chat sidebar with a button, so I can access the chatbot without leaving my tasks page.

**Why this priority**: Essential UI component - without the sidebar, users cannot access the chatbot feature at all.

**Independent Test**: Can be tested by clicking the chat toggle button and verifying the sidebar opens/closes.

**Acceptance Scenarios**:

1. **Given** I am on the tasks page, **When** I click the chat button, **Then** the chat sidebar opens
2. **Given** the chat sidebar is open, **When** I click the close button, **Then** the sidebar closes
3. **Given** the sidebar is open, **When** I click outside the sidebar, **Then** the sidebar remains open (non-dismissive)

---

### Edge Cases

- What happens when the AI service is unavailable? System shows friendly error message and suggests using the traditional UI.
- What happens when the user types gibberish? System responds that it didn't understand and asks user to rephrase.
- What happens when user references a task that doesn't exist? System informs user the task was not found.
- What happens when session expires during chat? System prompts user to log in again.
- What happens when user tries to modify another user's task? System only operates on authenticated user's tasks (enforced by user_id filtering).
- What happens when multiple tasks match a description? System asks for clarification or lists matching tasks.

## Requirements *(mandatory)*

### Functional Requirements

#### Chat Interface
- **FR-001**: System MUST provide a chat sidebar accessible from the tasks page
- **FR-002**: System MUST allow users to toggle the chat sidebar open/closed via a button
- **FR-003**: System MUST display chat history for the current session
- **FR-004**: System MUST provide a text input for users to type messages
- **FR-005**: System MUST display AI responses in a conversational format
- **FR-006**: System MUST show loading indicator while AI is processing

#### Natural Language Understanding
- **FR-007**: System MUST recognize task creation intents (e.g., "add", "create", "remember", "I need to")
- **FR-008**: System MUST recognize task viewing intents (e.g., "show", "list", "what's on my list")
- **FR-009**: System MUST recognize task completion intents (e.g., "done", "complete", "mark as done", "finish")
- **FR-010**: System MUST recognize task deletion intents (e.g., "delete", "remove", "get rid of")
- **FR-011**: System MUST recognize task update intents (e.g., "update", "change", "edit", "rename")
- **FR-012**: System MUST ask clarifying questions when intent is ambiguous

#### MCP Tools
- **FR-013**: System MUST provide an `add_task` tool that creates a new task for the user
- **FR-014**: System MUST provide a `list_tasks` tool that returns all tasks for the user
- **FR-015**: System MUST provide a `complete_task` tool that marks a task as complete/incomplete
- **FR-016**: System MUST provide a `delete_task` tool that removes a task
- **FR-017**: System MUST provide an `update_task` tool that modifies task title or description

#### Agent Behavior
- **FR-018**: System MUST confirm successful actions with friendly responses (e.g., "Done! I've added 'buy groceries' to your list")
- **FR-019**: System MUST handle errors gracefully with helpful messages
- **FR-020**: System MUST use conversation context to resolve ambiguous references (e.g., "Mark it as done" refers to previously mentioned task)

#### Session Management
- **FR-021**: Conversation history MUST be session-based (cleared on logout)
- **FR-022**: System MUST maintain conversation context within a session for multi-turn interactions
- **FR-023**: System MUST associate all operations with the authenticated user

#### Architecture
- **FR-024**: MCP Server MUST run as a separate process (originally separate service; now subprocess via stdio transport due to HF Spaces DNS limitation)
- **FR-025**: MCP Server MUST be stateless (no in-memory state between requests)
- **FR-026**: Chat endpoint MUST be stateless (conversation state in database only)

### Key Entities

- **Conversation**: Represents a chat session; associated with a user; contains messages; cleared on logout
- **Message**: A single message in a conversation; has role (user/assistant), content, and timestamp
- **MCP Tool**: An atomic operation exposed to the AI agent; includes add_task, list_tasks, complete_task, delete_task, update_task

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task via chat in under 5 seconds from typing to confirmation
- **SC-002**: System correctly interprets user intent at least 90% of the time for standard phrasings
- **SC-003**: Chat sidebar opens in under 500ms when user clicks the toggle button
- **SC-004**: System responds to user messages within 3 seconds under normal conditions
- **SC-005**: All 5 task operations (add, list, complete, delete, update) are accessible via natural language
- **SC-006**: Users can complete full task management workflow without touching the traditional UI
- **SC-007**: System gracefully handles AI service failures with user-friendly error messages
- **SC-008**: Conversation context is maintained for at least 10 message exchanges within a session

## Scope

### In Scope
- Chat sidebar UI component integrated into tasks page
- Natural language task management (CRUD operations)
- MCP Server with 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Session-based conversation history
- Integration with existing authentication (JWT)
- Integration with existing task database

### Out of Scope
- Voice input/output
- Multi-language support (English only for Phase 3)
- Persistent conversation history across sessions
- Task scheduling or reminders via chat
- Integration with external calendars
- Mobile-specific chat UI optimizations
- Conversation export/sharing

## Assumptions

- Users are already authenticated via the existing Phase 2 authentication system
- Gemini API is available and accessible via the OpenAI-compatible endpoint
- The existing task service can be reused by MCP tools
- Users have modern browsers that support the chat UI components
- Network latency to Gemini API is acceptable (under 2 seconds typical)
- MCP Server and Backend can both connect to the same PostgreSQL database

## Dependencies

- Phase 2 completion (authentication, task CRUD, database)
- Gemini API access (GEMINI_API_KEY)
- OpenAI Agents SDK compatibility with Gemini
- MCP SDK for Python

---

### User Story 7 - Deploy to Vercel + Railway (Priority: P1)

As a developer, I want to deploy the frontend to Vercel and the backend to Railway, so the application is publicly accessible on free-tier hosting after the DOKS cluster was decommissioned.

**Why this priority**: Without deployment, the application is not accessible to users. Migration from DOKS (deleted to stop ~$36/mo billing) to free-tier hosting is required.

**Independent Test**: Can be verified by accessing the Vercel URL and performing signup, login, task CRUD, and chat operations.

**Acceptance Scenarios**:

1. **Given** the backend is deployed on Railway, **When** I call `GET /health`, **Then** I receive a 200 response
2. **Given** the frontend is deployed on Vercel, **When** I visit the Vercel URL, **Then** the landing page loads
3. **Given** Vercel rewrites `/api/*` to Railway, **When** I call `/api/auth/me` unauthenticated, **Then** I receive a 401 response (not a CORS error)
4. **Given** I sign up on the Vercel frontend, **When** the backend sets a cookie, **Then** the cookie persists across page refreshes (SameSite=None, Secure=True)
5. **Given** I am logged in, **When** I create/read/update/delete tasks, **Then** all CRUD operations succeed
6. **Given** Railway terminates TLS at its proxy, **When** the backend receives requests, **Then** no infinite HTTP→HTTPS redirect loop occurs

**Services excluded from migration**: Audit Service (requires Dapr/Redpanda infrastructure not available on free tier). `DAPR_ENABLED` is already `false` by default.

---

### User Story 8 - Deploy MCP Server and Enable LLM-Driven Chat (Priority: P1)

As a user, I want the AI chatbot to use LLM reasoning (via MCP tools) instead of keyword matching, so the chatbot understands natural language more intelligently (e.g., "I need milk" creates a task, not just "add milk").

**Why this priority**: The current chatbot uses brittle keyword matching (`"add" in message`). Deploying the MCP server and wiring it to the OpenAI Agents SDK enables the LLM to decide which tool to call, dramatically improving intent recognition and enabling multi-step interactions.

**Independent Test**: Type "I really need to grab some milk on my way home" in the chat — a task should be created (currently it falls through to Gemini fallback without creating a task).

**Acceptance Scenarios**:

1. **Given** the MCP server is deployed on HF Spaces, **When** I call `GET /health`, **Then** I receive `{"status": "ok", "service": "mcp-server"}`
2. **Given** the backend's `MCP_SERVER_URL` points to the MCP Space, **When** a user sends a chat message, **Then** the backend connects to the MCP server via SSE transport
3. **Given** the Agents SDK is configured with MCP tools, **When** a user says "I need milk", **Then** the LLM calls `add_task` (not keyword match) and a task is created
4. **Given** the user says "Add milk and show my list", **When** the LLM processes the message, **Then** it chains `add_task` then `list_tasks` in one turn
5. **Given** the MCP server is unavailable, **When** a user sends a chat message, **Then** the backend falls back gracefully with a user-friendly error message

**Architecture change**: Backend `chat_service.py` switches from keyword-matching + direct DB calls to OpenAI Agents SDK with MCP server connection. The MCP server runs as a second HF Space, sharing the same Neon PostgreSQL database.

---

### User Story 9 - Bundle MCP Server via Stdio Transport (Priority: P1)

As a developer, I want the MCP server to run as a subprocess inside the backend container using stdio transport, so the chatbot works reliably on HF Spaces where inter-container DNS resolution is blocked.

**Why this priority**: HF Spaces containers cannot resolve other HF Spaces hostnames (`[Errno -2] Name or service not known`). The SSE transport approach (US8) fails at the network level. Without this fix, the MCP-powered chatbot does not work in production — it always falls back to plain LLM chat without tools.

**Independent Test**: Send "add buy milk" in the chat and verify a task is actually created in the database (not just an LLM text response).

**Acceptance Scenarios**:

1. **Given** the backend container bundles MCP server code, **When** a user sends a chat message, **Then** the Agents SDK spawns `mcp_server/server_stdio.py` as a subprocess and communicates via stdin/stdout
2. **Given** the stdio MCP server is running, **When** the LLM decides to call `add_task`, **Then** the tool executes against Neon PostgreSQL and a task row is inserted
3. **Given** the subprocess approach, **When** the backend is deployed on HF Spaces, **Then** no external DNS resolution is needed (all communication is in-process)
4. **Given** the subprocess fails to start, **When** a user sends a chat message, **Then** the system falls back to plain LLM chat with a user-friendly message
5. **Given** the MCP server code is bundled in the backend, **When** the backend container builds, **Then** all MCP dependencies (`mcp[cli]`, `asyncpg`) are included in the Dockerfile

**Architecture change**: MCP transport switches from SSE (network-based, `MCPServerSse`) to stdio (subprocess-based, `MCPServerStdio`). MCP server code (`server_stdio.py`, `tools.py`, `db.py`) is copied into `phase-02/backend/mcp_server/` and runs as a child process of the FastAPI backend. The separate HF Space (`anusbutt/mcp-servers`) remains available for external testing but is no longer required by the backend.

---

## Risks

- **LLM Response Variability**: AI responses may vary; mitigate with clear system prompts and tool definitions
- **API Rate Limits**: Gemini API may have rate limits; mitigate with error handling and user feedback
- **Context Window Limits**: Long conversations may exceed context limits; mitigate with session-based clearing
- **Railway free tier cold starts**: 10-30s wake time after inactivity; mitigate with user-facing loading states
- **Vercel rewrite timeout**: 10s limit on free tier; mitigate with fast backend responses
- **Cross-origin cookies**: Some browsers block third-party cookies; mitigated by Vercel rewrite proxy making requests same-origin
- **HF Spaces inter-container DNS**: Containers cannot resolve other HF Spaces hostnames; mitigated by bundling MCP server in backend container using stdio transport
