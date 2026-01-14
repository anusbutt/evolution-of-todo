# ADR-002: Backend Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Backend Stack" not separate ADRs for framework, ORM, database).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 002-phase-02-web-app (Phase 2 Full-Stack Web Application)
- **Context:** Phase 2 requires a RESTful API backend with database persistence, user authentication, and horizontal scalability. The constitution mandates specific technologies (FastAPI, SQLModel, Neon PostgreSQL) to ensure consistency across the evolution of the todo application through Phase V.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✓ YES - Backend architecture affects API design, database schema, scalability, security
     2) Alternatives: Multiple viable options considered with tradeoffs? ✓ YES - Django, Flask, Express.js considered
     3) Scope: Cross-cutting concern (not an isolated detail)? ✓ YES - Affects API contracts, database design, deployment, testing, authentication
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt an integrated backend technology stack consisting of:

- **Framework:** FastAPI 0.115+ (async Python web framework)
- **Language:** Python 3.13+
- **ORM:** SQLModel 0.0.22+ (combines Pydantic + SQLAlchemy)
- **Database:** Neon Serverless PostgreSQL 16+ (cloud-hosted with connection pooling)
- **Database Driver:** asyncpg 0.30+ (async PostgreSQL client)
- **Migrations:** Alembic 1.13+ (versioned schema evolution)
- **Validation:** Pydantic 2.0+ (request/response schemas)
- **ASGI Server:** Uvicorn 0.32+ (async server)
- **Architecture:** Layered (routes/ → services/ → models/) with middleware pipeline
- **Middleware:** CORS, JWT Auth, Rate Limiting (100 req/min per user per constitution)
- **Testing:** pytest 8+ with pytest-asyncio 0.24+, httpx 0.28+ (async test client), FastAPI TestClient
- **Coverage Target:** 75% minimum (constitution requirement)

This stack is **integrated and cohesive** - components work together for async performance and type safety across the entire backend.

## Consequences

### Positive

- **Constitution Compliance:** Meets Phase II requirements exactly (FastAPI, SQLModel, Neon PostgreSQL per §VI.Phase II:106-108)
- **Async Performance:** Full async/await support from HTTP requests through database queries (non-blocking I/O)
- **Type Safety:** End-to-end type checking (Pydantic schemas ↔ SQLModel models ↔ database)
- **Developer Experience:** Automatic OpenAPI documentation, interactive API docs at `/docs`, Pydantic validation errors
- **SQL Injection Prevention:** SQLModel ORM uses parameterized queries (never raw SQL)
- **Connection Pooling:** 10 persistent connections + 20 overflow (efficient connection reuse, < 50ms latency reduction)
- **Serverless Database:** Neon auto-scales, no server management, built-in connection pooling
- **Schema Migrations:** Alembic versioned migrations (reversible, auditable schema changes)
- **Fast Development:** FastAPI automatic request validation, clear error messages, hot reload
- **Horizontal Scalability:** Stateless API design (JWT tokens, no server-side sessions) ready for multi-instance deployment
- **Testing Integration:** FastAPI TestClient for synchronous tests, httpx for async tests, pytest fixtures for database isolation

### Negative

- **Python Async Complexity:** Requires understanding async/await, event loops, proper awaiting (mistakes cause blocking)
- **SQLModel Maturity:** Newer library (v0.0.x), fewer Stack Overflow answers, some SQLAlchemy patterns not supported
- **Neon Vendor Lock-In:** Migration to self-hosted PostgreSQL requires connection string changes, testing connection pooling
- **Alembic Learning Curve:** Migration scripts require understanding of database schema evolution, autogenerate not perfect
- **Cold Start Latency:** Serverless function cold starts can add 1-2 seconds (Vercel) or require dedicated API host
- **Type Complexity:** SQLModel + Pydantic dual models can be confusing (when to use SQLModel vs Pydantic schema)
- **Debugging Async:** Stack traces harder to read, race conditions harder to debug than synchronous code
- **Connection Pool Tuning:** Pool size/overflow requires experimentation for optimal performance (too small = waits, too large = resource exhaustion)

## Alternatives Considered

### Alternative Stack A: Django + Django ORM + PostgreSQL (self-hosted)

**Components:**
- Framework: Django 5.0 (batteries-included, synchronous)
- ORM: Django ORM (mature, migrations built-in)
- Database: Self-hosted PostgreSQL on DigitalOcean or AWS RDS

**Why Rejected:**
- **Constitution Violation:** Constitution mandates FastAPI and SQLModel (§VI.Phase II:106-107), not Django
- Synchronous framework (no async support) - slower for I/O-bound operations (database, API calls)
- Heavier framework (more overhead) - slower API response times
- Django ORM lacks Pydantic integration (separate validation layer needed)
- Self-hosted database requires server management, backups, scaling

### Alternative Stack B: Express.js + Prisma + Supabase PostgreSQL

**Components:**
- Framework: Express.js (Node.js, JavaScript/TypeScript)
- ORM: Prisma (TypeScript ORM with auto-generated client)
- Database: Supabase PostgreSQL (Firebase alternative)

**Why Rejected:**
- **Constitution Violation:** Constitution mandates Python FastAPI (§VI.Phase II:106), not Node.js Express
- Different language from Phase I (Python) - breaks continuity
- Supabase not mentioned in constitution (Neon mandated §VI.Phase II:108)
- Prisma migrations less mature than Alembic

### Alternative Stack C: Flask + SQLAlchemy + Neon PostgreSQL

**Components:**
- Framework: Flask 3.0 (micro-framework, synchronous)
- ORM: SQLAlchemy 2.0 (mature, widely used)
- Database: Neon PostgreSQL

**Why Rejected:**
- **Constitution Violation:** Constitution mandates FastAPI (§VI.Phase II:106), not Flask
- Synchronous framework (no async support) - slower I/O performance
- No automatic API documentation (FastAPI provides OpenAPI docs)
- No built-in request validation (FastAPI uses Pydantic)
- SQLAlchemy without Pydantic integration (manual validation layer)
- **Partial Compliance:** Meets database requirement (Neon) but violates framework and ORM mandates

## References

- Feature Spec: `../../specs/002-phase-02-web-app/spec.md` (User Stories 1-7, FR-001 to FR-058)
- Implementation Plan: `../../specs/002-phase-02-web-app/plan.md` (Design Decisions §2, §3, §9, Technical Context)
- Research: `../../specs/002-phase-02-web-app/research.md` (Section 2: SQLModel Async Queries, Section 4: Neon Connection Pooling)
- Constitution: `.specify/memory/constitution.md` (§VI.Phase II:106-108 - Backend: FastAPI, SQLModel, Neon PostgreSQL)
- Related ADRs: ADR-003 (Authentication Architecture uses this backend stack)
- Evaluator Evidence: `../../history/prompts/002-phase-02-web-app/002-phase-2-planning-complete.plan.prompt.md` (Constitution Check PASS)
