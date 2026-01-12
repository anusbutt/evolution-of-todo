<!--
Sync Impact Report:
- Version change: 1.0.0 (initial ratification)
- New principles: I-VII (Spec-Driven Development, Single Source of Truth, AI-Native Development, Progressive Enhancement, Feature Scope Discipline, Technology Stack Constraints, Quality Standards)
- Added sections: Code Quality Standards, Testing Requirements, Security Principles, Architecture Guidelines, AI Agent Development, Cloud-Native Principles, Deployment Standards, Documentation Requirements, Workflow Governance
- Templates requiring updates: ✅ All templates compatible with this constitution
- Follow-up TODOs: None - all placeholders filled
-->

# Evolution of Todo Constitution

## Purpose

This constitution defines the immutable principles, standards, and constraints that govern the development of the "Evolution of Todo" project across all five phases:

- **Phase I**: Console App (Python, in-memory)
- **Phase II**: Full-Stack Web (Next.js + FastAPI + Neon DB)
- **Phase III**: AI Chatbot (OpenAI Agents SDK + MCP)
- **Phase IV**: Local Kubernetes (Minikube + Helm + kubectl-ai)
- **Phase V**: Cloud Native (AKS/GKE/OKE + Kafka + Dapr)

---

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**The Sacred Loop:** `spec.md → plan.md → tasks.md → implementation`

- NO code without a task reference
- NO task without a plan section
- NO plan without a spec requirement
- **Even corrections flow through the loop**: If we forget something in `plan.md`, we MUST update `spec → plan → tasks → implement`
- Every code file MUST contain a comment linking it to the Task ID and Spec section: `[Task]: T-001 | [Spec]: spec.md §2.1`

**Rationale**: Prevents "vibe coding" and ensures every implementation decision traces to explicit requirements. Maintains architectural integrity across all five phases.

### II. Single Source of Truth

The hierarchy of documentation:

1. **Constitution** (this file): WHY - principles, constraints, non-negotiables
2. **Spec**: WHAT - requirements, acceptance criteria, user stories
3. **Plan**: HOW - architecture, components, interfaces
4. **Tasks**: BREAKDOWN - atomic, testable units with file paths
5. **Code**: IMPLEMENTATION - must reference task IDs

**Conflict Resolution**: If conflicts arise between levels, the higher level wins: `Constitution > Spec > Plan > Tasks > Code`

### III. AI-Native Development

- **Claude Code** is the primary implementation agent
- **MCP servers** provide tool interfaces (Phase III+)
- Agents MUST reference task IDs in all code commits
- Agents MUST NOT invent features, APIs, or contracts - they must request clarification
- All agent instructions documented in `CLAUDE.md`
- PHRs (Prompt History Records) MUST be created after every interaction
- ADRs (Architecture Decision Records) suggested for significant decisions, created only with user consent

**Rationale**: Establishes clear agent behavior patterns and ensures traceability of AI-generated decisions.

### IV. Progressive Enhancement

Each phase builds on the previous - NO SKIPPING PHASES:

1. **Phase I**: Foundation - In-memory Python console (Basic Level features)
2. **Phase II**: Persistence - Full-stack web with database and auth
3. **Phase III**: Intelligence - AI chatbot with natural language interface
4. **Phase IV**: Orchestration - Kubernetes deployment and scaling
5. **Phase V**: Distribution - Event-driven cloud-native architecture (Intermediate + Advanced features)

**Rule**: A phase MUST be complete and functional before advancing to the next phase.

### V. Feature Scope Discipline

**Basic Level Features (Phases I-V):**
- Add Task
- Delete Task
- Update Task
- View Task List
- Mark Complete

**Intermediate Level Features (Phase V ONLY):**
- Priorities & Tags
- Search & Filter
- Sort Tasks

**Advanced Level Features (Phase V ONLY):**
- Recurring Tasks
- Due Dates & Reminders

**Enforcement**: Do NOT implement Intermediate or Advanced features before Phase V. Each phase must complete only its designated scope.

### VI. Technology Stack Constraints

#### Phase I: Console App
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Storage**: In-memory (list/dict)
- **Interface**: CLI with text prompts
- **Testing**: pytest
- **Coverage**: Minimum 80%

#### Phase II: Full-Stack Web
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT tokens)
- **Architecture**: Monorepo (`/frontend`, `/backend`)
- **API Pattern**: RESTful with `/api/{user_id}/tasks` endpoints
- **Coverage**: Minimum 75%

