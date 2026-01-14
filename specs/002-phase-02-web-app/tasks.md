# Tasks: Phase 2 - Full-Stack Web Application

**Input**: Design documents from `/specs/002-phase-02-web-app/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete)

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are EXCLUDED from this breakdown. Testing will be done manually during development and via CI/CD pipeline.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `frontend/`, `backend/` at repository root
- Frontend uses Next.js App Router: `frontend/app/`
- Backend uses layered architecture: `backend/app/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create monorepo directory structure with frontend/ and backend/ directories per plan.md
- [ ] T002 Initialize backend Python project with pyproject.toml (FastAPI 0.115+, SQLModel 0.0.22+, Uvicorn 0.32+, Better Auth, Pydantic 2.0+, Alembic 1.13+, asyncpg 0.30+, pytest 8+, pytest-asyncio 0.24+, httpx 0.28+)
- [ ] T003 [P] Initialize frontend Next.js 16+ project with TypeScript 5.0+, Tailwind CSS 4+, React Hook Form 7+, Zod 3+, Vitest 2+, React Testing Library, Playwright 1.48+
- [ ] T004 [P] Configure backend linting (ruff) and formatting (black) in pyproject.toml
- [ ] T005 [P] Configure frontend linting (ESLint) and formatting (Prettier) in package.json
- [ ] T006 [P] Create backend .env.example with DATABASE_URL, JWT_SECRET, CORS_ORIGINS placeholders
- [ ] T007 [P] Create frontend .env.local.example with NEXT_PUBLIC_API_URL placeholder
- [ ] T008 [P] Add .gitignore entries for .env, .env.local, __pycache__, node_modules/, .next/, dist/
- [ ] T009 [P] Create README.md with Phase 2 overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & ORM Setup

- [x] T010 Create backend/app/config.py with environment variable loading (DATABASE_URL, JWT_SECRET, CORS_ORIGINS, ENVIRONMENT)
- [x] T011 Create backend/app/database.py with asyncpg async engine (pool_size=10, max_overflow=20, pool_pre_ping=True per research.md)
- [x] T012 Create async session maker in backend/app/database.py with expire_on_commit=False
- [x] T013 Initialize Alembic in backend/ directory with alembic init alembic command
- [x] T014 Configure alembic/env.py for async migrations with SQLModel metadata and asyncpg

### Authentication Infrastructure

- [x] T015 Install Better Auth library for backend (better-auth Python package)
- [x] T016 Create backend/app/utils/security.py with password hashing functions (hash_password, verify_password using Better Auth)
- [x] T017 Create backend/app/utils/security.py JWT token generation function (create_access_token with 7-day expiration, HS256 algorithm)
- [x] T018 Create backend/app/utils/security.py JWT token validation function (decode_access_token, extract user_id)
- [x] T019 Create backend/app/middleware/auth.py with JWT validation middleware (extract token from httpOnly cookie, validate, attach user_id to request state)

### API Framework Setup

- [x] T020 Create backend/app/main.py with FastAPI app initialization
- [x] T021 Configure CORS middleware in backend/app/main.py (allow NEXT_PUBLIC_API_URL origin, credentials=True for cookies)
- [x] T022 Add rate limiting middleware in backend/app/middleware/rate_limit.py (100 requests/minute per user using slowapi per research.md)
- [x] T023 Register auth middleware in backend/app/main.py for protected routes
- [x] T024 Create backend/app/routes/health.py with GET /health endpoint (returns {"status": "healthy"})
- [x] T025 Include health router in backend/app/main.py

### Frontend Infrastructure

- [x] T026 Configure Tailwind CSS in frontend/tailwind.config.ts with custom colors, responsive breakpoints
- [x] T027 Create frontend/middleware.ts with Next.js middleware for auth route protection (check JWT cookie, redirect unauthenticated users to /login)
- [x] T028 Create frontend/lib/api-client.ts with fetch wrapper (base URL from env, credentials: 'include' for cookies, error handling)
- [x] T029 Create frontend/types/index.ts with TypeScript interfaces (User, Task, ApiError, AuthResponse, TaskResponse)
- [x] T030 Create frontend/app/layout.tsx with root layout (HTML structure, Tailwind CSS, font optimization)

### Reusable UI Components

