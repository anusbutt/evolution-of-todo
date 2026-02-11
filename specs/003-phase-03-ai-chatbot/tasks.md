# Tasks: Phase 3 - AI Chatbot with MCP Integration

**Input**: Design documents from `/specs/003-phase-03-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec - tests omitted. Add test tasks if TDD approach needed.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1-US6 maps to spec.md user stories)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` (FastAPI service, port 8000)
- **MCP Server**: `mcp-server/` (new Python service, port 5001)
- **Frontend**: `frontend/` (Next.js, port 3000)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize MCP Server project and extend existing services

- [x] T001 Create MCP Server directory structure per plan.md in `mcp-server/`
- [x] T002 [P] Initialize MCP Server with `mcp-server/pyproject.toml` and `mcp-server/requirements.txt`
- [x] T003 [P] Create `mcp-server/.env.example` with DATABASE_URL and MCP_PORT
- [x] T004 [P] Create `mcp-server/config.py` for environment configuration
- [x] T005 [P] Create `mcp-server/database.py` for async PostgreSQL connection
- [x] T006 Install backend dependency: `pip install openai-agents-sdk` in `backend/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models and MCP server infrastructure - MUST complete before user stories

**Warning**: No user story work can begin until this phase is complete

### Backend Models (Define structure first)

- [x] T007 [P] Create Conversation SQLModel in `backend/app/models/conversation.py`
- [x] T008 [P] Create Message SQLModel in `backend/app/models/message.py`
- [x] T009 Export new models in `backend/app/models/__init__.py`

### Database Migration (Apply schema to DB)

- [x] T010 Create Alembic migration for conversations and messages tables in `backend/alembic/versions/xxx_add_chat_tables.py`
- [x] T011 Add database trigger for conversation.updated_at auto-update in migration
- [ ] T012 Run migrations: `alembic upgrade head`

### Backend Schemas (New)

- [x] T013 [P] Create ChatRequest/ChatResponse Pydantic schemas in `backend/app/schemas/chat.py`

### MCP Server Models (Shared)

- [x] T014 [P] Create Task model for MCP in `mcp-server/models/task.py`
- [x] T015 [P] Create User model for MCP in `mcp-server/models/user.py`
- [x] T016 Export models in `mcp-server/models/__init__.py`

### MCP Server Tools Structure

- [x] T017 Create tools barrel export in `mcp-server/tools/__init__.py`

### MCP Server Entry Point

- [x] T018 Create MCP server with HTTP/SSE transport in `mcp-server/server.py`
- [ ] T019 Verify MCP server starts: `python mcp-server/server.py` (health check on port 5001)

### Backend Environment

- [x] T020 Add GEMINI_API_KEY and MCP_SERVER_URL to `backend/.env.example`

**Checkpoint**: Foundation ready - MCP Server runs, database has chat tables, models exist

---

## Phase 3: User Story 6 - Chat Sidebar Toggle (Priority: P1) - MVP UI

**Goal**: Users can open/close chat sidebar on tasks page

**Independent Test**: Click chat toggle button, verify sidebar opens/closes

**Why First**: UI shell needed before other stories can be tested interactively

### Implementation for User Story 6

- [x] T021 [P] [US6] Create ChatToggle button component in `frontend/components/chat/chat-toggle.tsx`
- [x] T022 [P] [US6] Create ChatSidebar container component in `frontend/components/chat/chat-sidebar.tsx`
- [x] T023 [P] [US6] Create ChatMessage bubble component in `frontend/components/chat/chat-message.tsx`
- [x] T024 [P] [US6] Create ChatInput component in `frontend/components/chat/chat-input.tsx`
- [x] T025 [US6] Create chat components barrel export in `frontend/components/chat/index.ts`
- [x] T026 [US6] Integrate ChatSidebar into tasks page in `frontend/app/(dashboard)/tasks/page.tsx`
- [x] T027 [US6] Add sidebar open/close state management with useState hook
- [x] T028 [US6] Style sidebar with Tailwind (slide-in animation, responsive width)

**Checkpoint**: Chat sidebar opens/closes, shows empty message list and input field

---

## Phase 4: User Story 1 - Natural Language Task Creation (Priority: P1) - MVP Core

**Goal**: Users can create tasks by typing natural language in chat

**Independent Test**: Type "Add buy groceries" in chat, verify task appears in task list

### MCP Tool: add_task

- [x] T029 [P] [US1] Implement add_task MCP tool in `mcp-server/tools/add_task.py`
- [x] T030 [US1] Register add_task tool in `mcp-server/server.py`

### Backend Chat Service

- [x] T031 [US1] Create chat service with agent setup in `backend/app/services/chat_service.py`
- [x] T032 [US1] Define agent system prompt for task management in chat_service.py
- [x] T033 [US1] Configure OpenAI Agents SDK with Gemini endpoint in chat_service.py
- [x] T034 [US1] Configure MCP server connection (HTTP transport) in chat_service.py
- [x] T035 [US1] Implement conversation get_or_create logic in chat_service.py
- [x] T036 [US1] Implement message save logic in chat_service.py
- [x] T037 [US1] Implement conversation history loading for multi-turn context in chat_service.py

### Backend Chat Route

- [x] T038 [US1] Create POST /api/chat endpoint in `backend/app/routes/chat.py`
- [x] T039 [US1] Add JWT authentication to chat route
- [x] T040 [US1] Register chat router in `backend/app/main.py`

### Frontend Chat API Client

- [x] T041 [US1] Create chat API service in `frontend/services/chat.ts`
- [x] T042 [US1] Connect ChatInput to chat API in `frontend/components/chat/chat-input.tsx`
- [x] T043 [US1] Display AI responses in ChatSidebar
- [x] T044 [US1] Show loading indicator while AI processes
- [x] T045 [US1] Auto-refresh task list when task_updated is true

**Checkpoint**: "Add buy groceries" creates task, confirmed in chat, visible in task list

---

## Phase 5: User Story 2 - View Tasks via Chat (Priority: P1)

**Goal**: Users can ask chatbot to show their tasks

**Independent Test**: Type "Show my tasks" in chat, verify task list appears in chat response

### MCP Tool: list_tasks

- [x] T046 [P] [US2] Implement list_tasks MCP tool in `mcp-server/tools/list_tasks.py`
- [x] T047 [US2] Register list_tasks tool in `mcp-server/server.py`

### Agent Configuration

- [x] T048 [US2] Update agent system prompt to format task lists nicely in `backend/app/services/chat_service.py`

**Checkpoint**: "Show my tasks" returns formatted task list in chat

---

## Phase 6: User Story 3 - Mark Task Complete via Chat (Priority: P2)

**Goal**: Users can mark tasks complete using natural language

**Independent Test**: Type "Mark task 1 as done" in chat, verify task status changes

### MCP Tool: complete_task

- [x] T049 [P] [US3] Implement complete_task MCP tool in `mcp-server/tools/complete_task.py`
- [x] T050 [US3] Register complete_task tool in `mcp-server/server.py`

### Agent Enhancements

- [x] T051 [US3] Update agent prompt to handle completion intents in chat_service.py
- [x] T052 [US3] Ensure task list refreshes after completion

**Checkpoint**: "Mark task 1 as done" changes task status, confirmed in chat and UI

---

## Phase 7: User Story 4 - Delete Task via Chat (Priority: P2)

**Goal**: Users can delete tasks using natural language

**Independent Test**: Type "Delete task 3" in chat, verify task is removed

### MCP Tool: delete_task

- [x] T053 [P] [US4] Implement delete_task MCP tool in `mcp-server/tools/delete_task.py`
- [x] T054 [US4] Register delete_task tool in `mcp-server/server.py`

### Agent Enhancements

- [x] T055 [US4] Update agent prompt to handle deletion intents in chat_service.py

**Checkpoint**: "Delete task 3" removes task, confirmed in chat and task list

---

## Phase 8: User Story 5 - Update Task via Chat (Priority: P3)

**Goal**: Users can update task details using natural language

**Independent Test**: Type "Change task 2 to review documents" in chat, verify task title changes

### MCP Tool: update_task

- [x] T056 [P] [US5] Implement update_task MCP tool in `mcp-server/tools/update_task.py`
- [x] T057 [US5] Register update_task tool in `mcp-server/server.py`

### Agent Enhancements

- [x] T058 [US5] Update agent prompt to handle update intents in chat_service.py

**Checkpoint**: "Change task 2 to review documents" updates task, confirmed in chat

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, session management, and refinements

### Error Handling

- [x] T059 [P] Implement graceful error responses for LLM timeouts in chat_service.py
- [x] T060 [P] Implement fallback message when MCP server is unavailable
- [x] T061 [P] Add user-friendly error messages in ChatSidebar component

### Session Management

- [x] T062 Implement conversation clearing on logout in `backend/app/routes/auth.py`
- [x] T063 Add conversation_id persistence in frontend chat state

### UI Polish

- [x] T064 [P] Add auto-scroll to latest message in ChatSidebar
- [x] T065 [P] Preserve input text on send failure
- [x] T066 [P] Add message timestamps display
- [x] T067 Style loading indicator with animated dots

### Validation

- [x] T068 Run quickstart.md verification steps
- [x] T069 Test all 5 sample messages from quickstart.md
- [x] T070 Verify chat works on mobile viewport widths

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phase 3 (US6 Sidebar)**: Depends on Phase 2 - UI shell for all chat features
- **Phase 4 (US1 Create)**: Depends on Phase 2 + Phase 3 - Core functionality
- **Phase 5 (US2 View)**: Depends on Phase 2 + Phase 3 - Can parallel with US1
- **Phase 6 (US3 Complete)**: Depends on Phase 2 + Phase 3
- **Phase 7 (US4 Delete)**: Depends on Phase 2 + Phase 3
- **Phase 8 (US5 Update)**: Depends on Phase 2 + Phase 3
- **Phase 9 (Polish)**: Depends on all desired user stories being complete

### User Story Dependencies

| Story | Can Start After | Dependencies |
|-------|-----------------|--------------|
| US6 (Sidebar) | Phase 2 | None (UI only) |
| US1 (Create) | Phase 2 | US6 for interactive testing |
| US2 (View) | Phase 2 | US6 for interactive testing |
| US3 (Complete) | Phase 2 | US6 + US2 (need to see tasks first) |
| US4 (Delete) | Phase 2 | US6 + US2 (need to see tasks first) |
| US5 (Update) | Phase 2 | US6 + US2 (need to see tasks first) |

### Within Each User Story

1. MCP tool implementation first
2. Register tool in server.py
3. Backend service/route updates
4. Frontend integration
5. Verify independently

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T002, T003, T004, T005 can run in parallel
```

