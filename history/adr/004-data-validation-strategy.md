# ADR-004: Data Validation Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Validation Strategy" not separate ADRs for client validation, server validation).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 002-phase-02-web-app (Phase 2 Full-Stack Web Application)
- **Context:** Phase 2 requires input validation for user data (emails, passwords, task titles, descriptions). Security principle: "never trust client input" (constitution §Security Principles:222). User experience principle: provide immediate feedback for invalid inputs. These goals require **dual-layer validation** strategy with different technologies and tradeoffs on client vs server.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✓ YES - Validation affects security (SQL injection, XSS), data integrity, user experience
     2) Alternatives: Multiple viable options considered with tradeoffs? ✓ YES - Client-only, server-only, dual-layer considered
     3) Scope: Cross-cutting concern (not an isolated detail)? ✓ YES - Affects frontend forms, backend API endpoints, database schema constraints, error handling, testing
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt a **dual-layer validation strategy** with complementary technologies:

**Client-Side Validation (Frontend):**
- **Library:** Zod 3+ (TypeScript schema validation)
- **Integration:** React Hook Form 7+ (form state management)
- **Purpose:** Immediate user feedback (< 100ms), prevent unnecessary API calls
- **Scope:** Format validation (email format, password strength, title length), required fields
- **Error Display:** Inline error messages below form inputs
- **Execution:** Runs on input blur and form submit

**Server-Side Validation (Backend):**
- **Library:** Pydantic 2.0+ (Python data validation)
- **Integration:** FastAPI automatic request validation
- **Purpose:** Security (never trust client), enforce business rules, prevent bad data from reaching database
- **Scope:** All client validations PLUS business logic (email uniqueness, user authorization, rate limiting)
- **Error Response:** HTTP 400 with structured error JSON `{code, message, field, details}`
- **Execution:** Runs on every API request before handler execution

**Validation Rules (Applied on BOTH layers):**
- Email: Valid format (RFC 5322), max 255 characters
- Name: 1-255 characters, non-empty
- Password: Minimum 8 characters, at least one letter and one number
- Task Title: 1-200 characters, non-empty, not only whitespace
- Task Description: 0-1000 characters, optional

**Philosophy:** Client validation for UX, server validation for security. Both must exist and enforce **identical rules**.

## Consequences

### Positive

- **Constitution Compliance:** Meets security requirement for input validation on both client and server (§Security Principles:222)
- **Immediate Feedback:** Client validation provides instant error messages (better UX than waiting for API round-trip)
- **Security:** Server validation ensures malicious actors cannot bypass client checks (e.g., via curl, Postman)
- **Type Safety:** Zod generates TypeScript types from schemas, Pydantic integrates with FastAPI for automatic docs
- **Reduced Server Load:** Client validation prevents invalid requests from reaching server (fewer 400 errors)
- **Consistent Error Format:** Both layers return errors in similar format (field + message), easier to display in UI
- **SQL Injection Prevention:** Server-side Pydantic validation + SQLModel ORM (no raw SQL) prevents injection attacks
- **Clear Documentation:** Zod and Pydantic schemas serve as living documentation of validation rules
- **Easy Testing:** Validation schemas can be unit-tested independently from forms/endpoints
- **Progressive Enhancement:** Works even if client JS disabled (server validation catches all issues)

### Negative

- **Duplicate Rules:** Validation rules defined twice (Zod and Pydantic), must keep in sync manually
- **Maintenance Burden:** Changing validation rule requires updating both client and server schemas
- **Increased Bundle Size:** Zod adds ~13KB to frontend bundle (acceptable for validation benefits)
- **Complexity:** Developers must learn two validation libraries (Zod syntax differs from Pydantic)
- **Type Conversion Issues:** Client sends strings, server parses to Python types (e.g., "true" → True) - can cause mismatches
- **Error Message Duplication:** Same error (e.g., "Email already exists") must be handled on both client and server
- **Performance Overhead:** Validation runs twice per submission (client + server), adds ~50-100ms total
- **False Sense of Security:** Developers might assume client validation is sufficient (must enforce "always validate server-side" culture)

## Alternatives Considered

### Alternative A: Client-Side Validation Only

**Components:**
- Zod validation on frontend forms
- No server-side validation (trust client input)

**Why Rejected:**
- **Security Vulnerability:** Attackers can bypass client validation with curl/Postman (send invalid data directly to API)
- **Constitution Violation:** Constitution requires input validation on both sides (§Security Principles:222)
- **Data Integrity Risk:** Bad data can reach database (e.g., 10,000 character titles crash UI)
- **SQL Injection Risk:** Without server validation, malicious input could exploit ORM edge cases

### Alternative B: Server-Side Validation Only

**Components:**
- Pydantic validation on backend API
- No client-side validation

**Why Rejected:**
- **Poor User Experience:** User must wait for API round-trip to see validation errors (300-500ms latency)
- **Increased Server Load:** Every invalid form submission hits server (unnecessary 400 errors, wasted CPU)
- **Network Overhead:** Invalid requests waste bandwidth (frontend could have caught errors locally)
- **Frustrating UX:** User corrects one error, submits, gets next error, submits again (slow feedback loop)

### Alternative C: Single Validation Language (TypeScript Everywhere)

**Components:**
- Zod validation on frontend
- Zod validation on backend (requires Node.js backend or Zod port to Python)

**Why Rejected:**
- **Constitution Violation:** Backend must be Python FastAPI (§VI.Phase II:106), not Node.js
- **Pydantic Integration:** FastAPI deeply integrated with Pydantic (automatic request validation, OpenAPI docs)
- **No Zod for Python:** No mature Zod port for Python (would need to build custom integration)
- **Type System Mismatch:** TypeScript types ≠ Python types (Zod designed for TS, not Python)

### Alternative D: Shared Schema Definition Language (JSON Schema)

**Components:**
- Define validation rules in JSON Schema
- Generate Zod schemas for frontend, Pydantic schemas for backend

**Why Rejected:**
- **Added Complexity:** Requires schema generation step in build process, more moving parts
- **Loss of Type Safety:** JSON Schema is loosely typed, loses TypeScript/Python type inference benefits
- **Code Generation Brittleness:** Generated code can break on schema changes, harder to debug
- **Overhead:** Unnecessary abstraction for Phase 2 scope (10-15 validation rules total)
- **Better for Larger Scale:** JSON Schema generation makes sense for 100+ schemas, overkill for small project

## References

- Feature Spec: `../../specs/002-phase-02-web-app/spec.md` (FR-018, FR-029, Edge Cases on validation)
- Implementation Plan: `../../specs/002-phase-02-web-app/plan.md` (Design Decision §7, Security Considerations)
- Research: `../../specs/002-phase-02-web-app/research.md` (Section 1: Better Auth Integration mentions validation)
- Constitution: `.specify/memory/constitution.md` (§Security Principles:222 - Input Validation on both sides)
- Related ADRs: ADR-001 (Frontend Stack includes Zod + React Hook Form), ADR-002 (Backend Stack includes Pydantic + FastAPI)
- Evaluator Evidence: `../../history/prompts/002-phase-02-web-app/002-phase-2-planning-complete.plan.prompt.md` (Security Principles PASS, Input Validation planned)