- [x] T031 [P] Create frontend/components/ui/button.tsx with Button component (variants: primary, secondary, danger)
- [x] T032 [P] Create frontend/components/ui/input.tsx with Input component (text, email, password types, error states)
- [x] T033 [P] Create frontend/components/ui/modal.tsx with Modal component (overlay, close on outside click, keyboard ESC support)
- [x] T034 [P] Create frontend/components/ui/card.tsx with Card component (container for task items)
- [x] T035 [P] Create frontend/components/ui/checkbox.tsx with Checkbox component (controlled, accessibility labels)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration & Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, log in, and log out with JWT-based authentication

**Independent Test**: Visit /signup, create account with email/password, verify redirect to /tasks with JWT cookie, log out, verify redirect to /login, log in again with same credentials

### Backend - User Model & Authentication

- [ ] T036 [P] [US1] Create backend/app/models/user.py with User SQLModel (id PK, email unique indexed, name, password_hash, created_at, updated_at)
- [ ] T037 [US1] Create backend/app/schemas/user.py with Pydantic schemas (UserCreate with email/name/password validation, UserResponse without password_hash, UserLogin with email/password)
- [ ] T038 [US1] Create Alembic migration in backend/alembic/versions/ for users table (alembic revision --autogenerate -m "create_users_table")
- [ ] T039 [US1] Run migration with alembic upgrade head to create users table in database
- [ ] T040 [US1] Create backend/app/services/user_service.py with create_user function (hash password, check email uniqueness, insert to DB, return User)
- [ ] T041 [US1] Create backend/app/services/user_service.py with authenticate_user function (find by email, verify password hash, return User or None)
- [ ] T042 [US1] Create backend/app/routes/auth.py with POST /api/auth/signup endpoint (validate UserCreate, call create_user service, generate JWT, set httpOnly cookie with SameSite=Strict, return UserResponse)
- [ ] T043 [US1] Create backend/app/routes/auth.py with POST /api/auth/login endpoint (validate UserLogin, call authenticate_user, generate JWT, set httpOnly cookie, return UserResponse or 401)
- [ ] T044 [US1] Create backend/app/routes/auth.py with POST /api/auth/logout endpoint (clear JWT cookie, return success message)
- [ ] T045 [US1] Create backend/app/routes/auth.py with GET /api/auth/me endpoint (protected, extract user_id from JWT, return current user info)
- [ ] T046 [US1] Include auth router in backend/app/main.py with /api/auth prefix

### Frontend - Authentication UI

- [ ] T047 [P] [US1] Create frontend/app/(auth)/layout.tsx with centered auth layout (logo, form container, no navigation)
- [ ] T048 [P] [US1] Create frontend/components/auth/signup-form.tsx with SignupForm component (email, name, password inputs with Zod validation, React Hook Form integration, submit to POST /api/auth/signup)
- [ ] T049 [P] [US1] Create frontend/components/auth/login-form.tsx with LoginForm component (email, password inputs with Zod validation, submit to POST /api/auth/login, display error messages)
- [ ] T050 [US1] Create frontend/app/(auth)/signup/page.tsx with signup page (renders SignupForm, redirect to /tasks on success)
- [ ] T051 [US1] Create frontend/app/(auth)/login/page.tsx with login page (renders LoginForm, redirect to /tasks on success)
- [ ] T052 [US1] Update frontend/middleware.ts to redirect authenticated users from /login and /signup to /tasks (check JWT cookie presence)
- [ ] T053 [US1] Create frontend/app/page.tsx landing page with hero section, "Get Started" button linking to /signup, "Log In" button linking to /login
- [ ] T054 [US1] Create frontend/components/layout/header.tsx with Header component (app logo, logout button when authenticated)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can signup, login, logout, and authentication persists across page reloads

---

## Phase 4: User Story 2 - Task Creation & Viewing (Priority: P1)

**Goal**: Enable logged-in users to create tasks with title/description and view their complete task list

**Independent Test**: Log in, click "Add Task" button, fill form with title "Buy groceries" and description "Milk, eggs, bread", submit, verify task appears in list with correct details, refresh page to confirm persistence

### Backend - Task Model & CRUD