#### Phase III: AI Chatbot
- **AI UI**: OpenAI ChatKit
- **AI Logic**: OpenAI Agents SDK
- **Tool Interface**: Official MCP SDK (Python)
- **MCP Tools**: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- **Architecture**: Stateless chat endpoint, conversation state persisted in database
- **Models**: Task, Conversation, Message

#### Phase IV: Local Kubernetes
- **Containerization**: Docker Desktop
- **Docker AI**: Gordon (optional - fallback to standard Docker CLI)
- **Orchestration**: Kubernetes via Minikube
- **Package Manager**: Helm Charts
- **AIOps**: kubectl-ai, kagent
- **Deployment Target**: Local cluster with resource limits

#### Phase V: Cloud Native
- **Cloud Platform**: Azure AKS, Google GKE, or Oracle OKE
- **Event Streaming**: Kafka (Redpanda Cloud or self-hosted via Strimzi operator)
- **Distributed Runtime**: Dapr (Pub/Sub, State Management, Jobs API, Secrets, Service Invocation)
- **Kafka Topics**: `task-events`, `reminders`, `task-updates`
- **CI/CD**: GitHub Actions (test → build → push → deploy)
- **Services**: Chat API, Notification Service, Recurring Task Service, Audit Service

**Stack Immutability**: These technology choices are FIXED. No substitutions without amending this constitution through the proper amendment process.

### VII. Quality Standards

#### Code Readability
- Clear variable names (no abbreviations unless domain-standard: `user_id` OK, `usr` NOT OK)
- Functions do ONE thing (Single Responsibility Principle)
- Max function length: 50 lines (hard limit: 100 lines)
- Comments explain WHY, not WHAT
- Use type hints in Python, TypeScript types in frontend

#### Project Structure
- Consistent file naming: `snake_case` for Python, `kebab-case` for config files
- Logical module grouping: models, services, routes, utils
- Separation of concerns: business logic ≠ I/O ≠ presentation
- Follow structure defined in `plan.md` exactly

#### Error Handling
- Explicit error messages with actionable guidance
- NO silent failures - all errors must be logged
- User-facing errors: clear, actionable messages
- System errors: full context with stack traces for debugging
- Use structured exception types (not bare `Exception`)

#### Async/Await Pattern
- Use `async/await` for ALL I/O operations (DB, API, file, network)
- NEVER use blocking calls in async contexts
- Properly await all promises/coroutines

---

## Testing Requirements

### Phase I: Console App
- Unit tests for all task operations (add, delete, update, view, mark complete)
- Edge cases: empty list, invalid IDs, duplicate operations, boundary conditions
- Test coverage: Minimum 80%
- Test framework: pytest
- Test organization: `tests/test_tasks.py`

### Phase II: Web App
- **Backend**: API endpoint tests using FastAPI TestClient
- **Frontend**: Component tests using React Testing Library
- **Integration**: E2E tests for critical user flows using Playwright
- **Auth**: JWT token validation and user isolation tests
- Test coverage: Minimum 75%
- Test organization: `backend/tests/`, `frontend/tests/`

### Phase III: Chatbot
- MCP tool tests (input validation, DB operations, error handling)
- Agent response tests (mocked LLM calls for deterministic testing)
- Conversation flow tests (multi-turn scenarios)
- Natural language understanding tests (various phrasings)
- Statelessness validation (server restarts, concurrent requests)

### Phase IV-V: Kubernetes
- Container health checks (readiness, liveness probes)
- Helm chart validation (dry-run, template rendering)
- Deployment smoke tests (pod starts, services accessible)
- Kafka integration tests (event publishing, consumption)
- Dapr component tests (Pub/Sub, State, Jobs API)

**Universal Rule**: Tests MUST pass before marking tasks complete. Red-Green-Refactor cycle enforced.

---

## Security Principles

### Authentication & Authorization
- **Phase I**: No auth (single-user console)
- **Phase II+**: JWT tokens for API security (Better Auth)
- User isolation: All queries MUST filter by `user_id`
- No shared task access between users
- Token expiration: 7 days (configurable)
- HTTPS enforced in production

### Secrets Management
- NEVER commit secrets, API keys, or credentials to Git
- Use `.env` files (MUST be in `.gitignore`)
- **Phase IV+**: Kubernetes Secrets or Dapr Secrets API
- Rotate credentials regularly
- Use environment variables for all sensitive config

### Input Validation
- Sanitize ALL user inputs (frontend and backend)
- Use parameterized queries (SQLModel ORM handles this)
- Validate JSON schemas for API requests
- Rate limiting on API endpoints (Phase II+): 100 requests/minute per user
- Max request size: 1MB