**Phase 2 (Foundational)**:
```
T007, T008 (Backend models) can run in parallel
T013, T014, T015 (Schemas/MCP models) can run in parallel
```

**Phase 3 (US6 Sidebar)**:
```
T021, T022, T023, T024 (Chat components) can run in parallel
```

**MCP Tools across stories**:
```
After Phase 2, all MCP tools can be implemented in parallel:
T029 (add_task), T046 (list_tasks), T049 (complete_task), T053 (delete_task), T056 (update_task)
```

---

## Parallel Example: MCP Tools

```bash
# After Phase 2 completes, launch all MCP tools in parallel:
Task T029: "Implement add_task MCP tool in mcp-server/tools/add_task.py"
Task T046: "Implement list_tasks MCP tool in mcp-server/tools/list_tasks.py"
Task T049: "Implement complete_task MCP tool in mcp-server/tools/complete_task.py"
Task T053: "Implement delete_task MCP tool in mcp-server/tools/delete_task.py"
Task T056: "Implement update_task MCP tool in mcp-server/tools/update_task.py"
```

---

## Implementation Strategy

### MVP First (Phase 1-4 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T020)
3. Complete Phase 3: US6 Sidebar (T021-T028)
4. Complete Phase 4: US1 Create Task (T029-T045)
5. **STOP and VALIDATE**: Test "Add buy groceries" flow end-to-end
6. Deploy/demo MVP