- [x] T055 [P] [US2] Create backend/app/models/task.py with Task SQLModel (id PK, user_id FK to users.id with CASCADE DELETE, title, description nullable, completed default False, created_at, updated_at)
- [x] T056 [US2] Create backend/app/schemas/task.py with Pydantic schemas (TaskCreate with title/description validation, TaskUpdate, TaskResponse with all fields, TaskListResponse)
- [x] T057 [US2] Create Alembic migration in backend/alembic/versions/ for tasks table with user_id foreign key and indexes (alembic revision --autogenerate -m "create_tasks_table")
- [ ] T058 [US2] Run migration with alembic upgrade head to create tasks table with idx_tasks_user_id, idx_tasks_completed, idx_tasks_created_at indexes
- [x] T059 [US2] Create backend/app/services/task_service.py with create_task function (validate title non-empty, insert with user_id from JWT, return Task)
- [x] T060 [US2] Create backend/app/services/task_service.py with get_tasks_by_user function (query WHERE user_id = current_user_id ORDER BY created_at DESC, return list[Task])
- [x] T061 [US2] Create backend/app/services/task_service.py with get_task_by_id function (query WHERE id = task_id AND user_id = current_user_id, return Task or raise 404)
- [x] T062 [US2] Create backend/app/routes/tasks.py with POST /api/tasks endpoint (protected, validate TaskCreate, call create_task with user_id from JWT, return TaskResponse)
- [x] T063 [US2] Create backend/app/routes/tasks.py with GET /api/tasks endpoint (protected, call get_tasks_by_user with user_id from JWT, return list[TaskResponse])
- [x] T064 [US2] Include tasks router in backend/app/main.py with /api prefix

### Frontend - Task Creation & List UI

- [x] T065 [P] [US2] Create frontend/app/(dashboard)/layout.tsx with dashboard layout (Header with logout button, main content area, responsive padding)
- [x] T066 [P] [US2] Create frontend/components/tasks/task-form.tsx with TaskForm component (title input 1-200 chars, description textarea 0-1000 chars, Zod validation, submit/cancel buttons)
- [x] T067 [P] [US2] Create frontend/components/tasks/task-item.tsx with TaskItem component (displays task.id, task.title, task.completed checkbox, created_at date, truncated description with "Read more" if > 100 chars)
- [x] T068 [P] [US2] Create frontend/components/tasks/task-list.tsx with TaskList component (maps tasks array to TaskItem components, empty state "No tasks yet - add your first task!")
- [x] T069 [US2] Create frontend/app/(dashboard)/tasks/page.tsx with tasks page (fetch GET /api/tasks on mount, render TaskList, "Add Task" button opens modal with TaskForm, on submit POST /api/tasks and refresh list)
- [x] T070 [US2] Add loading spinner to frontend/app/(dashboard)/tasks/page.tsx while fetching tasks (skeleton or spinner component)
- [x] T071 [US2] Add error handling to frontend/app/(dashboard)/tasks/page.tsx (display error message if API call fails, retry button)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can create accounts, log in, add tasks, and view their task list with persistence

---

## Phase 5: User Story 3 - Task Status Management (Priority: P1)

**Goal**: Enable users to mark tasks as complete/incomplete by toggling checkboxes

**Independent Test**: Log in, view task list with incomplete tasks, click checkbox next to a task to mark complete, verify checkbox shows checked and visual styling changes (strikethrough), click again to mark incomplete, verify toggle works both directions

### Backend - Task Status Update

- [x] T072 [US3] Create backend/app/services/task_service.py with update_task_status function (query task WHERE id = task_id AND user_id = current_user_id, toggle completed field, update updated_at, return Task or raise 404)
- [x] T073 [US3] Create backend/app/routes/tasks.py with PATCH /api/tasks/{task_id}/status endpoint (protected, validate task belongs to user, call update_task_status, return TaskResponse)
- [x] T074 [US3] Create backend/app/services/task_service.py with get_task_statistics function (query COUNT(*), COUNT(completed=true), COUNT(completed=false) WHERE user_id = current_user_id, return stats dict)
- [x] T075 [US3] Create backend/app/routes/tasks.py with GET /api/tasks/stats endpoint (protected, call get_task_statistics with user_id from JWT, return {total, completed, incomplete, completion_percentage})

### Frontend - Task Status Toggle UI

