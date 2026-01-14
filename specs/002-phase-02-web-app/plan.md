# Implementation Plan: Phase 2 - Full-Stack Web Application

**Branch**: `002-phase-02-web-app` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-phase-02-web-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Phase 2 transforms the Phase 1 console application into a **multi-user full-stack web application** with persistent database storage, modern web interface, and authentication. Users can register accounts, manage their personal task lists through a browser, and access their data from any device. The system provides RESTful APIs for task operations, responsive UI for desktop/mobile devices, and secure user isolation ensuring each user sees only their own tasks.

**Technical Approach**: Monorepo architecture with separate `/frontend` (Next.js 16+ App Router, TypeScript, Tailwind CSS) and `/backend` (FastAPI, SQLModel, Neon PostgreSQL) directories. Frontend communicates with backend via RESTful APIs. Authentication via Better Auth with JWT tokens (7-day expiration, httpOnly cookies). Database schema includes `users` and `tasks` tables with foreign key relationships. Component-based UI architecture with reusable components (buttons, forms, modals). File-based routing in Next.js for pages (`/login`, `/signup`, `/tasks`). All 5 Phase 1 CRUD operations preserved with database persistence.

## Technical Context

**Language/Version**:
- **Frontend**: TypeScript 5.0+, Next.js 16+ (React 19+)
- **Backend**: Python 3.13+
- **Node Runtime**: Node.js 22+ (for Next.js)

**Primary Dependencies**:
- **Frontend**: Next.js 16+, React 19+, Tailwind CSS 4+, React Hook Form 7+, Zod 3+ (validation), Better Auth (client)
- **Backend**: FastAPI 0.115+, SQLModel 0.0.22+, Uvicorn 0.32+ (ASGI server), Better Auth (Python), Pydantic 2.0+ (validation), Alembic 1.13+ (migrations), asyncpg 0.30+ (PostgreSQL driver)
- **Database Driver**: asyncpg (async PostgreSQL client)
- **Testing - Frontend**: Vitest 2+, React Testing Library, Playwright 1.48+ (E2E)
- **Testing - Backend**: pytest 8+, pytest-asyncio 0.24+, httpx 0.28+ (async test client)

**Storage**:
- Neon Serverless PostgreSQL (cloud-hosted, connection pooling enabled)
- Schema: `users` table (id, email, name, password_hash, created_at, updated_at), `tasks` table (id, user_id FK, title, description, completed, created_at, updated_at)
- Indexes: `idx_tasks_user_id`, `idx_tasks_completed`, `idx_tasks_created_at`
- Migrations: Alembic for versioned schema evolution

**Testing**:
- **Backend**: pytest with pytest-asyncio for async tests, FastAPI TestClient for API endpoint tests, coverage target 75%
- **Frontend**: Vitest for component tests, React Testing Library for UI testing, Playwright for E2E user flows
- **Integration**: E2E tests cover critical paths (signup → login → add task → mark complete → logout)

**Target Platform**:
- **Development**: Windows 11 (local development), macOS/Linux compatible
- **Browser**: Modern browsers (Chrome 120+, Firefox 120+, Safari 17+, Edge 120+)
- **Deployment**: Vercel (frontend + serverless backend functions) or dedicated API host
- **Database**: Neon cloud (PostgreSQL 16+)

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- API response time: < 500ms p95 for CRUD operations
- Page load time: < 2 seconds for task list (up to 500 tasks)
- Database query time: < 100ms for task listing with user_id filter
- Frontend bundle size: < 500KB initial load (code splitting for routes)
- Concurrent users: 100 simultaneous users without degradation

**Constraints**:
- Must use technology stack from constitution (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)
- No OAuth/SSO in Phase 2 (email/password only per user decision)
- No password reset functionality (deferred per user decision)
- No email verification (immediate account activation per user decision)
- Simple list view (no pagination per user decision)
- Modal-based editing (not inline per user decision)
- Delete confirmation required (per user decision)
- Minimum 75% test coverage (constitution requirement)
- HTTPS enforced in production
- Rate limiting: 100 requests/minute per user

**Scale/Scope**:
- Initial target: 100-1000 users
- Tasks per user: Up to 500 tasks (constitution assumption for performance testing)
- Database size: ~10,000 total tasks across all users (for query performance testing)
- API endpoints: ~10 endpoints (auth: 3, tasks: 5, health: 1)
- Frontend routes: 4 main routes (landing, login, signup, tasks)
- React components: ~20-30 components (reusable UI + task-specific + auth-specific)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Technology Stack Compliance

