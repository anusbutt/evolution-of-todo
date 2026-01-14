# Phase 2 Roadmap: Full-Stack Web Application

**Status**: Planning Phase
**Created**: 2026-01-12
**Phase 1 Completion**: ✅ Complete (87.91% coverage, 71 tests passing)

---

## 📋 Executive Summary

Phase 2 transforms the console application into a **full-stack web application** with:
- 🌐 **Modern web interface** (Next.js + TypeScript)
- 🔐 **Multi-user authentication** (Better Auth + JWT)
- 💾 **Persistent database storage** (Neon PostgreSQL)
- 🚀 **RESTful API** (FastAPI + SQLModel)
- 🎨 **Responsive UI** (Tailwind CSS)

---

## 🎯 Core Objectives

### 1. Data Persistence
**Problem**: Phase 1 loses all data when the application closes
**Solution**: PostgreSQL database with proper migrations and schema design

### 2. Multi-User Support
**Problem**: Phase 1 is single-user only
**Solution**: Authentication system with user isolation (each user sees only their tasks)

### 3. Web Accessibility
**Problem**: Phase 1 requires command-line access
**Solution**: Browser-based interface accessible from any device

### 4. Scalability Foundation
**Problem**: Phase 1 is bound to single process/machine
**Solution**: Stateless API design ready for horizontal scaling

---

## 📊 Phase 1 → Phase 2 Evolution

### What We Keep (Business Logic)
✅ **5 Core Features** (from Phase 1):
1. Add Task (title + description)
2. View All Tasks (with status indicators)
3. Update Task (title/description)
4. Delete Task (permanent removal)
5. Mark Complete/Incomplete (toggle status)

✅ **Validation Rules**:
- Title: Required, 1-200 characters
- Description: Optional, 0-1000 characters
- Task IDs: Auto-incrementing, never reused
- Status: Boolean (complete/incomplete)

✅ **Test Coverage**: Maintain 75%+ (down from 80% per constitution)

### What Changes (Technical Implementation)

| Aspect | Phase 1 | Phase 2 |
|--------|---------|---------|
| **Storage** | In-memory (list/dict) | PostgreSQL database |
| **Interface** | CLI (text prompts) | Web UI (React components) |
| **Architecture** | Single file/process | Client-Server (Frontend + Backend) |
| **Users** | Single user | Multi-user with authentication |
| **Data Lifetime** | Session only | Persistent across sessions |
| **Access** | Local terminal | Browser (any device) |
| **State Management** | In-process variables | Database + JWT tokens |
| **Deployment** | `python main.py` | Frontend + Backend servers |

---

## 🏗️ Technology Stack (Per Constitution)

### Frontend
```
Technology: Next.js 16+ (App Router)
Language: TypeScript
Styling: Tailwind CSS
State: React hooks + Server components
Routing: Next.js App Router
Forms: React Hook Form + Zod validation
HTTP Client: fetch API (built-in)
```

### Backend
```
Framework: FastAPI
Language: Python 3.13+
ORM: SQLModel (Pydantic + SQLAlchemy)
Database: Neon Serverless PostgreSQL
Auth: Better Auth (JWT tokens)
Validation: Pydantic models
API Pattern: RESTful
```

### Architecture
```
Structure: Monorepo
Folders: /frontend, /backend
API Endpoints: /api/{user_id}/tasks
Auth Flow: JWT tokens (7-day expiration)
CORS: Configured for localhost + production domains
```

---

## 📐 Proposed Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Web Browser                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Next.js Frontend (Port 3000)            │   │
│  │  - React Components (TypeScript)                │   │
│  │  - Tailwind CSS Styling                         │   │
│  │  - Client-side validation                       │   │
│  │  - JWT token storage (httpOnly cookies)        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ├─ HTTP/JSON (fetch)
                          │
┌─────────────────────────▼─────────────────────────────┐
│         FastAPI Backend (Port 8000)                   │
│  ┌──────────────────────────────────────────────┐    │
│  │  API Routes (/api/{user_id}/tasks)          │    │
│  │  - JWT authentication middleware            │    │
│  │  - Request validation (Pydantic)            │    │
│  │  - Business logic (task operations)         │    │
│  └──────────────────────────────────────────────┘    │
│                        │                              │
│  ┌──────────────────────▼──────────────────────┐     │
│  │  SQLModel ORM (database layer)              │     │
│  │  - Task model                                │     │
│  │  - User model                                │     │
│  │  - Query building                            │     │
│  └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
                          │
                          ├─ PostgreSQL Protocol
                          │