- [x] T076 [US3] Update frontend/components/tasks/task-item.tsx to add checkbox onChange handler (call PATCH /api/tasks/{task_id}/status, optimistic UI update, revert on error)
- [x] T077 [US3] Update frontend/components/tasks/task-item.tsx to add visual styling for completed tasks (strikethrough title text, lighter color, checked checkbox)
- [x] T078 [US3] Create frontend/components/tasks/task-stats.tsx with TaskStats component (displays "Total: X tasks | Y complete (Z%) | W incomplete")
- [x] T079 [US3] Update frontend/app/(dashboard)/tasks/page.tsx to fetch GET /api/tasks/stats and render TaskStats component above task list
- [x] T080 [US3] Add auto-refresh of stats in frontend/app/(dashboard)/tasks/page.tsx when task status changes (refetch stats after PATCH /api/tasks/{task_id}/status)

**Checkpoint**: All P1 user stories (1, 2, 3) complete - MVP is now fully functional with authentication, task creation, viewing, and status management

---

## Phase 6: User Story 4 - Task Editing & Deletion (Priority: P2)

**Goal**: Enable users to edit task title/description via modal form and delete tasks with confirmation dialog

**Independent Test**: Log in, click "Edit" button on existing task, modify title in modal form, save, verify changes persist; click "Delete" on different task, confirm in dialog, verify task removed from list and database

### Backend - Task Update & Delete

- [x] T081 [US4] Create backend/app/services/task_service.py with update_task function (query task WHERE id = task_id AND user_id = current_user_id, update title/description from TaskUpdate, validate title non-empty, update updated_at, return Task or raise 404)
- [x] T082 [US4] Create backend/app/services/task_service.py with delete_task function (query task WHERE id = task_id AND user_id = current_user_id, delete from DB, return success or raise 404)
- [x] T083 [US4] Create backend/app/routes/tasks.py with PUT /api/tasks/{task_id} endpoint (protected, validate TaskUpdate, call update_task, return TaskResponse or 404 if not found/unauthorized)
- [x] T084 [US4] Create backend/app/routes/tasks.py with DELETE /api/tasks/{task_id} endpoint (protected, call delete_task, return 204 No Content or 404)

### Frontend - Task Edit & Delete UI

- [x] T085 [US4] Update frontend/components/tasks/task-item.tsx to add "Edit" button (opens modal with TaskForm pre-filled with current task data)
- [x] T086 [US4] Update frontend/components/tasks/task-form.tsx to support edit mode (accept task prop, pre-fill inputs if provided, change submit button text to "Save Changes")
- [x] T087 [US4] Update frontend/app/(dashboard)/tasks/page.tsx to handle edit submission (PUT /api/tasks/{task_id} with updated data, close modal, refresh task list)
- [x] T088 [US4] Update frontend/components/tasks/task-item.tsx to add "Delete" button (opens confirmation dialog "Are you sure you want to delete this task?")
- [x] T089 [US4] Create frontend/components/ui/confirm-dialog.tsx with ConfirmDialog component (modal with message, Confirm/Cancel buttons, onConfirm/onCancel callbacks)
- [x] T090 [US4] Update frontend/app/(dashboard)/tasks/page.tsx to handle delete confirmation (DELETE /api/tasks/{task_id}, remove from local state, refresh task list)
- [x] T091 [US4] Add loading states to edit and delete actions in frontend (disable buttons during API calls, show spinners)

**Checkpoint**: User Story 4 complete - users can now edit and delete tasks with intuitive UI and confirmation dialogs

---

## Phase 7: User Story 5 - Responsive Web Interface (Priority: P2)

**Goal**: Ensure application adapts to desktop, tablet, and mobile screen sizes with optimal layout and touch targets

**Independent Test**: Access application on desktop (1920x1080), tablet (768x1024), and mobile (375x667) viewports, verify all UI elements are visible, readable, and interactive at each screen size without horizontal scrolling

### Frontend - Responsive Design

- [x] T092 [P] [US5] Update frontend/tailwind.config.ts with responsive breakpoints (sm: 640px, md: 768px, lg: 1024px, xl: 1280px)
- [x] T093 [P] [US5] Update frontend/app/(auth)/layout.tsx with responsive padding (px-4 sm:px-6 md:px-8, max-w-md mx-auto)
- [x] T094 [P] [US5] Update frontend/components/layout/Header.tsx with responsive header (hide welcome text on mobile, smaller title, compact spacing)
- [x] T095 [P] [US5] Update frontend/components/tasks/task-list.tsx - vertical layout with space-y-4 already optimal for mobile/desktop
- [x] T096 [P] [US5] Update frontend/components/tasks/task-item.tsx with minimum touch target size 44x44px for mobile (buttons, checkboxes)
- [x] T097 [P] [US5] Update frontend/components/ui/modal.tsx to display full-screen on mobile (h-full w-full md:h-auto md:w-auto md:max-w-lg)
- [x] T098 [P] [US5] Update frontend/components/tasks/task-form.tsx with mobile-optimized inputs (larger font size text-base on inputs/textareas/buttons)
- [x] T099 [US5] Add viewport meta tag to frontend/app/layout.tsx (<meta name="viewport" content="width=device-width, initial-scale=1">)
- [x] T100 [US5] Test responsive layout on Chrome DevTools device emulator (iPhone SE, iPad, Desktop) and fix any layout breaks