**MVP Scope**: 45 tasks for basic chat + task creation

### Incremental Delivery

1. MVP (Phases 1-4): Chat sidebar + create task via chat
2. Add US2 (Phase 5): View tasks via chat
3. Add US3 (Phase 6): Complete tasks via chat
4. Add US4 (Phase 7): Delete tasks via chat
5. Add US5 (Phase 8): Update tasks via chat
6. Polish (Phase 9): Error handling, UX improvements

### Service Startup Order

1. PostgreSQL (already running from Phase 2)
2. MCP Server: `cd mcp-server && python server.py` (port 5001)
3. Backend: `cd backend && uvicorn app.main:app --reload` (port 8000)
4. Frontend: `cd frontend && npm run dev` (port 3000)

---

## Task Summary

| Phase | Description | Task Count | Parallelizable |
|-------|-------------|------------|----------------|
| 1 | Setup | 6 | 4 |
| 2 | Foundational | 14 | 5 |
| 3 | US6 Sidebar | 8 | 4 |
| 4 | US1 Create | 17 | 1 |
| 5 | US2 View | 3 | 1 |
| 6 | US3 Complete | 4 | 1 |
| 7 | US4 Delete | 3 | 1 |
| 8 | US5 Update | 3 | 1 |
| 9 | Polish | 12 | 6 |
| **Total** | | **70** | **24** |