┌─────────────────────────▼─────────────────────────────┐
│      Neon PostgreSQL Database (Serverless)            │
│  ┌──────────────────────────────────────────────┐    │
│  │  Tables:                                      │    │
│  │  - users (id, email, name, created_at)       │    │
│  │  - tasks (id, user_id, title, description,   │    │
│  │           completed, created_at, updated_at) │    │
│  └──────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────┘
```

### Directory Structure

```
evolution-of-todo/
├── phase-01-console/          # Phase 1 (complete)
│   └── ...
├── phase-02-web/              # Phase 2 (new)
│   ├── frontend/
│   │   ├── app/               # Next.js App Router
│   │   │   ├── (auth)/       # Auth-protected routes
│   │   │   │   ├── tasks/    # Task management pages
│   │   │   │   └── layout.tsx
│   │   │   ├── api/          # API routes (if needed)
│   │   │   ├── login/        # Login page
│   │   │   ├── signup/       # Signup page
│   │   │   └── layout.tsx    # Root layout
│   │   ├── components/       # React components
│   │   │   ├── ui/           # Reusable UI components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskItem.tsx
│   │   ├── lib/              # Utilities
│   │   │   ├── api.ts        # API client
│   │   │   └── auth.ts       # Auth helpers
│   │   ├── types/            # TypeScript types
│   │   ├── public/           # Static assets
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   └── README.md
│   ├── backend/
│   │   ├── app/
│   │   │   ├── models/       # SQLModel models
│   │   │   │   ├── user.py
│   │   │   │   └── task.py
│   │   │   ├── routes/       # API endpoints
│   │   │   │   ├── auth.py   # Login, signup, logout
│   │   │   │   └── tasks.py  # Task CRUD operations
│   │   │   ├── services/     # Business logic
│   │   │   │   └── task_service.py
│   │   │   ├── middleware/   # JWT auth, CORS
│   │   │   ├── database.py   # DB connection
│   │   │   ├── config.py     # Settings
│   │   │   └── main.py       # FastAPI app
│   │   ├── tests/
│   │   │   ├── test_auth.py
│   │   │   └── test_tasks.py
│   │   ├── alembic/          # Database migrations
│   │   ├── requirements.txt
│   │   ├── pyproject.toml
│   │   └── README.md
│   ├── .env.example
│   ├── docker-compose.yml    # Local development
│   └── README.md
├── specs/
│   ├── 001-phase-01-console-todo/  # Phase 1 specs (complete)
│   └── 002-phase-02-web-app/       # Phase 2 specs (to create)
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── data-model.md
│       ├── api-contracts.md
│       └── checklists/
└── PHASE-2-ROADMAP.md         # This file
```

---

## 🗄️ Database Schema (Preliminary)

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

**Key Design Decisions**:
- `user_id` foreign key ensures referential integrity
- Cascade delete: When user deleted, their tasks are automatically deleted
- Indexes on query-heavy columns (user_id, completed, created_at)
- `updated_at` tracked for audit purposes
- VARCHAR(200) matches Phase 1 title length constraint

---

## 🔐 Authentication Flow

### Registration
```
1. User fills signup form (email, name, password)
2. Frontend validates input (email format, password strength)
3. POST /api/auth/signup with credentials
4. Backend validates (no duplicate email)
5. Password hashed (Better Auth handles this)
6. User record created in database
7. JWT token generated and returned
8. Frontend stores token (httpOnly cookie)
9. User redirected to tasks page
```

### Login
```
1. User fills login form (email, password)
2. Frontend validates input
3. POST /api/auth/login with credentials
4. Backend verifies credentials (email + password hash)
5. JWT token generated (7-day expiration)
6. Token returned to frontend
7. Frontend stores token (httpOnly cookie)
8. User redirected to tasks page
```

### Protected Routes
```
1. User navigates to /tasks
2. Frontend checks for valid JWT token
3. If no token → redirect to /login
4. If token exists → include in Authorization header
5. Backend validates token on every API request
6. If invalid/expired → return 401 Unauthorized
7. Frontend clears token and redirects to /login
```

---

## 🌐 API Design (RESTful)

### Authentication Endpoints
```
POST   /api/auth/signup        # Register new user
POST   /api/auth/login         # Authenticate user
POST   /api/auth/logout        # Invalidate token
GET    /api/auth/me            # Get current user info
```

### Task Endpoints (All require authentication)
```
GET    /api/{user_id}/tasks              # List all tasks for user
POST   /api/{user_id}/tasks              # Create new task
GET    /api/{user_id}/tasks/{task_id}    # Get single task
PUT    /api/{user_id}/tasks/{task_id}    # Update task
DELETE /api/{user_id}/tasks/{task_id}    # Delete task
PATCH  /api/{user_id}/tasks/{task_id}/complete   # Mark complete
PATCH  /api/{user_id}/tasks/{task_id}/incomplete # Mark incomplete
```

### Request/Response Examples

**Create Task**:
```json
POST /api/1/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