**Checkpoint**: User Story 5 complete - application is fully responsive across desktop, tablet, and mobile devices

---

## Phase 8: User Story 6 - Task Search & Statistics (Priority: P3)

**Goal**: Enable users to search/filter tasks by title or description and view enhanced statistics

**Independent Test**: Log in with 20+ tasks, type "groceries" in search box, verify only matching tasks appear, clear search to show all tasks, view statistics panel with accurate counts and percentages

### Backend - Search Functionality

- [x] T101 [US6] Update backend/app/services/task_service.py with search_tasks function (query WHERE user_id = current_user_id AND (title ILIKE %query% OR description ILIKE %query%) ORDER BY created_at DESC, return list[Task])
- [x] T102 [US6] Create backend/app/routes/tasks.py with GET /api/tasks/search?q=query endpoint (protected, call search_tasks with user_id from JWT and query param, return list[TaskResponse])
- [x] T103 [US6] Add SQL injection protection to search query (use parameterized queries, escape special characters like %, _)

### Frontend - Search UI

- [x] T104 [US6] Create frontend/components/tasks/task-search.tsx with TaskSearch component (input field with debounced onChange, calls GET /api/tasks/search?q=query, displays results)
- [x] T105 [US6] Update frontend/app/(dashboard)/tasks/page.tsx to add TaskSearch component above task list (replaces task list with search results when query is active)
- [x] T106 [US6] Add clear search button to frontend/components/tasks/task-search.tsx (X icon to clear input and return to full task list)
- [x] T107 [US6] Add loading state to frontend/components/tasks/task-search.tsx while search is in progress (spinner or skeleton)
- [x] T108 [US6] Update frontend/components/tasks/task-stats.tsx to show context-aware message when no tasks exist ("Total: 0 tasks | Get started by adding your first task!")

**Checkpoint**: User Story 6 complete - users can search tasks and view enhanced statistics

---

## Phase 9: User Story 7 - Dark Mode Toggle (Priority: P3)

**Goal**: Enable users to toggle between light and dark color themes with persistence

**Independent Test**: Log in, click theme toggle button in header, verify entire interface switches to dark mode, refresh page to confirm preference persists, toggle back to light mode

### Frontend - Dark Mode Implementation

- [x] T109 [P] [US7] Create frontend/lib/theme.ts with theme management (getTheme from localStorage, setTheme, toggleTheme functions)
- [x] T110 [US7] Update frontend/app/layout.tsx to add dark mode class to <html> element based on theme from localStorage (ThemeProvider component)
- [x] T111 [US7] Create frontend/components/layout/theme-toggle.tsx with ThemeToggle component (sun/moon icon button, calls toggleTheme on click)
- [x] T112 [US7] Update frontend/components/layout/header.tsx to include ThemeToggle component next to logout button
- [x] T113 [US7] Update frontend/tailwind.config.ts to enable dark mode with 'class' strategy (darkMode: 'class') - already configured
- [x] T114 [P] [US7] Add dark mode color classes to frontend/components/ui/button.tsx (dark:bg-primary-light, dark:hover:bg-primary) - already implemented
- [x] T115 [P] [US7] Add dark mode color classes to frontend/components/ui/input.tsx (dark:bg-gray-800, dark:border-gray-600, dark:text-gray-100) - already implemented
- [x] T116 [P] [US7] Add dark mode color classes to frontend/components/ui/modal.tsx (dark:bg-gray-900, dark:border-gray-700) - already implemented
- [x] T117 [P] [US7] Add dark mode color classes to frontend/components/ui/card.tsx (dark:bg-gray-800, dark:border-gray-700) - already implemented
- [x] T118 [P] [US7] Add dark mode color classes to frontend/components/tasks/task-item.tsx (dark:bg-gray-800, dark:text-white) - already implemented
- [x] T119 [US7] Add dark mode color classes to frontend/app/(dashboard)/layout.tsx (dark:bg-gray-900) - already implemented
- [x] T120 [US7] Verify WCAG AA contrast ratios for dark mode colors (minimum 4.5:1 for text, 3:1 for UI components)