### Tasks per User Story

| User Story | Tasks | MVP? |
|------------|-------|------|
| US6 (Sidebar) | 8 | Yes |
| US1 (Create) | 17 | Yes |
| US2 (View) | 3 | No |
| US3 (Complete) | 4 | No |
| US4 (Delete) | 3 | No |
| US5 (Update) | 3 | No |

---

---

## Phase 10: Deployment Migration — Vercel + Railway (User Story 7)

**Purpose**: Migrate from deleted DOKS cluster to free-tier hosting (Vercel frontend, Railway backend)

**Context**: DOKS deleted to stop ~$36/mo billing. Neon PostgreSQL stays. Audit Service and MCP Server skipped (require Dapr/Redpanda).

### Backend Code Changes

- [x] T071 [US7] Fix cross-origin cookies in `phase-02/backend/app/routes/auth.py` — set `samesite="none"`, `secure=True`, `path="/"` on all 3 cookie operations (signup, login, logout)
  - **Acceptance**: Cookie attributes include SameSite=None and Secure in HTTP response headers
  - **Test**: `curl -v POST /api/auth/login` shows `Set-Cookie` with `SameSite=None; Secure; Path=/`

- [x] T072 [US7] Remove HTTP→HTTPS redirect in `phase-02/backend/app/main.py` (lines 82-89) — Railway terminates TLS at proxy, causing infinite redirect loop
  - **Acceptance**: No 301 redirect when backend receives HTTP request in production
  - **Test**: `curl http://localhost:8000/health` returns 200, not 301

- [x] T073 [US7] Add proxy headers to backend Dockerfile CMD in `phase-02/backend/Dockerfile` — add `--proxy-headers --forwarded-allow-ips *` to uvicorn
  - **Acceptance**: Dockerfile CMD includes proxy-headers flags
  - **Test**: `docker build` succeeds; uvicorn logs show proxy headers enabled

### Frontend Code Changes

- [x] T074 [US7] Update rewrite config in `phase-02/frontend/next.config.ts` — require `INTERNAL_API_URL` env var (no hardcoded Docker-internal fallback)
  - **Acceptance**: Rewrites use `process.env.INTERNAL_API_URL`; returns empty array if not set
  - **Test**: `INTERNAL_API_URL=http://localhost:8000 npm run build` succeeds

### Deploy Backend on Railway

- [ ] T075 [US7] Deploy backend to Railway: New Project → GitHub repo, Root Directory `phase-02/backend`, Dockerfile builder
  - **Acceptance**: Railway deployment succeeds, service is running
  - **Test**: `curl <railway-url>/health` returns `{"status": "healthy"}`

- [ ] T076 [US7] Configure Railway environment variables: DATABASE_URL, JWT_SECRET, ENVIRONMENT=production, GEMINI_API_KEY, DAPR_ENABLED=false, PORT=8000
  - **Acceptance**: All required env vars are set in Railway dashboard
  - **Test**: Backend starts without missing-env-var errors

### Deploy Frontend on Vercel

- [ ] T077 [US7] Deploy frontend to Vercel: Import GitHub repo, Root Directory `phase-02/frontend`, Install Command `npm install --legacy-peer-deps`
  - **Acceptance**: Vercel build and deployment succeeds
  - **Test**: Vercel URL loads the landing page

- [ ] T078 [US7] Set Vercel env var `INTERNAL_API_URL` to Railway backend URL
  - **Acceptance**: Vercel rewrite proxy forwards `/api/*` to Railway
  - **Test**: `curl <vercel-url>/api/health` returns backend health response

### Connect Frontend ↔ Backend

- [ ] T079 [US7] Update Railway `CORS_ORIGINS` env var to include Vercel URL
  - **Acceptance**: Railway auto-redeploys with new CORS origins
  - **Test**: No CORS errors in browser console

### End-to-End Verification

- [ ] T080 [US7] Verify full auth flow: signup → login → cookie persistence across refresh → logout
  - **Acceptance**: User can sign up, log in, refresh page (stays authenticated), and log out
  - **Test**: Manual browser test on Vercel URL