✅ **Frontend**: Next.js 16+ (App Router) - **COMPLIANT**
- Using Next.js 16+ as specified in constitution §VI.Phase II:104
- App Router architecture (file-based routing in `app/` directory)
- TypeScript for type safety
- Tailwind CSS for styling

✅ **Backend**: Python FastAPI - **COMPLIANT**
- Using FastAPI as specified in constitution §VI.Phase II:106
- Python 3.13+ as required in constitution §VI.Phase II:104

✅ **ORM**: SQLModel - **COMPLIANT**
- Using SQLModel as specified in constitution §VI.Phase II:107
- Combines Pydantic validation with SQLAlchemy ORM

✅ **Database**: Neon Serverless PostgreSQL - **COMPLIANT**
- Using Neon as specified in constitution §VI.Phase II:108
- Connection pooling enabled for performance

✅ **Authentication**: Better Auth (JWT tokens) - **COMPLIANT**
- Using Better Auth as specified in constitution §VI.Phase II:109
- JWT tokens with 7-day expiration
- httpOnly cookies for XSS protection

✅ **Architecture**: Monorepo (`/frontend`, `/backend`) - **COMPLIANT**
- Monorepo structure as specified in constitution §VI.Phase II:110
- Separate frontend and backend directories

✅ **API Pattern**: RESTful with `/api/{user_id}/tasks` - **COMPLIANT**
- RESTful endpoints as specified in constitution §VI.Phase II:111
- User-scoped endpoints for task isolation

✅ **Coverage**: Minimum 75% - **COMPLIANT**
- Target coverage 75% as specified in constitution §VI.Phase II:112
- Both frontend and backend tested

### Feature Scope Discipline

✅ **Basic Level Features (Phase I-V)** - **COMPLIANT**
- Add Task ✓
- Delete Task ✓
- Update Task ✓
- View Task List ✓
- Mark Complete ✓

❌ **Intermediate Level Features (Phase V ONLY)** - **DEFERRED**
- Priorities & Tags - NOT in Phase 2 (constitution §V:84-91)
- Search & Filter - Marked as P3 (nice-to-have), can be added if time permits
- Sort Tasks - NOT in Phase 2

❌ **Advanced Level Features (Phase V ONLY)** - **DEFERRED**
- Recurring Tasks - NOT in Phase 2
- Due Dates & Reminders - NOT in Phase 2

**Verdict**: ✅ COMPLIANT - All Basic features included, Intermediate/Advanced deferred to Phase V as required

### Spec-Driven Development Compliance

✅ **Spec → Plan → Tasks → Implementation Loop** - **COMPLIANT**
- spec.md created and validated (12/12 checklist items passed)
- plan.md (this file) being created now
- tasks.md will be created via `/sp.tasks` command
- Implementation will reference task IDs in code comments

✅ **Traceability** - **PLANNED**
- Every code file will contain comment: `# [Task]: T-XXX | [Spec]: spec.md §Y.Z`
- As specified in constitution §I:34

### Testing Requirements

✅ **Backend Testing** - **PLANNED**
- API endpoint tests using FastAPI TestClient (constitution §Testing Requirements:179)
- Unit tests for models and services
- Integration tests for database operations

✅ **Frontend Testing** - **PLANNED**
- Component tests using React Testing Library (constitution §Testing Requirements:180)
- E2E tests for critical flows using Playwright (constitution §Testing Requirements:181)