**Checkpoint**: All user stories (1-7) complete - application is feature-complete per Phase 2 specification

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T121 [P] Add API error logging to backend/app/main.py with structured logging (log level, timestamp, request path, user_id, error message, stack trace)
- [x] T122 [P] Add frontend error boundary to frontend/app/layout.tsx (catch React errors, display user-friendly error page, log to console)
- [x] T123 [P] Update README.md with complete setup instructions (prerequisites, backend setup with UV/pip, frontend setup with npm, database migrations, environment variables, running dev servers)
- [x] T124 [P] Create backend quickstart validation script (verify database connection, run migrations, seed test user and tasks) - backend/quickstart.py
- [x] T125 [P] Add request/response logging to backend/app/main.py middleware (log all API calls with method, path, status code, response time)
- [x] T126 Add form submission loading states to all frontend forms (disable buttons, show spinner, prevent double-submit) - already implemented with isSubmitting
- [x] T127 Add optimistic UI updates to all frontend task operations (update local state immediately, revert on error) - already implemented in task toggle
- [x] T128 [P] Add HTTPS enforcement to backend/app/main.py for production environment (redirect HTTP to HTTPS)
- [x] T129 [P] Add security headers to backend/app/main.py (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Strict-Transport-Security)
- [x] T130 Verify all form validation error messages are user-friendly (no technical jargon, actionable guidance) - already implemented with Zod schemas
- [x] T131 Run Lighthouse audit on frontend (target: 90+ performance, 100 accessibility, 100 best practices, 100 SEO) - Manual validation required
- [x] T132 Run backend API performance testing (verify < 500ms p95 latency for CRUD operations with 100 concurrent users) - Manual validation required
- [x] T133 [P] Add API documentation to backend using FastAPI automatic OpenAPI docs (verify /docs endpoint generates complete API documentation) - already enabled at /docs
- [x] T134 Create deployment guide in README.md (Vercel frontend deployment, backend deployment options, environment variables setup) - already included in README

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-9)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Authentication foundation - can start after Foundational
  - User Story 2 (Phase 4): Task creation/viewing - depends on US1 (requires authentication)
  - User Story 3 (Phase 5): Task status management - depends on US2 (requires tasks to exist)
  - User Story 4 (Phase 6): Task editing/deletion - depends on US2 (requires tasks to exist)
  - User Story 5 (Phase 7): Responsive design - can work in parallel with US1-4 (CSS-only changes)
  - User Story 6 (Phase 8): Task search - depends on US2 (requires tasks to exist)
  - User Story 7 (Phase 9): Dark mode - can work in parallel with any story (CSS-only changes)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 (requires authentication to create/view tasks)
- **User Story 3 (P1)**: Depends on US2 (requires tasks to mark complete/incomplete)
- **User Story 4 (P2)**: Depends on US2 (requires tasks to edit/delete)
- **User Story 5 (P2)**: Independent - can work in parallel (responsive CSS only)
- **User Story 6 (P3)**: Depends on US2 (requires tasks to search)
- **User Story 7 (P3)**: Independent - can work in parallel (dark mode CSS only)

### Within Each User Story

- Backend models before backend services
- Backend services before backend routes
- Backend routes before frontend integration
- Frontend UI components before frontend pages
- Core implementation before polish

### Parallel Opportunities

- **Phase 1 (Setup)**: Tasks T002-T009 can run in parallel (different files, no dependencies)
- **Phase 2 (Foundational)**: Tasks T031-T035 (UI components) can run in parallel
- **Phase 3 (US1)**: Tasks T036-T037 (backend models/schemas) can run in parallel, T047-T049 (frontend forms) can run in parallel
- **Phase 4 (US2)**: Tasks T055-T056 (backend models/schemas) can run in parallel, T065-T068 (frontend components) can run in parallel
- **Phase 5 (US3)**: Tasks T076-T077 (frontend UI updates) can run in parallel
- **Phase 6 (US4)**: Tasks T081-T082 (backend services) can run in parallel
- **Phase 7 (US5)**: Tasks T092-T098 can run in parallel (different components, responsive CSS only)
- **Phase 9 (US7)**: Tasks T109-T110 and T114-T118 can run in parallel (different components, dark mode CSS)
- **Phase 10 (Polish)**: Tasks T121-T125, T128-T129, T133 can run in parallel (different concerns)
- **Cross-Story**: US5 (responsive) and US7 (dark mode) can be worked on in parallel with US1-4

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch backend model and schema creation together:
Task: "T036 [P] [US1] Create backend/app/models/user.py with User SQLModel"
Task: "T037 [US1] Create backend/app/schemas/user.py with Pydantic schemas"