- [ ] T081 [US7] Verify task CRUD: create → read → update → delete tasks
  - **Acceptance**: All task operations work through the Vercel-proxied API
  - **Test**: Create a task, verify it appears, update title, delete it

---

## Phase 11: Deploy MCP Server + Enable LLM-Driven Chat (User Story 8)

**Purpose**: Deploy MCP server to HF Spaces and refactor chat_service.py to use Agents SDK with MCP tools instead of keyword matching

**Context**: MCP server has no Dapr/Redpanda dependency — only needs DATABASE_URL. Deploying it enables true LLM-driven tool selection.

**Depends on**: Phase 10 (backend must be deployed first)

### MCP Server Deployment

- [ ] T082 [US8] Update MCP server Dockerfile port from 5001 to 7860 in `phase-03/mcp-servers/Dockerfile` — HF Spaces requires port 7860
  - **Acceptance**: Dockerfile EXPOSE and CMD use port 7860
  - **Test**: `docker build` succeeds

- [ ] T083 [US8] Update MCP server config to read PORT from env var in `phase-03/mcp-servers/config.py` — allow HF Spaces to set port via `MCP_PORT` env var
  - **Acceptance**: Server starts on `MCP_PORT` if set, otherwise 7860
  - **Test**: `MCP_PORT=7860 python server.py` starts on 7860

- [ ] T084 [US8] Create HF Space `anusbutt/todo-mcp-server` with Docker SDK
  - **Acceptance**: Space created and visible at huggingface.co/spaces/anusbutt/todo-mcp-server
  - **Test**: Space page loads

- [ ] T085 [US8] Push `phase-03/mcp-servers/` code to HF Space repo
  - **Acceptance**: All MCP server files pushed, build starts
  - **Test**: HF build logs show successful Docker build

- [ ] T086 [US8] Configure HF Space secrets: DATABASE_URL, MCP_PORT=7860
  - **Acceptance**: Secrets set in Space settings
  - **Test**: Factory reboot → server starts without missing-env-var errors

- [ ] T087 [US8] Verify MCP server health: `GET /health` returns OK
  - **Acceptance**: `curl https://anusbutt-todo-mcp-server.hf.space/health` returns `{"status": "ok"}`
  - **Test**: HTTP 200 response

### Backend Integration

- [ ] T088 [US8] Add `MCP_SERVER_URL` secret to backend HF Space pointing to MCP server URL
  - **Acceptance**: Backend Space has `MCP_SERVER_URL=https://anusbutt-todo-mcp-server.hf.space`
  - **Test**: Backend restarts and can resolve the MCP URL

- [ ] T089 [US8] Refactor `phase-02/backend/app/services/chat_service.py` — replace keyword matching + direct DB calls with OpenAI Agents SDK + MCP server connection via SSE transport
  - **Acceptance**: `_call_agent()` uses `Runner.run()` with MCP server, not keyword `if/elif` chains
  - **Test**: "I need milk" creates a task (currently falls through to Gemini fallback)
  - **Fallback**: If MCP server unreachable, return user-friendly error message

- [ ] T090 [US8] Push updated backend code to HF Space and verify deployment
  - **Acceptance**: Backend rebuilds successfully on HF Spaces
  - **Test**: Container logs show successful startup

### End-to-End Verification

- [ ] T091 [US8] Test LLM-driven task creation: "I really need to grab some milk on my way home"
  - **Acceptance**: Task "grab some milk" (or similar) is created
  - **Test**: Task appears in task list after chat message

- [ ] T092 [US8] Test multi-step: "Add buy groceries and show my tasks"
  - **Acceptance**: Task is created AND task list is returned in one response
  - **Test**: Chat response confirms task creation and shows full list

- [ ] T093 [US8] Test MCP server down fallback: stop MCP Space and send chat message
  - **Acceptance**: Backend returns friendly error, no 500 crash
  - **Test**: "Sorry, I'm having trouble..." message displayed in chat

**Checkpoint**: Chat uses LLM reasoning for intent detection, multi-step works, graceful fallback on MCP failure

---

## Notes

- All tasks include exact file paths
- [P] tasks can run in parallel within their phase
- Each user story checkpoint enables independent testing
- MVP = 45 tasks (Phases 1-4) for core chat + task creation
- Full feature = 70 tasks including all CRUD operations
- MCP tools are independently testable via curl to port 5001
- Phase 10 (deployment): 11 tasks for Vercel + HF Spaces migration
- Phase 11 (MCP deploy): 12 tasks for MCP server deployment + Agents SDK integration