### OWASP Top 10 Awareness
- **SQL Injection**: Prevented via SQLModel ORM (never use raw SQL)
- **XSS**: React escapes by default, no `dangerouslySetInnerHTML`
- **CSRF**: SameSite cookies, CORS properly configured
- **Broken Auth**: JWT tokens, secure password hashing (Better Auth)
- **Sensitive Data Exposure**: HTTPS only, no secrets in logs
- Secure headers: CORS, CSP, X-Frame-Options

---

## Architecture Guidelines

### Statelessness (Phase III+)
- Chat endpoint: Stateless request/response cycle
- All conversation state persisted in database
- Server holds NO in-memory state between requests
- Horizontal scalability-ready (multiple instances safe)
- Load balancer can route to any backend instance

**Benefits**: Resilience (server restarts don't lose state), scalability (add instances without coordination), testability (each request independent).

### Event-Driven Architecture (Phase V)
- Decouple services via Kafka topics
- **Producers**: Task operations (create, update, delete, complete) publish events to `task-events`
- **Consumers**:
  - Notification Service subscribes to `reminders`
  - Recurring Task Service subscribes to `task-events` (for recurring task spawning)
  - Audit Service subscribes to `task-events` (for activity log)
- Idempotent consumers (handle duplicate events gracefully)
- Event schema: `event_type`, `task_id`, `task_data`, `user_id`, `timestamp`

### Microservices Principles (Phase IV-V)
- **Single Responsibility**: Each service owns one domain (tasks, notifications, audit)
- **API Contracts**: Explicit interfaces (MCP tools, REST endpoints, Kafka schemas)
- **Independent Deployability**: Services can deploy without coordinating
- **Database per Service**: Each service owns its data (or shared DB with clear boundaries)
- **Service Discovery**: Kubernetes DNS (Phase IV+), Dapr Service Invocation (Phase V)

### Database Design
- **Normalization**: 3NF minimum (no redundant data)
- **Foreign Keys**: Enforced for referential integrity
- **Indexes**: On query-heavy columns (`user_id`, `completed`, `due_date`, `created_at`)
- **Migrations**: Versioned, reversible migration scripts
- **Schema**:
  - `users`: `id` (PK), `email`, `name`, `created_at`
  - `tasks`: `id` (PK), `user_id` (FK), `title`, `description`, `completed`, `created_at`, `updated_at`
  - `conversations`: `id` (PK), `user_id` (FK), `created_at`, `updated_at`
  - `messages`: `id` (PK), `conversation_id` (FK), `user_id` (FK), `role`, `content`, `created_at`

---

## AI Agent Development

### MCP Server Design (Phase III+)
- **Tools as Primitives**: One tool = one atomic operation
- **Stateless**: Tools read/write DB, hold no in-memory state
- **Validation**: Input schemas strictly enforced (Pydantic models)
- **Error Responses**: Structured JSON with error codes and messages
- **Tool Schema**: Name, description, parameters (type, required, description), returns

### Agent Behavior Specification
- **Confirmation**: Always confirm actions with friendly response ("✓ Task added: Buy groceries")
- **Disambiguation**: If unclear, ask clarifying questions ("Which task do you want to delete?")
- **Graceful Degradation**: Handle tool failures gracefully ("Sorry, I couldn't complete that. Please try again.")
- **Context Awareness**: Use conversation history to resolve ambiguous references ("Mark it as done" → uses previous task ID)

### Natural Language Understanding
- Support varied phrasings:
  - "Add a task" = "Create a todo" = "Remember to" = "I need to"
  - "Show my tasks" = "List all" = "What's on my list" = "What do I need to do"
- Infer intent from context (previous turns)
- Handle typos and informal language
- Support both explicit ("Mark task 3 as complete") and implicit ("Done with groceries") references

---

## Cloud-Native Principles (Phase IV-V)

### 12-Factor App Compliance
1. **Codebase**: One codebase tracked in Git, multiple deploys
2. **Dependencies**: Explicitly declared (requirements.txt, package.json)
3. **Config**: Stored in environment variables (never hardcoded)
4. **Backing Services**: Attached resources (DB, Kafka) via URLs
5. **Build/Release/Run**: Strict separation of stages
6. **Processes**: Stateless, share-nothing processes
7. **Port Binding**: Self-contained services export via port binding
8. **Concurrency**: Scale out via process model (horizontal scaling)
9. **Disposability**: Fast startup, graceful shutdown
10. **Dev/Prod Parity**: Keep environments as similar as possible
11. **Logs**: Treat logs as event streams (stdout/stderr)
12. **Admin Processes**: Run admin/management tasks as one-off processes

### Observability
- **Logging**: Structured JSON logs with correlation IDs
- **Metrics**: Task operations per second, MCP tool invocations, API latency, error rates
- **Health Checks**: `/health` (liveness), `/ready` (readiness) endpoints
- **Distributed Tracing**: Phase V with Dapr (trace task creation → Kafka → notification)

### Resilience
- **Retry Logic**: Exponential backoff for transient failures (max 3 retries)
- **Circuit Breakers**: Phase V via Dapr (prevent cascading failures)
- **Timeouts**: All external calls timeout (DB: 5s, API: 10s, LLM: 30s)
- **Graceful Degradation**: Fallback responses when non-critical services fail

---

## Deployment Standards

### Phase II: Web App
- **Frontend**: Vercel (automatic deployments from Git main branch)
- **Backend**: Vercel Serverless Functions or dedicated API host
- **Database**: Neon Serverless PostgreSQL (connection pooling enabled)
- **Environment**: `.env.local` for development, Vercel environment variables for production

### Phase III: Chatbot
- Same as Phase II + OpenAI API integration
- **Domain Allowlist**: Configure OpenAI ChatKit domain allowlist (required for hosted ChatKit)
- **Environment Variables**: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`, `OPENAI_API_KEY`

### Phase IV: Local Kubernetes
- **Platform**: Minikube with resource limits (4 CPU, 8GB RAM)
- **Packaging**: Helm charts for all services
- **Commands**: `kubectl-ai` for assisted operations ("deploy frontend with 2 replicas")
- **Kagent**: Advanced cluster analysis and optimization
- **Image Registry**: Local Docker registry or Docker Hub

### Phase V: Cloud Kubernetes
- **Platform**: Azure AKS, Google GKE, or Oracle OKE
- **Kafka**: Redpanda Cloud (free tier) or self-hosted via Strimzi operator
- **Dapr**: Full building blocks enabled (Pub/Sub, State, Jobs API, Secrets, Service Invocation)
- **CI/CD Pipeline**: GitHub Actions
  - Trigger: Push to main branch
  - Steps: Run tests → Build Docker images → Push to registry → Deploy via Helm → Smoke tests
- **Monitoring**: Cloud provider monitoring (Azure Monitor, Google Cloud Monitoring, Oracle Cloud Observability)

---

## Documentation Requirements

### README.md (Repository Root)
- Project overview and hackathon context
- Setup instructions per phase (Phase I: Python setup, Phase II: Full-stack, etc.)
- Architecture diagrams (Phase III+)
- Deployment guide (local and cloud)
- Submission requirements checklist

### CLAUDE.md (Repository Root)
- Agent instructions and workflow
- Reference to this constitution
- Spec-Kit workflow explanation
- PHR and ADR creation guidelines

### Phase-Specific Documentation
- Each phase in `specs/phase-XX/`:
  - `spec.md`: Requirements and acceptance criteria
  - `plan.md`: Architecture and technical approach
  - `tasks.md`: Task breakdown with file paths
- Phase transitions documented (what carries over, what changes)

### Code Comments
- Task references: `# [Task]: T-001 | [Spec]: specs/phase-01/spec.md §2.1`
- Complex logic explained (WHY, not WHAT)
- API contracts documented via docstrings (Google-style for Python, JSDoc for TypeScript)
- Edge cases and assumptions documented

---

## Workflow Governance

### Spec → Plan → Tasks → Implement Flow

1. **Spec Phase**: Architect defines WHAT
   - User stories with priorities (P1, P2, P3)
   - Functional requirements (FR-001, FR-002, ...)
   - Acceptance criteria (Given/When/Then)
   - Success criteria (measurable outcomes)

2. **Plan Phase**: Engineer proposes HOW
   - Technical context (language, dependencies, platform)
   - Constitution check (compliance verification)
   - Project structure (directory layout, module organization)
   - Architecture diagrams (system components, data flow)
   - Complexity tracking (justified violations)

3. **Tasks Phase**: Break into atomic units
   - Task ID, description, file paths
   - Dependencies and parallel opportunities
   - Test tasks (if tests required)
   - User story mapping (US1, US2, US3)

4. **Implement Phase**: Engineer executes
   - Write tests first (if TDD requested)
   - Implement per task specification
   - Reference task IDs in commits
   - Pass all tests before marking complete

### Approval Gates

- **Spec → Plan**: Architect approval REQUIRED before planning begins
- **Plan → Tasks**: Architect approval REQUIRED before task breakdown
- **Tasks → Implement**: Architect approval REQUIRED before coding starts
- **Implementation Complete**: Tests MUST pass + Architect validation

**No gate skipping permitted.**

### PHR (Prompt History Records)

**Purpose**: Capture every interaction for traceability and learning.

**Routing** (automatic, all under `history/prompts/`):
- `constitution` stage → `history/prompts/constitution/`
- Feature stages (`spec`, `plan`, `tasks`, `red`, `green`, `refactor`, `explainer`, `misc`) → `history/prompts/<feature-name>/`
- `general` stage → `history/prompts/general/`

**Content**:
- ID, title, stage, date
- Full user prompt (verbatim, not truncated)
- Concise assistant response
- Files created/modified
- Tests run/added
- Links to spec, ticket, ADR, PR

**Creation**: Agent-native tools preferred (Read template, fill placeholders, Write file). Shell fallback if needed.

### ADR (Architecture Decision Records)

**Purpose**: Document significant architectural decisions with reasoning and tradeoffs.

**Significance Test** (ALL must be true):
- **Impact**: Long-term consequences (framework choice, data model, API design, security pattern, platform selection)
- **Alternatives**: Multiple viable options considered (not obvious choice)
- **Scope**: Cross-cutting, influences system design (affects multiple components or phases)

**Workflow**:
1. During `/sp.plan` or `/sp.tasks`, test for significance
2. If significant, suggest: "📋 Architectural decision detected: [brief]. Document? Run `/sp.adr [title]`"
3. Wait for user consent (NEVER auto-create)
4. User runs `/sp.adr` command explicitly
5. ADR created in `history/adr/`

**Examples of Significant Decisions**:
- Using MCP vs REST API for AI tools (Phase III)
- Stateless chat architecture (Phase III)
- Kafka vs RabbitMQ for event streaming (Phase V)
- Dapr vs direct Kafka clients (Phase V)
- JWT vs session-based auth (Phase II)

---

## Roles and Collaboration

### Architect (User)
- Defines requirements (WHAT)
- Validates architectural approach (HOW)
- Approves specs, plans, tasks before implementation
- Makes final decisions on tradeoffs
- Authority over constitutional amendments

### Engineer (Claude Code)
- Proposes implementations (HOW)
- Executes the SDD loop (spec → plan → tasks → implement)
- Creates PHRs for every interaction
- Suggests ADRs for significant decisions
- Waits for explicit approval before implementing

**Decision Authority**: When in doubt, Engineer MUST ask Architect. Treat Architect as a specialized tool for clarification and decision-making.

---

## Amendment Process

### Proposing Amendments

1. **Identify Need**: Conflict with current practice, missing constraint, or new requirement
2. **Draft Amendment**: Propose specific changes with rationale
3. **Architect Review**: Present to Architect with justification
4. **Update Constitution**: Increment version according to semantic versioning
5. **Propagate Changes**: Update `CLAUDE.md`, templates, and notify all agents

### Amendment Authority

- **Architect**: Final approval on ALL amendments
- **Engineer**: Can propose, MUST justify with evidence and reasoning

### Versioning (Semantic Versioning: MAJOR.MINOR.PATCH)

- **MAJOR**: Principle changes or removals (e.g., remove spec-driven requirement, change core workflow)
- **MINOR**: Add new constraints, sections, or principles (e.g., add new tech stack, new phase)
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

**Current Version**: See footer.

### Amendment Impact

- Update this constitution file with sync impact report (HTML comment at top)
- Check all templates for consistency (`spec-template.md`, `plan-template.md`, `tasks-template.md`)
- Update `CLAUDE.md` references
- Create ADR if amendment is architecturally significant

---

## Governance

**This constitution supersedes all other practices.**

- All specs, plans, tasks, and code MUST comply with this constitution
- Code reviews MUST verify constitution adherence
- Complexity MUST be justified against these principles (see "Complexity Tracking" in plan template)
- When in doubt, favor simplicity and the spec-driven flow

**Hierarchy of Truth**:

```
Constitution > Spec > Plan > Tasks > Code
```

If conflicts arise between levels, the higher level wins.

**Enforcement**:
- Every PR/commit reviewed for compliance
- Unjustified complexity rejected
- Phase skipping prohibited
- Technology stack deviations rejected (unless constitution amended)

**Guidance Files**:
- This constitution: Principles and constraints
- `CLAUDE.md`: Runtime agent behavior
- Templates: Structured artifact formats

---

**Version**: 1.0.0
**Ratified**: 2026-01-09
**Last Amended**: 2026-01-09
**Architect**: [Your Name]
**Engineer**: Claude Code (Sonnet 4.5)