✅ **Auth Testing** - **PLANNED**
- JWT token validation tests (constitution §Testing Requirements:182)
- User isolation tests (prevent User A from accessing User B's tasks)

✅ **Coverage Target** - **PLANNED**
- 75% minimum coverage (constitution §Testing Requirements:183)
- Test organization: `backend/tests/`, `frontend/tests/` (constitution §Testing Requirements:184)

### Security Principles

✅ **Authentication & Authorization** - **PLANNED**
- JWT tokens for API security via Better Auth (constitution §Security Principles:208)
- User isolation: All queries filter by `user_id` (constitution §Security Principles:209)
- No shared task access between users (constitution §Security Principles:210)
- 7-day token expiration (constitution §Security Principles:211)
- HTTPS enforced in production (constitution §Security Principles:212)

✅ **Secrets Management** - **PLANNED**
- `.env` files for local development (in `.gitignore`) (constitution §Security Principles:216)
- Environment variables for sensitive config (constitution §Security Principles:219)
- Never commit secrets to Git (constitution §Security Principles:215)

✅ **Input Validation** - **PLANNED**
- Sanitize all user inputs (frontend and backend) (constitution §Security Principles:222)
- Parameterized queries via SQLModel ORM (constitution §Security Principles:223)
- JSON schema validation for API requests (constitution §Security Principles:224)
- Rate limiting: 100 requests/minute per user (constitution §Security Principles:225)
- Max request size: 1MB (constitution §Security Principles:226)

✅ **OWASP Top 10 Awareness** - **PLANNED**
- SQL Injection: Prevented via SQLModel ORM (constitution §Security Principles:229)
- XSS: React escapes by default, no `dangerouslySetInnerHTML` (constitution §Security Principles:230)
- CSRF: SameSite cookies, CORS configured (constitution §Security Principles:231)
- Broken Auth: JWT tokens, Better Auth password hashing (constitution §Security Principles:232)
- Sensitive Data: HTTPS only, no secrets in logs (constitution §Security Principles:233)

### Database Design

✅ **Normalization** - **PLANNED**
- 3NF minimum (constitution §Database Design:267)
- No redundant data

✅ **Foreign Keys** - **PLANNED**
- Enforced referential integrity (constitution §Database Design:268)
- `tasks.user_id` references `users.id` with CASCADE DELETE

✅ **Indexes** - **PLANNED**
- `idx_tasks_user_id` (query-heavy column) (constitution §Database Design:269)
- `idx_tasks_completed` (filtering)
- `idx_tasks_created_at` (sorting)

✅ **Migrations** - **PLANNED**
- Alembic for versioned, reversible migrations (constitution §Database Design:270)

✅ **Schema** - **PLANNED**
- `users`: `id` (PK), `email`, `name`, `password_hash`, `created_at`, `updated_at` (constitution §Database Design:272-273)
- `tasks`: `id` (PK), `user_id` (FK), `title`, `description`, `completed`, `created_at`, `updated_at` (constitution §Database Design:273)

### Code Quality Standards

✅ **Code Readability** - **COMMIT TO FOLLOW**
- Clear variable names (no abbreviations) (constitution §VII:143)
- Functions do ONE thing (SRP) (constitution §VII:144)
- Max 50 lines per function (hard limit: 100) (constitution §VII:145)
- Comments explain WHY, not WHAT (constitution §VII:146)
- Type hints (Python), TypeScript types (frontend) (constitution §VII:147)

✅ **Project Structure** - **COMMIT TO FOLLOW**
- `snake_case` for Python, `kebab-case` for configs (constitution §VII:150)
- Logical grouping: models, services, routes, utils (constitution §VII:151)
- Separation of concerns (constitution §VII:152)
- Follow plan.md structure exactly (constitution §VII:153)

✅ **Error Handling** - **COMMIT TO FOLLOW**
- Explicit, actionable error messages (constitution §VII:156)
- NO silent failures, all logged (constitution §VII:157)
- User-facing: clear messages (constitution §VII:158)
- System errors: full context + stack traces (constitution §VII:159)
- Structured exception types (constitution §VII:160)

✅ **Async/Await Pattern** - **COMMIT TO FOLLOW**
- `async/await` for ALL I/O (DB, API, file, network) (constitution §VII:163)
- Never blocking calls in async contexts (constitution §VII:164)
- Properly await all promises/coroutines (constitution §VII:165)

### Constitution Check Result

✅ **GATE PASSED** - No violations detected. All constitution requirements are met:
- ✅ Technology stack matches Phase II specification exactly
- ✅ Feature scope limited to Basic Level (no Intermediate/Advanced)
- ✅ Spec-driven development workflow followed
- ✅ Testing requirements planned (75% coverage target)
- ✅ Security principles incorporated in design
- ✅ Database design follows normalization and indexing guidelines
- ✅ Code quality standards committed to

**Next**: Proceed to Phase 0 (Research) to resolve technical unknowns and document design decisions.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-02-web-app/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (PENDING)
├── data-model.md        # Phase 1 output (PENDING)
├── quickstart.md        # Phase 1 output (PENDING)
├── contracts/           # Phase 1 output (PENDING)
│   ├── auth-api.yaml        # Authentication endpoints (OpenAPI 3.1)
│   ├── tasks-api.yaml       # Task CRUD endpoints (OpenAPI 3.1)
│   └── types.ts             # Shared TypeScript types
├── checklists/
│   └── requirements.md  # Spec validation (COMPLETE)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT YET)
```

### Source Code (repository root)

```text
phase-02-web/
├── frontend/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx                # Root layout
│   │   ├── page.tsx                  # Landing page (/)
│   │   ├── (auth)/                   # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx          # /login
│   │   │   ├── signup/
│   │   │   │   └── page.tsx          # /signup
│   │   │   └── layout.tsx            # Auth layout (shared)
│   │   ├── (dashboard)/              # Dashboard route group
│   │   │   ├── tasks/
│   │   │   │   └── page.tsx          # /tasks (main list)
│   │   │   └── layout.tsx            # Dashboard layout (with nav)
│   │   └── api/                      # API routes (server actions if needed)
│   ├── components/
│   │   ├── ui/                       # Reusable UI primitives
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── modal.tsx
│   │   │   ├── card.tsx
│   │   │   └── checkbox.tsx
│   │   ├── tasks/                    # Task-specific components
│   │   │   ├── task-list.tsx
│   │   │   ├── task-item.tsx
│   │   │   ├── task-form.tsx
│   │   │   └── task-stats.tsx
│   │   ├── auth/                     # Auth-specific components
│   │   │   ├── login-form.tsx
│   │   │   └── signup-form.tsx
│   │   └── layout/                   # Layout components
│   │       ├── header.tsx
│   │       └── footer.tsx
│   ├── lib/
│   │   ├── api-client.ts             # Backend API client
│   │   ├── auth.ts                   # Better Auth client config
│   │   └── utils.ts                  # Utility functions
│   ├── types/
│   │   └── index.ts                  # TypeScript type definitions
│   ├── middleware.ts                 # Auth middleware (route protection)
│   ├── tests/
│   │   ├── unit/                     # Component unit tests
│   │   └── e2e/                      # Playwright E2E tests
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── .env.local                    # Local environment vars
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── config.py                 # Configuration (env vars)
│   │   ├── database.py               # Database connection & session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User SQLModel
│   │   │   └── task.py               # Task SQLModel
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User Pydantic schemas
│   │   │   └── task.py               # Task Pydantic schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py       # User business logic
│   │   │   └── task_service.py       # Task business logic
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # Auth endpoints (signup, login, logout)
│   │   │   ├── tasks.py              # Task CRUD endpoints
│   │   │   └── health.py             # Health check endpoint
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # JWT validation middleware
│   │   │   └── rate_limit.py         # Rate limiting middleware
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── security.py           # Password hashing, token utils
│   ├── alembic/
│   │   ├── versions/                 # Migration files
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py               # Pytest fixtures
│   │   ├── unit/
│   │   │   ├── test_user_model.py
│   │   │   ├── test_task_model.py
│   │   │   ├── test_user_service.py
│   │   │   └── test_task_service.py
│   │   ├── integration/
│   │   │   ├── test_auth_endpoints.py
│   │   │   ├── test_task_endpoints.py
│   │   │   └── test_user_isolation.py
│   │   └── contract/
│   │       └── test_api_contracts.py # OpenAPI schema validation
│   ├── alembic.ini
│   ├── pyproject.toml                # UV project config
│   ├── requirements.txt              # Python dependencies
│   └── .env                          # Local environment vars
│
├── phase-01-console/                 # Phase 1 (existing, unchanged)
│   └── [existing Phase 1 structure]
│
├── .gitignore
├── README.md                         # Updated with Phase 2 setup
└── PHASE-2-ROADMAP.md                # Planning document
```

**Structure Decision**: Selected **Option 2: Web application** structure as this is a full-stack web app with separate frontend and backend. The monorepo structure keeps related code together while maintaining clear separation of concerns. Frontend uses Next.js App Router file-based routing with route groups for organization. Backend follows layered architecture (routes → services → models) for maintainability. Phase 1 code remains in separate `phase-01-console/` directory, unchanged.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All design decisions comply with constitution requirements. No complexity tracking needed.

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Next.js Frontend                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │  Pages     │  │ Components │  │  Better Auth     │   │  │
│  │  │  (App      │  │  (Task UI, │  │  Client          │   │  │
│  │  │   Router)  │  │   Auth UI) │  │  (JWT Storage)   │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  │         │                │                  │             │  │
│  │         └────────────────┴──────────────────┘             │  │
│  │                          │                                │  │
│  │                          v                                │  │
│  │                  ┌──────────────┐                         │  │
│  │                  │  API Client  │                         │  │
│  │                  │  (fetch API) │                         │  │
│  │                  └──────────────┘                         │  │
│  └────────────────────────┬─────────────────────────────────┘  │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             │ HTTPS + JWT Cookie
                             │
                             v
┌────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Middleware Layer                       │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │ │
│  │  │  CORS       │  │  JWT Auth    │  │  Rate Limit    │  │ │
│  │  │  Middleware │  │  Middleware  │  │  Middleware    │  │ │
│  │  └─────────────┘  └──────────────┘  └────────────────┘  │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                           │                                     │
│                           v                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                      Routes Layer                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐ │ │
│  │  │  /auth      │  │  /tasks     │  │  /health         │ │ │
│  │  │  (signup,   │  │  (CRUD)     │  │  (liveness)      │ │ │
│  │  │   login)    │  │             │  │                  │ │ │
│  │  └─────────────┘  └─────────────┘  └──────────────────┘ │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                           │                                     │
│                           v                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                   Services Layer                          │ │
│  │  ┌──────────────────┐         ┌───────────────────────┐  │ │
│  │  │  UserService     │         │  TaskService          │  │ │
│  │  │  (auth logic)    │         │  (CRUD logic)         │  │ │
│  │  └──────────────────┘         └───────────────────────┘  │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                           │                                     │
│                           v                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Models Layer                           │ │
│  │  ┌────────────────┐         ┌─────────────────────────┐  │ │
│  │  │  User Model    │         │  Task Model             │  │ │
│  │  │  (SQLModel)    │         │  (SQLModel)             │  │ │
│  │  └────────────────┘         └─────────────────────────┘  │ │
│  └────────────────────────┬───────────────────────────────────┘ │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              │ SQLModel ORM
                              │ (async queries)
                              v
┌─────────────────────────────────────────────────────────────────┐
│              Neon Serverless PostgreSQL Database                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Tables:                                                  │  │
│  │    • users (id, email, name, password_hash, timestamps)   │  │
│  │    • tasks (id, user_id FK, title, description,           │  │
│  │              completed, timestamps)                       │  │
│  │                                                            │  │
│  │  Indexes:                                                  │  │
│  │    • idx_tasks_user_id                                    │  │
│  │    • idx_tasks_completed                                  │  │
│  │    • idx_tasks_created_at                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram (Example: Add Task)

```
User Action                Frontend                Backend                 Database
─────────────────────────────────────────────────────────────────────────────────

1. Click                 TaskForm
   "Add Task"            opens modal
      │
      ▼
2. Fill form             Collect inputs
   (title,               (title, desc)
    description)         Validate locally
      │                  (Zod schema)
      ▼
3. Submit form           POST /api/tasks
      │                  Body: {title, desc}
      │                  Headers: Cookie(JWT)
      │ ─────────────────────────────────────────────▶
      │                                              Auth Middleware
      │                                              • Validate JWT
      │                                              • Extract user_id
      │                                              • Attach to request
      │                                                     │
      │                                                     ▼
      │                                              TasksRoute
      │                                              • Validate input
      │                                              • Call TaskService
      │                                                     │
      │                                                     ▼
      │                                              TaskService
      │                                              • Create Task obj
      │                                              • Set user_id
      │                                              • Call DB
      │                                                     │
      │                                                     ▼
      │                                              Task Model (SQLModel)
      │                                              • Build INSERT query
      │ ──────────────────────────────────────────────────────────────────▶
      │                                                                    INSERT
      │                                                                    INTO tasks
      │ ◀──────────────────────────────────────────────────────────────────
      │                                              • Return task object
      │                                              • with ID
      │ ◀─────────────────────────────────────────
      │                  Response: {
      │                    id: 123,
      │                    title: "...",
      │                    ...
      │                  }
      ▼
4. Display task          Update UI state
   in list               Append to list
                         Close modal
                         Show success msg
```

### Authentication Flow Diagram

```
User Action              Frontend                 Backend              Database
────────────────────────────────────────────────────────────────────────────────

────── SIGNUP ──────

1. Visit /signup       SignupForm
      │                displays
      ▼
2. Enter email,        Validate inputs
   name, password      (client-side)
      │
      ▼
3. Submit form         POST /auth/signup
      │                Body: {
      │                  email, name,
      │                  password
      │                }
      │ ──────────────────────────────────────────────▶
      │                                            AuthRoute
      │                                            • Check email unique ────────▶ SELECT
      │                                            • Hash password                WHERE email
      │                                            • Create user ────────────────▶ INSERT
      │                                            • Generate JWT                  INTO users
      │                                            • Set httpOnly cookie ◀────────
      │ ◀───────────────────────────────────────────
      │                Response: 201 Created
      │                Set-Cookie: auth-token=<JWT>
      ▼
4. Auto-login          Redirect to /tasks
   (JWT stored in
    cookie)

────── LOGIN ──────

1. Visit /login        LoginForm
      │                displays
      ▼
2. Enter email,        Validate inputs
   password            (client-side)
      │
      ▼
3. Submit form         POST /auth/login
      │                Body: {
      │                  email, password
      │                }
      │ ──────────────────────────────────────────────▶
      │                                            AuthRoute
      │                                            • Find user by email ─────────▶ SELECT
      │                                            • Verify password hash          WHERE email
      │                                            • Generate JWT ◀──────────────
      │                                            • Set httpOnly cookie
      │ ◀───────────────────────────────────────────
      │                Response: 200 OK
      │                Set-Cookie: auth-token=<JWT>
      ▼
4. Redirect            Navigate to /tasks
                       (JWT stored)

────── PROTECTED ROUTE ACCESS ──────

1. Visit /tasks        Middleware checks
      │                for JWT cookie
      │
      │                If missing:
      │                  redirect to /login
      │
      │                If present:
      │ ──────────────────────────────────────────────▶
      │                                            Auth Middleware
      │                                            • Validate JWT signature
      │                                            • Check expiration
      │                                            • Extract user_id
      │                                            • Attach to request
      │                                                     │
      │                                            If invalid:
      │                                              return 401
      │                                            If valid:
      │                                              continue ─────────▶ Route Handler
      ▼
2. Load page           Display tasks page
                       (authenticated)

────── LOGOUT ──────

1. Click logout        POST /auth/logout
      │                Cookie: auth-token=<JWT>
      │ ──────────────────────────────────────────────▶
      │                                            AuthRoute
      │                                            • Clear cookie
      │                                            • (JWT itself expires
      │                                               naturally, stateless)
      │ ◀───────────────────────────────────────────
      │                Response: 200 OK
      │                Clear-Cookie: auth-token
      ▼
2. Redirect            Navigate to /login
                       (logged out)
```

### Frontend Component Hierarchy

```
App Layout (layout.tsx)
│
├── Header
│   ├── Logo
│   ├── Navigation (if logged in)
│   └── Logout Button (if logged in)
│
├── Page Content (page.tsx)
│   │
│   ├── Landing Page (/)
│   │   ├── Hero Section
│   │   ├── Features List
│   │   └── CTA Buttons (Login, Signup)
│   │
│   ├── Auth Pages (/login, /signup)
│   │   ├── Auth Layout
│   │   │   └── Auth Form Container
│   │   ├── LoginForm
│   │   │   ├── Input (email)
│   │   │   ├── Input (password)
│   │   │   ├── Button (submit)
│   │   │   └── Link (to signup)
│   │   └── SignupForm
│   │       ├── Input (email)
│   │       ├── Input (name)
│   │       ├── Input (password)
│   │       ├── Button (submit)
│   │       └── Link (to login)
│   │
│   └── Tasks Page (/tasks)
│       ├── Dashboard Layout
│       │   ├── Header (app name, logout)
│       │   └── Main Content
│       ├── TaskStats
│       │   ├── Total Count
│       │   ├── Completed Count
│       │   └── Incomplete Count
│       ├── Button (Add Task)
│       ├── TaskList
│       │   └── TaskItem (repeated)
│       │       ├── Checkbox (complete toggle)
│       │       ├── Task Title
│       │       ├── Task Description (truncated)
│       │       ├── Button (Edit)
│       │       └── Button (Delete)
│       │
│       ├── Modal (Add Task) - conditionally rendered
│       │   └── TaskForm
│       │       ├── Input (title)
│       │       ├── Textarea (description)
│       │       ├── Button (Cancel)
│       │       └── Button (Save)
│       │
│       ├── Modal (Edit Task) - conditionally rendered
│       │   └── TaskForm (pre-filled)
│       │       ├── Input (title)
│       │       ├── Textarea (description)
│       │       ├── Button (Cancel)
│       │       └── Button (Save)
│       │
│       └── Modal (Delete Confirmation) - conditionally rendered
│           ├── Text ("Are you sure?")
│           ├── Button (Cancel)
│           └── Button (Confirm Delete)
│
└── Footer
    └── Copyright / Links
```

### Backend Request Flow

```
HTTP Request
    │
    ▼
FastAPI Application (main.py)
    │
    ▼
Middleware Pipeline (executed in order)
    ├── CORS Middleware
    │   └── Add CORS headers, validate origin
    │
    ├── Auth Middleware
    │   └── Validate JWT token (if protected route)
    │       ├── Extract user_id from token
    │       └── Attach to request.state.user_id
    │
    └── Rate Limit Middleware
        └── Check request count for user
            ├── If exceeded: Return 429 Too Many Requests
            └── If OK: Continue
    │
    ▼
Route Handler (routes/auth.py or routes/tasks.py)
    │
    ├── Parse request body (Pydantic validation)
    ├── Call service method
    │
    ▼
Service Layer (services/user_service.py or services/task_service.py)
    │
    ├── Business logic validation
    ├── Prepare data for database
    ├── Call model methods
    │
    ▼
Model Layer (models/user.py or models/task.py)
    │
    ├── SQLModel ORM methods
    ├── Build SQL queries (parameterized)
    ├── Execute async database operations
    │
    ▼
Database (Neon PostgreSQL)
    │
    ├── Execute query
    ├── Return results
    │
    ◀── Results flow back up
    │
    ▼
Service Layer
    │
    ├── Transform data if needed
    ├── Return domain objects
    │
    ▼
Route Handler
    │
    ├── Serialize response (Pydantic schemas)
    ├── Set HTTP status code
    ├── Add headers if needed
    │
    ▼
HTTP Response
```

## Design Decisions

### 1. Monorepo vs Multi-Repo

**Decision**: Monorepo with `/frontend` and `/backend` directories

**Rationale**:
- Constitution specifies monorepo architecture (§VI.Phase II:110)
- Easier to manage shared types and contracts
- Simplified deployment (single repository)
- Better for small team (hackathon context)
- Clear separation of concerns while keeping related code together

**Alternatives Considered**:
- Multi-repo: Rejected because increases complexity for managing versions, shared types, and deployment

### 2. Authentication Strategy

**Decision**: JWT tokens with httpOnly cookies, 7-day expiration

**Rationale**:
- Constitution specifies Better Auth with JWT tokens (§VI.Phase II:109)
- httpOnly cookies prevent XSS attacks (client JS cannot access token)
- 7-day expiration balances security and user convenience
- Stateless: No session storage on server (horizontal scalability ready)

**Alternatives Considered**:
- Session-based auth: Rejected because requires server-side session storage (not stateless)
- Local storage JWT: Rejected because vulnerable to XSS attacks

### 3. Database ORM Choice

**Decision**: SQLModel for Python backend

**Rationale**:
- Constitution specifies SQLModel (§VI.Phase II:107)
- Combines Pydantic validation with SQLAlchemy ORM
- Type-safe queries with Python type hints
- Async support for performance
- Prevents SQL injection via parameterized queries

**Alternatives Considered**:
- Raw SQL: Rejected because error-prone, no type safety, SQL injection risk
- Plain SQLAlchemy: Rejected because less integration with Pydantic validation

### 4. Frontend Routing Architecture

**Decision**: Next.js App Router with file-based routing

**Rationale**:
- Constitution specifies Next.js 16+ with App Router (§VI.Phase II:105)
- File-based routing is intuitive (`app/login/page.tsx` → `/login`)
- Route groups `(auth)` and `(dashboard)` organize related pages
- Server components by default (better performance)
- Middleware for auth protection (redirect unauthenticated users)

**Alternatives Considered**:
- Pages Router: Rejected because App Router is newer, more powerful (constitution specifies App Router)
- React Router: N/A (using Next.js framework routing)

### 5. Task Editing UI Pattern

**Decision**: Modal form for editing tasks

**Rationale**:
- User explicitly requested modal-based editing (not inline)
- Provides focus: user sees only the task being edited
- Prevents accidental edits: explicit "Save" and "Cancel" actions
- Reusable: Same TaskForm component for add and edit
- Mobile-friendly: Full-screen modal on small screens

**Alternatives Considered**:
- Inline editing: Rejected per user decision
- Separate edit page: Rejected because adds extra navigation step

### 6. Task List View Strategy

**Decision**: Simple list without pagination

**Rationale**:
- User explicitly requested simple list view (no pagination)
- Spec allows up to 500 tasks per user
- Performance target: Load 500 tasks in < 2 seconds (achievable with indexed queries)
- Simplifies implementation (no page state management)
- Can add pagination in Phase 3 if needed

**Alternatives Considered**:
- Pagination: Rejected per user decision (can revisit if performance issues arise)
- Virtual scrolling: Deferred (more complex, can add later if needed)

### 7. Form Validation Approach

**Decision**: Dual-layer validation (client + server)

**Rationale**:
- Client-side: Zod schemas for immediate feedback (better UX)
- Server-side: Pydantic schemas for security (never trust client)
- Prevents invalid data from reaching database
- Constitution requires input validation on both sides (§Security Principles:222)

**Alternatives Considered**:
- Client-only: Rejected because insecure (can bypass)
- Server-only: Rejected because poor UX (slow feedback)

### 8. Error Handling Strategy

**Decision**: User-friendly messages on frontend, detailed logs on backend

**Rationale**:
- Constitution requires clear, actionable user-facing errors (§VII:156-160)
- Backend logs full context with stack traces for debugging
- Frontend translates error codes to friendly messages
- Structured exception types (not bare `Exception`)

**Example**:
- Backend returns: `{code: "EMAIL_EXISTS", message: "Email already registered"}`
- Frontend displays: "This email is already registered. Please log in or use a different email."

### 9. Testing Strategy

**Decision**: Unit + Integration + E2E tests across frontend and backend

**Rationale**:
- Constitution requires 75% coverage (§VI.Phase II:112)
- **Backend**: pytest for unit/integration, FastAPI TestClient for API tests
- **Frontend**: Vitest for components, Playwright for E2E user flows
- Test critical paths: auth, CRUD operations, user isolation
- E2E tests validate complete user journeys (signup → task operations → logout)

**Alternatives Considered**:
- Unit tests only: Rejected because doesn't catch integration issues
- E2E tests only: Rejected because too slow, doesn't isolate failures

### 10. Deployment Strategy

**Decision**: Vercel for frontend and backend

**Rationale**:
- Simplest deployment for Next.js + FastAPI
- Automatic deployments from Git main branch
- Serverless functions for backend (or dedicated API host if needed)
- Neon PostgreSQL for database (serverless, connection pooling)
- HTTPS enforced automatically

**Alternatives Considered**:
- Separate hosting: Rejected because increases complexity
- Self-hosted: Deferred to Phase IV (Kubernetes)

## Next Steps

### Phase 0: Research (PENDING)
- Generate `research.md` documenting:
  - Better Auth integration patterns (Python + TypeScript)
  - SQLModel async query best practices
  - Next.js App Router auth middleware patterns
  - Neon PostgreSQL connection pooling configuration
  - Rate limiting implementation strategies

### Phase 1: Design Artifacts (PENDING)
- Create `data-model.md` with full database schema
- Generate API contracts in `contracts/` directory:
  - `auth-api.yaml` (OpenAPI 3.1)
  - `tasks-api.yaml` (OpenAPI 3.1)
  - `types.ts` (shared TypeScript types)
- Create `quickstart.md` for local development setup

### Phase 2: Task Breakdown (NOT YET - via `/sp.tasks`)
- Generate `tasks.md` with atomic, testable tasks
- Map tasks to user stories
- Identify dependencies and parallel opportunities

### Phase 3: Implementation (NOT YET - after task approval)
- Execute tasks in order
- Write tests first (TDD) for critical paths
- Reference task IDs in all code commits
- Achieve 75% coverage target