Response (201 Created):
{
  "id": 1,
  "user_id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-12T10:30:00Z",
  "updated_at": "2026-01-12T10:30:00Z"
}
```

**List Tasks**:
```json
GET /api/1/tasks?completed=false&sort=created_at&order=desc
Authorization: Bearer <jwt_token>

Response (200 OK):
{
  "tasks": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-12T10:30:00Z",
      "updated_at": "2026-01-12T10:30:00Z"
    }
  ],
  "total": 1,
  "completed": 0,
  "incomplete": 1
}
```

---

## 🎨 UI/UX Considerations

### Key Pages

1. **Landing Page** (`/`)
   - Hero section explaining the app
   - "Sign Up" and "Login" CTAs
   - Feature highlights

2. **Signup Page** (`/signup`)
   - Email, name, password fields
   - Client-side validation
   - Link to login page

3. **Login Page** (`/login`)
   - Email, password fields
   - "Forgot password" link (future)
   - Link to signup page

4. **Tasks Dashboard** (`/tasks`)
   - Task list with status indicators
   - "Add Task" button (opens modal/form)
   - Filter: All / Active / Completed
   - Sort: Date / Title
   - Each task has: Edit, Delete, Complete/Incomplete actions

5. **Task Form** (Modal or inline)
   - Title input (required)
   - Description textarea (optional)
   - Save / Cancel buttons

### Design Principles
- **Mobile-first**: Responsive design works on all screen sizes
- **Accessibility**: Keyboard navigation, ARIA labels, semantic HTML
- **Performance**: Server components, minimal client JS
- **User feedback**: Loading states, success/error messages
- **Consistent**: Tailwind design system

---

## 🚧 Key Technical Challenges

### 1. User Isolation
**Challenge**: Ensure users only see their own tasks
**Solution**:
- Every API endpoint filters by `user_id`
- JWT token contains `user_id` claim
- Database queries always include `WHERE user_id = :user_id`
- Test: Attempt to access another user's task → 404 Not Found

### 2. State Management
**Challenge**: Keep frontend and backend in sync
**Solution**:
- Optimistic updates (immediate UI feedback)
- Server state management (React Query or SWR)
- Error handling and rollback on failure
- Real-time sync on focus (refetch on window focus)

### 3. Authentication Security
**Challenge**: Secure token storage and transmission
**Solution**:
- httpOnly cookies (not localStorage - XSS protection)
- HTTPS only in production
- Token expiration (7 days)
- CORS properly configured
- Rate limiting (100 requests/minute per user)

### 4. Database Migrations
**Challenge**: Schema evolution without data loss
**Solution**:
- Alembic for versioned migrations
- Reversible migrations (up/down)
- Test migrations on staging first
- Backup before production migrations

### 5. Error Handling
**Challenge**: Graceful failures with user feedback
**Solution**:
- Structured error responses (FastAPI HTTPException)
- Frontend error boundaries
- User-friendly error messages
- Logging for debugging (backend)

---

## ✅ Success Criteria (Definition of Done)

### Functional Requirements
- ✅ Users can sign up with email/password
- ✅ Users can log in with credentials
- ✅ Users can log out (token invalidated)
- ✅ Users can create tasks (title + description)
- ✅ Users can view all their tasks
- ✅ Users can update task title/description
- ✅ Users can delete tasks
- ✅ Users can mark tasks complete/incomplete
- ✅ Users see ONLY their own tasks (user isolation)
- ✅ Tasks persist across sessions (database storage)

### Technical Requirements
- ✅ **Test Coverage**: Minimum 75% (constitution requirement)
- ✅ **Backend Tests**: API endpoint tests (FastAPI TestClient)
- ✅ **Frontend Tests**: Component tests (React Testing Library)
- ✅ **E2E Tests**: Critical user flows (Playwright)
- ✅ **Database**: PostgreSQL with proper migrations
- ✅ **API**: RESTful endpoints with JWT authentication
- ✅ **Security**: Input validation, SQL injection prevention, XSS protection
- ✅ **Documentation**: API docs (FastAPI auto-generated), README with setup instructions

### Non-Functional Requirements
- ✅ **Performance**: Page load < 2 seconds
- ✅ **Responsive**: Works on mobile, tablet, desktop
- ✅ **Accessibility**: WCAG 2.1 Level AA compliance
- ✅ **Error Handling**: User-friendly error messages
- ✅ **Code Quality**: TypeScript strict mode, Python type hints

---

## 📅 Proposed User Stories (For spec.md)

### User Story 1: User Registration & Authentication (P1)
**As a** new user
**I want to** create an account with email and password
**So that** I can securely access my tasks from any device

**Acceptance Criteria**:
- User can register with unique email
- Password is securely hashed
- JWT token generated on successful login
- Token expires after 7 days
- User can log out (token invalidated)

---

### User Story 2: Task Management (P1)
**As a** logged-in user
**I want to** perform CRUD operations on my tasks
**So that** I can manage my todo list efficiently

**Acceptance Criteria**:
- User can create task with title (required) and description (optional)
- User can view all their tasks with status indicators
- User can update task title and description
- User can delete tasks
- User can mark tasks complete/incomplete
- All tasks persist in database

---

### User Story 3: User Isolation (P1)
**As a** user
**I want to** see only my own tasks
**So that** my task list remains private and secure

**Acceptance Criteria**:
- Each task is associated with a user_id
- API endpoints filter tasks by authenticated user
- Attempting to access another user's task returns 404
- Database queries enforce user isolation

---

### User Story 4: Responsive UI (P2)
**As a** user on any device
**I want to** access my tasks from mobile, tablet, or desktop
**So that** I can manage tasks wherever I am

**Acceptance Criteria**:
- UI adapts to screen size (mobile-first design)
- Touch-friendly on mobile devices
- Keyboard navigation works on desktop
- All features accessible on all device types

---

### User Story 5: Task Filtering & Sorting (P3)
**As a** user with many tasks
**I want to** filter and sort my task list
**So that** I can focus on what's relevant

**Acceptance Criteria**:
- Filter: All / Active / Completed
- Sort: Date (newest/oldest), Title (A-Z/Z-A)
- Filters and sorts can be combined
- Selection persists during session

---

## 🎯 Next Steps

### 1. Specification Phase (Next)
Create comprehensive spec.md with:
- All user stories detailed with acceptance scenarios
- Edge cases documented
- Success criteria defined
- Testing strategy outlined

### 2. Planning Phase
Create plan.md with:
- Detailed architecture diagrams
- Component breakdown
- API contract specifications
- Database schema finalization
- Technology decisions documented

### 3. Task Breakdown
Create tasks.md with:
- Granular, testable tasks
- Task dependencies identified
- Parallel opportunities marked
- Estimated complexity/effort

### 4. Implementation Phases
Proposed implementation order:
1. **Phase 2.1**: Database setup + migrations
2. **Phase 2.2**: Backend API (auth + tasks)
3. **Phase 2.3**: Frontend UI (auth pages)
4. **Phase 2.4**: Frontend UI (task management)
5. **Phase 2.5**: Integration testing + polish

---

## 🤔 Open Questions for Discussion

Before starting spec.md, we should discuss:

### 1. Scope Questions
- **Password Reset**: Include "forgot password" flow in Phase 2, or defer to later?
- **Email Verification**: Require email verification on signup, or skip for now?
- **Task Sharing**: Allow sharing tasks between users? (Probably Phase 3+)
- **Task Categories/Tags**: Defer to Phase 5 per constitution?

### 2. Technical Questions
- **Deployment**: Where will we host? (Vercel for frontend, Railway/Render for backend?)
- **Database**: Use Neon free tier or local PostgreSQL for development?
- **Testing**: Which E2E testing framework? (Playwright, Cypress, or skip for Phase 2?)
- **CI/CD**: Set up GitHub Actions in Phase 2, or defer?

### 3. UX Questions
- **Task Display**: Infinite scroll, pagination, or load all?
- **Task Editing**: Inline editing or modal form?
- **Confirmation Dialogs**: Confirm before delete, or allow easy undo?
- **Loading States**: Skeleton screens or spinners?

---

## 📚 Resources & References

### Constitution
- `/.specify/memory/constitution.md` - Phase 2 requirements (lines 104-112)

### Phase 1 Implementation
- `/phase-01-console/` - Working implementation to reference
- `/specs/001-phase-01-console-todo/` - Phase 1 specifications

### Technology Documentation
- [Next.js 16 Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Better Auth Docs](https://www.better-auth.com/docs)
- [Neon PostgreSQL Docs](https://neon.tech/docs/introduction)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

## ✍️ Summary

Phase 2 transforms our console app into a modern, full-stack web application with:
- ✅ Multi-user authentication
- ✅ Persistent database storage
- ✅ RESTful API architecture
- ✅ Responsive web interface
- ✅ Security best practices

**Foundation for Future Phases**:
- Phase 3 will add AI chatbot interface
- Phase 4 will containerize and deploy to Kubernetes
- Phase 5 will scale with event-driven architecture

**Ready to discuss and create spec.md!** 🚀