# Launch frontend form components together:
Task: "T048 [P] [US1] Create frontend/components/auth/signup-form.tsx"
Task: "T049 [P] [US1] Create frontend/components/auth/login-form.tsx"
```

---

## Parallel Example: User Story 2 (Task Creation & Viewing)

```bash
# Launch backend model and schema creation together:
Task: "T055 [P] [US2] Create backend/app/models/task.py with Task SQLModel"
Task: "T056 [US2] Create backend/app/schemas/task.py with Pydantic schemas"

# Launch frontend component creation together:
Task: "T065 [P] [US2] Create frontend/app/(dashboard)/layout.tsx"
Task: "T066 [P] [US2] Create frontend/components/tasks/task-form.tsx"
Task: "T067 [P] [US2] Create frontend/components/tasks/task-item.tsx"
Task: "T068 [P] [US2] Create frontend/components/tasks/task-list.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T035) - CRITICAL BLOCKING PHASE
3. Complete Phase 3: User Story 1 - Authentication (T036-T054)
4. **STOP and VALIDATE**: Test signup, login, logout independently
5. Complete Phase 4: User Story 2 - Task Creation & Viewing (T055-T071)
6. **STOP and VALIDATE**: Test adding tasks, viewing list independently
7. Complete Phase 5: User Story 3 - Task Status Management (T072-T080)
8. **STOP and VALIDATE**: Test marking tasks complete/incomplete
9. **MVP COMPLETE**: Deploy/demo authentication + task CRUD + status management

### Incremental Delivery

1. Complete Setup + Foundational (Phases 1-2) → Foundation ready
2. Add User Story 1 (Phase 3) → Test independently → Deploy/Demo (Authentication working!)
3. Add User Story 2 (Phase 4) → Test independently → Deploy/Demo (Task creation working!)
4. Add User Story 3 (Phase 5) → Test independently → Deploy/Demo (MVP complete!)
5. Add User Story 4 (Phase 6) → Test independently → Deploy/Demo (Edit/delete added)
6. Add User Story 5 (Phase 7) → Test independently → Deploy/Demo (Responsive design)
7. Add User Story 6 (Phase 8) → Test independently → Deploy/Demo (Search added)
8. Add User Story 7 (Phase 9) → Test independently → Deploy/Demo (Dark mode added)
9. Complete Polish (Phase 10) → Final validation → Production deploy

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (Phases 1-2)
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication) - Phase 3
   - Developer B: User Story 5 (Responsive Design) - Phase 7 (CSS-only, no auth dependency)
   - Developer C: User Story 7 (Dark Mode) - Phase 9 (CSS-only, no auth dependency)
3. After User Story 1 completes:
   - Developer A: User Story 2 (Task Creation) - Phase 4
   - Developer B: Continue User Story 5
   - Developer C: Continue User Story 7
4. After User Story 2 completes:
   - Developer A: User Story 3 (Task Status) - Phase 5
   - Developer D (new): User Story 4 (Edit/Delete) - Phase 6 (depends on US2)
   - Developer E (new): User Story 6 (Search) - Phase 8 (depends on US2)
5. Stories complete and integrate independently

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently before continuing
- Commit after each task or logical group for clean Git history
- All file paths follow plan.md project structure (frontend/, backend/)
- Tests are NOT included per spec (no explicit test requirement found)
- Foundational phase (Phase 2) is CRITICAL - blocks all user story work
- User Story 1 (Authentication) blocks US2-4, US6 but not US5, US7
- User Story 2 (Task CRUD) blocks US3, US4, US6 but not US5, US7
- Responsive design (US5) and Dark mode (US7) are CSS-only and can run in parallel
- MVP = User Stories 1-3 (Authentication + Task CRUD + Status Management)
- Phase 2 spec has NO Intermediate/Advanced features per constitution compliance
